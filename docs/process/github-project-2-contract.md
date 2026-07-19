# GitHub Project Management Contract — Project 2 (Agent Team Operations Board)

**Status:** Drafted; field-setup scripted (`scripts/setup-project-2-fields.sh`), not yet run against the live board
**Applies to:** [`IncusLuminis/projects/2/views/1`](https://github.com/orgs/IncusLuminis/projects/2/views/1)
**Owner:** `Product_Owner` agent role
**Version:** 0.2 — 2026-07-19
**Relationship to Project 1:** This contract does not replace or modify `platform/standards/docs/process/github-project-management-contract.md` (v1.0), which remains the source of truth for `IncusLuminis/projects/1` and product Epic/Story work. Project 2 is a separate board scoped to the agent team's own operational work: building out agent capability, cross-cutting process/tooling initiatives, and anything spanning multiple products that doesn't belong on a single product's backlog.

## 1. Purpose

Same mechanics as the v1.0 contract — one consistent way to structure, type, and track work — applied to a different scope of work and (proposed) a different default repo.

## 2. Scope: what goes on Project 2 vs Project 1

| Goes on Project 2 | Stays on Project 1 |
|---|---|
| Building/refining the six agent roles themselves | Any product feature/bugfix work (RoadsOfTimes, NebulaCast, Stellar Attractor, Visualization Studio, etc.) |
| Org-wide process/standards changes (e.g. formalizing the branch policy in `orchestration.md §4`) | Product-specific Stories, even if implemented by an agent |
| Cross-cutting initiatives touching 3+ repos with no single product owner | Single-product infra/content work |
| GitHub MCP / tooling setup for the agent team | — |

When in doubt, `Product_Owner` should default to Project 1 — Project 2 exists for genuinely agent-team-scoped work, not as a second home for product Stories.

**Project 1 is also the team's first pilot target.** Once the infrastructure/CLI setup in `../agents/setup.md` is done, the pilot (`../agents/implementation-roadmap.md §1` step 5) runs `Product_Owner` → `Coder` → `Validator` against a real Story on Project 1 — not a synthetic task invented on Project 2. Project 2 tracks the *building* of the team; Project 1 is where the team does its first real work.

## 3. Hierarchy and required fields

Identical to v1.0 §2–3 (Epic → Story via Issue Type + native Sub-issues; Status/Priority/Size/Estimate/Start date/Target date/Sub-issues progress). Not repeated here to avoid drift — see the canonical text in `platform/standards`.

**Addition specific to Project 2:** an `Agent Role` field (single-select: `Product_Owner`, `Coder`, `Validator`, `DevOps`, `Publisher`, `Media_keeper`) so a card's owning role is visible on the board without reading the body. This does not exist on Project 1 and is not proposed there — it's specific to a board whose primary axis of organization is "which agent owns this," rather than "which product." `scripts/setup-project-2-fields.sh` creates this field (plus `Size`/`Estimate`) via `gh`, idempotently — not yet run against the live board.

## 4. Default repo

**Resolved (2026-07-19): `IncusLuminis/ai` (`shared/ai`).** This is also where the agent team's executable definitions live (`.claude/agents/`, `.claude/skills/` — see `../agents/execution-model.md §3`), so the repo housing Project 2's default issues and the repo housing the agents that work them are the same one.

## 5. Epic and Story templates

Same templates as v1.0 §5–6, with one substitution: the Epic's `## Source` line should point at the design doc(s) in `shared/ai/docs/agents/` this work derives from, the same way a product Epic points at its spec.

## 6. Access

GitHub MCP is the access mechanism for `Product_Owner` (and any other role that needs to create/move cards), run locally on Mihal's machine via `scripts/setup-github-mcp.sh` (see `../agents/setup.md`) — not through Cowork's connector registry, which had no matching connector at design time. Until the script has actually been run with a real Personal Access Token, fall back to `gh` CLI, matching the existing product-owner skill's documented fallback for browser/API-less environments.

## 7. Non-goals

Same as v1.0 §8: sprint cadence, capacity planning, cross-Epic roadmap sequencing are out of scope here too.
