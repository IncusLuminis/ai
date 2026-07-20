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
from pathlib import Path

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# scripts/slack-bridge/bridge.py -> repo root is two levels up.
REPO_ROOT = Path(__file__).resolve().parents[2]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("slack-bridge")


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

    @app.event("app_mention")
    def handle_app_mention(event, say, client):
        channel = event["channel"]
        ts = event["ts"]
        raw_text = event.get("text", "")
        # Strip the leading "<@BOTID>" mention token(s).
        text = " ".join(w for w in raw_text.split() if not (w.startswith("<@") and w.endswith(">")))
        text = text.strip()

        if not text:
            say(text="Слышу тебя, но сообщение пустое — напиши, что нужно сделать.", channel=channel, thread_ts=ts)
            return

        try:
            client.reactions_add(channel=channel, timestamp=ts, name="eyes")
        except Exception:
            pass  # non-fatal - e.g. missing reactions:write scope

        prompt = (
            f'You are acting as the IncusLuminis "{agent_role}" agent, responding to a Slack '
            f"message in the team channel. Your mission, responsibilities and boundaries are "
            f"defined in {agent_role_doc} and the corresponding skill/agent definition under "
            f".claude/ in this repo - follow them. Respond concisely, the way a teammate would "
            f"in chat, not a full written report unless the message actually asks for one.\n\n"
            f"Slack message:\n{text}"
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
