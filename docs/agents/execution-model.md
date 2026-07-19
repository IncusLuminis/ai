# Execution Model: Claude Code CLI

**Status:** Draft / Proposed
**Decision (2026-07-19):** the agent team runs via **Claude Code CLI**, not only as ad hoc Cowork chat sessions. This document maps the six roles onto CLI primitives and says what that unlocks and what it still requires.

## 1. Why CLI, not just chat

Drafting this design inside a Cowork sandbox surfaced the concrete limits of chat-only execution:

- No SSH access to `github.com:IncusLuminis/*` from the sandbox — this design's own branch (`feature/agent-team-design`) could be committed locally but not pushed. A CLI session running on a real machine or CI runner, with real `gh auth`/SSH already configured, doesn't have this problem.
- No GitHub MCP connector available through Cowork's connector registry (checked during this design pass). The CLI isn't limited to that registry — MCP servers are added directly via `claude mcp add` or a repo's `.mcp.json`.
- Chat sessions are inherently manual — someone has to open the conversation and ask. The CLI supports headless, non-interactive invocation (`claude -p "..." --output-format json`), which is what turns "ask Validator to look at this" into "Validator runs automatically on every PR."
- Chat has no hook mechanism to enforce policy programmatically. The CLI does — `orchestration.md §4`'s branch/merge rule can become a pre-commit/pre-push hook instead of a document an agent could in principle ignore.

None of this makes Cowork wrong for the *design* work (like this document) — it's a reasonable place to plan and to run occasional interactive sessions. It's the wrong place for the *standing* team to actually live.

## 2. Mapping roles to CLI primitives

| Role | Primitive | Why | Typical trigger |
|---|---|---|---|
| `Product_Owner` | Skill — `.claude/skills/product-owner` (already exists in `platform/standards`), extended for Project 2 | Process/knowledge, not isolated execution; runs inside whichever session needs it | Interactive session, or `claude -p` for scheduled reporting |
| `Coder` | Agent — `.claude/agents/coder.md`, worktree-isolated | Needs its own branch/worktree, shouldn't pollute the invoking session's context, output is a PR | Dispatched per-Story (script reads `Ready` cards off the board, invokes the agent per Story) |
| `Validator` | Agent — `.claude/agents/validator.md` | Independent judgment; must not share Coder's context/bias; read-mostly tools | GitHub Actions on `pull_request` events, headless |
| `DevOps` | Skill for routine runbooks + Agent for larger isolated infra changes | Most DevOps work is "follow the runbook" inside an existing session; big changes warrant isolation | Cron health checks, CI-failure webhook, explicit Task issue |
| `Publisher` | Skill — orchestrates the existing `docx`/`pdf`/`pptx`/`schedule` skills | No isolation benefit; it's composing other skills | `schedule` skill's own cron, or dispatch on Story `Done` |
| `Media_keeper` | Skill for lifecycle standards + Agent for batch processing jobs | Day-to-day rules are a runbook; bulk re-encoding/dedup jobs benefit from isolation | Handoff from Coder/Publisher, or scheduled audits |

Skill vs Agent per role isn't a hard rule — it's "does this need its own isolated context and tool surface, or is it a process that runs inside whoever invoked it." Several roles are both, depending on the task's size.

## 3. Packaging: one internal plugin

Recommendation: package all six roles as a single Claude Code **plugin** rather than loose per-repo `.claude/` folders, so there's one source of truth instead of six things drifting independently:

```text
incusluminis-agent-team/           (proposed plugin name, not final)
├── skills/
│   ├── product-owner/             (already exists — moved/synced in, not rewritten)
│   ├── devops/
│   ├── publisher/
│   └── media-keeper/
├── agents/
│   ├── coder.md
│   ├── validator.md
│   ├── devops.md                  (heavier, isolated-infra variant)
│   └── media-keeper.md            (batch-processing variant)
├── hooks/
│   └── enforce-branch-policy.*    (blocks direct commits to main, per orchestration.md §4)
└── .mcp.json                      (GitHub MCP; later R2 / CMS / social MCPs as they exist)
```

This directly resolves `implementation-roadmap.md`'s open question about where executable definitions should live: **`platform/standards`**, packaged as a plugin — consistent with it already being the org's home for `product-owner` and `repo-migration`, and installable into any product repo that needs the team without copy-pasting files.

## 4. What running on CLI unlocks operationally

- **Headless runs** for anything that shouldn't need a human to open a chat: `claude -p "..." --output-format json`, scriptable from cron or CI.
- **Hooks** enforcing the branch/merge policy at the tool-call level, not just as a written rule.
- **Per-repo GitHub Actions** triggering `Validator` on PR open, `DevOps` on deploy/CI-failure events.
- **Cron** (via the `schedule` skill or plain OS cron on wherever the CLI runs) for `Product_Owner` reporting and `Media_keeper` audits.
- **MCP servers wired directly**, not gated by a connector registry — closes the GitHub access gap flagged in `../process/github-project-2-contract.md §6`.

## 5. Still open — not decided here

- **Where the CLI actually runs**: Mihal's local machine, a dedicated always-on runner, or both. Affects secrets handling and whether cron/webhook triggers are even reachable.
- **Plugin/marketplace repo**: proposing `platform/standards`; not finalized.
- **Per-agent `tools:` allowlists**: need to be written to least-privilege before any agent gets real push/deploy/publish access — not drafted in this pass.
- **GitHub MCP server choice** and its `.mcp.json` configuration.
- **Service identity for automated triggers** (e.g. Validator's GitHub Action): a bot/service account vs. reusing a human token — security decision, not made here.
