# Setup: running the team on your machine

This is what actually turns the design in this folder into something runnable, on Mihal's local machine, via Claude Code CLI. Nothing here has been executed as part of building this document — this sandbox has no `claude` binary and isn't the target machine.

## Prerequisites

- [Claude Code CLI](https://code.claude.com) installed.
- A GitHub Personal Access Token with at least `repo` scope (`project` scope too if `Product_Owner` should manage Project fields, not just create/move issues): https://github.com/settings/personal-access-tokens/new
- `gh`/SSH already authenticated for the `IncusLuminis` GitHub org, so `Coder` can actually push branches and open PRs.

## 1. Connect GitHub MCP

```bash
cd shared/ai
cp .env.example .env
# edit .env, set GITHUB_PAT to a real token
./scripts/setup-github-mcp.sh
claude mcp list         # confirm "github" is there
```

This registers the official remote GitHub MCP server (`github/github-mcp-server`, Streamable HTTP) at Claude Code's default **local** scope — stored in your user-level `~/.claude.json`, never written into this repo. `.env` and `.mcp.json` are both gitignored regardless, in case a project-scoped setup is used later.

## 2. Launch Claude Code from this repo

```bash
cd shared/ai
claude
```

Launching from `shared/ai` is what makes its `.claude/agents/` and `.claude/skills/` load. From inside that session, `Coder`/`DevOps`/`Media_keeper` reach other repos via relative paths (`../../products/nebulacast/nebulacast-app`, etc.) since every repo in the portfolio is a sibling directory under `IncusLuminis/` — see `execution-model.md §3`.

## 3. Try each role

- **Product_Owner**: ask it to decompose a spec, or say which board (Project 1 vs Project 2 — see `../process/github-project-2-contract.md §2` for which is which).
- **Coder**: point it at a specific `Ready` Story and the target repo.
- **Validator**: point it at an open PR.
- **DevOps** / **Media_keeper**: point at an infra Task or an asset job respectively.
- **Publisher**: point at approved content ready to go out.

## 4. What's not automated yet

Per the "local machine, no other runners" decision, there's no webhook- or CI-triggered automation — see `execution-model.md §4`. Everything above is invoked by hand (or by a local cron/`launchd` job you set up yourself) until the pilot (`implementation-roadmap.md §1` step 6) is done and automation is revisited.

## 5. If something looks wrong

- `claude mcp list` / `claude mcp get github` — verify the MCP connection.
- Check `/mcp` inside a Claude Code session for connection status.
- Token issues are the most common failure — confirm scopes, confirm it hasn't expired.
