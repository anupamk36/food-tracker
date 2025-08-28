#!/usr/bin/env bash
set -euo pipefail
# Requires: pip install git-filter-repo
# Usage: ./scripts/scrub_git_history.sh 'path/to/secret.file' 'another/secret.env'
if ! command -v git-filter-repo >/dev/null 2>&1; then
  echo "Please install git-filter-repo first (https://github.com/newren/git-filter-repo)"
  exit 1
fi
git filter-repo --invert-paths --path "$@"

echo "Done. Force push once you've checked locally: git push --force-with-lease"
