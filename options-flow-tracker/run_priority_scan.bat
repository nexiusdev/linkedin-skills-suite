@echo off
REM Options Flow Tracker - Priority Scan (Scan 1 of 2)
REM Scans watchlist + first 300 stocks at 8:00 AM

cd /d "C:\Users\melve\.claude\skills\options-flow-tracker"

echo ========================================
echo PRIORITY SCAN - Watchlist + First Half
echo ========================================
echo Time: %TIME%
echo.

REM Run priority scan (first 300 stocks including watchlist)
python scripts/flow_scanner.py --split-mode priority

echo.
echo ========================================
echo Priority Scan Complete
echo Next: Remaining Market Scan at 10:00 AM
echo ========================================

REM Pause if running manually
if "%1"=="" pause
