@echo off
REM Stock Swing Trader - Daily Scan Runner
REM This script runs the daily stock scan and sends results to Telegram

cd /d "%~dp0.."
python scripts/trader.py

REM Log execution
echo [%date% %time%] Daily scan completed >> data/automation.log
