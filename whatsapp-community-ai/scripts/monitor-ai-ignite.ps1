# {{CLIENT_COMMUNITY_NAME}} WhatsApp Monitor
# Runs Claude Code to check for unanswered questions and auto-reply
# Schedule this script to run every 15 minutes via Windows Task Scheduler

# Set working directory
Set-Location "{{CLIENT_WORKSPACE_ROOT}}"

# Check if within active hours (7 AM - 11 PM {{CLIENT_TIMEZONE}})
$currentHour = (Get-Date).Hour
if ($currentHour -lt 7 -or $currentHour -ge 23) {
    Write-Host "Outside active hours (7 AM - 11 PM). Skipping monitoring."
    exit 0
}

# Run Claude Code with monitoring command
Write-Host "Starting {{CLIENT_COMMUNITY_NAME}} monitoring at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
claude "monitor ai ignite"

Write-Host "Monitoring complete at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
