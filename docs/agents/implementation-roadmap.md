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
- **2026-07-19** — **secrets hygiene tightened.** Raised by Mihal after seeing the raw PAT sitting in `.env`: gitignored is not the same as safe from an agent with `Read` access to the whole repo. Response: `.env` deleted once `setup-github-mcp.sh` had run (the live credential lives in `~/.claude.json`, outside the repo, not in `.env`); added `.claude/settings.json` with `permissions.deny` rules blocking `Read`/`Bash(cat ...)` on `.env` and `.mcp.json` as defense in depth — explicitly documented as imperfect (known Anthropic issue with `Read` deny not always covering `.env`; `Bash` deny only matches the literal command pattern listed, not every way to read a file). Real protection is "the secret isn't sitting in a file agents can read," not the deny rule.
- **2026-07-19** — **approved for merge to `main`.** Mihal reviewed this session's work and gave explicit sign-off to merge `feature/agent-team-design` (this repo) and `chore/point-product-owner-skill-to-shared-ai` (`platform/standards`) into their respective `main` branches — this is the human-approval step `orchestration.md §4` requires; nothing here was merged unsupervised. The actual push/merge has to run on Mihal's machine, not from the sandbox that authored these docs (no `origin` write access here) — see the commands given in chat.
- **2026-07-19** — **first real concurrency test, post-merge.** Mihal ran `claude` from `shared/ai` and dispatched `Coder`, `Validator`, `DevOps`, and `Media_keeper` in parallel via the Task tool on independent, read-only audits. All four completed and wrote reports to `sandbox/reports/`. `Validator` found 6 internal doc inconsistencies (stale skill/agent mapping, a stale `product-owner.md` reference, two status-flow gaps for non-PR work, an uncited claim, a stale README header) — all fixed in this pass. `Coder`, `DevOps`, and `Media_keeper` surfaced real portfolio findings (13/14 repos have zero CI; `tools` repo has a version mismatch and committed cruft; `shared/assets` is 928 MB locally with some duplicate files but correctly keeps binaries out of git) — not yet turned into backlog items; see the reports and the next roadmap step.
- **2026-07-20** — **six separate Slack apps, not one app + `chat:write.customize`.** Each agent role gets its own Slack app (own name, own avatar) so the team channel reads as six distinct teammates. Rejected the alternative of one shared app using `chat:write.customize` to override username/icon per message — too easy for agent code to forget to pass it, and identity would live in application code instead of Slack config. First one created: "Incus PO" for `Product_Owner`.
- **2026-07-20** — **two-way Slack via Socket Mode, not Slack's hosted MCP Server.** Slack's own MCP server (`mcp.slack.com`) was considered for letting agents read/post to Slack, but it authenticates as the human user who did OAuth, not as a distinct bot — would collapse all six personas into one voice. Built instead: `scripts/slack-bridge/bridge.py`, a per-role Socket Mode listener (no public webhook needed — fits the local-machine-only constraint) that answers `@mentions` with a headless `claude -p` call and posts the reply back in-thread. Wired for `Product_Owner` only so far; not yet validated against a real tool-heavy task. See `slack-bridge.md`.
- **2026-07-20** — **shared context, single responder.** Once a real second bot was imminent, added a passive `message` event handler to `bridge.py`: every bot now reads every channel message into an in-memory rolling buffer (`message.channels` event, now a required Slack app subscription, not optional) purely for context — it never triggers a reply. Only `app_mention` triggers a reply, and that reply's prompt now includes the recent buffer. Avoids both "bot is deaf outside direct mentions" and "all six bots answer every message" at once. See `slack-bridge.md §6`.

## 1. Sequenced next steps

1. ~~Review and approve this design~~ — done; the decisions above are the approval.
2. ~~Check prerequisites, then configure Project 2 on GitHub~~ — done: `check-prereqs.sh`, `setup-github-mcp.sh`, `setup-project-2-fields.sh` all run successfully on Mihal's machine (2026-07-19). Remaining: 3 manual UI steps the last script printed (Status option values, Priority/Start date/Target date as columns, confirm default repo `IncusLuminis/ai`).
3. ~~Install Claude Code CLI on the local machine~~ — done, including working around an `nvm`-vs-Homebrew-Node install issue (`setup.md §6`).
4. ~~Run the three setup scripts~~ — done, see above.
5. **Turn the 2026-07-19 audit findings into real Stories/Tasks**, using `Product_Owner` — candidates already surfaced organically by the concurrency test rather than invented for the purpose: `DevOps`'s finding that 13/14 repos have zero CI, `Coder`'s findings in `tools` (version mismatch, committed `.DS_Store`/`__pycache__`, empty `LICENSE`), `Media_keeper`'s duplicate-file findings in `shared/assets`. See `sandbox/reports/`.
6. **Pilot on one of those real Stories from Project 1**, once the 3 manual UI steps above are done — run `Product_Owner` → `Coder` → `Validator` end to end. No gate on the other three roles; use them as soon as there's a real Task/asset/publish need, pilot or not.
7. **Revisit hook enforcement** after the pilot, per the deferred decision above.
8. **Tighten `tools:` allowlists** on each agent definition based on what actually gets used — the ones shipped so far are reasonable starting points, not a security review.
9. **Wire up local automation** once there's a reason to: local cron/`launchd` jobs on Mihal's machine for `Product_Owner` reporting, `Media_keeper` audits, etc. — not GitHub Actions, which would count as "another runner."
10. **Specify Publisher/Media_keeper external integrations one at a time**, as each becomes the actual bottleneck — e.g. Cloudflare R2 credentials the first time `Media_keeper` needs to push somewhere real, a CMS/social connector the first time `Publisher` needs to post somewhere real.
11. **Define a reporting cadence** for `Product_Owner` once there's enough board activity on Project 2 to report on.
12. **Validate the Slack bridge end to end**: run `scripts/slack-bridge/bridge.py` for Incus PO, `@mention` it with a real tool-heavy request (e.g. something that needs GitHub MCP, not just a text question), confirm it replies without hanging on a permission prompt it can't answer headlessly. Then repeat the Slack-app + bridge setup for the other five roles. See `slack-bridge.md`.

## 2. Open questions still not decided

- **Cross-linking the v1.0 contract to the Project 2 contract**: `platform/standards/docs/process/github-project-management-contract.md`'s Owner line now points at `shared/ai`, but nothing in it yet mentions Project 2 exists. Small remaining edit, not done yet.
- **Which Project 1 Story to pilot on**: no longer a blank slate — step 5's audit findings (no-CI gap, `tools` repo cleanup, asset dedup) are real candidates. Still need `Product_Owner` to actually write them up and one to get picked.

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

`scripts/setup-project-2-fields.sh` has also been run: `Size` and `Estimate` already existed on the live Project 2 board (it was apparently created from a template that includes them — not something we set up), and `Agent Role` was newly created. **All scriptable infra setup is now done.** Remaining before the pilot: the three manual UI steps the script printed (Status option values, Priority/Start date/Target date as columns, confirm default repo), and picking an actual Story on Project 1 to pilot on.

In `platform/standards` (separate repo, branch `chore/point-product-owner-skill-to-shared-ai`):

- `skills/product-owner/SKILL.md` replaced with a redirect to `shared/ai`.
- `docs/process/github-project-management-contract.md`'s Owner line updated to match; contract content otherwise untouched.

Still not done: the 3 manual Project 2 UI steps (see above), no hook. Nothing pushed to `origin` on either repo — both branches are local-only.
