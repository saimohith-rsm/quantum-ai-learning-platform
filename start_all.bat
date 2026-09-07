@echo off
chcp 65001 >nul
set PYTHONUTF8=1
title QuantumAI - Launching Full Platform (SIH 2026 #26140)

echo ========================================================================
echo  QUANTUMAI: AI-BASED INTERACTIVE QUANTUM ALGORITHM LEARNING PLATFORM
echo  Smart India Hackathon 2026 (Problem Statement #26140, Team Human X)
echo ========================================================================
echo.

:: Clear any stale processes that might be holding the ports
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 "') do (
    if not "%%a"=="" if not "%%a"=="0" taskkill /F /PID %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173 "') do (
    if not "%%a"=="" if not "%%a"=="0" taskkill /F /PID %%a >nul 2>&1
)

echo [1/2] Launching FastAPI Backend on http://127.0.0.1:8000 ...
start "QuantumAI Backend" cmd /k "cd /d "%~dp0backend" && chcp 65001 >nul && set PYTHONUTF8=1 && python run.py"

echo [2/2] Launching React Frontend on http://localhost:5173 ...
start "QuantumAI Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================================================
echo  Both services launched successfully!
echo  Backend Docs: http://127.0.0.1:8000/docs
echo  Frontend UI:  http://localhost:5173
echo ========================================================================
echo Opening browser in 3 seconds...
ping 127.0.0.1 -n 4 >nul
start http://localhost:5173
