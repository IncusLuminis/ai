#!/usr/bin/env python3
"""
Incus Luminis Slack <-> Claude Code bridge.

Runs a Socket Mode connection for one agent role's Slack app (e.g. "Incus PO"
for Product_Owner) and forwards @mentions to a headless `claude -p`
invocation, posting the reply back to the same Slack thread.

Two ways to run several roles: as separate processes (`python3 bridge.py
--env-file ../../.env.coder` per role, one terminal each), or all in this
one process via `run_all.py`, which imports `run_role()` from here and
starts each role in its own thread. Either way each role is still its own
Slack app / Socket Mode connection - `run_all.py` just avoids needing N
open terminals for N connections.

This is a first pass, not a finished integration: synchronous per role,
only responds to @mentions. See docs/agents/slack-bridge.md for the design
and known limitations.
"""

import argparse
import logging
import os
import subprocess
import sys
import threading
import uuid
from collections import defaultdict, deque
from pathlib import Path

from dotenv import dotenv_values
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# scripts/slack-bridge/bridge.py -> repo root is two levels up.
REPO_ROOT = Path(__file__).resolve().parents[2]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("slack-bridge")

# Passive channel-history buffer: every bot reads every message (so it has
# real conversational context), but only the bot that's actually @mentioned
# replies. Each bridge process keeps its own buffer, keyed by channel, capped
# at MAX_HISTORY_MESSAGES entries; deduped by Slack message `ts` so the same
# message recorded via both the "message" and "app_mention" events (Slack
# fires both for a channel message that mentions the bot) doesn't double up.
_HISTORY_LOCK = threading.Lock()
_SKIP_SUBTYPES = {
    "message_changed",
    "message_deleted",
    "channel_join",
    "channel_leave",
    "channel_topic",
    "channel_purpose",
}
_name_cache = {}


# Read lazily (per new channel seen), not once at import time, so it still
# picks up MAX_HISTORY_MESSAGES if set later. This buffer is process-wide by
# design: when several roles run in one process via run_all.py, they share
# it (they're all watching the same live channel anyway, so one buffer is
# simpler and more consistent than N duplicate copies) - so this setting
# isn't really "per role" once you're running that way. Set it as a real
# exported env var, not inside a single role's .env.<role> file.
_channel_history = defaultdict(lambda: deque(maxlen=int(os.environ.get("MAX_HISTORY_MESSAGES", "30"))))


def _display_name(client, event):
    """Best-effort human/bot display name for a Slack message event."""
    if event.get("bot_id"):
        name = event.get("username") or (event.get("bot_profile") or {}).get("name")
        return name or "bot"
    user_id = event.get("user")
    if not user_id:
        return "someone"
    with _HISTORY_LOCK:
        cached = _name_cache.get(user_id)
    if cached:
        return cached
    name = user_id
    try:
        info = client.users_info(user=user_id)
        name = info["user"].get("real_name") or info["user"].get("name") or user_id
    except Exception:
        pass  # missing users:read scope, API hiccup, etc. - fall back to the raw ID
    with _HISTORY_LOCK:
        _name_cache[user_id] = name
    return name


def _record_message(client, event):
    """Passively remember a message for context. Never replies."""
    if event.get("subtype") in _SKIP_SUBTYPES:
        return
    text = (event.get("text") or "").strip()
    if not text:
        return
    channel = event.get("channel")
    ts = event.get("ts")
    if not channel or not ts:
        return
    name = _display_name(client, event)
    with _HISTORY_LOCK:
        hist = _channel_history[channel]
        if any(existing_ts == ts for existing_ts, _ in hist):
            return
        hist.append((ts, f"{name}: {text}"))


def _format_history(channel, exclude_ts=None):
    with _HISTORY_LOCK:
        lines = [line for ts, line in _channel_history.get(channel, []) if ts != exclude_ts]
    if not lines:
        return ""
    return "Recent channel context (oldest to newest):\n" + "\n".join(lines) + "\n\n"


# Persistent per-role Claude Code session: one continuous conversation per
# bot, surviving across separate @mentions (not just within one), so the bot
# remembers its own prior replies instead of starting fresh every time. Not
# shared across roles/bots - each has its own session file and its own
# actual Claude Code conversation. Survives bridge.py restarts (the session
# id is on disk); does NOT survive `claude` itself losing/expiring the
# session, which is handled with a one-time fallback below.
_SESSIONS_DIR = Path(__file__).resolve().parent / ".sessions"


def _session_file(role_slug):
    return _SESSIONS_DIR / f"{role_slug}.txt"


def _load_session_id(role_slug):
    f = _session_file(role_slug)
    if f.exists():
        sid = f.read_text().strip()
        return sid or None
    return None


def _save_session_id(role_slug, session_id):
    _SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    _session_file(role_slug).write_text(session_id)


def _run_claude(prompt, role_slug, claude_bin, timeout_seconds):
    """Run `claude -p`, resuming this role's persistent session if one
    exists, so the bot has real multi-turn memory of its own conversation.
    Starts a fresh session (new id) the first time, or if resuming an old
    one fails (expired/missing - `claude` isn't ours to guarantee)."""
    session_id = _load_session_id(role_slug)
    if session_id:
        cmd = [claude_bin, "--resume", session_id, "-p", prompt]
    else:
        session_id = str(uuid.uuid4())
        cmd = [claude_bin, "--session-id", session_id, "-p", prompt]

    result = subprocess.run(
        cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=timeout_seconds
    )

    if result.returncode != 0 and _load_session_id(role_slug):
        log.warning(
            "Resuming session %s failed (exit %s) - starting a fresh one for %s",
            session_id,
            result.returncode,
            role_slug,
        )
        session_id = str(uuid.uuid4())
        cmd = [claude_bin, "--session-id", session_id, "-p", prompt]
        result = subprocess.run(
            cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=timeout_seconds
        )

    _save_session_id(role_slug, session_id)
    return result


