#!/usr/bin/env bash
# Read-only checks that this machine is ready to run the IncusLuminis
# agent team before touching scripts/setup-github-mcp.sh or
# scripts/setup-project-2-fields.sh. Changes nothing; safe to re-run.
#
# See docs/agents/setup.md.

set -uo pipefail  # no -e: run every check, report all results at the end

all_ok=1

check() {
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then
    echo "[ok]   $desc"
  else
    echo "[MISS] $desc"
    all_ok=0
  fi
}

echo "Checking prerequisites for the IncusLuminis agent team..."
echo

check "claude (Claude Code CLI) on PATH" command -v claude
check "gh (GitHub CLI) on PATH" command -v gh
check "git on PATH" command -v git
check "gh authenticated" gh auth status

# SSH's own test connection to GitHub always exits non-zero even on
# success, by GitHub's design - so check the greeting text instead of
# the exit code.
ssh_out="$(ssh -T -o BatchMode=yes -o ConnectTimeout=5 git@github.com 2>&1 || true)"
if echo "$ssh_out" | grep -q "successfully authenticated"; then
  echo "[ok]   SSH access to github.com"
else
  echo "[MISS] SSH access to github.com"
  all_ok=0
fi

echo
if [ "$all_ok" = "1" ]; then
  echo "All good. Next: ./scripts/setup-github-mcp.sh, then ./scripts/setup-project-2-fields.sh"
else
  echo "Fix the [MISS] items above first - see docs/agents/setup.md."
fi
