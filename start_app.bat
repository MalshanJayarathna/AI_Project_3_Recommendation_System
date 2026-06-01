@echo off
title DecodeLabs — AI Course Recommendation System

:: ============================================================
:: start_app.bat
:: DecodeLabs AI Project 3 — One-Click App Launcher
::
:: Double-click this file to:
::   1. Start the Flask web server
::   2. Automatically open the app in your browser
::
:: To stop the server: close this window or press Ctrl+C
:: ============================================================

echo.
echo  ============================================================
echo    DecodeLabs ^| AI Project 3 ^| Course Recommendation System
echo  ============================================================
echo.
echo  [1/3] Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo  [2/3] Installing / verifying dependencies...
pip install -r requirements.txt --quiet

echo  [3/3] Starting Flask server...
echo.
echo  ============================================================
echo   App is running at: http://127.0.0.1:5000
echo   Press Ctrl+C in this window to stop the server.
echo  ============================================================
echo.

:: Wait 2 seconds then open browser
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:5000"

:: Start Flask app (keeps running in this window)
python app.py

echo.
echo  Server stopped. Press any key to close this window.
pause >nul
