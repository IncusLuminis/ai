# Implementation Roadmap (not executed in this pass)

This design pass produced documents only — charters, orchestration model, and a Project 2 contract draft. Nothing below has been done yet. This is the "what we'd do next" list.

## 1. Sequenced next steps

1. **Review and approve this design** — confirm the six charters, the orchestration model, and the Project 2 scope actually match intent before anything is built.
2. **Configure Project 2 on GitHub**: create/confirm the board, add the Status/Priority/Size/Estimate fields matching v1.0's shape, add the proposed `Agent Role` field, confirm default repo.
3. **Connect a GitHub MCP server** so agents can create/move issues and read PRs programmatically, per the answer already given (MCP preferred over `gh` CLI or browser automation as the primary path). Verify write access for `Product_Owner` first, since it's the only role that strictly needs it on day one.
4. **Cross-link the two contracts**: add a one-line pointer from `platform/standards/docs/process/github-project-management-contract.md` (v1.0) to the new `docs/process/github-project-2-contract.md`, so anyone reading the org-wide standard knows Project 2 exists. No changes to v1.0's own content.
5. **Decide where executable skill definitions live**: `platform/standards/skills/` already holds `product-owner` and `repo-migration` as the org's skill home. Two options: (a) put all six agents' skills there for consistency with existing precedent, or (b) keep them in `shared/ai` alongside this design so the "ai team" repo is self-contained. Not decided in this pass — see open questions.
6. **Author the actual SKILL.md-style definitions** for each of the six roles, once the above is settled — this design's charter files are the source material, not the executable form.
7. **Formalize the branch/merge policy** (`orchestration.md §4`) as an org-wide default in `platform/standards`, rather than leaving it documented only in `nebulacast-app/Claude.md`.
8. **Pilot end-to-end on one low-risk Story** — recommend starting inside `shared/ai` or `tools` rather than a live product — running `Product_Owner` → `Coder` → `Validator` only, before giving `DevOps`, `Publisher`, or `Media_keeper` write access to real infra, CDN, or publishing channels.
9. **Wire up Publisher/Media_keeper external integrations** as they become available: CDN (Cloudflare R2) API credentials for `Media_keeper`; blog/CMS and social scheduling connectors for `Publisher` (none found in the current MCP registry search — likely needs direct API keys or a custom connector).
10. **Define a reporting cadence** for `Product_Owner` (e.g. weekly rollup) once there's enough board activity to report on.

## 2. Open questions (flagged, not decided here)

- **Skill home**: `platform/standards/skills/` vs `shared/ai` for the six agents' executable definitions (see step 5).
- **Project 2 default repo**: is `IncusLuminis/ai` the right default, or should a different repo own agent-team process issues?
- **Branch/merge policy formalization**: worth doing now, or wait until the pilot (step 8) surfaces real friction first?
- **Human approver of record**: is Mihal the sole merge/publish approver across every repo, or do individual products eventually get their own approver?
- **Rollout order**: this roadmap assumes a phased pilot (PO/Coder/Validator first). Confirm that's the right order versus standing up all six at once.
- **Publisher/Media_keeper external tooling**: no CDN or CMS/social MCP connector currently exists in this workspace's registry — confirms these two roles are further from "ready to operate" than the other four regardless of approval timing.

## 3. Explicitly out of scope for this pass

No agent skill files were created. No MCP connectors were installed. No GitHub board/fields were configured. No changes were made to `platform/standards`' existing v1.0 contract. Nothing was pushed to `origin` — this work exists only on the local `feature/agent-team-design` branch in `shared/ai` pending review.
