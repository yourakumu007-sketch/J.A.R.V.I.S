@echo off
title J.A.R.V.I.S -- Wake Word Service
color 0A

echo ==============================================
echo   J.A.R.V.I.S -- Starting Wake Word Listener...
echo ==============================================

cd /d "%~dp0"

REM ── Check if setup has been completed ──────────────────────────────
if not exist ".jarvis_setup_complete" (
    echo First-time launch detected. Running setup first...
    echo.
    python JARVIS_SETUP.py
    if %ERRORLEVEL% NEQ 0 (
        echo Setup failed. Check the messages above.
        pause
        exit /b %ERRORLEVEL%
    )
)

echo.
echo Launching Wake Word Listener ("wake up jarvis")...
set PYTHONIOENCODING=utf-8
python wake_service.py

echo.
pause
