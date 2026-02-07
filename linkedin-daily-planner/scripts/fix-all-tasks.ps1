# Enable Wake-to-Run for all LinkedIn tasks

$taskNames = @(
    'LinkedIn-Morning-Block',
    'LinkedIn-Content-Block',
    'LinkedIn-Midday-Block',
    'LinkedIn-Afternoon-Block',
    'LinkedIn-Evening-Block',
    'LinkedIn-Daily-Planner'
)

foreach ($taskName in $taskNames) {
    try {
        $task = Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
        $task.Settings.WakeToRun = $true
        Set-ScheduledTask -InputObject $task | Out-Null
        Write-Host "[OK] $taskName - WakeToRun enabled" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] $taskName - $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "All LinkedIn tasks updated. Your computer will now wake up to run scheduled tasks."
