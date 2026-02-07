@echo off
REM Options Flow Tracker - Market Scan (Scan 2 of 2)
REM Scans remaining stocks (301+) at 10:00 AM

cd /d "C:\Users\melve\.claude\skills\options-flow-tracker"

echo ========================================
echo MARKET SCAN - Remaining Stocks
echo ========================================
echo Time: %TIME%
echo.

REM Run remaining scan (stocks 301+, no duplicates)
python scripts/flow_scanner.py --split-mode remaining

echo.
echo ========================================
echo Market Scan Complete
echo Running consolidated analysis...
echo ========================================
echo.

REM Analyze all signals from both scans and send consolidated report
python scripts/flow_analyzer.py

echo.
echo ========================================
echo Daily Flow Analysis Complete
echo Check Telegram for recommendations
echo ========================================

REM Pause if running manually
if "%1"=="" pause
