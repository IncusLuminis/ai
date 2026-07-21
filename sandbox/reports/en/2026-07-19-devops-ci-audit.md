# Audit: CI/CD coverage across the portfolio

- **Agent:** devops
- **Date:** 2026-07-19
- **Scope:** 14 IncusLuminis portfolio repos (read-only survey, no changes made)

## Bottom line
**Not a single repo in this list has an active CI/CD configuration —
14/14 repos have zero effective CI.**

## Per-repo table

| Repo | Has CI? | Notes |
|---|---|---|
| tools | No | `.github/workflows/` exists but contains only `.gitkeep` |
| repo-template | No | same — placeholder only |
| docs | No | same — placeholder only |
| .github | No | no `.github/workflows` dir at all; only `profile/` (org profile repo) |
| platform/publishing | No | no `.github` dir; has docs (CONTRACT.md, Pipeline.md) but no automation |
| platform/workflows | No | ironically, the repo meant to host shared workflows has only a `.gitkeep` placeholder |
| platform/standards | No | placeholder only |
| shared/core | No | placeholder only |
| shared/ai | No | placeholder only |
| shared/data | No | placeholder only |
| shared/assets | No | placeholder only |
| exploration/research | No | placeholder only |
| exploration/labs | No | placeholder only |
| products/Photomaps | No | no `.github` dir; collection of Jupyter notebooks, no automation |

## Details
No alternate CI substitutes found either — each repo was checked for
`.gitlab-ci.yml`, `.circleci/config.yml`, `Makefile` (ci target), and
`.pre-commit-config.yaml`: none present anywhere.

The `.gitkeep` files in 10 repos suggest workflows were scaffolded (likely
from `repo-template`) but never populated — a template gap, not per-repo
drift. `platform/workflows`, the intended home for reusable workflow
definitions, is itself empty, so there's no shared workflow library to call
from other repos yet. `.github` (org profile), `platform/publishing`, and
`products/Photomaps` don't even have the scaffold.

Flagging for follow-up: populating `platform/workflows` with reusable
lint/test/build workflows, then wiring `repo-template`'s placeholder into a
real starter workflow, would be the natural next step — but that's a scoping
decision for whoever owns the roadmap, not something acted on here.
