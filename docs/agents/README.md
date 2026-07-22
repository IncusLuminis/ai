# IncusLuminis Agent Team

**Status:** Connected and running — GitHub MCP live, Project 2 fields configured, all four Agent roles verified running concurrently on real (read-only) work. Formal pilot (`Product_Owner` → `Coder` → `Validator` on a Project 1 Story) not started yet.
**Owner:** Product_Owner role (until a human owner is assigned)
**Version:** 0.5 — 2026-07-21
**Branch:** `feature/agent-team-design`, reviewed and merged into `main` by Mihal

## 1. Purpose

IncusLuminis runs a portfolio of independent repositories (products, shared libraries, platform standards, tooling, content, media) under one organization. This folder designs *and now hosts* a standing team of specialized agents to help run that portfolio day to day: turning specs into tracked work, writing and validating code, keeping infrastructure healthy, and getting finished content and media out the door. Six roles are built and running; several more content/production roles are proposed (see the Status column below).

`shared/ai` is the team's home: executable agent/skill definitions live in `.claude/` at this repo's root; this `docs/agents/` folder is the design and reference material behind them. See `setup.md` for how to actually run any of it. See `implementation-roadmap.md` for current status and what's still not done.

## 2. Roster

| Agent | One-line mission | Charter | Executable definition | Status |
|---|---|---|---|---|
| `Product_Owner` | Owns roadmaps, requirements, specs, backlog, progress reporting | [product-owner.md](./product-owner.md) | `.claude/skills/product-owner/` | Built |
| `Coder` | Implements Stories in code, in its own branch, per repo | [coder.md](./coder.md) | `.claude/agents/coder.md` | Built |
| `Validator` | QA gate: validates quality of code/content before merge | [validator.md](./validator.md) | `.claude/agents/validator.md` | Built |
| `DevOps` | Infrastructure, CI/CD, supporting scripts, environments | [devops.md](./devops.md) | `.claude/agents/devops.md` | Built |
| `Publisher` ("Fellow Publisher") | Publishes finished content Content_Master produces — local files (PDFs), blogs, social | [publisher.md](./publisher.md) | `.claude/skills/publisher/` | Built |
| `Media_keeper` ("Media Librarian") | Produces and owns all binary media — including external platforms (HeyGen, TikTok, YouTube) — and CDN, across every site | [media-keeper.md](./media-keeper.md) | `.claude/agents/media-keeper.md` | Built |
| `Content_Master` ("Master") | Produces and owns all text content across every site | [content-master.md](./content-master.md) | `.claude/agents/content-master.md` | Built |
| `Content_Editor` ("Editor") | Reviews content from `Content_Master` and `Content_Translator` for style, clichés, and readability, against a shared house linguistic rule set | [content-editor.md](./content-editor.md) | `.claude/agents/content-editor.md` | Built |
| `Studio_Visualizer` ("Visualizer") | Produces all animations (scientific or HUD) for Visualization Studio and Stellar Attractor, as Python/Jupyter notebooks rendering to webm/gif/mp4 | [studio-visualizer.md](./studio-visualizer.md) | *(not yet built)* | Proposed |
| `Content_Translator` ("Translator") | Translates content and UI copy between Russian and English, org-wide | [content-translator.md](./content-translator.md) | `.claude/agents/content-translator.md` | Built |
| `Fellow_Astrophysicist` ("Astrophysicist") | Reviews scientific content for accuracy on request, and researches/structures sourced infographic content briefs for Incus_Designer (physics/astronomy, biology/astrobiology, and adjacent hard sciences; NebulaCast, Visualization Studio, Stellar Attractor) | [fellow-astrophysicist.md](./fellow-astrophysicist.md) | `.claude/agents/fellow-astrophysicist.md` | Built |
| `Fellow_Historian` ("Historian") | Reviews Roads of Times content for historical accuracy on request, and researches/structures sourced write-ups (article/VK-post/infographic content brief for Incus_Designer) on historical topics | [fellow-historian.md](./fellow-historian.md) | `.claude/agents/fellow-historian.md` | Built |
| `Incus_Designer` ("Designer") | Owns logo and graphic design across every site - infographics (SVG) plus generative images via Codex CLI | [incus-designer.md](./incus-designer.md) | `.claude/agents/incus-designer.md` | Built |

Each charter file follows the same shape: mission, responsibilities, inputs/outputs, tools & access required, explicit boundaries (what it does *not* do), handoffs to the other roles, and success metrics. See `execution-model.md §2` for why each built role became a Skill vs. an Agent. The `Proposed` rows aren't approved/built yet — see [proposed-new-roles.md](./proposed-new-roles.md) for the reasoning behind this set (Stellar Attractor's named in-universe personas are a separate, later effort — not part of this functional roster).

## 3. How the pieces fit together

See [orchestration.md](./orchestration.md) for the end-to-end workflow, the status-flow across the GitHub Project board, and a RACI table across all six roles.

See [execution-model.md](./execution-model.md) for how the six roles run in practice: the team runs via **Claude Code CLI**, entirely from this repo, on Mihal's local machine only (all decided 2026-07-19). See [setup.md](./setup.md) for how to actually turn this on.

## 4. Governance this design builds on

This design does not invent process from scratch — it extends conventions already active in the org:

- `platform/standards/docs/process/github-project-management-contract.md` (v1.0) — the existing contract for **Project 1** (`IncusLuminis/projects/1`), the product Epic/Story board. Its content is unchanged; only its Owner line now points at `shared/ai` (see below).
- `platform/standards/skills/product-owner/` — the original Product Owner skill. **Superseded 2026-07-19**: replaced with a redirect to `.claude/skills/product-owner/` in this repo, which covers Project 1 and Project 2 both.
- Per-repo agent rules such as `products/nebulacast/nebulacast-app/Claude.md` (own working branch, no direct commits to `main`, PR + explicit human approval to merge) — this design proposes generalizing that pattern org-wide (flagged as an open decision, not yet made). Merge/publish approval itself is resolved: Mihal is the sole approver, across every repo.
- `docs/docs/architecture/migration-target-model.md` — the target repo layout and the code/content/media separation principle that `Media_keeper` and `DevOps` boundaries are built around.

## 5. New in this design: Project 2, and Project 1 as the first pilot target

Per the request that started this work, the agent team gets **its own operational board**: [`IncusLuminis/projects/2/views/1`](https://github.com/orgs/IncusLuminis/projects/2/views/1). This is *not* a replacement for Project 1 — product Epics/Stories continue to live there under the existing v1.0 contract. Project 2 is scoped to the agent team's own work: building out agent capabilities, cross-cutting initiatives that span multiple products, and process/tooling improvements. The contract for it is drafted in [`../process/github-project-2-contract.md`](../process/github-project-2-contract.md).

Confirmed 2026-07-19: **Project 1** ([`IncusLuminis/projects/1`](https://github.com/orgs/IncusLuminis/projects/1)) is the first real project the agents will actually work on — that's where the pilot runs, once setup is done. Current focus is finishing that setup, not piloting yet (see `implementation-roadmap.md §1`).

GitHub access for all six roles runs through the GitHub MCP server, registered locally via `scripts/setup-github-mcp.sh` — connected and verified on Mihal's machine (`claude mcp list` shows `github: ... ✔ Connected`). `gh` CLI remains the documented fallback for anything the MCP tools don't cover.

## 6. Open questions

Flagged explicitly rather than decided unilaterally — see `implementation-roadmap.md §Open questions` for the full list and reasoning.
