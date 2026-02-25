# LinkedIn Content Block - 9:00 AM
# Create and schedule save-worthy content

$logFile = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\logs\content-block.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    Add-Content -Path $logFile -Value "[$timestamp] Starting content block..."

    # Execute content block tasks
    $prompt = "Resume LinkedIn daily plan - execute content block tasks"
    $result = & codex $prompt 2>&1

    Add-Content -Path $logFile -Value "[$timestamp] Content block completed"
    Add-Content -Path $logFile -Value $result

    exit 0
} catch {
    Add-Content -Path $logFile -Value "[$timestamp] ERROR: $_"
    exit 1
}
