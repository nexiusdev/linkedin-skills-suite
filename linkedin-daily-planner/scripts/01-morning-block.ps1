# LinkedIn Morning Block - 8:00 AM
# Engage with 3 Peers + 3 Prospects + 3 Thought Leaders

$logFile = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\logs\morning-block.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    Add-Content -Path $logFile -Value "[$timestamp] Starting morning block..."

    # Execute morning block tasks
    $prompt = "Execute morning block tasks from today's LinkedIn plan"
    $result = & claude-code $prompt 2>&1

    Add-Content -Path $logFile -Value "[$timestamp] Morning block completed"
    Add-Content -Path $logFile -Value $result

    exit 0
} catch {
    Add-Content -Path $logFile -Value "[$timestamp] ERROR: $_"
    exit 1
}
