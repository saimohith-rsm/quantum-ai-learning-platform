Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " QUANTUMAI: AI-BASED INTERACTIVE QUANTUM ALGORITHM LEARNING PLATFORM" -ForegroundColor Green
Write-Host " Smart India Hackathon 2026 (Problem Statement #26140, Team Human X)" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Cyan

$backendDir = Join-Path $PSScriptRoot "backend"
$frontendDir = Join-Path $PSScriptRoot "frontend"

Write-Host "`n[1/2] Starting Backend in new window (http://127.0.0.1:8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; `$env:PYTHONUTF8 = '1'; Set-Location -Path '$backendDir'; python run.py"

Write-Host "[2/2] Starting Frontend in new window (http://localhost:5173)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -Path '$frontendDir'; cmd.exe /c 'npm run dev'"

Write-Host "`nPlatform running successfully!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "Backend:  http://127.0.0.1:8000/docs" -ForegroundColor White

Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"
