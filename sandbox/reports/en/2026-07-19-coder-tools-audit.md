# Audit: `tools` repo — state & stack

- **Agent:** coder
- **Date:** 2026-07-19
- **Scope:** `/Users/mloktionov/Projects/IncusLuminis/tools` (read-only survey, no changes made)

## Purpose
A Python CLI (`incus-tools`, invoked as `incus`) providing organization-wide
automation for IncusLuminis — primarily repository lifecycle management
(creating/validating/removing GitHub and local repos per a defined
"repository type" architecture, e.g. product/platform/shared repo
scaffolding).

## Tech stack
- Python (>=3.11), packaged with `hatchling`.
- CLI built on `typer` + `rich` for console output.
- `pytest` and `ruff` for testing/linting (dev extras).
- Dependency/venv managed via standard `pyproject.toml` (no
  lockfile/poetry/uv observed).
- Shell scripts (`scripts/*.sh`) supplement the Python CLI for GitHub/local
  repo checks and cleanup.

## Current state
Actively developed — all 6 commits (plus 1 merged PR) are dated 2026-07-17,
just two days before this inspection, with a clear feature progression
(bootstrap → repo type architecture → validation → improved creation/
maintenance). Early-stage/WIP: version `0.1.0` in `pyproject.toml` but the
CLI reports `0.2.0` internally (inconsistent versioning) — not yet mature/
stable.

## Structure and gaps
- Key modules: `src/incus_tools/` (cli.py, github.py, config.py, shell.py)
  and `src/incus_tools/repository/` (creator, model, types, naming, layouts,
  definitions) — a reasonably factored domain model for repo creation.
- `tests/` has two test files (`test_cli.py`, `test_repository_creator.py`) —
  some coverage exists but likely thin given module count.
- `docs/adr`, `docs/api`, `docs/architecture` exist but are mostly empty/
  template stubs; README's "Overview" and "Getting Started" sections are
  still boilerplate/unfilled.
- `.github/workflows/` contains only `.gitkeep` — **no CI configured**,
  despite ROADMAP listing "CI/CD" as a "Next" priority.
- `LICENSE` file is present but empty (0 bytes).
- Stray `.DS_Store` files and `__pycache__`/`.pytest_cache`/`.ruff_cache`/
  `.venv` artifacts appear tracked in the working tree — worth verifying
  `.gitignore` coverage.
