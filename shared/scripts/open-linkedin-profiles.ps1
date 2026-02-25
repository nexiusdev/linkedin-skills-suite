# LinkedIn Activity Scanner - CSV-driven Profile Opener
# Opens recent activity pages for prospects listed in shared/logs/activity-scan-results-template.csv

$colors = @{
    Header = 'Cyan'
    Info = 'White'
    Success = 'Green'
    Warning = 'Yellow'
    Error = 'Red'
    Highlight = 'Magenta'
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = 'White'
    )
    Write-Host $Message -ForegroundColor $colors[$Color]
}

function Open-ProspectProfile {
    param(
        [pscustomobject]$Prospect
    )

    $url = "https://www.linkedin.com/in/$($Prospect.Username)/recent-activity/all/"
    Write-ColorOutput "  Row #$($Prospect.Row): $($Prospect.Name)" -Color Highlight
    Start-Process $url
}

$csvPath = Join-Path (Split-Path -Parent $PSScriptRoot) "logs\activity-scan-results-template.csv"

if (-not (Test-Path $csvPath)) {
    Write-ColorOutput "CSV not found: $csvPath" -Color Error
    Write-ColorOutput "Create or restore shared/logs/activity-scan-results-template.csv first." -Color Warning
    exit 1
}

$prospects = Import-Csv $csvPath | ForEach-Object {
    $row = 0
    [void][int]::TryParse($_.Row, [ref]$row)
    $name = [string]$_.Name
    $username = [string]$_.Profile_Username
    [pscustomobject]@{
        Row = $row
        Name = $name.Trim()
        Username = $username.Trim()
    }
} | Where-Object {
    $_.Row -gt 0 -and
    $_.Username -ne "" -and
    $_.Username -notmatch '^\s*\{\{.+\}\}\s*$'
} | Sort-Object Row

if ($prospects.Count -eq 0) {
    Write-ColorOutput "No valid prospects found in CSV: $csvPath" -Color Error
    Write-ColorOutput "Populate Row, Name, and Profile_Username first." -Color Warning
    exit 1
}

$minRow = ($prospects | Select-Object -First 1).Row
$maxRow = ($prospects | Select-Object -Last 1).Row

Write-ColorOutput ""
Write-ColorOutput "=== LinkedIn Activity Scanner ===" -Color Header
Write-ColorOutput "Prospects loaded from CSV: $($prospects.Count) (Rows #$minRow-$maxRow)" -Color Info
Write-ColorOutput "Source CSV: $csvPath" -Color Info
Write-ColorOutput ""
Write-ColorOutput "Choose scanning mode:" -Color Info
Write-ColorOutput "1. Batch mode (open 10 profiles at a time)" -Color Highlight
Write-ColorOutput "2. Full scan (open all loaded profiles)" -Color Warning
Write-ColorOutput "3. Custom row range" -Color Highlight
Write-ColorOutput "4. Single profile by row number" -Color Highlight
Write-ColorOutput "5. Exit" -Color Info
Write-ColorOutput ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-ColorOutput "`nBatch Mode Selected" -Color Success
        $batchSize = 10
        $totalBatches = [Math]::Ceiling($prospects.Count / $batchSize)
        Write-ColorOutput "Total batches: $totalBatches" -Color Info
        $startBatch = Read-Host "Start from which batch? (1-$totalBatches)"

        $startBatchNum = [int]$startBatch
        if ($startBatchNum -lt 1 -or $startBatchNum -gt $totalBatches) {
            Write-ColorOutput "Invalid batch number. Exiting." -Color Error
            exit 1
        }

        for ($batch = $startBatchNum; $batch -le $totalBatches; $batch++) {
            $startIdx = ($batch - 1) * $batchSize
            $endIdx = [Math]::Min($startIdx + $batchSize - 1, $prospects.Count - 1)

            Write-ColorOutput "`n--- Batch $batch of $totalBatches ---" -Color Header
            Write-ColorOutput "Opening profiles $($startIdx + 1) to $($endIdx + 1)..." -Color Info

            for ($i = $startIdx; $i -le $endIdx; $i++) {
                Open-ProspectProfile -Prospect $prospects[$i]
                Start-Sleep -Milliseconds 500
            }

            if ($batch -lt $totalBatches) {
                Write-ColorOutput "`nBatch $batch complete. Press any key for next batch..." -Color Warning
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            }
        }

        Write-ColorOutput "`nAll batches complete." -Color Success
    }

    "2" {
        Write-ColorOutput "`nWARNING: This will open $($prospects.Count) LinkedIn tabs." -Color Warning
        $confirm = Read-Host "Are you sure? (yes/no)"

        if ($confirm -eq "yes") {
            foreach ($prospect in $prospects) {
                Open-ProspectProfile -Prospect $prospect
                Start-Sleep -Milliseconds 300
            }
            Write-ColorOutput "All profiles opened." -Color Success
        } else {
            Write-ColorOutput "Cancelled." -Color Info
        }
    }

    "3" {
        Write-ColorOutput "`nCustom Range Mode" -Color Success
        $startRow = Read-Host "Enter start row number ($minRow-$maxRow)"
        $endRow = Read-Host "Enter end row number ($minRow-$maxRow)"

        $startRowNum = [int]$startRow
        $endRowNum = [int]$endRow

        if ($startRowNum -gt $endRowNum) {
            Write-ColorOutput "Invalid range. Exiting." -Color Error
            exit 1
        }

        $filtered = $prospects | Where-Object { $_.Row -ge $startRowNum -and $_.Row -le $endRowNum }
        if ($filtered.Count -eq 0) {
            Write-ColorOutput "No prospects found in that row range." -Color Error
            exit 1
        }

        Write-ColorOutput "`nOpening rows $startRowNum to $endRowNum ($($filtered.Count) profiles)..." -Color Info
        foreach ($prospect in $filtered) {
            Open-ProspectProfile -Prospect $prospect
            Start-Sleep -Milliseconds 500
        }
        Write-ColorOutput "Range complete." -Color Success
    }

    "4" {
        Write-ColorOutput "`nSingle Profile Mode" -Color Success
        $rowNum = Read-Host "Enter row number"
        $target = $prospects | Where-Object { $_.Row -eq [int]$rowNum } | Select-Object -First 1

        if ($null -ne $target) {
            Write-ColorOutput "`nOpening Row #$($target.Row): $($target.Name)" -Color Highlight
            Open-ProspectProfile -Prospect $target
            Write-ColorOutput "Profile opened." -Color Success
        } else {
            Write-ColorOutput "Row not found in CSV. Exiting." -Color Error
            exit 1
        }
    }

    "5" {
        Write-ColorOutput "Exiting." -Color Info
        exit 0
    }

    default {
        Write-ColorOutput "Invalid choice. Exiting." -Color Error
        exit 1
    }
}

Write-ColorOutput "`nRemember to update the CSV with activity status after review." -Color Warning
Write-ColorOutput "Results template: $csvPath" -Color Info
