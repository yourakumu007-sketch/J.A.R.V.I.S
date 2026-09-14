@echo off
title J.A.R.V.I.S -- AI Desktop Assistant
color 0A

echo ===================================================
echo    J.A.R.V.I.S AI Engine -- Launcher
echo ===================================================
echo.

cd /d "%~dp0"

REM ── Check if setup has been completed ─────────────────────────────────
if not exist ".jarvis_setup_complete" (
    echo First-time launch detected. Running setup...
    echo.
    
    where python >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Python was not found on this PC.
        echo.
        echo Please install Python 3.10 or newer from https://python.org
        echo During install, make sure to check "Add python.exe to PATH".
        echo Then double-click this file again.
        echo.
        pause
        exit /b 1
    )
    
    python JARVIS_SETUP.py
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Setup failed. Check the messages above.
        pause
        exit /b %ERRORLEVEL%
    )
)

REM ── Launch J.A.R.V.I.S ─────────────────────────────────────────────────────
echo Launching J.A.R.V.I.S...
set PYTHONIOENCODING=utf-8
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo J.A.R.V.I.S closed with an error code %ERRORLEVEL%.
    pause
)
