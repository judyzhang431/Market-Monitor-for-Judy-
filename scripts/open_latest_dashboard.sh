#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${JMM_PORT:-8765}"
if ! lsof -iTCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1; then
  nohup python -m job_market_monitor.run serve >/tmp/jmm_server.log 2>&1 &
  sleep 1
fi
python -m job_market_monitor.run open-latest
