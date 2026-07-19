# IncusLuminis Agent Team

**Status:** Charters designed, executable definitions built, key operating decisions resolved, not yet connected/piloted
**Owner:** Product_Owner role (until a human owner is assigned)
**Version:** 0.3 — 2026-07-19
**Branch:** `feature/agent-team-design`

## 1. Purpose

IncusLuminis runs a portfolio of independent repositories (products, shared libraries, platform standards, tooling, content, media) under one organization. This folder designs *and now hosts* a standing team of six specialized agents to help run that portfolio day to day: turning specs into tracked work, writing and validating code, keeping infrastructure healthy, and getting finished content and media out the door.

`shared/ai` is the team's home: executable agent/skill definitions live in `.claude/` at this repo's root; this `docs/agents/` folder is the design and reference material behind them. See `setup.md` for how to actually run any of it. See `implementation-roadmap.md` for what's still not done — no GitHub MCP connection has been made yet, no board has been configured, and nothing has been piloted.

## 2. Roster

| Agent | One-line mission | Charter | Executable definition |
|---|---|---|---|
| `Product_Owner` | Owns roadmaps, requirements, specs, backlog, progress reporting | [product-owner.md](./product-owner.md) | `.claude/skills/product-owner/` |
| `Coder` | Implements Stories in code, in its own branch, per repo | [coder.md](./coder.md) | `.claude/agents/coder.md` |
| `Validator` | QA gate: validates quality of code/content before merge | [validator.md](./validator.md) | `.claude/agents/validator.md` |
| `DevOps` | Infrastructure, CI/CD, supporting scripts, environments | [devops.md](./devops.md) | `.claude/agents/devops.md` |
| `Publisher` | Publishes finished content: blogs, social, PDFs, documents | [publisher.md](./publisher.md) | `.claude/skills/publisher/` |
| `Media_keeper` | Manages binary/media assets and CDN + local storage | [media-keeper.md](./media-keeper.md) | `.claude/agents/media-keeper.md` |

Each charter file follows the same shape: mission, responsibilities, inputs/outputs, tools & access required, explicit boundaries (what it does *not* do), handoffs to the other five roles, and success metrics. See `execution-model.md §2` for why each role became a Skill vs. an Agent.

## 3. How the pieces fit together

See [orchestration.md](./orchestration.md) for the end-to-end workflow, the status-flow across the GitHub Project board, and a RACI table across all six roles.

See [execution-model.md](./execution-model.md) for how the six roles run in practice: the team runs via **Claude Code CLI**, entirely from this repo, on Mihal's local machine only (all decided 2026-07-19). See [setup.md](./setup.md) for how to actually turn this on.

## 4. Governance this design builds on

This design does not invent process from scratch — it extends conventions already active in the org:

- `platform/standards/docs/process/github-project-management-contract.md` (v1.0) — the existing contract for **Project 1** (`IncusLuminis/projects/1`), the product Epic/Story board. Its content is unchanged; only its Owner line now points at `shared/ai` (see below).
- `platform/standards/skills/product-owner/` — the original Product Owner skill. **Superseded 2026-07-19**: replaced with a redirect to `.claude/skills/product-owner/` in this repo, which covers Project 1 and Project 2 both.
- Per-repo agent rules such as `products/nebulacast/nebulacast-app/Claude.md` (own working branch, no direct commits to `main`, PR + explicit human approval to merge) — this design proposes generalizing that pattern org-wide (flagged as an open decision, not yet made). Merge/publish approval itself is resolved: Mihal is the sole approver, across every repo.
- `docs/docs/architecture/migration-target-model.md` — the target repo layout and the code/content/media separation principle that `Media_keeper` and `DevOps` boundaries are built around.

## 5. New in this design: Project 2

Per the request that started this work, the agent team gets **its own operational board**: [`IncusLuminis/projects/2/views/1`](https://github.com/orgs/IncusLuminis/projects/2/views/1). This is *not* a replacement for Project 1 — product Epics/Stories continue to live there under the existing v1.0 contract. Project 2 is scoped to the agent team's own work: building out agent capabilities, cross-cutting initiatives that span multiple products, and process/tooling improvements. The contract for it is drafted in [`../process/github-project-2-contract.md`](../process/github-project-2-contract.md).

GitHub access for all six roles runs through the GitHub MCP server, registered locally via `scripts/setup-github-mcp.sh` (see `setup.md`) — not yet actually run against a real token as of this commit. Until it has been, any agent needing GitHub write access falls back to `gh` CLI, matching the existing product-owner skill's documented fallback.

## 6. Open questions

Flagged explicitly rather than decided unilaterally — see `implementation-roadmap.md §Open questions` for the full list and reasoning.
