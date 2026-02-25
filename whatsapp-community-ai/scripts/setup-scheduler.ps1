# Setup script for {{CLIENT_COMMUNITY_NAME}} Monitor scheduled task
# Run this script once to create the 15-minute monitoring task

$taskName = "Community-Monitor"
$scriptPath = "{{CLIENT_WORKSPACE_ROOT}}\whatsapp-community-ai\scripts\monitor-community.ps1"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the action
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

# Create trigger - every 15 minutes, starting now
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration (New-TimeSpan -Days 9999)

# Create settings
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Monitor {{CLIENT_COMMUNITY_NAME}} WhatsApp every 15 mins for unanswered questions and auto-reply"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SUCCESS: Scheduled task created!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Task Name: $taskName"
Write-Host "Frequency: Every 15 minutes"
Write-Host "Script: $scriptPath"
Write-Host ""
Write-Host "To verify, run: Get-ScheduledTask -TaskName '$taskName'"
Write-Host "To disable, run: Disable-ScheduledTask -TaskName '$taskName'"
Write-Host "To remove, run: Unregister-ScheduledTask -TaskName '$taskName'"
