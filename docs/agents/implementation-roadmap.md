# Implementation Roadmap

## 0. Decision log

- **2026-07-19** — the agent team runs via **Claude Code CLI**, not only as ad hoc Cowork chat sessions. See [`execution-model.md`](./execution-model.md).
- **2026-07-19** — **skill/agent home resolved: `shared/ai`.** All six roles' executable definitions (agents + skills) live in this repo, under `.claude/`, not in `platform/standards`. This repo *is* the agent team's home now — not just its design doc.
- **2026-07-19** — **CLI runtime resolved: Mihal's local machine only.** No dedicated runner, no self-hosted or cloud CI executing agents. This caps what "automation" can mean (see `execution-model.md §4`, revised): cron-style triggers only work while the machine is on; nothing runs on GitHub-hosted infrastructure.
- **2026-07-19** — **Project 2 default repo resolved: `shared/ai`.** Matches the skill/agent home decision — one repo, one source of truth.
- **2026-07-19** — **branch/merge policy hook enforcement deferred.** Chose "let the pilot surface real friction first" over building the hook up front. The policy itself (`orchestration.md §4`) still applies as a written rule from day one; the *programmatic* (hook-based) enforcement of it is intentionally not built until the pilot (§1 step 6) shows what actually needs enforcing.

## 1. Sequenced next steps

1. ~~Review and approve this design~~ — done; the decisions above are the approval, scoped to what's decided so far.
2. **Configure Project 2 on GitHub**: create/confirm the board, add the Status/Priority/Size/Estimate fields matching the v1.0 contract's shape, add the `Agent Role` field proposed in `github-project-2-contract.md`, confirm default repo `IncusLuminis/ai`. Not done yet — needs GitHub org-admin access, which this build pass doesn't have.
3. **Install Claude Code CLI on the local machine** (if not already) and confirm `gh`/SSH auth works there — that's what makes real push/PR access possible, unlike this Cowork sandbox.
4. **Run `scripts/setup-github-mcp.sh`** (added in this pass) to register the GitHub MCP server for this project, using a Personal Access Token stored in `.env` (gitignored, never committed). See `setup.md`.
5. **Cross-link the two contracts**: add a one-line pointer from `platform/standards/docs/process/github-project-management-contract.md` (v1.0) to `docs/process/github-project-2-contract.md`, so anyone reading the org-wide standard knows Project 2 exists. This is an edit to a *different* repo (`platform/standards`) — deliberately not made in this pass without being asked.
6. **Pilot end-to-end on one low-risk Story inside `shared/ai` itself** — run `Product_Owner` → `Coder` → `Validator` only, using the agent/skill definitions added in this pass, before giving `DevOps`, `Publisher`, or `Media_keeper` real write access to infra, CDN, or publishing channels.
7. **Revisit hook enforcement** after the pilot, per the deferred decision above — write the actual hook only once the pilot shows what it needs to catch.
8. **Tighten `tools:` allowlists** on each agent definition based on what the pilot actually needed — the ones shipped in this pass are reasonable starting points, not a security review.
9. **Wire up local automation** once the pilot works: since there's no other runner, this means local cron/`launchd` jobs on Mihal's machine (for `Product_Owner` reporting, `Media_keeper` audits) — not GitHub Actions, which would count as "another runner."
10. **Wire up Publisher/Media_keeper external integrations** as they become available: CDN (Cloudflare R2) API credentials for `Media_keeper`; blog/CMS and social scheduling for `Publisher` (no matching MCP connector found during this design's research — likely needs direct API keys added to `.mcp.json`, or a custom MCP server).
11. **Define a reporting cadence** for `Product_Owner` once there's enough board activity on Project 2 to report on.

## 2. Open questions still not decided

- **Human approver of record**: is Mihal the sole merge/publish approver across every repo, or do individual products eventually get their own approver?
- **Rollout order**: this roadmap assumes a phased pilot (`Product_Owner`/`Coder`/`Validator` first, step 6). Confirmed direction, but the exact trigger for expanding to `DevOps`/`Publisher`/`Media_keeper` isn't defined yet — presumably "pilot succeeds," but that's not measurable as written.
- **Publisher/Media_keeper external tooling**: no CDN or CMS/social MCP connector currently exists — these two roles are further from "ready to operate" than the other four regardless of everything else in this roadmap.
- **What happens to the `product-owner` skill already in `platform/standards`**: this pass adds an adapted copy to `shared/ai` (aware of both Project 1 and Project 2). The `platform/standards` original is untouched — whether it should later be deprecated/pointed at the `shared/ai` version, or kept as the Project-1-only variant, isn't decided.

## 3. What this pass actually built (2026-07-19, second session)

Unlike the first design pass, this one added real, usable files to `shared/ai`:

- `.claude/agents/coder.md`, `validator.md`, `devops.md`, `media-keeper.md` — Claude Code subagent definitions.
- `.claude/skills/product-owner/`, `devops/`, `publisher/`, `media-keeper/` — Claude Code skill definitions.
- `scripts/setup-github-mcp.sh`, `.env.example`, `.gitignore` entries — local GitHub MCP setup, no secrets committed.
- `setup.md` — step-by-step instructions for running all of this from Mihal's machine.

Still not done: nothing was actually connected (no PAT exists yet, no `claude mcp add` was run — this sandbox has no `claude` binary and isn't Mihal's machine), no GitHub board configuration, no hook, no cross-repo edit to `platform/standards`. Nothing pushed to `origin` — still local-only on `feature/agent-team-design`.
