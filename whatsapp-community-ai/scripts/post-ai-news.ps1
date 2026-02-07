# AI Ignite News Poster
# Runs Claude Code to find and post AI news to WhatsApp
# Schedule: 10 AM and 8 PM SGT, weekdays only

# Set working directory
Set-Location "C:\Users\melve\.claude\skills"

# Check if weekend (Saturday=6, Sunday=0)
$dayOfWeek = (Get-Date).DayOfWeek.value__
if ($dayOfWeek -eq 0 -or $dayOfWeek -eq 6) {
    Write-Host "Weekend detected. Skipping AI news posting."
    exit 0
}

# Run Claude Code with posting command
Write-Host "Starting AI Ignite news posting at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
claude "post ai news to ai ignite"

Write-Host "Posting complete at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
