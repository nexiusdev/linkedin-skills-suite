# Stock Swing Trader - Automatic Task Scheduler Setup
# This script creates a Windows scheduled task to run daily scans

Write-Host "Setting up Stock Swing Trader Daily Scan..." -ForegroundColor Green

# Define task parameters
$TaskName = "Stock-Swing-Trader-Daily-Scan"
$ScriptPath = "C:\Users\melve\.claude\skills\stock-swing-trader\run_daily_scan.bat"
$Description = "Daily stock scan for swing trading signals (TraderGPS strategy)"

# Set time: 6:30 AM GMT+8 (after US market close and EOD data available)
# US market closes at 4:00 PM ET = 5:00 AM GMT+8 next day
# EOD data available by 5:00 PM ET = 6:00 AM GMT+8
$TriggerTime = "06:30"  # 6:30 AM GMT+8 in 24-hour format

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    Write-Host "Task already exists. Removing old task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create the scheduled task action
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$ScriptPath`""

# Create the trigger (daily at specified time)
$Trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime

# Create task settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Register the scheduled task
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description $Description `
    -User $env:USERNAME

Write-Host ""
Write-Host "SUCCESS! Task scheduled successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Task Details:" -ForegroundColor Cyan
Write-Host "  Name: $TaskName"
Write-Host "  Schedule: Daily at $TriggerTime (4:45 PM)"
Write-Host "  Script: $ScriptPath"
Write-Host ""
Write-Host "The scan will run automatically every day after market close." -ForegroundColor Green
Write-Host "You'll receive Telegram alerts when signals are found." -ForegroundColor Green
Write-Host ""
Write-Host "To view/manage the task:" -ForegroundColor Yellow
Write-Host "  1. Open Task Scheduler (taskschd.msc)"
Write-Host "  2. Look for '$TaskName'"
Write-Host ""
Write-Host "To test run now:" -ForegroundColor Yellow
Write-Host "  Right-click the task and select 'Run'"
