# LinkedIn Daily Planner - 8:00 AM
# Creates today's LinkedIn activity plan

$logFile = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\logs\daily-planner.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    Add-Content -Path $logFile -Value "[$timestamp] Starting daily planner..."

    # Invoke claude-code to run the linkedin-daily-planner skill
    $result = & claude-code "/linkedin-daily-planner" 2>&1

    Add-Content -Path $logFile -Value "[$timestamp] Daily planner completed"
    Add-Content -Path $logFile -Value $result

    exit 0
} catch {
    Add-Content -Path $logFile -Value "[$timestamp] ERROR: $_"
    exit 1
}
