# Bid On — one-shot local setup (Windows PowerShell)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "==> Bid On local setup" -ForegroundColor Cyan

if (Get-Command docker -ErrorAction SilentlyContinue) {
  Write-Host "==> Starting Postgres (docker compose)..."
  docker compose up -d
} else {
  Write-Host "Docker not found — make sure PostgreSQL is running on localhost:5432" -ForegroundColor Yellow
}

if (-not (Test-Path "backend\.env")) {
  Copy-Item "backend\.env.example" "backend\.env"
  Write-Host "Created backend/.env from example"
}
if (-not (Test-Path "frontend\.env.local")) {
  Copy-Item "frontend\.env.example" "frontend\.env.local"
  Write-Host "Created frontend/.env.local from example"
}

Write-Host "==> Installing backend deps..."
Set-Location "$Root\backend"
npm install --include=dev
npx prisma migrate deploy
if ($LASTEXITCODE -ne 0) { npx prisma migrate dev --name init }
npm run db:seed

Write-Host "==> Installing frontend deps..."
Set-Location "$Root\frontend"
npm install --include=dev

Write-Host ""
Write-Host "Done. Run in two terminals:" -ForegroundColor Green
Write-Host "  cd backend;  npm run dev     # http://localhost:4000"
Write-Host "  cd frontend; npm run dev     # http://localhost:3000"
Write-Host "Diagrams: cd docs/diagrams; python -m http.server 8765"
Write-Host "  then open http://127.0.0.1:8765/view-diagrams.html"
