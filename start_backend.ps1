Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " Starting QuantumAI Platform Backend (FastAPI + SQLite + NumPy)" -ForegroundColor Green
Write-Host " Smart India Hackathon 2026 - Team Human X (TEAM-186)" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Cyan

$backendDir = Join-Path $PSScriptRoot "backend"
Set-Location -Path $backendDir
python run.py
