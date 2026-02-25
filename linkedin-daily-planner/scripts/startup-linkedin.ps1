# LinkedIn Daily Workflow - Windows Startup Script
# This script runs at Windows login to set up and start the LinkedIn workflow
#
# Setup: Run setup-startup.ps1 to add this to Windows startup

param(
    [switch]$SkipWorkflow  # Use -SkipWorkflow to only launch Chrome without running workflow
)

# Configuration
$ChromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$ChromeProfile = "Default"  # Change if using a different Chrome profile
$WaitForChrome = 15  # Seconds to wait for Chrome to fully load
$LinkedInUrl = "https://www.linkedin.com/feed/"

# Log file
$logPath = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\logs"
if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath -Force | Out-Null
}
$logFile = Join-Path $logPath "startup-log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log {
    param($Message)
    $logEntry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
    Add-Content -Path $logFile -Value $logEntry
    Write-Host $logEntry
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LinkedIn Startup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Log "Startup script initiated"

# Step 1: Check if Chrome is already running
$chromeRunning = Get-Process -Name "chrome" -ErrorAction SilentlyContinue

if ($chromeRunning) {
    Write-Log "Chrome is already running"
} else {
    Write-Log "Launching Chrome..."

    # Launch Chrome with LinkedIn
    if (Test-Path $ChromePath) {
        Start-Process $ChromePath -ArgumentList "--profile-directory=$ChromeProfile", $LinkedInUrl
        Write-Log "Chrome launched with LinkedIn"
    } else {
        # Try default chrome command
        Start-Process "chrome.exe" -ArgumentList "--profile-directory=$ChromeProfile", $LinkedInUrl
        Write-Log "Chrome launched via PATH"
    }
}

# Step 2: Wait for Chrome to fully load
Write-Host ""
Write-Host "Waiting $WaitForChrome seconds for Chrome to load..." -ForegroundColor Yellow
Write-Log "Waiting $WaitForChrome seconds for Chrome..."

for ($i = $WaitForChrome; $i -gt 0; $i--) {
    Write-Host "`rWaiting... $i seconds remaining   " -NoNewline -ForegroundColor Gray
    Start-Sleep -Seconds 1
}
Write-Host "`rChrome should be ready now.        " -ForegroundColor Green
Write-Log "Wait complete"

# Step 3: Check if we should run the workflow
if ($SkipWorkflow) {
    Write-Log "Workflow skipped (-SkipWorkflow flag)"
    Write-Host ""
    Write-Host "Chrome launched. Workflow skipped." -ForegroundColor Yellow
    Write-Host "Run 'start linkedin' manually when ready." -ForegroundColor Yellow
    exit 0
}

# Step 4: Check current time - only run workflow during work hours
$hour = (Get-Date).Hour
$dayOfWeek = (Get-Date).DayOfWeek

# Skip weekends
if ($dayOfWeek -eq "Saturday" -or $dayOfWeek -eq "Sunday") {
    Write-Log "Weekend detected - skipping workflow"
    Write-Host ""
    Write-Host "It's the weekend! LinkedIn workflow skipped." -ForegroundColor Yellow
    Write-Host "Chrome is ready if you want to browse manually." -ForegroundColor Gray
    exit 0
}

# Skip if outside work hours (before 8am or after 9pm)
if ($hour -lt 8 -or $hour -gt 21) {
    Write-Log "Outside work hours ($hour:00) - skipping workflow"
    Write-Host ""
    Write-Host "Outside work hours. LinkedIn workflow skipped." -ForegroundColor Yellow
    Write-Host "Chrome is ready if you want to browse manually." -ForegroundColor Gray
    exit 0
}

# Step 5: Run LinkedIn workflow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting LinkedIn Workflow" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Log "Starting LinkedIn autonomous workflow"

# Determine current block
if ($hour -lt 10) { $block = "Morning" }
elseif ($hour -lt 12) { $block = "Content" }
elseif ($hour -lt 15) { $block = "Midday" }
elseif ($hour -lt 18) { $block = "Afternoon" }
else { $block = "Evening" }

Write-Host "Current time block: $block" -ForegroundColor Yellow
Write-Log "Time block: $block"

# Run the LinkedIn workflow
$scriptPath = "{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\scripts\start-linkedin.ps1"

if (Test-Path $scriptPath) {
    Write-Log "Executing start-linkedin.ps1"
    & $scriptPath
} else {
    Write-Log "ERROR: start-linkedin.ps1 not found"
    Write-Host "Error: start-linkedin.ps1 not found at $scriptPath" -ForegroundColor Red
    Write-Host "Run 'start linkedin' manually in Claude Code." -ForegroundColor Yellow
}

Write-Log "Startup script completed"
