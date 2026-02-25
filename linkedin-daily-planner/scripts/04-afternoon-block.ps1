# LinkedIn Afternoon Block - 3:00 PM
# Handle connections, DMs, and admin tasks

$logFile = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\logs\afternoon-block.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    Add-Content -Path $logFile -Value "[$timestamp] Starting afternoon block..."

    # Execute afternoon block tasks
    $prompt = "Resume LinkedIn daily plan - execute afternoon block tasks"
    $result = & claude-code $prompt 2>&1

    Add-Content -Path $logFile -Value "[$timestamp] Afternoon block completed"
    Add-Content -Path $logFile -Value $result

    exit 0
} catch {
    Add-Content -Path $logFile -Value "[$timestamp] ERROR: $_"
    exit 1
}
