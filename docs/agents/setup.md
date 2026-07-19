# Setup: running the team on your machine

This is what actually turns the design in this folder into something runnable, on Mihal's local machine, via Claude Code CLI. Nothing here has been executed as part of building this document — this sandbox has no `claude`/`gh` binaries and isn't the target machine.

## 0. Check prerequisites

```bash
cd shared/ai
./scripts/check-prereqs.sh
```

Read-only, changes nothing. Confirms `claude`, `gh`, `git` are on `PATH`, `gh` is authenticated, and SSH access to `github.com` works. Fix anything it flags before continuing — everything below assumes this passes.

## 1. Connect GitHub MCP

Create a token at https://github.com/settings/personal-access-tokens/new (fine-grained):

- **Resource owner:** `IncusLuminis`
- **Repository access:** All repositories (agents can potentially touch any repo in the portfolio; narrow later if needed)
- **Repository permissions:** Contents — Read and write; Issues — Read and write; Pull requests — Read and write; Workflows — Read and write (needed separately from Contents to touch `.github/workflows/*`); Metadata — Read-only (auto-included); Actions — Read-only (optional, for CI status)
- **Organization permissions:** Projects — Read and write (so `Product_Owner` can manage cards on Project 1/2)

If the org restricts fine-grained tokens and you land on a classic-token page instead, use scopes `repo`, `workflow`, `project`.

This is a starting point, not a finished least-privilege review — narrow it once real usage shows what's actually needed (same caveat as the `tools:` allowlists in `implementation-roadmap.md`).

```bash
cp .env.example .env
# edit .env, set GITHUB_PAT to the token above
./scripts/setup-github-mcp.sh
claude mcp list         # confirm "github" is there
```

This registers the official remote GitHub MCP server (`github/github-mcp-server`, Streamable HTTP) at Claude Code's default **local** scope — stored in your user-level `~/.claude.json`, never written into this repo. `.env` and `.mcp.json` are both gitignored regardless, in case a project-scoped setup is used later.

## 2. Configure the Project 2 board

Project 2 (`IncusLuminis/projects/2`) is the agent team's *own* operational board — where `Product_Owner` tracks work on building out this team itself. It's separate from **Project 1** (`IncusLuminis/projects/1`), the org's actual product backlog, which is where the team's agents will do their first real, non-synthetic work once this setup is done — see `../process/github-project-2-contract.md §2` for the full split.

```bash
./scripts/setup-project-2-fields.sh
```

Idempotent — creates the `Size`, `Estimate`, and `Agent Role` custom fields on Project 2 if they don't already exist, skips any that do. It prints a short list of remaining steps that `gh` can't automate (the default `Status` field's option values, and adding org-level Issue fields as visible columns) — do those once, by hand, in the Project 2 UI.

## 3. Launch Claude Code from this repo

```bash
claude
```

Launching from `shared/ai` is what makes its `.claude/agents/` and `.claude/skills/` load. From inside that session, `Coder`/`DevOps`/`Media_keeper` reach other repos via relative paths (`../../products/nebulacast/nebulacast-app`, etc.) since every repo in the portfolio is a sibling directory under `IncusLuminis/` — see `execution-model.md §3`.

## 4. Try each role

- **Product_Owner**: ask it to decompose a spec onto Project 2 (agent-team work) or Project 1 (product work).
- **Coder**: point it at a specific `Ready` Story and the target repo — Project 1's default repo is `visualization-studio-tools`, but a Story can name any repo in the portfolio.
- **Validator**: point it at an open PR.
- **DevOps** / **Media_keeper**: point at an infra Task or an asset job respectively — built and idle until there's real demand, per the rollout decision in `implementation-roadmap.md §0`.
- **Publisher**: point at approved content ready to go out.

Once steps 0–3 are done, **Project 1 is where the first real pilot happens** (`Product_Owner` → `Coder` → `Validator` on an actual Story, per `implementation-roadmap.md §1` step 5) — not a synthetic task invented inside `shared/ai`.

## 5. What's not automated yet

Per the "local machine, no other runners" decision, there's no webhook- or CI-triggered automation — see `execution-model.md §4`. Everything above is invoked by hand (or by a local cron/`launchd` job you set up yourself) until the pilot is done and automation is revisited.

## 6. If something looks wrong

- `./scripts/check-prereqs.sh` — re-run it, it's read-only.
- `claude mcp list` / `claude mcp get github` — verify the MCP connection.
- Check `/mcp` inside a Claude Code session for connection status.
- Token issues are the most common failure — confirm scopes, confirm it hasn't expired.
- `gh project field-list 2 --owner IncusLuminis` — check what fields actually exist on Project 2 if the field-setup script's idempotency check seems off.

**`claude: Error: claude native binary not installed`** (seen during this repo's own setup, 2026-07-19): usually means two Node installs are fighting over `PATH` — e.g. `nvm` active in the shell while `claude` actually lives under Homebrew's Node (`/opt/homebrew/bin/claude -> ../lib/node_modules/@anthropic-ai/claude-code/...`). Symptom: `npm install -g @anthropic-ai/claude-code-darwin-arm64` (or whichever `@anthropic-ai/claude-code-<platform>` package the error names) reports success, but `claude --version` still fails — because it installed into the *other* Node's `node_modules`, not the one `claude` resolves from. Fix: find the real target with `ls -la $(which claude)`, then explicitly use the npm binary next to that Node (e.g. `/opt/homebrew/bin/npm install -g @anthropic-ai/claude-code-darwin-arm64`), then re-run the package's own postinstall directly (`node <path-to-claude-code>/install.cjs`).
