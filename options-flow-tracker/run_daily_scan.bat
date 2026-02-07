@echo off
REM Options Flow Tracker - Daily Scan + Analysis
REM Runs after market close to check for unusual flow and generate recommendations

cd /d "C:\Users\melve\.claude\skills\options-flow-tracker"

REM Step 1: Run the daily flow scan (detects raw signals)
echo ========================================
echo STEP 1: Scanning for Options Flow
echo ========================================
python scripts/flow_scanner.py

REM Step 2: Analyze and generate recommendations
echo.
echo ========================================
echo STEP 2: Analyzing Signals
echo ========================================
python scripts/flow_analyzer.py

REM Pause to see results if running manually
pause
