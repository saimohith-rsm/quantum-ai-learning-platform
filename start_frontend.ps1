Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " Starting QuantumAI Platform Frontend (React + Vite + Three.js)" -ForegroundColor Green
Write-Host " Smart India Hackathon 2026 - Team Human X (TEAM-186)" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Cyan

$frontendDir = Join-Path $PSScriptRoot "frontend"
Set-Location -Path $frontendDir
& cmd.exe /c "npm run dev"
