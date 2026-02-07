@echo off
REM Start Telegram Bot Listener for Options Flow Tracker
REM Allows you to trigger scans by sending commands to your Telegram bot

cd /d "%~dp0"
python scripts\telegram_bot_listener.py
pause
