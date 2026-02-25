# {{CLIENT_COMMUNITY_NAME}} News Poster
# Runs Codex Code to find and post AI news to WhatsApp
# Schedule: 10 AM and 8 PM {{CLIENT_TIMEZONE}}, weekdays only

# Set working directory
Set-Location "{{CLIENT_WORKSPACE_ROOT}}"

# Check if weekend (Saturday=6, Sunday=0)
$dayOfWeek = (Get-Date).DayOfWeek.value__
if ($dayOfWeek -eq 0 -or $dayOfWeek -eq 6) {
    Write-Host "Weekend detected. Skipping AI news posting."
    exit 0
}

# Run codex with posting command
Write-Host "Starting {{CLIENT_COMMUNITY_NAME}} news posting at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
codex "post ai news to {{CLIENT_COMMUNITY_NAME}}"

Write-Host "Posting complete at $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
