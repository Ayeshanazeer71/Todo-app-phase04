# Deploy Todo Chatbot to Minikube (Backend + Frontend, Neon DB)
# Prerequisites: Docker Desktop running, Minikube and Helm installed

param(
    [switch]$SkipBuild,
    [switch]$SkipStart
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $ProjectRoot

Write-Host "=== Todo Chatbot - Minikube Deploy ===" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot" -ForegroundColor Gray

if (-not $SkipStart) {
    Write-Host "`n[1/5] Starting Minikube..." -ForegroundColor Yellow
    minikube start
    if ($LASTEXITCODE -ne 0) { throw "minikube start failed" }

    Write-Host "`n[2/5] Using Minikube Docker daemon..." -ForegroundColor Yellow
    & minikube -p minikube docker-env --shell powershell | Invoke-Expression
}

if (-not $SkipBuild) {
    Write-Host "`n[3/5] Building backend image..." -ForegroundColor Yellow
    Set-Location "$ProjectRoot\backend"
    docker build -t todo-chatbot-backend:latest .
    if ($LASTEXITCODE -ne 0) { throw "backend build failed" }

    Write-Host "`n[4/5] Building frontend image (NEXT_PUBLIC_API_URL=http://localhost:8000)..." -ForegroundColor Yellow
    Set-Location "$ProjectRoot\frontend"
    docker build -t todo-chatbot-frontend:latest `
        --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 `
        --build-arg NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 .
    if ($LASTEXITCODE -ne 0) { throw "frontend build failed" }
    Set-Location $ProjectRoot
} else {
    Write-Host "`n[3/4] Skipping image build (use -SkipBuild to skip)." -ForegroundColor Gray
}

Write-Host "`n[5/5] Deploying with Helm..." -ForegroundColor Yellow
helm upgrade --install todo-chatbot "$ProjectRoot\helm\todo-chatbot" --wait --timeout 5m
if ($LASTEXITCODE -ne 0) { throw "helm install failed" }

Write-Host "`n=== Deploy done ===" -ForegroundColor Green
kubectl get pods
kubectl get svc

Write-Host "`nTo access the app, run in TWO separate terminals:" -ForegroundColor Cyan
Write-Host "  Terminal 1: kubectl port-forward service/todo-chatbot-frontend 3000:80" -ForegroundColor White
Write-Host "  Terminal 2: kubectl port-forward service/todo-chatbot-backend 8000:8000" -ForegroundColor White
Write-Host "`nThen open: Frontend http://localhost:3000  |  Backend API http://localhost:8000" -ForegroundColor White
Write-Host "`nBackend uses Neon PostgreSQL; tables are created automatically on first start." -ForegroundColor Gray
