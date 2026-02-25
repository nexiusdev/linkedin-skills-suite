# Create LinkedIn Daily Planner Scheduled Tasks

Write-Host "Creating LinkedIn scheduled tasks..." -ForegroundColor Cyan

# Task 1: Daily Planner at 8:00 AM
Unregister-ScheduledTask -TaskName 'LinkedIn-Daily-Planner' -Confirm:$false -ErrorAction SilentlyContinue
$action1 = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -WindowStyle Hidden -File {{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\00-daily-planner.ps1'
$trigger1 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 08:00
$settings1 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName 'LinkedIn-Daily-Planner' -Description 'Generate daily LinkedIn activity plan' -Action $action1 -Trigger $trigger1 -Settings $settings1 | Out-Null
Write-Host "Created: LinkedIn-Daily-Planner at 08:00 AM" -ForegroundColor Green

# Task 2: Morning Block at 8:05 AM (5 min after planner)
Unregister-ScheduledTask -TaskName 'LinkedIn-Morning-Block' -Confirm:$false -ErrorAction SilentlyContinue
$action2 = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -WindowStyle Hidden -File {{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\01-morning-block.ps1'
$trigger2 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 08:05
$settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName 'LinkedIn-Morning-Block' -Description 'Morning engagement with Peers, Prospects, Thought Leaders' -Action $action2 -Trigger $trigger2 -Settings $settings2 | Out-Null
Write-Host "Created: LinkedIn-Morning-Block at 08:05 AM" -ForegroundColor Green

# Task 3: Content Block at 9:00 AM
Unregister-ScheduledTask -TaskName 'LinkedIn-Content-Block' -Confirm:$false -ErrorAction SilentlyContinue
$action3 = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -WindowStyle Hidden -File {{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\02-content-block.ps1'
$trigger3 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 09:00
$settings3 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName 'LinkedIn-Content-Block' -Description 'Create and schedule save-worthy content' -Action $action3 -Trigger $trigger3 -Settings $settings3 | Out-Null
Write-Host "Created: LinkedIn-Content-Block at 09:00 AM" -ForegroundColor Green

# Task 4: Midday Block at 12:00 PM
Unregister-ScheduledTask -TaskName 'LinkedIn-Midday-Block' -Confirm:$false -ErrorAction SilentlyContinue
$action4 = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -WindowStyle Hidden -File {{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\03-midday-block.ps1'
$trigger4 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 12:00
$settings4 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName 'LinkedIn-Midday-Block' -Description 'Golden Hour: Post and engage PROSPECT posts' -Action $action4 -Trigger $trigger4 -Settings $settings4 | Out-Null
Write-Host "Created: LinkedIn-Midday-Block at 12:00 PM" -ForegroundColor Green

# Task 5: Afternoon Block at 3:00 PM
Unregister-ScheduledTask -TaskName 'LinkedIn-Afternoon-Block' -Confirm:$false -ErrorAction SilentlyContinue
$action5 = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -WindowStyle Hidden -File {{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\04-afternoon-block.ps1'
$trigger5 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 15:00
$settings5 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName 'LinkedIn-Afternoon-Block' -Description 'Handle connections, DMs, admin tasks' -Action $action5 -Trigger $trigger5 -Settings $settings5 | Out-Null
Write-Host "Created: LinkedIn-Afternoon-Block at 03:00 PM" -ForegroundColor Green

# Task 6: Evening Block at 6:00 PM
Unregister-ScheduledTask -TaskName 'LinkedIn-Evening-Block' -Confirm:$false -ErrorAction SilentlyContinue
$action6 = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument '-ExecutionPolicy Bypass -WindowStyle Hidden -File {{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\05-evening-block.ps1'
$trigger6 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 18:00
$settings6 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName 'LinkedIn-Evening-Block' -Description 'Inbound engagement and PROSPECT comments' -Action $action6 -Trigger $trigger6 -Settings $settings6 | Out-Null
Write-Host "Created: LinkedIn-Evening-Block at 06:00 PM" -ForegroundColor Green

Write-Host ""
Write-Host "All LinkedIn tasks created successfully!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Daily Schedule (Monday-Friday):" -ForegroundColor Yellow
Write-Host "  08:00 AM - Daily Planner (creates plan)"
Write-Host "  08:05 AM - Morning Block (diverse engagement)"
Write-Host "  09:00 AM - Content Block (create content)"
Write-Host "  12:00 PM - Midday Block (Golden Hour)"
Write-Host "  03:00 PM - Afternoon Block (connections)"
Write-Host "  06:00 PM - Evening Block (inbound engagement)"
