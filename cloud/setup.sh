#!/usr/bin/env bash
# Run in the Claude cloud environment's setup script: bash cloud/setup.sh
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
node -e 'if (+process.versions.node.split(".")[0] < 22) throw Error("Node 22+ required")'
if [ "$(uname -s)" = Linux ]; then
  APT=(apt-get)
  if [ "$(id -u)" != 0 ]; then APT=(sudo apt-get); fi
  "${APT[@]}" update -qq
  DEBIAN_FRONTEND=noninteractive "${APT[@]}" install -y -qq --no-install-recommends \
    ffmpeg fonts-liberation libnss3 libatk-bridge2.0-0 libxkbcommon0 libgbm1 libasound2t64
fi
command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
npm ci --prefix "$ROOT/cloud" --no-audit --no-fund
"$ROOT/cloud/node_modules/.bin/hyperframes" browser ensure
echo 'Megaphone cloud motion runtime is installed. Run python3 cloud/smoke.py to verify rendering.'
