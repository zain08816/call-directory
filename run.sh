#!/usr/bin/env bash
# Run both backend and frontend. Ctrl+C stops both.
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# Backend: ensure venv and deps
if ! [ -d .venv ]; then
  echo "Creating venv..."
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi

# Start backend in background
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cleanup() { kill $BACKEND_PID 2>/dev/null; exit 0; }
trap cleanup EXIT INT TERM

# Give backend a moment to start
sleep 1.5

# Frontend: use nvm if available
if [ -s "$HOME/.nvm/nvm.sh" ]; then
  export NVM_DIR="$HOME/.nvm"
  . "$NVM_DIR/nvm.sh"
  [ -f admin/.nvmrc ] && (cd admin && nvm use)
fi
if ! [ -d admin/node_modules ]; then
  echo "Installing frontend dependencies..."
  (cd admin && npm install)
fi

echo ""
echo "  Backend:  http://127.0.0.1:8000"
echo "  Frontend: http://127.0.0.1:5173/admin/"
echo "  Press Ctrl+C to stop both."
echo ""

(cd admin && npm run dev)
