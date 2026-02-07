# Show LinkedIn Scheduled Tasks

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  LinkedIn Daily Planner - Scheduled Tasks" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

$tasks = Get-ScheduledTask -TaskName 'LinkedIn-*' | Sort-Object TaskName

foreach ($task in $tasks) {
    $info = Get-ScheduledTaskInfo -TaskName $task.TaskName -ErrorAction SilentlyContinue
    $trigger = $task.Triggers[0]

    Write-Host "$($task.TaskName)" -ForegroundColor Yellow
    Write-Host "  State: $($task.State)" -ForegroundColor $(if ($task.State -eq 'Ready') { 'Green' } else { 'Red' })
    Write-Host "  Description: $($task.Description)"

    if ($trigger.StartBoundary) {
        $time = ([datetime]::Parse($trigger.StartBoundary)).ToString("hh:mm tt")
        Write-Host "  Schedule: Weekdays at $time"
    }

    if ($info.LastRunTime -and $info.LastRunTime -ne [datetime]::MinValue) {
        Write-Host "  Last Run: $($info.LastRunTime)"
    }

    if ($info.NextRunTime -and $info.NextRunTime -ne [datetime]::MinValue) {
        Write-Host "  Next Run: $($info.NextRunTime)"
    }

    Write-Host ""
}

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "All tasks are scheduled to run Monday-Friday only" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Cyan
