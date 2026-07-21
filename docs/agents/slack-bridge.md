# Slack Two-Way Bridge

**Status:** First pass built and wired for one role (`Product_Owner` / "Incus PO"), not yet validated end to end against a real tool-heavy task.
**Added:** 2026-07-20

## 1. What this is

Each agent role gets its own Slack app ("Incus PO", "Incus Coder", etc. — own name, own avatar) so the team channel reads like a real team, not one bot with a shared voice. This doc covers making those bots *two-way*: able to receive an `@mention` in Slack and reply, backed by that role's actual Claude Code agent/skill definition — not just post one-way status updates (which only needs a bot token and `chat.postMessage`, already covered in `setup.md`).

## 2. Why Socket Mode, not a public webhook

`execution-model.md §4` already decided: the agent team runs on Mihal's local machine only, no dedicated runner, no self-hosted or cloud CI. A classic Slack Events API integration needs a public HTTPS Request URL for Slack to push events to — that would mean exposing something from the local machine to the internet (e.g. via ngrok), which is a step up in exposure this design deliberately avoided elsewhere.

**Socket Mode** avoids that: the local script opens an outbound WebSocket connection to Slack and receives events over it — no inbound port, no public URL, fits "local machine only" without any new exception.

## 3. Why per-role bots, not Slack's hosted MCP Server

Slack also ships its own hosted MCP server (`https://mcp.slack.com/mcp`, one-line install for Claude Code via `claude plugin install slack`) that gives an MCP client tools to search, read, and post to Slack. Considered and rejected for *this* purpose: it authenticates as the human user who did the OAuth flow, not as a distinct bot — every agent using it would speak with Mihal's own voice, defeating the point of six distinct personas. It may still be useful later as a read/search tool for an agent's own context-gathering, just not as the thing that makes each agent look like a separate teammate.

## 4. How it works

```text
Slack (@mention in channel)
        |  (Socket Mode, no public URL)
        v
scripts/slack-bridge/bridge.py   (one process per role)
        |  subprocess: `claude -p "<prompt>"` in shared/ai
        v
Claude Code CLI, loads that role's .claude/agents or .claude/skills
        |
        v
reply text  -->  posted back to the same Slack thread
```

One `bridge.py` process per role, each with its own Slack app tokens (`.env.<role>` at the repo root, gitignored) and its own `AGENT_ROLE` / `AGENT_ROLE_DOC` pointing at that role's charter. See `scripts/slack-bridge/README.md` for exact setup and run steps.

## 5. Slack app configuration this depends on

Beyond the one-way setup in `setup.md`, each bot's Slack app additionally needs:

- **Bot Token Scopes**: `app_mentions:read`, `channels:history` (added on top of `chat:write`, `chat:write.public`, `users:read`, etc.)
- **Socket Mode**: enabled, with an **App-Level Token** (scope `connections:write`) generated under Basic Information
- **Event Subscriptions**: enabled, subscribed to bot events `app_mention` **and** `message.channels` (both required — see §8)
- App reinstalled to the workspace after adding these scopes

## 6. Shared context, single responder

Principle, set 2026-07-20 once a second Slack app entered the picture: **every bot passively reads every channel message, but only the one actually `@mention`ed replies.** Without this, subscribing to `message.channels` at all would have no point, and without the "only the mentioned one replies" half, six bots in one channel would each answer every message — noise, and cross-talk between bots replying to each other's replies.

Implementation in `bridge.py`: a `message` event handler records every message (text + best-effort sender name) into an in-memory, per-channel rolling buffer (`MAX_HISTORY_MESSAGES`, default 30) — it never calls `say()`, so it can't itself trigger a reply. The `app_mention` handler is the only place a reply is ever sent; when it fires, it pulls that buffer as context and includes it in the `claude -p` prompt, so the reply is grounded in the actual recent conversation, not just the single message that mentioned it.

This buffer is **per-process, not shared across bots** — each role's `bridge.py` instance builds its own copy from the same live Slack event stream, so as long as all six have been running, they end up with equivalent (not identical) context. No shared database or file needed for this; nothing persists across a restart.

### 6.1 Persistent per-role sessions

Added 2026-07-20, once character-persona agents made "answers with amnesia after every message" actually matter (a chat companion that forgets the last exchange isn't a companion). Each role's `bridge.py` process now keeps **one continuous `claude` session across all its `@mentions`**, via `claude --session-id <uuid>` on first use and `claude --resume <uuid>` on every one after, with the uuid persisted in `scripts/slack-bridge/.sessions/<role-slug>.txt` (gitignored) so it survives process restarts. This is distinct from, and complementary to, the passive channel-history buffer above: the session is the bot's memory of its *own* conversation; the buffer is its peripheral awareness of everyone else's. See `scripts/slack-bridge/README.md § Persistent sessions` for the operational detail (including how to reset one).

## 7. Known gaps (v1, not yet solved)

- **Prompt grows unbounded over a long session** — persistent sessions (§6.1) plus the channel-history block on every turn means a bot that's been running and chatting for days accumulates a large conversation. No rotation/summarization yet; delete its `.sessions/<role>.txt` to reset.
- **Synchronous / single-threaded** — one bridge process handles one mention at a time. Fine for the current one-human, one-bot-at-a-time usage; would need a queue or async handling to scale.
- **Headless permission behavior untested** — `claude -p` may hit a tool-use permission prompt it can't answer non-interactively for anything beyond what `.claude/settings.json` already allows. Needs a real test against a task that actually exercises tools (e.g. GitHub MCP), not just a text-only question.
- **Five roles not wired yet** — only `Product_Owner` has a Socket Mode app configured. Repeating the Slack-app-config steps and running another `bridge.py` instance per role is mechanical but not done.

## 8. Next steps

See `implementation-roadmap.md` decision log (2026-07-20 entries) and step list — validating this end to end on a real Product_Owner task is the immediate next step before replicating it to the other five roles.
