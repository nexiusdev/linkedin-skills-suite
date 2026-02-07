@echo off
title AI Ignite Monitor
powershell -ExecutionPolicy Bypass -File "%~dp0monitor-loop.ps1"
pause
