@echo off
chcp 65001 >nul
set PYTHONUTF8=1
title QuantumAI - First-Time Setup on New Laptop (SIH 2026 #26140)

echo ========================================================================
echo  QUANTUMAI: FIRST-TIME SETUP ON NEW LAPTOP
echo  Smart India Hackathon 2026 (Problem Statement #26140, Team Human X)
echo ========================================================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo IMPORTANT: Make sure to check "Add python.exe to PATH" during install!
    pause
    exit /b 1
)
python --version

echo.
echo [2/3] Checking Node.js installation...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed or not in PATH!
    echo Please install Node.js LTS from https://nodejs.org/
    pause
    exit /b 1
)
node --version

echo.
echo [3/3] Installing Dependencies...
echo.
echo --> Installing Python backend packages...
cd /d "%~dp0backend"
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Python dependencies.
    pause
    exit /b 1
)

echo.
echo --> Installing Frontend npm packages...
cd /d "%~dp0frontend"
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install npm packages.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo  SETUP COMPLETED SUCCESSFULLY!
echo  You can now run the platform anytime by double-clicking "start_all.bat"
echo ========================================================================
pause
