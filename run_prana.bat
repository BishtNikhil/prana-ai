@echo off
title PranaAI (प्राण AI) — Urban Air Quality & Winter Smog Assistant
echo ========================================================================
echo        🔱 PRANA-AI (प्राण AI) — URBAN AIR QUALITY & SMOG ASSISTANT 🔱
echo                 Google Developer PromptWars Virtual Challenge 06
echo ========================================================================
echo.

cd /d "%~dp0"

echo [1/3] Verifying Python Environment...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not detected in PATH. Please install Python 3.11+.
    pause
    exit /b 1
)

echo [2/3] Checking dependencies...
pip install -r requirements.txt --quiet

echo [3/3] Launching PranaAI Fast Uvicorn Server on http://localhost:8000 ...
echo Press Ctrl+C to terminate the server.
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
