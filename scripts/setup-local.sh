#!/usr/bin/env bash
# Bid On — one-shot local setup (macOS / Linux)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Bid On local setup"

if command -v docker >/dev/null 2>&1; then
  echo "==> Starting Postgres (docker compose)..."
  docker compose up -d
else
  echo "Docker not found — ensure PostgreSQL is running on localhost:5432"
fi

[[ -f backend/.env ]] || cp backend/.env.example backend/.env
[[ -f frontend/.env.local ]] || cp frontend/.env.example frontend/.env.local

echo "==> Installing backend deps..."
cd "$ROOT/backend"
npm install --include=dev
npx prisma migrate deploy || npx prisma migrate dev --name init
npm run db:seed

echo "==> Installing frontend deps..."
cd "$ROOT/frontend"
npm install --include=dev

echo ""
echo "Done. Run in two terminals:"
echo "  cd backend  && npm run dev     # http://localhost:4000"
echo "  cd frontend && npm run dev     # http://localhost:3000"
echo "Diagrams: cd docs/diagrams && python3 -m http.server 8765"
echo "  then open http://127.0.0.1:8765/view-diagrams.html"
