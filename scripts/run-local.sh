#!/bin/bash
# Victor.I - Local run: start Django, Node WS, and Next.js frontend.
# Run each command in a separate terminal (or run backend + node in background and frontend in foreground).

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Full-Stack AI Analytics - Local run"
echo "-----------------------------------"
echo "From repo root: $ROOT"
echo ""
echo "Terminal 1 - Django API (run from repo root so src/ is found):"
echo "  pip install -r backend/requirements.txt && python backend/manage.py migrate && PYTHONPATH=. python backend/manage.py runserver"
echo "  (If port 8000 is in use: PYTHONPATH=. python backend/manage.py runserver 8080)"
echo ""
echo "Terminal 2 - Node WebSocket server:"
echo "  cd node-server && npm install && npm run dev"
echo ""
echo "Terminal 3 - Next.js frontend:"
echo "  cd frontend && npm install && npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo "-----------------------------------"
