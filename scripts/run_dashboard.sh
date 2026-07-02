#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
PORT="${PORT:-8501}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python interpreter not found. Install Python 3.10+ and re-run." >&2
  exit 1
fi

exec "$PYTHON_BIN" -m streamlit run dashboard/app.py --server.headless false --server.port "$PORT" --server.address 0.0.0.0
