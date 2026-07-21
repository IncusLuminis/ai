#!/usr/bin/env bash
# Registers the official GitHub MCP server (remote, Streamable HTTP) for this
# project, using Claude Code's default "local" scope - stored in your
# user-level ~/.claude.json, not committed to this repo.
#
# Decision context: shared/ai/docs/agents/execution-model.md and
# shared/ai/docs/process/github-project-2-contract.md §6.
#
# Usage:
#   1. cp .env.example .env
#   2. Edit .env and set GITHUB_PAT to a real GitHub Personal Access Token
#   3. Run this script from the repo root: ./scripts/setup-github-mcp.sh
#   4. claude mcp list        # confirm "github" is registered
#   5. claude mcp get github  # inspect its config
#
# Requires: Claude Code CLI installed and on PATH. Run this on the machine
# that will actually run the agents (per the "local machine only" decision -
# this is not meant to run in CI or any other runner).
#
# Reference: https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if ! command -v claude >/dev/null 2>&1; then
  echo "claude CLI not found on PATH. Install Claude Code first: https://code.claude.com" >&2
  exit 1
fi

if [ ! -f .env ]; then
  echo "No .env found. Run: cp .env.example .env, then fill in GITHUB_PAT." >&2
  exit 1
fi

GITHUB_PAT="$(grep '^GITHUB_PAT=' .env | cut -d '=' -f2-)"

if [ -z "${GITHUB_PAT}" ]; then
  echo "GITHUB_PAT is empty in .env. Fill it in with a real token first." >&2
  exit 1
fi

# X-MCP-Toolsets: the remote server's *default* toolset (used when this
# header is omitted) does NOT include `projects` - Product_Owner needs it to
# read/update GitHub Projects boards (Project 1, Project 2). Explicit list
# below = default toolset's coverage (repos, issues, pull_requests, orgs,
# users, labels) plus `projects`. See docs/agents/slack-bridge.md and
# https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md#optional-headers
claude mcp remove github >/dev/null 2>&1 || true
claude mcp add-json github "{\"type\":\"http\",\"url\":\"https://api.githubcopilot.com/mcp\",\"headers\":{\"Authorization\":\"Bearer ${GITHUB_PAT}\",\"X-MCP-Toolsets\":\"repos,issues,pull_requests,orgs,users,labels,projects\"}}"

echo
echo "Done. Verify with:"
echo "  claude mcp list"
echo "  claude mcp get github"
echo
echo "If 'claude mcp add-json' isn't recognized, you're on Claude Code < 2.1.1 -"
echo "use the legacy form instead:"
echo "  claude mcp remove github"
echo "  claude mcp add --transport http github https://api.githubcopilot.com/mcp \\"
echo "    -H \"Authorization: Bearer \$GITHUB_PAT\" \\"
echo "    -H \"X-MCP-Toolsets: repos,issues,pull_requests,orgs,users,labels,projects\""
