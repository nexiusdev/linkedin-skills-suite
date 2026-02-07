@echo off
echo =====================================================
echo Stock Swing Trader - Quick Setup
echo =====================================================
echo.
echo This will create a scheduled task for daily scans at 5:30 AM
echo.
echo Please click YES on the UAC prompt that appears...
echo.
pause

powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy', 'Bypass', '-NoExit', '-File', 'C:\Users\melve\.claude\skills\stock-swing-trader\scripts\quick-setup.ps1' -Verb RunAs"

echo.
echo UAC prompt triggered. Check for the dialog box!
echo.
pause
