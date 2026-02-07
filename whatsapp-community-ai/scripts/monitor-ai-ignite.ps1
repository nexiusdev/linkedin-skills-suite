# AI Ignite WhatsApp Monitor
# Runs Claude Code to check for unanswered questions and auto-reply
# Schedule this script to run every 15 minutes via Windows Task Scheduler

# Set working directory
Set-Location "C:\Users\melve\.claude\skills"

# Check if within active hours (7 AM - 11 PM SGT)
$currentHour = (Get-Date).Hour
if ($currentHour -lt 7 -or $currentHour -ge 23) {
    Write-Host "Outside active hours (7 AM - 11 PM). Skipping monitoring."
    exit 0
}

# Run Claude Code with monitoring command
Write-Host "Starting AI Ignite monitoring at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
claude "monitor ai ignite"

Write-Host "Monitoring complete at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
