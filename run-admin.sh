#!/usr/bin/env bash
# Run the backend (serves the admin dashboard at /admin/)
set -e
cd "$(dirname "$0")"

if ! [ -d .venv ]; then
  echo "Creating venv..."
  python3 -m venv .venv
fi
.venv/bin/pip install -q -r requirements.txt

# If port 8000 is in use (e.g. leftover backend), free it
if command -v fuser &>/dev/null && fuser 8000/tcp &>/dev/null; then
  echo "Port 8000 in use; freeing it..."
  fuser -k 8000/tcp 2>/dev/null || true
  sleep 1
fi

echo "Starting server at http://0.0.0.0:8000"
echo ""
echo "  Local:        http://127.0.0.1:8000/"
echo "  Admin:        http://127.0.0.1:8000/admin/"
echo ""
echo "  If you use Cursor/VS Code REMOTE (SSH, Codespaces, etc.):"
echo "  - Open the 'Ports' panel (View -> Ports)"
echo "  - Forward port 8000 if it's not listed"
echo "  - Click 'Open in Browser' for port 8000"
echo ""
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
