#!/usr/bin/env python3
"""
Incus Luminis Slack <-> Claude Code bridge.

Runs a Socket Mode connection for one agent role's Slack app (e.g. "Incus PO"
for Product_Owner) and forwards @mentions to a headless `claude -p`
invocation, posting the reply back to the same Slack thread.

One process per role. To wire up a second role, create another
`.env.<role>` file at the repo root and run another instance of this script
pointed at it — see README.md in this folder.

This is a first pass, not a finished integration: synchronous, no memory
across messages, only responds to @mentions. See
docs/agents/slack-bridge.md for the design and known limitations.
"""

import argparse
import logging
import os
import subprocess
import sys
import threading
from collections import defaultdict, deque
from pathlib import Path

from dotenv import load_dotenv
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


def _make_history():
    max_len = int(os.environ.get("MAX_HISTORY_MESSAGES", "30"))
    return defaultdict(lambda: deque(maxlen=max_len))


_channel_history = _make_history()


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


def parse_args():
    parser = argparse.ArgumentParser(description="Bridge a Slack app to a Claude Code agent role.")
    parser.add_argument(
        "--env-file",
        default=str(REPO_ROOT / ".env.product-owner"),
        help="Path to the .env file with this role's Slack tokens (default: %(default)s)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    env_path = Path(args.env_file)
    if env_path.exists():
        load_dotenv(env_path)
        log.info("Loaded env from %s", env_path)
    else:
        log.warning("%s not found - relying on already-exported environment variables", env_path)

    bot_token = os.environ.get("SLACK_BOT_TOKEN")
    app_token = os.environ.get("SLACK_APP_TOKEN")
    if not bot_token or not app_token:
        sys.exit("SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set (via --env-file or the environment).")

    agent_role = os.environ.get("AGENT_ROLE", "Product_Owner")
    agent_role_doc = os.environ.get("AGENT_ROLE_DOC", "docs/agents/product-owner.md")
    claude_bin = os.environ.get("CLAUDE_BIN", "claude")
    timeout_seconds = int(os.environ.get("CLAUDE_TIMEOUT_SECONDS", "300"))
    max_reply_chars = int(os.environ.get("MAX_REPLY_CHARS", "3000"))

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

        log.info("Invoking %s for: %s", claude_bin, text[:200])
        try:
            result = subprocess.run(
                [claude_bin, "-p", prompt],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
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


if __name__ == "__main__":
    main()
