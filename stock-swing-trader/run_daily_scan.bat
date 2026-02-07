@echo off
REM Stock Swing Trader - Daily Scan
REM Runs after market close to check for signals

cd /d "C:\Users\melve\.claude\skills\stock-swing-trader"

REM Run the daily scan (conservative mode)
python scripts/trader.py

REM Pause to see results if running manually
pause
