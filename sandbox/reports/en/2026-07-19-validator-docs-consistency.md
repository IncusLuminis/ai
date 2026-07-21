# Review: docs/agents & docs/process internal consistency

- **Agent:** validator
- **Date:** 2026-07-19
- **Scope:** `docs/agents/*` and `docs/process/github-project-2-contract.md` in this repo (read-only review, no files modified)

Reviewed all 12 files (10 agent docs + orchestration/execution-model, plus
the Project 2 contract). Overall the docs are largely consistent — skill/
agent mapping, the DevOps/Media_keeper bucket-vs-lifecycle split, the
Publisher/Media_keeper asset handoff, and the Coder/Validator/DevOps
boundaries all line up cleanly. Four concrete inconsistencies stood out.

## 1. Stale "not yet run" status in the Project 2 contract vs. the roadmap's "done" claim
`docs/process/github-project-2-contract.md` header states field-setup is
"scripted (`scripts/setup-project-2-fields.sh`), not yet run against the
live board," and §6 says to fall back to `gh` CLI "until the script has
actually been run with a real Personal Access Token." But
`implementation-roadmap.md` (§0 last bullet, §3) and `README.md`'s status
line both say the script *has* been run and Project 2 fields are
configured. Same date (2026-07-19) on both docs, directly contradictory.

## 2. Default repo "resolved" vs. "still needs confirming"
`github-project-2-contract.md §4` declares the default repo "Resolved
(2026-07-19): `IncusLuminis/ai`." But `implementation-roadmap.md §1` step 2
lists "confirm default repo `IncusLuminis/ai`" as one of three still-
outstanding manual UI steps — i.e. not actually resolved yet.

## 3. RACI table vs. Coder's explicit boundary on merging
`orchestration.md §3`'s RACI table marks Coder as **R** (Responsible) for
"Merge to main." This conflicts with `coder.md`'s explicit boundary ("does
NOT ... merge its own PR, or approve its own work as QA-complete") and with
`orchestration.md`'s own flow diagram in §1, where merge is a distinct step
performed only by "Human (Mihal)" after Validator approval, with no Coder
action in between.

## 4. Validator's card-moving permission vs. the status-ownership table
`validator.md` grants itself the ability to "move the board card between
`In Review` and `In Progress`," but `orchestration.md §2`'s Board status
ownership table lists only `Coder`, `DevOps`, `Media_keeper`, or `Publisher`
as who may enter `In Progress` — Validator is omitted, even though the §1
flow diagram shows Validator's change-request explicitly sending a card
back to `In Progress`.

## Note
The roadmap's decision log claims a prior audit pass already found and
fixed "6 internal doc inconsistencies." These four appear to be new/
remaining ones, not covered by that fix.
