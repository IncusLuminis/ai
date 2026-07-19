# IncusLuminis Agent Team — Design

**Status:** Draft / Proposed — not yet implemented
**Owner:** Product_Owner role (until a human owner is assigned)
**Version:** 0.1 — 2026-07-19
**Branch:** `feature/agent-team-design`

## 1. Purpose

IncusLuminis runs a portfolio of independent repositories (products, shared libraries, platform standards, tooling, content, media) under one organization. This document set designs a standing team of six specialized agents to help run that portfolio day to day: turning specs into tracked work, writing and validating code, keeping infrastructure healthy, and getting finished content and media out the door.

This is a **design document**, not an implementation. No agent skills, MCP connections, or board configuration have been created yet — see `implementation-roadmap.md` for what would happen next if this design is approved.

## 2. Roster

| Agent | One-line mission | Detail |
|---|---|---|
| `Product_Owner` | Owns roadmaps, requirements, specs, backlog, progress reporting | [product-owner.md](./product-owner.md) |
| `Coder` | Implements Stories in code, in its own branch, per repo | [coder.md](./coder.md) |
| `Validator` | QA gate: validates quality of code/content before merge | [validator.md](./validator.md) |
| `DevOps` | Infrastructure, CI/CD, supporting scripts, environments | [devops.md](./devops.md) |
| `Publisher` | Publishes finished content: blogs, social, PDFs, documents | [publisher.md](./publisher.md) |
| `Media_keeper` | Manages binary/media assets and CDN + local storage | [media-keeper.md](./media-keeper.md) |

Each role file follows the same shape: mission, responsibilities, inputs/outputs, tools & access required, explicit boundaries (what it does *not* do), handoffs to the other five roles, and success metrics.

## 3. How the pieces fit together

See [orchestration.md](./orchestration.md) for the end-to-end workflow, the status-flow across the GitHub Project board, and a RACI table across all six roles.

## 4. Governance this design builds on

This design does not invent process from scratch — it extends conventions already active in the org:

- `platform/standards/docs/process/github-project-management-contract.md` (v1.0) — the existing contract for **Project 1** (`IncusLuminis/projects/1`), the product Epic/Story board. That contract is unchanged by this work.
- `platform/standards/skills/product-owner/` — the existing Product Owner skill, which this design's `Product_Owner` role adopts as-is for Project 1 work, and extends for Project 2 (see below).
- Per-repo agent rules such as `products/nebulacast/nebulacast-app/Claude.md` (own working branch, no direct commits to `main`, PR + explicit human approval to merge) — this design proposes generalizing that pattern org-wide (flagged as an open decision, not yet made).
- `docs/docs/architecture/migration-target-model.md` — the target repo layout and the code/content/media separation principle that `Media_keeper` and `DevOps` boundaries are built around.

## 5. New in this design: Project 2

Per the request that started this work, the agent team gets **its own operational board**: [`IncusLuminis/projects/2/views/1`](https://github.com/orgs/IncusLuminis/projects/2/views/1). This is *not* a replacement for Project 1 — product Epics/Stories continue to live there under the existing v1.0 contract. Project 2 is scoped to the agent team's own work: building out agent capabilities, cross-cutting initiatives that span multiple products, and process/tooling improvements. The contract for it is drafted in [`../process/github-project-2-contract.md`](../process/github-project-2-contract.md).

GitHub access for all six roles is designed around a GitHub MCP connector (not yet installed in this workspace — see roadmap). Until that's connected, any agent needing GitHub write access falls back to `gh` CLI, matching the existing product-owner skill's documented fallback.

## 6. Open questions

Flagged explicitly rather than decided unilaterally — see `implementation-roadmap.md §Open questions` for the full list and reasoning.
