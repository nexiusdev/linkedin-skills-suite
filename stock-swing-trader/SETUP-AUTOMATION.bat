@echo off
REM Stock Swing Trader - Automation Setup
REM RIGHT-CLICK THIS FILE AND SELECT "RUN AS ADMINISTRATOR"

echo =====================================================
echo Stock Swing Trader - Automation Setup
echo =====================================================
echo.
echo This will create a scheduled task to run daily scans
echo at 5:30 AM and send results to your Telegram.
echo.
pause

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "scripts\setup-automation.ps1"

pause
