#!/bin/bash
# Victor.I - Kill processes on dev ports, apply migrations, then start Django (8080), Node WS, and Next.js.

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

kill_port() {
  local port="$1"
  local pids
  pids=$(lsof -ti ":$port" 2>/dev/null) || true
  if [ -n "$pids" ]; then
    echo "Killing process(es) on port $port: $pids"
    echo "$pids" | xargs kill -9 2>/dev/null || true
    sleep 1
  fi
}

echo "Stopping existing dev processes..."
for port in 8000 8080 3000 3001; do
  kill_port "$port"
done
echo "Waiting for ports to be released..."
sleep 3
echo "Ports cleared."
echo ""

# Export API URLs and WS URL so Node and Next see them (avoid sourcing .env due to spaces/comments)
export DJANGO_API_URL="${DJANGO_API_URL:-http://localhost:8080}"
export NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8080}"
export NODE_WS_PORT="${NODE_WS_PORT:-3001}"
export NEXT_PUBLIC_WS_URL="${NEXT_PUBLIC_WS_URL:-ws://localhost:3001}"
if [ -f .env ]; then
  while IFS= read -r line; do
    [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
    if [[ "$line" =~ ^(DJANGO_API_URL|NEXT_PUBLIC_API_URL|NODE_WS_PORT|NEXT_PUBLIC_WS_URL)= ]]; then
      export "$line"
    fi
  done < .env
fi

echo "Applying Django migrations..."
PYTHONPATH=. python backend/manage.py migrate || echo "Warning: migrate failed, continuing anyway."
echo ""

echo "Starting Django on 8080..."
PYTHONPATH=. python backend/manage.py runserver 8080 &
DJANGO_PID=$!
echo "Starting Node WebSocket server on 3001..."
(cd node-server && node server.js) &
NODE_PID=$!
echo ""

sleep 2
echo "Django PID: $DJANGO_PID  Node PID: $NODE_PID"
echo "Starting Next.js (frontend) on 3000..."
echo "To stop backend and Node later: kill $DJANGO_PID $NODE_PID"
echo ""

cd frontend && npm run dev
