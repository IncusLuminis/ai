# Audit: CI/CD coverage across the portfolio

- **Agent:** devops
- **Date:** 2026-07-19
- **Scope:** 14 IncusLuminis portfolio repos (read-only survey, no changes made)

## Bottom line
**13 of 14 repos have zero CI configuration.** No repo in the portfolio
currently runs any automated CI (lint/test/build/deploy) via GitHub Actions or
otherwise.

## Per-repo table

| Repo | Has CI? | Notes |
|---|---|---|
| tools | No | `.github/workflows/` contains only `.gitkeep`; no Makefile/gitlab-ci/pre-commit |
| repo-template | No | same — placeholder only |
| docs | No | same — placeholder only |
| .github | No | org profile repo; no `.github/workflows` dir at all, just `profile/` |
| platform/publishing | No | no `.github` dir; no Makefile/gitlab-ci/pre-commit found |
| platform/workflows | No | placeholder only (ironic given repo's purpose — no reusable workflows defined yet) |
| platform/standards | No | placeholder only |
| shared/core | No | placeholder only |
| shared/ai | No | placeholder only (this repo) |
| shared/data | No | placeholder only |
| shared/assets | No | placeholder only |
| exploration/research | No | placeholder only |
| exploration/labs | No | placeholder only |
| products/Photomaps | No | no `.github` dir; only notebooks/scripts, no Makefile/CI config |

## Details
Every repo checked has `pull_request_template.md` under `.github/`, but the
`workflows/` subfolder (where present) contains only an empty `.gitkeep` —
scaffolding was created but no actual workflow YAML was ever added.
`platform/publishing` and `products/Photomaps` lack even the `.github`
scaffold. No alternative CI (`.gitlab-ci.yml`, `Makefile` CI target,
pre-commit config) exists in any of the 14 repos.

This is a gap worth flagging to the orchestrator/human, since it affects the
Validator's ability to gate merges and the promotion pipelines referenced in
product docs.
