# Fix LinkedIn Morning Block task to run whether logged in or not

$action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -WindowStyle Hidden -File {{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\01-morning-block.ps1'

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday,Saturday -At 08:05

$principal = New-ScheduledTaskPrincipal -UserId '{{CLIENT_LOCAL_USER}}' -LogonType Password -RunLevel Limited

Set-ScheduledTask -TaskName 'LinkedIn-Morning-Block' -Action $action -Trigger $trigger -Principal $principal

Write-Host "Task updated successfully. LogonType changed to Password (runs whether logged in or not)"
