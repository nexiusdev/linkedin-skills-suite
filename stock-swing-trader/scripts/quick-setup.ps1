$ErrorActionPreference = "Stop"

$taskName = "StockSwingTrader-DailyScan"
$scriptPath = "C:\Users\melve\.claude\skills\stock-swing-trader\scripts\run-daily-scan.bat"
$workingDir = "C:\Users\melve\.claude\skills\stock-swing-trader"

Write-Host "Creating scheduled task..." -ForegroundColor Cyan

# Create the action
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory $workingDir

# Create the trigger (daily at 5:30 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At "05:30"

# Create the settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Remove existing task if present
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Gray
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Daily stock swing trading scan with Telegram alerts" `
    -User $env:USERNAME `
    -RunLevel Highest | Out-Null

Write-Host ""
Write-Host "SUCCESS! Task created successfully." -ForegroundColor Green
Write-Host "Schedule: Daily at 05:30 AM" -ForegroundColor White
Write-Host ""
Write-Host "Testing Telegram connection..." -ForegroundColor Cyan

cd C:\Users\melve\.claude\skills\stock-swing-trader
python scripts/telegram_notifier.py --test

Write-Host ""
Write-Host "Setup complete! You'll receive daily scans at 5:30 AM." -ForegroundColor Green
