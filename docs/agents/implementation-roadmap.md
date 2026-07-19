# Implementation Roadmap

## 0. Decision log

- **2026-07-19** — the agent team runs via **Claude Code CLI**, not only as ad hoc Cowork chat sessions. See [`execution-model.md`](./execution-model.md).
- **2026-07-19** — **skill/agent home resolved: `shared/ai`.** All six roles' executable definitions (agents + skills) live in this repo, under `.claude/`, not in `platform/standards`. This repo *is* the agent team's home now — not just its design doc.
- **2026-07-19** — **CLI runtime resolved: Mihal's local machine only.** No dedicated runner, no self-hosted or cloud CI executing agents. This caps what "automation" can mean (see `execution-model.md §4`): cron-style triggers only work while the machine is on; nothing runs on GitHub-hosted infrastructure.
- **2026-07-19** — **Project 2 default repo resolved: `shared/ai`.** Matches the skill/agent home decision — one repo, one source of truth.
- **2026-07-19** — **branch/merge policy hook enforcement deferred.** Chose "let the pilot surface real friction first" over building the hook up front. The policy itself (`orchestration.md §4`) still applies as a written rule from day one; the *programmatic* (hook-based) enforcement of it is intentionally not built until the pilot (§1 step 5) shows what actually needs enforcing.
- **2026-07-19** — **human approver of record resolved: Mihal, sole approver, across every repo, no exceptions carved out yet.** `orchestration.md` already reflected this; treated as confirmed rather than open now.
- **2026-07-19** — **no phased rollout gate.** All six roles are built. `Product_Owner`, `Coder`, `Validator` are the ones with an obvious, immediate reason to be used (there's a design to pilot on). `DevOps`, `Publisher`, `Media_keeper` are equally ready but have no queued work yet — they stay idle and get invoked whenever real demand shows up, not on a schedule or a "pilot passed" gate.
- **2026-07-19** — **Publisher/Media_keeper external tooling deliberately deferred.** CDN (R2) and CMS/social integrations will be specified one at a time, as each is actually needed, rather than designed speculatively now.
- **2026-07-19** — **`platform/standards`'s `product-owner` skill superseded, not removed.** Replaced its `SKILL.md` with a short redirect to `shared/ai/.claude/skills/product-owner/` (done on branch `chore/point-product-owner-skill-to-shared-ai` in that repo) and updated the v1.0 contract's Owner line to match. The contract's substantive content is untouched. `references/github-project-contract.md` alongside the old skill is left in place, unused but harmless.
- **2026-07-19** — **Project 1 vs Project 2 confirmed.** Project 2 is for developing the agent team itself. The agents obviously work on other, real projects too — **Project 1** (`IncusLuminis/projects/1`) is the first of those, and is where the pilot (step 5 below) will actually run. Current focus, per direct instruction: finish infrastructure/CLI setup before piloting — not start piloting yet.

## 1. Sequenced next steps

1. ~~Review and approve this design~~ — done; the decisions above are the approval.
2. **Check prerequisites, then configure Project 2 on GitHub**: run `scripts/check-prereqs.sh`, then `scripts/setup-github-mcp.sh`, then `scripts/setup-project-2-fields.sh` (all added this session — see `setup.md`). The field-creation script handles `Size`/`Estimate`/`Agent Role` via `gh`; Status option values and org-level Issue-field columns still need one manual pass in the Project 2 UI (the script prints exactly what's left).
3. **Install Claude Code CLI on the local machine** (if not already) — `check-prereqs.sh` verifies this.
4. **Run the three setup scripts above** in order (prereqs → MCP → Project 2 fields), using a PAT stored in `.env` (gitignored). See `setup.md`.
5. **Pilot on a real Story from Project 1**, once steps 2–4 are done — run `Product_Owner` → `Coder` → `Validator` end to end against an actual product Story, not a synthetic task. No gate on the other three roles; use them as soon as there's a real Task/asset/publish need, pilot or not.
6. **Revisit hook enforcement** after the pilot, per the deferred decision above.
7. **Tighten `tools:` allowlists** on each agent definition based on what actually gets used — the ones shipped so far are reasonable starting points, not a security review.
8. **Wire up local automation** once there's a reason to: local cron/`launchd` jobs on Mihal's machine for `Product_Owner` reporting, `Media_keeper` audits, etc. — not GitHub Actions, which would count as "another runner."
9. **Specify Publisher/Media_keeper external integrations one at a time**, as each becomes the actual bottleneck — e.g. Cloudflare R2 credentials the first time `Media_keeper` needs to push somewhere real, a CMS/social connector the first time `Publisher` needs to post somewhere real.
10. **Define a reporting cadence** for `Product_Owner` once there's enough board activity on Project 2 to report on.

## 2. Open questions still not decided

- **Cross-linking the v1.0 contract to the Project 2 contract**: `platform/standards/docs/process/github-project-management-contract.md`'s Owner line now points at `shared/ai`, but nothing in it yet mentions Project 2 exists. Small remaining edit, not done yet.
- **Which Project 1 Story to pilot on**: step 5 needs a specific, actual Story picked once setup is done — not chosen yet.

## 3. What's been built so far (2026-07-19, second session)

In `shared/ai`:

- `.claude/agents/coder.md`, `validator.md`, `devops.md`, `media-keeper.md` — Claude Code subagent definitions.
- `.claude/skills/product-owner/`, `publisher/` — Claude Code skill definitions. (`DevOps` and `Media_keeper` ended up as agent-only, not also skills — see `execution-model.md §2`.)
- `scripts/check-prereqs.sh` — read-only check for `claude`/`gh`/`git`/SSH access.
- `scripts/setup-github-mcp.sh`, `.env.example`, `.gitignore` entries — local GitHub MCP setup, no secrets committed.
- `scripts/setup-project-2-fields.sh` — idempotent `gh`-based creation of Project 2's `Size`/`Estimate`/`Agent Role` fields.
- `setup.md` — step-by-step instructions for running all of the above from Mihal's machine.

**Verified on Mihal's actual machine (2026-07-19):** `scripts/check-prereqs.sh` passes clean — `claude`, `gh`, `git` on `PATH`, `gh` authenticated, SSH access to `github.com` confirmed. `scripts/setup-github-mcp.sh` has been run with a real IncusLuminis-scoped PAT — `claude mcp list` shows `github: https://api.githubcopilot.com/mcp (HTTP) - ✔ Connected`. Along the way, hit and fixed an unrelated `nvm`-vs-Homebrew-Node `claude` install issue (documented in `setup.md §6`). Next: `setup-project-2-fields.sh` — not run yet.

Also present but unrelated: `claude mcp list` shows a second, pre-existing entry `plugin:github:github` that fails to connect — looks like a bundled Claude Code plugin distinct from what this script adds. Not investigated yet; doesn't block anything since our own `github` entry connects fine.

In `platform/standards` (separate repo, branch `chore/point-product-owner-skill-to-shared-ai`):

- `skills/product-owner/SKILL.md` replaced with a redirect to `shared/ai`.
- `docs/process/github-project-management-contract.md`'s Owner line updated to match; contract content otherwise untouched.

Still not done: Project 2's `Size`/`Estimate`/`Agent Role` fields not created yet (`setup-project-2-fields.sh` not run), no hook. Nothing pushed to `origin` on either repo — both branches are local-only.
