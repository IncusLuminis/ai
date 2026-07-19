# Execution Model: Claude Code CLI

**Status:** Decided, partially built
**Decision (2026-07-19):** the agent team runs via **Claude Code CLI**, not only as ad hoc Cowork chat sessions, entirely from **`shared/ai`** on **Mihal's local machine** (no other runner). This document maps the six roles onto CLI primitives, says what that unlocks, and how a session rooted in `shared/ai` reaches the rest of the portfolio.

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
| `Product_Owner` | Skill — `.claude/skills/product-owner`, adapted here to cover both Project 1 and Project 2 | Process/knowledge, not isolated execution; runs inside whichever session needs it | Interactive session, or `claude -p` for scheduled reporting |
| `Coder` | Agent — `.claude/agents/coder.md`, worktree-isolated | Needs its own branch/worktree, shouldn't pollute the invoking session's context, output is a PR | Dispatched per-Story: Mihal (or `Product_Owner`) tells the session which Story to pick up |
| `Validator` | Agent — `.claude/agents/validator.md` | Independent judgment; must not share Coder's context/bias; read-mostly tools | Invoked on a PR once opened — manually, or by a local script polling for new PRs (see §4) |
| `DevOps` | Agent — `.claude/agents/devops.md`, for routine runbooks and larger isolated infra changes alike | Kept as a single agent rather than split skill/agent — see §3 note | Explicit dispatch, or local cron health checks |
| `Publisher` | Skill — `.claude/skills/publisher`, orchestrates the existing `docx`/`pdf`/`pptx`/`schedule` skills | No isolation benefit; it's composing other skills | `schedule` skill's own cron, or dispatch on Story `Done` |
| `Media_keeper` | Agent — `.claude/agents/media-keeper.md`, covers both day-to-day lifecycle rules and batch jobs | Kept as a single agent — see §3 note | Handoff from Coder/Publisher, or scheduled audits |

Skill vs Agent per role isn't a hard rule — it's "does this need its own isolated context and tool surface, or is it a process that runs inside whoever invoked it." `Coder`, `Validator`, `DevOps`, `Media_keeper` all touch the filesystem/shell in ways worth isolating, so this build gave all four an Agent definition; `Product_Owner` and `Publisher` stay Skills since neither needs its own branch/worktree.

### Running multiple agents at once

Verified in practice 2026-07-19 (Mihal ran `Coder`/`Validator`/`DevOps`/`Media_keeper` concurrently on independent read-only audits — see `sandbox/reports/`). There are three distinct ways to get concurrency, at different levels of isolation:

1. **Task-tool dispatch within one session** — what was actually used. One `claude` session (one process, one conversation) fans out to multiple of the four Agent-type roles via its Task tool; each gets its own context, but all are children of the same parent session and report back into it. Good for a single orchestrator collecting results from independent, non-conflicting work — as in the audit above, all four were read-only, so there was no risk of two agents fighting over the same files.
2. **Separate terminal windows, each running its own `claude`** — full OS-level process isolation, own context each, but coordinated by hand (you decide what runs where).
3. **`claude --worktree` (`-w`), native since Claude Code v2.1.49 (Feb 2026)** — the right mechanism once agents are actually *writing*, not just reading. Creates a dedicated git worktree (`.claude/worktrees/<n>/`) on its own branch and starts a session inside it, so two `Coder` sessions can implement two different Stories in the same repo at the same time with zero file/branch collision. This is what "worktree-isolated" in the `Coder` row above should concretely mean once multiple Stories are in flight — option 1 is fine for read-only fan-out, but real parallel *writes* to the same repo want separate worktrees, not separate Task-tool branches within one session.

## 3. Where everything actually lives

Resolved 2026-07-19: **everything lives in `shared/ai`**, not split across `platform/standards` and `shared/ai`, and not packaged as a separate installable plugin for now:

```text
shared/ai/
├── .claude/
│   ├── agents/
│   │   ├── coder.md
│   │   ├── validator.md
│   │   ├── devops.md
│   │   └── media-keeper.md
│   └── skills/
│       ├── product-owner/
│       └── publisher/
├── scripts/
│   └── setup-github-mcp.sh
├── .env.example                   (copy to .env, fill in a real PAT — never commit .env)
├── .mcp.json                      (created by the setup script; gitignored)
└── docs/agents/                   (this design)
```

This repo *is* the agent team's home now, not just its design doc. A plugin bundle remains a reasonable future step if these definitions ever need to be installed into other orgs/repos without cloning `shared/ai`, but nothing here requires that today — since every product repo lives as a sibling directory under the same `IncusLuminis/` root, a Claude Code session rooted in `shared/ai` can already reach `../../products/*`, `../../platform/*`, etc. directly.

**How a session reaches other repos:** launch `claude` from inside `shared/ai` (so its `.claude/` and `.mcp.json` load), then have `Coder`/`DevOps`/`Media_keeper` operate on the target repo via relative (`../../products/nebulacast/nebulacast-app`) or absolute paths — Claude Code doesn't sandbox file/Bash access to the launch directory the way this Cowork session's sandbox does. Each target repo keeps owning its own git history and its own `Claude.md` conventions (e.g. `nebulacast-app/Claude.md`'s branch rules) — the agent honors those, `shared/ai` just supplies the agent itself.

## 4. What running on CLI unlocks — revised for local-machine-only

The original draft of this section assumed GitHub Actions or a dedicated runner could trigger agents. That's ruled out by the "local machine, no other runners" decision — GitHub-hosted or self-hosted Actions runners both count as "another runner." What's actually available:

- **Headless runs** on Mihal's machine: `claude -p "..." --output-format json`, invoked manually or by a local script.
- **Local cron / `launchd`** jobs (macOS) for anything that should happen on a schedule — `Product_Owner` reporting, `Media_keeper` audits. These only fire while the machine is on and awake; there's no 24/7 guarantee.
- **No instant webhook-triggered `Validator` runs.** Without a runner, a PR being opened doesn't automatically invoke anything. The realistic pattern is either manual ("review PR #12") or a local polling script that checks for new PRs periodically while the machine is on.
- **Hooks** (once built — deferred per the roadmap's decision log) still work locally regardless of the runner question, since they fire on tool calls within a running Claude Code session.
- **MCP servers wired directly** via `.mcp.json`, not gated by a connector registry — see `setup.md` for the actual GitHub MCP setup.

## 5. Still open — not decided here

- **Per-agent `tools:` allowlists**: the definitions added in this pass are reasonable starting points, not a completed least-privilege review.
- **GitHub MCP token scope**: a Personal Access Token is required (see `setup.md`); exact scopes needed depend on which GitHub MCP tools `Product_Owner`/`Coder` end up using.
- **Local polling vs. manual dispatch for `Validator`**: not built in this pass — noted above as the realistic option given no runner, but the mechanism itself isn't implemented.

Resolved since the first draft of this section: human approver of record (Mihal, sole, every repo) and rollout order (no gate — `DevOps`/`Publisher`/`Media_keeper` are built and idle, used on demand rather than after a pilot milestone). See `implementation-roadmap.md §0`.