def run_role(env_file):
    """Load one role's `.env.<role>` file and start its Slack Socket Mode
    connection. Blocks forever (SocketModeHandler.start()).

    Deliberately does NOT use `dotenv.load_dotenv()`, which would write into
    the shared process environment (`os.environ`) - fine for one role per
    process, but a race when `run_all.py` calls this from several threads at
    once (each role's SLACK_BOT_TOKEN etc. would stomp on the others').
    Instead reads this role's file into its own local dict via
    `dotenv_values()`, so each call/thread is fully isolated.
    """
    env_path = Path(env_file)
    file_vars = dotenv_values(env_path) if env_path.exists() else {}
    if not env_path.exists():
        log.warning("%s not found - relying on already-exported environment variables", env_path)

    def cfg(key, default=None):
        # This role's .env file wins, then anything already exported in the
        # shell, then the default.
        return file_vars.get(key) or os.environ.get(key) or default

    bot_token = cfg("SLACK_BOT_TOKEN")
    app_token = cfg("SLACK_APP_TOKEN")
    if not bot_token or not app_token:
        sys.exit(f"SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set for {env_file} (file or environment).")

    agent_role = cfg("AGENT_ROLE", "Product_Owner")
    agent_role_doc = cfg("AGENT_ROLE_DOC", "docs/agents/product-owner.md")
    claude_bin = cfg("CLAUDE_BIN", "claude")
    timeout_seconds = int(cfg("CLAUDE_TIMEOUT_SECONDS", "300"))
    max_reply_chars = int(cfg("MAX_REPLY_CHARS", "3000"))
    role_slug = cfg("ROLE_SLUG") or agent_role.lower().replace("_", "-").replace(" ", "-")

    app = App(token=bot_token)

    @app.event("message")
    def handle_message(event, client):
        # Passive listener: every bot reads every channel message so it has
        # real context, but replying only ever happens in handle_app_mention
        # below - this handler never calls `say`.
        _record_message(client, event)

    @app.event("app_mention")
    def handle_app_mention(event, say, client):
        channel = event["channel"]
        ts = event["ts"]
        raw_text = event.get("text", "")
        # Strip the leading "<@BOTID>" mention token(s).
        text = " ".join(w for w in raw_text.split() if not (w.startswith("<@") and w.endswith(">")))
        text = text.strip()

        # Record this message too (in case the "message" event for it hasn't
        # arrived yet, or never does) - _record_message dedupes by ts.
        _record_message(client, event)

        if not text:
            say(text="Слышу тебя, но сообщение пустое — напиши, что нужно сделать.", channel=channel, thread_ts=ts)
            return

        try:
            client.reactions_add(channel=channel, timestamp=ts, name="eyes")
        except Exception:
            pass  # non-fatal - e.g. missing reactions:write scope

        history_block = _format_history(channel, exclude_ts=ts)
        sender = _display_name(client, event)

        prompt = (
            f'You are acting as the IncusLuminis "{agent_role}" agent, responding to a Slack '
            f"message in the team channel. Your mission, responsibilities and boundaries are "
            f"defined in {agent_role_doc} and the corresponding skill/agent definition under "
            f".claude/ in this repo - follow them. Respond concisely, the way a teammate would "
            f"in chat, not a full written report unless the message actually asks for one. "
            f"Other agents may be present in the same channel and reply to their own mentions "
            f"separately - only respond to what's addressed to you.\n\n"
            f"{history_block}"
            f"Slack message (mentions you) from {sender}:\n{text}"
        )

        log.info("Invoking %s (session=%s) for: %s", claude_bin, role_slug, text[:200])
        try:
            result = _run_claude(prompt, role_slug, claude_bin, timeout_seconds)
            reply = (result.stdout or "").strip()
            if result.returncode != 0:
                err = (result.stderr or "").strip()[-1500:]
                reply = (
                    f"Что-то пошло не так (exit {result.returncode}):\n```{err}```"
                    if err
                    else f"claude завершился с кодом {result.returncode} и без вывода."
                )
        except subprocess.TimeoutExpired:
            reply = f"Не уложился в {timeout_seconds}s — задача, похоже, слишком большая для чат-ответа."
        except FileNotFoundError:
            reply = f"Не могу найти `{claude_bin}` в PATH на этой машине."

        if not reply:
            reply = "(пустой ответ от claude — возможно, ушёл только в tool-вызовы без текста)"
        if len(reply) > max_reply_chars:
            reply = reply[:max_reply_chars] + f"\n\n… (обрезано, полный ответ длиннее {max_reply_chars} символов)"

        say(text=reply, channel=channel, thread_ts=ts)

        try:
            client.reactions_remove(channel=channel, timestamp=ts, name="eyes")
            client.reactions_add(channel=channel, timestamp=ts, name="white_check_mark")
        except Exception:
            pass

    log.info("Starting Socket Mode for role=%s ...", agent_role)
    SocketModeHandler(app, app_token).start()


def parse_args():
    parser = argparse.ArgumentParser(description="Bridge a single Slack app to a Claude Code agent role.")
    parser.add_argument(
        "--env-file",
        default=str(REPO_ROOT / ".env.product-owner"),
        help="Path to the .env file with this role's Slack tokens (default: %(default)s)",
    )
    return parser.parse_args()


def main():
    """CLI entry point for running one role standalone (one process, one
    terminal). To run several roles in a single process/terminal instead,
    use run_all.py."""
    args = parse_args()
    run_role(args.env_file)


if __name__ == "__main__":
    main()
