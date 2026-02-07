# LinkedIn Daily Planner - Automated Launcher
# This script launches Claude Code with the daily planner at scheduled times
# Set up with Windows Task Scheduler for automation

param(
    [string]$TimeBlock = "auto"  # auto, morning, content, midday, afternoon, evening
)

# Determine current time block if auto
function Get-CurrentTimeBlock {
    $hour = (Get-Date).Hour

    if ($hour -lt 10) { return "morning" }
    elseif ($hour -lt 12) { return "content" }
    elseif ($hour -lt 15) { return "midday" }
    elseif ($hour -lt 18) { return "afternoon" }
    else { return "evening" }
}

# Set time block
if ($TimeBlock -eq "auto") {
    $TimeBlock = Get-CurrentTimeBlock
}

# Define prompts for each time block
$prompts = @{
    "morning" = "Check my LinkedIn schedule and start the Morning Block. I need to do 9 comments (3 Peer, 3 Prospect, 3 Thought Leader) before posting. Find posts to engage with and help me draft comments."

    "content" = "Check my LinkedIn schedule. I'm in the Content Block. Help me create today's post using linkedin-elite-post, generate an image with linkedin-image-generator, and schedule it for the optimal window."

    "midday" = "Check my LinkedIn schedule. I'm in the Midday Block (Golden Hour). Help me reply to comments on my post and engage with 5-10 other posts."

    "afternoon" = "Check my LinkedIn schedule. I'm in the Afternoon Block. Check for connection acceptances, send any pending Value DMs, and help me send new connection requests."

    "evening" = "Check my LinkedIn schedule. I'm in the Evening Block. Run the full inbound engagement audit: check post engagement, comment likes, profile views, new followers. Screen all for ICP fit and update the shared activity log."

    "full" = "Plan my LinkedIn day. Create the full daily to-do list and help me execute each block."
}

# Get the prompt for this time block
$prompt = $prompts[$TimeBlock]

# Log the launch
$logPath = "C:\Users\melve\.claude\skills\linkedin-daily-planner\logs"
if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath -Force
}

$logFile = Join-Path $logPath "launcher-log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logFile -Value "[$timestamp] Launching $TimeBlock block"

# Display info
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "LinkedIn Daily Planner - $TimeBlock Block" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Time: $(Get-Date -Format 'HH:mm')" -ForegroundColor Yellow
Write-Host "Block: $TimeBlock" -ForegroundColor Yellow
Write-Host ""
Write-Host "Launching Claude Code with prompt:" -ForegroundColor Green
Write-Host $prompt -ForegroundColor White
Write-Host ""

# Launch Claude Code with the prompt
# Option 1: Interactive mode (opens Claude Code for user interaction)
claude --print "$prompt"

# Note: The above command prints the prompt. User can copy/paste or
# modify to use: claude "$prompt" for direct execution

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Session complete. Log updated." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
