#!/usr/bin/env bash
# Paste this file's contents into the dedicated Claude cloud environment setup.
# Setup is not necessarily launched from the repository working directory.
set -euo pipefail
for base in "$PWD" /home/user /workspace /root; do
  [ -d "$base" ] || continue
  setup=$(find "$base" -maxdepth 5 -type f -path '*/megaphone-claude-plugin/cloud/setup.sh' -print -quit 2>/dev/null || true)
  if [ -n "$setup" ]; then
    bash "$setup"
    exit 0
  fi
done
echo 'Repository setup not available during bootstrap; run bash cloud/setup.sh after checkout.'
