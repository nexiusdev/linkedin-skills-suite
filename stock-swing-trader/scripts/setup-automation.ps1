# Stock Swing Trader - Automation Setup
# Creates a Windows scheduled task to run daily stock scans

$ErrorActionPreference = "Stop"

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Stock Swing Trader - Automation Setup" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$taskName = "StockSwingTrader-DailyScan"
$scriptPath = Join-Path $PSScriptRoot "run-daily-scan.bat"
$skillPath = Split-Path $PSScriptRoot -Parent

# Verify script exists
if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: Script not found at $scriptPath" -ForegroundColor Red
    exit 1
}

Write-Host "Script path: $scriptPath" -ForegroundColor Gray
Write-Host "Skill path: $skillPath" -ForegroundColor Gray
Write-Host ""

# Ask for scan time
Write-Host "When should the daily scan run?" -ForegroundColor Yellow
Write-Host "Recommended: 05:30 AM (after US market close, data settled)" -ForegroundColor Gray
Write-Host ""
$timeInput = Read-Host "Enter time (HH:MM format, 24-hour) or press Enter for 05:30"

if ([string]::IsNullOrWhiteSpace($timeInput)) {
    $timeInput = "05:30"
}

# Parse time
try {
    $timeParts = $timeInput -split ':'
    $hour = [int]$timeParts[0]
    $minute = [int]$timeParts[1]

    if ($hour -lt 0 -or $hour -gt 23 -or $minute -lt 0 -or $minute -gt 59) {
        throw "Invalid time"
    }

    $scheduledTime = "{0:D2}:{1:D2}" -f $hour, $minute
} catch {
    Write-Host "ERROR: Invalid time format. Use HH:MM (e.g., 05:30)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setting up scheduled task..." -ForegroundColor Yellow

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Gray
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create action
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory $skillPath

# Create trigger (daily at specified time)
$trigger = New-ScheduledTaskTrigger -Daily -At $scheduledTime

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Register task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Daily stock swing trading scan with Telegram alerts" `
    -User $env:USERNAME `
    -RunLevel Highest | Out-Null

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "SUCCESS! Automation configured" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Task Name: $taskName" -ForegroundColor White
Write-Host "Schedule: Daily at $scheduledTime" -ForegroundColor White
Write-Host "Script: $scriptPath" -ForegroundColor White
Write-Host ""
Write-Host "The scan will run daily and send results to your Telegram." -ForegroundColor Cyan
Write-Host ""
Write-Host "To manage this task:" -ForegroundColor Yellow
Write-Host "  - View: Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
Write-Host "  - Run now: Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
Write-Host "  - Disable: Disable-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
Write-Host "  - Remove: Unregister-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
Write-Host ""
Write-Host "Would you like to run a test scan now? (Y/N)" -ForegroundColor Yellow
$testRun = Read-Host

if ($testRun -eq 'Y' -or $testRun -eq 'y') {
    Write-Host ""
    Write-Host "Running test scan..." -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $taskName
    Write-Host "Task started. Check your Telegram for the results." -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
