@echo off
title {{CLIENT_COMMUNITY_NAME}} Monitor
powershell -ExecutionPolicy Bypass -File "%~dp0monitor-loop.ps1"
pause
