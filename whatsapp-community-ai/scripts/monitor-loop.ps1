# {{CLIENT_COMMUNITY_NAME}} WhatsApp Monitor - Continuous Loop
# Keep this terminal window open while working
# Press Ctrl+C to stop

$intervalMinutes = 15
$activeStartHour = 7   # 7 AM
$activeEndHour = 23    # 11 PM

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔄 {{CLIENT_COMMUNITY_NAME}} MONITOR - CONTINUOUS MODE" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Interval: Every $intervalMinutes minutes"
Write-Host "Active hours: ${activeStartHour}:00 - ${activeEndHour}:00"
Write-Host "Press Ctrl+C to stop"
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Set working directory
Set-Location "{{CLIENT_WORKSPACE_ROOT}}"

$cycleCount = 0

while ($true) {
    $currentHour = (Get-Date).Hour
    $currentTime = Get-Date -Format "HH:mm:ss"

    Write-Host ""

    # Check if within active hours
    if ($currentHour -lt $activeStartHour -or $currentHour -ge $activeEndHour) {
        Write-Host "[$currentTime] ⏸️ Outside active hours. Sleeping..." -ForegroundColor Yellow
    }
    else {
        $cycleCount++
        Write-Host "[$currentTime] 🔍 Starting monitoring cycle #$cycleCount..." -ForegroundColor Green
        Write-Host ""

        # Run codex with monitoring command
        codex "monitor {{CLIENT_COMMUNITY_NAME}}"

        Write-Host ""
        Write-Host "[$currentTime] ✅ Cycle #$cycleCount complete" -ForegroundColor Green
    }

    # Calculate next run time
    $nextRun = (Get-Date).AddMinutes($intervalMinutes).ToString("HH:mm:ss")
    Write-Host "[$currentTime] ⏰ Next check at: $nextRun" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

    # Sleep for interval
    Start-Sleep -Seconds ($intervalMinutes * 60)
}
