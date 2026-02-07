# LinkedIn Midday Block - 12:00 PM (Golden Hour)
# Post content + engage with PROSPECT posts only

$logFile = "C:\Users\melve\.claude\skills\linkedin-daily-planner\logs\midday-block.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    Add-Content -Path $logFile -Value "[$timestamp] Starting midday block (Golden Hour)..."

    # Execute midday block tasks
    $prompt = "Resume LinkedIn daily plan - execute midday block Golden Hour tasks"
    $result = & claude-code $prompt 2>&1

    Add-Content -Path $logFile -Value "[$timestamp] Midday block completed"
    Add-Content -Path $logFile -Value $result

    exit 0
} catch {
    Add-Content -Path $logFile -Value "[$timestamp] ERROR: $_"
    exit 1
}
