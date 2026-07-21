# Checklist: Adding a New Slack Agent

Step-by-step for turning one more agent role into a two-way Slack teammate, the same way `Product_Owner` ("Incus PO") was done. Repeat once per remaining role.

| Role | `AGENT_ROLE` | `AGENT_ROLE_DOC` | Suggested app name |
|---|---|---|---|
| Coder | `Coder` | `docs/agents/coder.md` | Incus Coder |
| Validator | `Validator` | `docs/agents/validator.md` | Incus Validator |
| DevOps | `DevOps` | `docs/agents/devops.md` | Incus DevOps |
| Publisher | `Publisher` | `docs/agents/publisher.md` | Incus Publisher |
| Media_keeper | `Media_keeper` | `docs/agents/media-keeper.md` | Incus Media Keeper |

## 1. Create the Slack app

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**.
2. Name it (e.g. `Incus Coder`), pick workspace **Incus Luminis** → **Create App**.

## 2. Give it a face

3. **Basic Information → Display Information**: upload an avatar/icon, optionally a short description (can double as the "character/tagline" note).

## 3. Bot Token Scopes

4. **OAuth & Permissions → Scopes → Bot Token Scopes → Add an OAuth Scope**, add each of:
   - `chat:write`
   - `chat:write.public`
   - `files:write`
   - `reactions:write`
   - `users:read`
   - `app_mentions:read`
   - `channels:history`

   (Add `chat:write` first if any scope refuses to show up in search — some depend on it.)

## 4. Socket Mode

5. Left sidebar → **Socket Mode** → toggle **Enable Socket Mode**.
6. Slack prompts for an **App-Level Token** → name it anything → scope **`connections:write`** → **Generate**.
7. Copy the token (`xapp-...`) somewhere safe — it goes into that role's `.env.<role>` file in step 9, not into the repo directly.

## 5. Event Subscriptions

8. Left sidebar → **Event Subscriptions** → toggle **Enable Events** (no Request URL needed — Socket Mode delivers events over the websocket).
9. **Subscribe to bot events** → add both `app_mention` **and** `message.channels`. Both are required: every bot passively reads all channel messages for context (`message.channels`), but only replies when actually `@mention`ed (`app_mention`) — see `slack-bridge.md §6`.
10. **Save Changes**.

## 6. Install and get the bot token

11. Left sidebar → **Install App** (or the "reinstall" banner if scopes changed) → **Install to Workspace** → **Allow**.
12. Back on **OAuth & Permissions**, copy the **Bot User OAuth Token** (`xoxb-...`).

## 7. Invite it to the channel

13. In Slack, open the team channel → `/invite @<app name>` (e.g. `/invite @Incus Coder`).

## 8. Wire it into the bridge

14. At the repo root (`shared/ai/`), create `.env.<role-slug>` (e.g. `.env.coder` — already gitignored by the existing `.env.*` rule):

    ```
    SLACK_BOT_TOKEN=xoxb-...
    SLACK_APP_TOKEN=xapp-...
    AGENT_ROLE=Coder
    AGENT_ROLE_DOC=docs/agents/coder.md
    ```

    (Fill in the row from the table above for whichever role you're adding.)

15. From `scripts/slack-bridge/`, reuse the existing virtualenv (no need to recreate it), then run it one of two ways:

    **Standalone** (its own process/terminal, alongside whatever's already running for other roles):

    ```bash
    source .venv/bin/activate
    python3 bridge.py --env-file ../../.env.coder
    ```

    **Or together with the rest**, one process/terminal for every role that has a `.env.<role>` file — stop whatever's currently running (`Ctrl+C`) and restart with:

    ```bash
    source .venv/bin/activate
    python3 run_all.py
    ```

    See `../../scripts/slack-bridge/README.md § Running several roles in one process` for details.

16. Leave it running.

## 9. Test it

17. In the Slack channel: `@Incus Coder are you there?` — should get a reply within `CLAUDE_TIMEOUT_SECONDS` (default 300s), with 👀 then ✅ reactions on your message along the way.

## Things that trip people up (seen while setting up Incus PO)

- **App Credentials** (Client ID/Secret, Signing Secret, Verification Token) on the Basic Information page — not needed for any of this; those are for public OAuth distribution or verifying inbound webhook requests, neither of which applies here.
- **`chat:write.customize`** — not needed either; identity (name/avatar) is set once at the app level (step 2), not passed per-message.
- Don't confuse the **workspace** admin pages (Settings → Customize) with an individual **app's** settings (api.slack.com/apps) — OAuth & Permissions only exists per-app.

See [`slack-bridge.md`](./slack-bridge.md) for why this shape (Socket Mode, one app per role) was chosen, and [`../../scripts/slack-bridge/README.md`](../../scripts/slack-bridge/README.md) for the bridge script itself.
