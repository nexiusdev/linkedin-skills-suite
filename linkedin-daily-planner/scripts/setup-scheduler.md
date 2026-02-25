# LinkedIn Daily Planner - Automation Setup Guide

## Overview

This guide sets up Windows Task Scheduler to automatically trigger your LinkedIn workflow at optimal times each day.

## Recommended Schedule

| Time | Block | Task Scheduler Trigger |
|------|-------|------------------------|
| 09:00 | Morning | Start comments warm-up |
| 10:00 | Content | Create and schedule post |
| 12:30 | Midday | Golden Hour engagement |
| 15:00 | Afternoon | Connections and DMs |
| 18:30 | Evening | Daily audit |

## Quick Setup (PowerShell)

Run this PowerShell script as Administrator to create all scheduled tasks:

```powershell
# Create scheduled tasks for LinkedIn Daily Planner

$scriptPath = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\daily-launcher.ps1"

# Morning Block - 9:00 AM (Weekdays only)
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`" -TimeBlock morning"
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd
Register-ScheduledTask -TaskName "LinkedIn-Morning" -Action $action -Trigger $trigger -Settings $settings -Description "LinkedIn Morning Block - Comments warm-up"

# Content Block - 10:00 AM
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`" -TimeBlock content"
$trigger = New-ScheduledTaskTrigger -Daily -At 10:00AM
Register-ScheduledTask -TaskName "LinkedIn-Content" -Action $action -Trigger $trigger -Settings $settings -Description "LinkedIn Content Block - Create and schedule post"

# Midday Block - 12:30 PM
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`" -TimeBlock midday"
$trigger = New-ScheduledTaskTrigger -Daily -At 12:30PM
Register-ScheduledTask -TaskName "LinkedIn-Midday" -Action $action -Trigger $trigger -Settings $settings -Description "LinkedIn Midday Block - Golden Hour"

# Afternoon Block - 3:00 PM
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`" -TimeBlock afternoon"
$trigger = New-ScheduledTaskTrigger -Daily -At 3:00PM
Register-ScheduledTask -TaskName "LinkedIn-Afternoon" -Action $action -Trigger $trigger -Settings $settings -Description "LinkedIn Afternoon Block - Connections"

# Evening Block - 6:30 PM
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`" -TimeBlock evening"
$trigger = New-ScheduledTaskTrigger -Daily -At 6:30PM
Register-ScheduledTask -TaskName "LinkedIn-Evening" -Action $action -Trigger $trigger -Settings $settings -Description "LinkedIn Evening Block - Audit"

Write-Host "All LinkedIn scheduled tasks created!" -ForegroundColor Green
```

## Manual Setup (Task Scheduler GUI)

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create New Task**
   - Click "Create Task" (not "Create Basic Task")

3. **General Tab**
   - Name: `LinkedIn-Morning` (or block name)
   - Description: `LinkedIn Morning Block - Comments warm-up`
   - Check "Run only when user is logged on"

4. **Triggers Tab**
   - Click "New"
   - Begin: "On a schedule"
   - Daily, Start: 9:00 AM
   - Repeat: Every 1 day
   - Optional: Check "Stop task if runs longer than 1 hour"

5. **Actions Tab**
   - Click "New"
   - Action: "Start a program"
   - Program: `PowerShell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\daily-launcher.ps1" -TimeBlock morning`

6. **Conditions Tab**
   - Uncheck "Start only if computer is on AC power"
   - Check "Wake the computer to run this task" (optional)

7. **Repeat for each time block** with appropriate times

## Notification Integration (Optional)

Add Windows Toast notifications before each block:

```powershell
# Add to daily-launcher.ps1 at the start

# Show Windows notification
$notify = New-Object -ComObject WScript.Shell
$notify.Popup("LinkedIn $TimeBlock Block starting!`n`nOpen Claude Code to continue.", 10, "LinkedIn Daily Planner", 64)
```

## Alternative: Single Daily Trigger

If you prefer one trigger that creates the full day plan:

```powershell
# Single trigger at 8:30 AM
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`" -TimeBlock full"
$trigger = New-ScheduledTaskTrigger -Daily -At 8:30AM
Register-ScheduledTask -TaskName "LinkedIn-DailyPlan" -Action $action -Trigger $trigger -Description "LinkedIn Full Day Plan"
```

## Skip Weekends (Optional)

Modify triggers to skip Saturday and Sunday:

```powershell
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 9:00AM
```

## Verify Setup

List all LinkedIn scheduled tasks:

```powershell
Get-ScheduledTask | Where-Object {$_.TaskName -like "LinkedIn*"} | Format-Table TaskName, State, Description
```

## Remove Tasks (if needed)

```powershell
Unregister-ScheduledTask -TaskName "LinkedIn-Morning" -Confirm:$false
Unregister-ScheduledTask -TaskName "LinkedIn-Content" -Confirm:$false
Unregister-ScheduledTask -TaskName "LinkedIn-Midday" -Confirm:$false
Unregister-ScheduledTask -TaskName "LinkedIn-Afternoon" -Confirm:$false
Unregister-ScheduledTask -TaskName "LinkedIn-Evening" -Confirm:$false
```

## Troubleshooting

**Task doesn't run:**
- Check Task Scheduler History (enable it first)
- Ensure PowerShell execution policy allows scripts
- Run manually first to test

**Claude Code doesn't open:**
- Ensure `claude` is in your PATH
- Try full path: `C:\Users\{{CLIENT_LOCAL_USER}}\.claude\bin\claude.exe`

**Browser not ready:**
- Claude for Chrome must be open and logged in
- Consider adding a delay at script start
