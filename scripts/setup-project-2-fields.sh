#!/usr/bin/env bash
# Adds the project-specific custom fields Project 2 needs, per
# docs/process/github-project-2-contract.md §3, using gh CLI.
#
# What this can and can't do:
# - CAN create the missing fields: Size (single-select XS-XL), Estimate
#   (number), Agent Role (single-select, one per team role) - idempotent,
#   skips any that already exist.
# - CANNOT configure the default "Status" field's option values
#   (Backlog/Ready/In Progress/In Review/Done) - gh CLI has no
#   field-edit-options command. Do that once by hand: Project 2 ->
#   Settings -> Fields -> Status.
# - CANNOT add the org-level Issue fields (Priority, Start date,
#   Target date) as visible columns on this project - also a manual
#   UI step, once, per project.
#
# Requires: gh CLI installed and authenticated with access to the
# IncusLuminis org's Projects. Run scripts/check-prereqs.sh first.

set -euo pipefail

OWNER="IncusLuminis"
PROJECT_NUMBER=2

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found on PATH. Install it first: https://cli.github.com" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

echo "Reading existing fields on project $PROJECT_NUMBER (owner: $OWNER)..."
existing_fields="$(gh project field-list "$PROJECT_NUMBER" --owner "$OWNER" --format json --jq '.fields[].name' 2>&1)" \
  || { echo "Couldn't list fields - check the project number/owner and your access." >&2; echo "$existing_fields" >&2; exit 1; }

field_exists() {
  printf '%s\n' "$existing_fields" | grep -Fxq "$1"
}

create_field_if_missing() {
  local name="$1"; shift
  if field_exists "$name"; then
    echo "  '$name' already exists - skipping."
  else
    echo "  Creating '$name'..."
    gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "$name" "$@"
  fi
}

create_field_if_missing "Size" --data-type "SINGLE_SELECT" --single-select-options "XS,S,M,L,XL"
create_field_if_missing "Estimate" --data-type "NUMBER"
create_field_if_missing "Agent Role" --data-type "SINGLE_SELECT" \
  --single-select-options "Product_Owner,Coder,Validator,DevOps,Publisher,Media_keeper"

echo
echo "Done with what's scriptable. Remaining manual steps, once, in the Project 2 UI:"
echo "  - Set Status field options to: Backlog, Ready, In Progress, In Review, Done"
echo "  - Add Priority / Start date / Target date as visible columns if not already"
echo "  - Confirm the default repo for new issues is IncusLuminis/ai"
