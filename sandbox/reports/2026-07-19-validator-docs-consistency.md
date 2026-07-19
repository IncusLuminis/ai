# Review: docs/agents & docs/process internal consistency

- **Agent:** validator
- **Date:** 2026-07-19
- **Scope:** `docs/agents/*` and `docs/process/github-project-2-contract.md` in this repo (read-only review, no files modified)

Reviewed all 11 files (README, coder/devops/execution-model/
implementation-roadmap/orchestration/product-owner/publisher/setup/
validator/media-keeper.md, and the Project 2 contract). Found six concrete
inconsistencies.

## 1. Skill/agent mapping contradiction
`execution-model.md §3`'s file-tree diagram shows `skills/devops/` and
`skills/media-keeper/` as built directories, but `execution-model.md §2`'s own
role table maps both `DevOps` and `Media_keeper` to Agent only (no skill), and
`implementation-roadmap.md §3` explicitly states "`DevOps` and `Media_keeper`
ended up as agent-only, not also skills." The §3 tree is stale/wrong relative
to §2 and the roadmap.

## 2. Stale product-owner tooling reference
`product-owner.md` "Tools & access required" still says it uses
`platform/standards/skills/product-owner/` "used as-is for Project 1." But
`implementation-roadmap.md`'s decision log and `execution-model.md §2` state
that skill was superseded 2026-07-19 with a redirect to
`.claude/skills/product-owner/` in `shared/ai`, which now covers both
Project 1 and 2. `product-owner.md` was not updated to reflect this.

## 3. Board-status gap for Media_keeper/Publisher
`orchestration.md §2`'s status table only allows `Coder` or `DevOps` to move a
card to `In Progress`. But the RACI table (§3) makes `Media_keeper` and
`Publisher` R/A for their own workstreams, and both role docs describe
standalone scheduled/batch work (audits, recurring publishing) not gated
behind a Coder PR. No status-entry path is defined for them.

## 4. "Done" criteria gap for DevOps-only Tasks
`orchestration.md §2`'s Done rule requires "Validator approval + human merge,"
but `devops.md` explicitly says DevOps "handle[s] infra-only Tasks that don't
need full Epic/Story decomposition" — implying no PR/Validator step. No path
to `Done` is defined for that case.

## 5. Unverified repo claim
`setup.md §4` asserts "Project 1's default repo is `visualization-studio-tools`."
This repo name appears nowhere else in README.md, orchestration.md,
product-owner.md, or `github-project-2-contract.md` — unlike Project 2's
default repo (`shared/ai`), which is consistently documented across multiple
files.

## 6. Stale README header
README.md's status line still reads "not yet connected/piloted" and lists
branch `feature/agent-team-design`, but `implementation-roadmap.md`'s decision
log records that branch as already reviewed and merge-approved by Mihal, and
git history shows it merged.
