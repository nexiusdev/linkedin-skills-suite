# Setup LinkedIn Startup Script
# Run this script ONCE to add LinkedIn workflow to Windows startup
# Run as: .\setup-startup.ps1

param(
    [switch]$Remove,      # Use -Remove to remove from startup
    [switch]$TaskScheduler  # Use -TaskScheduler to use Task Scheduler instead of Startup folder
)

$scriptPath = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\startup-linkedin.ps1"
$shortcutName = "LinkedIn-Startup.lnk"
$startupFolder = [Environment]::GetFolderPath("Startup")
$shortcutPath = Join-Path $startupFolder $shortcutName
$taskName = "LinkedIn-Startup"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LinkedIn Startup Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Remove mode
if ($Remove) {
    Write-Host "Removing LinkedIn from startup..." -ForegroundColor Yellow

    # Remove shortcut
    if (Test-Path $shortcutPath) {
        Remove-Item $shortcutPath -Force
        Write-Host "✓ Removed startup shortcut" -ForegroundColor Green
    }

    # Remove scheduled task
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "✓ Removed scheduled task" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "LinkedIn removed from Windows startup." -ForegroundColor Green
    exit 0
}

# Check if script exists
if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: Startup script not found at:" -ForegroundColor Red
    Write-Host $scriptPath -ForegroundColor Red
    exit 1
}

if ($TaskScheduler) {
    # Method 2: Task Scheduler (runs even if startup folder is slow)
    Write-Host "Setting up via Task Scheduler..." -ForegroundColor Yellow

    # Remove existing task if present
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "  Removed existing task" -ForegroundColor Gray
    }

    # Create new task
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Normal -File `"$scriptPath`""
    $trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "LinkedIn Daily Workflow - Launches Chrome and starts autonomous workflow at login"

    Write-Host "✓ Task Scheduler entry created" -ForegroundColor Green

} else {
    # Method 1: Startup Folder (simpler, more visible)
    Write-Host "Setting up via Startup folder..." -ForegroundColor Yellow

    # Create shortcut
    $WshShell = New-Object -ComObject WScript.Shell
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "PowerShell.exe"
    $shortcut.Arguments = "-ExecutionPolicy Bypass -WindowStyle Normal -File `"$scriptPath`""
    $shortcut.WorkingDirectory = Split-Path $scriptPath
    $shortcut.Description = "LinkedIn Daily Workflow Startup"
    $shortcut.Save()

    Write-Host "✓ Startup shortcut created" -ForegroundColor Green
    Write-Host "  Location: $shortcutPath" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "What happens at login:" -ForegroundColor Yellow
Write-Host "  1. Chrome launches with LinkedIn" -ForegroundColor White
Write-Host "  2. Waits 15 seconds for Chrome to load" -ForegroundColor White
Write-Host "  3. Starts LinkedIn autonomous workflow" -ForegroundColor White
Write-Host ""
Write-Host "Notes:" -ForegroundColor Yellow
Write-Host "  - Skips weekends automatically" -ForegroundColor Gray
Write-Host "  - Skips if outside work hours (8am-9pm)" -ForegroundColor Gray
Write-Host "  - Logs activity to linkedin-daily-planner/logs/" -ForegroundColor Gray
Write-Host ""
Write-Host "To test now:" -ForegroundColor Yellow
Write-Host "  .\startup-linkedin.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "To remove from startup:" -ForegroundColor Yellow
Write-Host "  .\setup-startup.ps1 -Remove" -ForegroundColor Cyan
Write-Host ""
