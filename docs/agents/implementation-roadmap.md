# Implementation Roadmap (not executed in this pass)

This design pass produced documents only — charters, orchestration model, and a Project 2 contract draft. Nothing below has been done yet. This is the "what we'd do next" list.

## 0. Decision log

- **2026-07-19** — the agent team runs via **Claude Code CLI**, not only as ad hoc Cowork chat sessions. See [`execution-model.md`](./execution-model.md) for what that means per role and what it unlocks (headless runs, hooks, direct MCP config, per-repo GitHub Actions triggers).

## 1. Sequenced next steps

1. **Review and approve this design** — confirm the six charters, the orchestration model, and the Project 2 scope actually match intent before anything is built.
2. **Configure Project 2 on GitHub**: create/confirm the board, add the Status/Priority/Size/Estimate fields matching v1.0's shape, add the proposed `Agent Role` field, confirm default repo.
3. **Set up Claude Code CLI as the runtime** for the team, per `execution-model.md`: decide where it runs (local machine vs. a dedicated always-on runner), confirm `gh`/SSH auth is available there for real push/PR access.
4. **Add a GitHub MCP server to `.mcp.json`** so agents can create/move issues and read PRs programmatically — this is a direct CLI config step now, not gated on Cowork's connector registry (which had no match at design time). Verify write access for `Product_Owner` first, since it's the only role that strictly needs it on day one.
5. **Cross-link the two contracts**: add a one-line pointer from `platform/standards/docs/process/github-project-management-contract.md` (v1.0) to the new `docs/process/github-project-2-contract.md`, so anyone reading the org-wide standard knows Project 2 exists. No changes to v1.0's own content.
6. **Build the `incusluminis-agent-team` plugin** in `platform/standards` (recommended location — see `execution-model.md §3`): the four Skills (`product-owner` moved/synced in, plus `devops`, `publisher`, `media-keeper`) and the Agent definitions (`coder.md`, `validator.md`, and heavier isolated variants of `devops`/`media-keeper`) live here as one versioned, installable unit rather than being copy-pasted per repo.
7. **Write least-privilege `tools:` allowlists** for each Agent definition before any of them gets real push/deploy/publish access — not drafted in this design pass.
8. **Add the branch-policy hook** (`orchestration.md §4`) as an actual Claude Code hook in the plugin, so "no direct commits to `main`" is enforced at the tool-call level, not just documented — and formalize the same rule as an org-wide written default in `platform/standards`, rather than leaving it documented only in `nebulacast-app/Claude.md`.
9. **Pilot end-to-end on one low-risk Story** — recommend starting inside `shared/ai` or `tools` rather than a live product — running `Product_Owner` → `Coder` → `Validator` only, before giving `DevOps`, `Publisher`, or `Media_keeper` write access to real infra, CDN, or publishing channels.
10. **Wire up automation triggers** once the pilot works: a per-repo GitHub Actions workflow invoking `Validator` headlessly on `pull_request`, cron for `Product_Owner` reporting and `Media_keeper` audits.
11. **Wire up Publisher/Media_keeper external integrations** as they become available: CDN (Cloudflare R2) API credentials for `Media_keeper`; blog/CMS and social scheduling connectors for `Publisher` (none found in the current MCP registry search — likely needs direct API keys or a custom MCP server added via `.mcp.json`).
12. **Define a reporting cadence** for `Product_Owner` (e.g. weekly rollup) once there's enough board activity to report on.

## 2. Open questions (flagged, not decided here)

- **Skill/agent home** — *leaning resolved*: package as the `incusluminis-agent-team` plugin in `platform/standards` (step 6), consistent with it already hosting `product-owner`/`repo-migration`. Not fully final — the plugin/marketplace name and repo are still a recommendation, not a confirmed decision.
- **Where the CLI runs**: Mihal's local machine, a dedicated always-on runner, or both — affects secrets handling and whether cron/webhook triggers (step 10) are even reachable. Not decided.
- **Project 2 default repo**: is `IncusLuminis/ai` the right default, or should a different repo own agent-team process issues?
- **Branch/merge policy formalization + hook enforcement**: worth doing before the pilot, or let the pilot (step 9) surface real friction first?
- **Human approver of record**: is Mihal the sole merge/publish approver across every repo, or do individual products eventually get their own approver? Also determines the service identity for automated triggers (step 10) — a bot/service account vs. reusing a human token.
- **Rollout order**: this roadmap assumes a phased pilot (PO/Coder/Validator first). Confirm that's the right order versus standing up all six at once.
- **Publisher/Media_keeper external tooling**: no CDN or CMS/social MCP connector currently exists — confirms these two roles are further from "ready to operate" than the other four regardless of approval timing.

## 3. Explicitly out of scope for this pass

No agent/skill files, plugin, or hooks were created. No MCP servers were configured. No GitHub board/fields were configured. No changes were made to `platform/standards`' existing v1.0 contract. No CLI runtime was set up. Nothing was pushed to `origin` — this work exists only on the local `feature/agent-team-design` branch in `shared/ai` pending review.
