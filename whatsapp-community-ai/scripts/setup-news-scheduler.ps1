# Setup script for AI Ignite News Poster scheduled tasks
# Run this script once to create the 10 AM and 8 PM posting tasks (weekdays only)

$taskName = "AI-Ignite-News-Poster"
$scriptPath = "C:\Users\melve\.claude\skills\whatsapp-community-ai\scripts\post-ai-news.ps1"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the action
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

# Create triggers - 10 AM and 8 PM, weekdays only (Mon-Fri)
$trigger10AM = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 10:00AM
$trigger8PM = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 8:00PM

# Create settings
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Register the task with both triggers
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger10AM,$trigger8PM -Settings $settings -Description "Post AI news to AI Ignite WhatsApp at 10 AM and 8 PM SGT, weekdays only"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SUCCESS: Scheduled task created!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Task Name: $taskName"
Write-Host "Schedule: 10:00 AM and 8:00 PM SGT"
Write-Host "Days: Monday - Friday (weekdays only)"
Write-Host "Script: $scriptPath"
Write-Host ""
Write-Host "To verify, run: Get-ScheduledTask -TaskName '$taskName'"
Write-Host "To see triggers, run: Get-ScheduledTask -TaskName '$taskName' | Get-ScheduledTaskInfo"
Write-Host "To disable, run: Disable-ScheduledTask -TaskName '$taskName'"
Write-Host "To remove, run: Unregister-ScheduledTask -TaskName '$taskName'"
