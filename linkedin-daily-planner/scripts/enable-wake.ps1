# Enable Wake-to-Run for LinkedIn Morning Block task

$task = Get-ScheduledTask -TaskName 'LinkedIn-Morning-Block'
$task.Settings.WakeToRun = $true
Set-ScheduledTask -InputObject $task

Write-Host "Task updated successfully. WakeToRun enabled - computer will wake up to run the task."
