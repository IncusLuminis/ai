# Audit: `tools` repo — state & stack

- **Agent:** coder
- **Date:** 2026-07-19
- **Scope:** `/Users/mloktionov/Projects/IncusLuminis/tools` (read-only survey, no changes made)

## Purpose
Internal CLI tooling repo (`incus-tools`), providing an `incus` command-line tool to
automate creation and maintenance of GitHub repositories across the IncusLuminis
portfolio (e.g. `incus repo new`, `incus product create` to scaffold a full set of
site/content/app/mobile/backend repos for a product from templates).

## Tech stack
- Python 3.11+, packaged with Hatchling (`pyproject.toml`), installable as
  `incus-tools` with console script `incus`.
- Libraries: Typer (CLI framework), Rich (console output).
- Dev/test tooling: pytest, ruff (linter).
- Supporting shell scripts (`scripts/*.sh`) for checking/removing created
  GitHub/local repos, presumably invoking the `gh` CLI and git.

## Current state
Very young and actively being built: only 6 commits total, all dated 2026-07-17
(2 days before this audit), most recent via a merged PR ("improve repository
creation and maintenance tools"). Working tree clean and in sync with
`origin/main`. Clearly WIP/early-stage:
- README and CONTRIBUTING still contain templated/placeholder prose
  ("Describe the purpose of the repository...").
- CHANGELOG is empty ("Unreleased" with blank bullets).
- ROADMAP lists "CI/CD, Testing, Releases" as future work rather than done.
- Version mismatch: `VERSION` file says `0.1.0`, but `cli.py` reports `0.2.0`
  internally.

## Structure & gaps
- `src/incus_tools/`: core package (`cli.py`, `config.py`, `github.py`,
  `shell.py`, plus a `repository/` submodule with `creator.py`,
  `definitions.py`, `layouts.py`, `model.py`, `naming.py`, `types.py`) —
  reasonably factored architecture for repo-type-driven scaffolding.
- `tests/`: has `test_cli.py` and `test_repository_creator.py` (some test
  coverage exists), but coverage of `github.py`/`config.py` unclear.
- `docs/adr`, `docs/api`, `docs/architecture`, `docs/images`: all empty except
  a placeholder ADR template — documentation is scaffolded but not filled in.
- `.github/workflows/` contains only a `.gitkeep` — **no CI pipeline
  configured yet**, despite pytest/ruff being present.
- Stray `.DS_Store` and `__pycache__`/`.pyc` files are committed under `src/`
  and `tests/` — `.gitignore` may need tightening.
- `LICENSE` file is present but empty (0 bytes) despite `PROJECT.yml`
  declaring MIT.
