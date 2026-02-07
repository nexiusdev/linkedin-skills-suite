# Options Flow Tracker - Split Scan Scheduler Setup
# Creates TWO scheduled tasks to avoid timeout issues
# Scan 1: 8:00 AM - Priority (watchlist + first 300 stocks)
# Scan 2: 10:00 AM - Remaining (stocks 301+) + Analysis

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Options Flow Tracker - Split Scan Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$skillPath = "C:\Users\melve\.claude\skills\options-flow-tracker"

# ============================================
# TASK 1: Priority Scan (8:00 AM)
# ============================================

$task1Name = "Options-Flow-Priority-Scan"
$task1Script = "$skillPath\run_priority_scan.bat"
$task1Time = "08:00"
$task1Desc = "Options flow priority scan - watchlist + first 300 stocks"

Write-Host "Setting up Task 1: Priority Scan (8:00 AM)..." -ForegroundColor Yellow

# Remove existing task if exists
$existing = Get-ScheduledTask -TaskName $task1Name -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "  Removing old task..." -ForegroundColor Gray
    Unregister-ScheduledTask -TaskName $task1Name -Confirm:$false
}

# Create task
$action1 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$task1Script`" auto"
$trigger1 = New-ScheduledTaskTrigger -Daily -At $task1Time
$settings1 = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

Register-ScheduledTask `
    -TaskName $task1Name `
    -Action $action1 `
    -Trigger $trigger1 `
    -Settings $settings1 `
    -Description $task1Desc `
    -User $env:USERNAME | Out-Null

Write-Host "  OK Task 1 created: $task1Name at $task1Time" -ForegroundColor Green

# ============================================
# TASK 2: Remaining Scan (10:00 AM)
# ============================================

$task2Name = "Options-Flow-Market-Scan"
$task2Script = "$skillPath\run_remaining_scan.bat"
$task2Time = "10:00"
$task2Desc = "Options flow market scan - remaining stocks + consolidated analysis"

Write-Host ""
Write-Host "Setting up Task 2: Market Scan (10:00 AM)..." -ForegroundColor Yellow

# Remove existing task if exists
$existing = Get-ScheduledTask -TaskName $task2Name -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "  Removing old task..." -ForegroundColor Gray
    Unregister-ScheduledTask -TaskName $task2Name -Confirm:$false
}

# Create task
$action2 = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$task2Script`" auto"
$trigger2 = New-ScheduledTaskTrigger -Daily -At $task2Time
$settings2 = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

Register-ScheduledTask `
    -TaskName $task2Name `
    -Action $action2 `
    -Trigger $trigger2 `
    -Settings $settings2 `
    -Description $task2Desc `
    -User $env:USERNAME | Out-Null

Write-Host "  OK Task 2 created: $task2Name at $task2Time" -ForegroundColor Green

# ============================================
# REMOVE OLD SINGLE-SCAN TASK (if exists)
# ============================================

Write-Host ""
Write-Host "Cleaning up old single-scan task..." -ForegroundColor Yellow

$oldTask = Get-ScheduledTask -TaskName "Options-Flow-Tracker-Daily-Scan" -ErrorAction SilentlyContinue
if ($oldTask) {
    Unregister-ScheduledTask -TaskName "Options-Flow-Tracker-Daily-Scan" -Confirm:$false
    Write-Host "  OK Old task removed" -ForegroundColor Green
} else {
    Write-Host "  No old task found (OK)" -ForegroundColor Gray
}

# ============================================
# SUMMARY
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SUCCESS! Split scan setup complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "TASK 1: Priority Scan" -ForegroundColor White
Write-Host "  Name: $task1Name" -ForegroundColor Gray
Write-Host "  Time: Daily at $task1Time (8:00 AM)" -ForegroundColor Gray
Write-Host "  Scans: Watchlist + first 300 stocks" -ForegroundColor Gray
Write-Host ""
Write-Host "TASK 2: Market Scan + Analysis" -ForegroundColor White
Write-Host "  Name: $task2Name" -ForegroundColor Gray
Write-Host "  Time: Daily at $task2Time (10:00 AM)" -ForegroundColor Gray
Write-Host "  Scans: Remaining stocks (301+)" -ForegroundColor Gray
Write-Host "  Sends: Consolidated Telegram report" -ForegroundColor Gray
Write-Host ""
Write-Host "BENEFITS:" -ForegroundColor Cyan
Write-Host "  - No more timeouts (split into 2 parts)" -ForegroundColor Gray
Write-Host "  - Full market coverage (all 600 stocks)" -ForegroundColor Gray
Write-Host "  - Priority stocks scanned first" -ForegroundColor Gray
Write-Host "  - No duplicates between scans" -ForegroundColor Gray
Write-Host "  - Single consolidated report at 10:00 AM" -ForegroundColor Gray
Write-Host ""
Write-Host "To view tasks:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask -TaskName 'Options-Flow-*'" -ForegroundColor Gray
Write-Host ""
Write-Host "To test run now:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$task1Name'" -ForegroundColor Gray
Write-Host ""
