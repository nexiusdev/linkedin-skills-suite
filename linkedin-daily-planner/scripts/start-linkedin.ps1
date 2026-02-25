# LinkedIn Daily Workflow - Single Autonomous Trigger
# Usage: .\start-linkedin.ps1
# Or add alias: Set-Alias startlinkedin "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\start-linkedin.ps1"

# Determine current time block
$hour = (Get-Date).Hour

if ($hour -lt 10) { $block = "Morning" }
elseif ($hour -lt 12) { $block = "Content" }
elseif ($hour -lt 15) { $block = "Midday" }
elseif ($hour -lt 18) { $block = "Afternoon" }
else { $block = "Evening" }

$day = (Get-Date).DayOfWeek

# Log the launch
$logPath = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\logs"
if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath -Force | Out-Null
}
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path "$logPath\launcher-log.txt" -Value "[$timestamp] Autonomous start - $block Block"

# Single autonomous prompt
$prompt = @"
Run my LinkedIn daily workflow autonomously. Current time block: $block Block ($day).

AUTONOMOUS MODE - Execute without asking questions:
1. Check current time block and what tasks are due
2. Read shared activity log for today's progress
3. Execute all pending tasks for current block
4. Use Chrome DevTools MCP to perform LinkedIn actions
5. Auto-select best variations for posts and comments
6. Log all activities to shared log
7. Move to next task until block is complete

Do NOT ask me which task to start - just execute them in order.
Do NOT ask me to select variations - AI selects the best one.
Do NOT wait for confirmation - proceed autonomously.

Start now.
"@

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LinkedIn Autonomous Workflow" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Day: $day" -ForegroundColor Yellow
Write-Host "  Time: $(Get-Date -Format 'HH:mm')" -ForegroundColor Yellow
Write-Host "  Block: $block" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Starting Codex Code..." -ForegroundColor Green
Write-Host ""

# Launch Codex Code with autonomous prompt
Codex "$prompt"
