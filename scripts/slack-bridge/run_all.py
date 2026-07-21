#!/usr/bin/env python3
"""
Run every configured role's Slack bridge from one command/terminal, each in
its own OS process.

Each role is still its own Slack app / Socket Mode connection (its own
bot token, app token, session file) - this just avoids needing a separate
open terminal per role. `bridge.py` itself is unchanged and still works
standalone for running just one role, if you'd rather keep it fully
isolated.

Uses `multiprocessing`, not `threading`: an earlier version used threads,
but `slack_bolt`'s Socket Mode client isn't reliable across more than one
instance sharing a process/thread (observed directly - a second role's
connection would start and then silently hang forever, no error, while a
first role in the same process connected fine; running that same role
standalone in its own process worked immediately). Separate processes give
each role its own real Python interpreter - the same isolation as running
`bridge.py` in six terminals, just launched together. One tradeoff: the
shared in-memory channel-history buffer (see slack-bridge.md §6) is no
longer shared across roles the way it would be within a single process -
each process now builds its own copy again, same as before run_all.py
existed. Each role still independently reads every channel message, so
"only the mentioned bot replies" still holds; they just don't literally
share one buffer object in memory anymore.

Usage:
    python3 run_all.py
        Auto-discovers every `.env.<role>` file at the repo root
        (shared/ai/.env.product-owner, .env.coder, ...) and starts all of
        them.

    python3 run_all.py .env.product-owner .env.coder
        Starts only the roles named explicitly (paths relative to the repo
        root, or absolute).

Ctrl+C stops all of them. A crash in one role's process is logged but does
not take down the others - check the logs (all roles log to the same
terminal, tagged by role in the log line) to see which one, if any, died.
"""

import glob
import multiprocessing
import sys
import time
from pathlib import Path

from dotenv import dotenv_values

from bridge import REPO_ROOT, log, run_role


def discover_env_files():
    """Only files that actually look like a role config - skips
    .env.example, and skips stray leftovers like .env.deleted-empty (a
    marker file from GitHub PAT setup, not a role) that happen to match the
    .env.* glob but have no SLACK_BOT_TOKEN in them."""
    candidates = [Path(p) for p in glob.glob(str(REPO_ROOT / ".env.*")) if not p.endswith(".example")]
    files = []
    for p in candidates:
        values = dotenv_values(p)
        if values.get("SLACK_BOT_TOKEN"):
            files.append(p)
        else:
            log.info("Skipping %s - no SLACK_BOT_TOKEN in it, doesn't look like a role config", p.name)
    return sorted(files)


def resolve_env_files(args):
    if not args:
        return discover_env_files()
    resolved = []
    for a in args:
        p = Path(a)
        resolved.append(p if p.is_absolute() else REPO_ROOT / p)
    return resolved


def run_role_guarded(env_file):
    """Wrap run_role so one role's crash is logged clearly and doesn't take
    the others down. Runs inside its own child process, so an uncaught
    exception here only ends that process."""
    try:
        run_role(str(env_file))
    except SystemExit as e:
        log.error("Role from %s exited: %s", env_file, e)
    except Exception:
        log.exception("Role from %s crashed", env_file)


def main():
    env_files = resolve_env_files(sys.argv[1:])
    if not env_files:
        sys.exit(
            f"No .env.<role> files found at {REPO_ROOT} and none given on the command line.\n"
            f"Create one per role first (see adding-a-slack-agent.md), or pass paths explicitly."
        )

    missing = [f for f in env_files if not f.exists()]
    if missing:
        sys.exit("These files don't exist: " + ", ".join(str(f) for f in missing))

    log.info("Starting %d role(s) in this process: %s", len(env_files), ", ".join(f.name for f in env_files))

    procs = []
    for env_file in env_files:
        p = multiprocessing.Process(target=run_role_guarded, args=(env_file,), name=env_file.stem, daemon=True)
        p.start()
        procs.append(p)
        time.sleep(1.5)  # stagger connects rather than opening N sockets at once

    try:
        while True:
            time.sleep(1)
            alive = [p.name for p in procs if p.is_alive()]
            if not alive:
                log.error("All roles have stopped. Exiting.")
                break
    except KeyboardInterrupt:
        log.info("Stopping (Ctrl+C)...")
        for p in procs:
            p.terminate()


if __name__ == "__main__":
    main()
