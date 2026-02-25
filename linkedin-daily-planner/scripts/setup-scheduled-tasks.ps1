# Setup LinkedIn Daily Planner Scheduled Tasks
# Creates all time-block tasks for automated LinkedIn workflow

$scriptDir = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts"

# Task configurations
$tasks = @(
    @{
        Name = "LinkedIn-Daily-Planner"
        Description = "Generate daily LinkedIn activity plan"
        Script = "$scriptDir\00-daily-planner.ps1"
        Time = "08:00"
    },
    @{
        Name = "LinkedIn-Morning-Block"
        Description = "Morning engagement: 3 Peers + 3 Prospects + 3 Thought Leaders"
        Script = "$scriptDir\01-morning-block.ps1"
        Time = "08:00"
    },
    @{
        Name = "LinkedIn-Content-Block"
        Description = "Create and schedule save-worthy content"
        Script = "$scriptDir\02-content-block.ps1"
        Time = "09:00"
    },
    @{
        Name = "LinkedIn-Midday-Block"
        Description = "Golden Hour: Post + engage PROSPECT posts only"
        Script = "$scriptDir\03-midday-block.ps1"
        Time = "12:00"
    },
    @{
        Name = "LinkedIn-Afternoon-Block"
        Description = "Handle connections, DMs, and admin tasks"
        Script = "$scriptDir\04-afternoon-block.ps1"
        Time = "15:00"
    },
    @{
        Name = "LinkedIn-Evening-Block"
        Description = "Inbound engagement + PROSPECT comments only"
        Script = "$scriptDir\05-evening-block.ps1"
        Time = "18:00"
    }
)

Write-Host "Setting up LinkedIn Daily Planner scheduled tasks..." -ForegroundColor Cyan
Write-Host ""

foreach ($task in $tasks) {
    Write-Host "Creating task: $($task.Name) at $($task.Time)" -ForegroundColor Yellow

    # Remove existing task if it exists
    Unregister-ScheduledTask -TaskName $task.Name -Confirm:$false -ErrorAction SilentlyContinue

    # Create action
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
        -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$($task.Script)`""

    # Create trigger for weekdays only
    $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At $task.Time

    # Create settings
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -ExecutionTimeLimit (New-TimeSpan -Hours 2)

    # Register task
    Register-ScheduledTask `
        -TaskName $task.Name `
        -Description $task.Description `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -User $env:USERNAME `
        -RunLevel Limited

    Write-Host "  ✓ Created successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "All tasks created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Daily Schedule:" -ForegroundColor Cyan
Write-Host "  08:00 AM - Daily Planner + Morning Block (diverse engagement)"
Write-Host "  09:00 AM - Content Block (create save-worthy content)"
Write-Host "  12:00 PM - Midday Block (Golden Hour posting)"
Write-Host "  03:00 PM - Afternoon Block (connections and admin)"
Write-Host "  06:00 PM - Evening Block (inbound engagement)"
Write-Host ""
Write-Host "Tasks run Monday-Friday only." -ForegroundColor Yellow
