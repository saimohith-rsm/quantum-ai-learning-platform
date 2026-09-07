@echo off
chcp 65001 >nul
set PYTHONUTF8=1
title QuantumAI Backend - SIH 2026 (Problem #26140)
echo ========================================================================
echo  Starting QuantumAI Platform Backend (FastAPI + SQLite + NumPy)
echo  Smart India Hackathon 2026 - Team Human X (TEAM-186)
echo ========================================================================
cd /d "%~dp0backend"
python run.py
pause
