# LinkedIn Evening Block - 6:00 PM
# Inbound engagement + PROSPECT comments only

$logFile = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\logs\evening-block.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    Add-Content -Path $logFile -Value "[$timestamp] Starting evening block..."

    # Execute evening block tasks
    $prompt = "Resume LinkedIn daily plan - execute evening block tasks"
    $result = & claude-code $prompt 2>&1

    Add-Content -Path $logFile -Value "[$timestamp] Evening block completed"
    Add-Content -Path $logFile -Value $result

    exit 0
} catch {
    Add-Content -Path $logFile -Value "[$timestamp] ERROR: $_"
    exit 1
}
