# LinkedIn Activity Scanner - Automated Profile Opener
# Opens recent activity pages for prospects in batches to speed up manual scanning

# Color definitions
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

# List of all 50 prospects (rows #55-104)
$prospects = @(
    @{Row=55; Name="Birch Sio"; Username="birch-sio-177164b"},
    @{Row=56; Name="Osla Chan"; Username="osla-chan-a5074535"},
    @{Row=57; Name="Sharon Ngiam"; Username="sharonngiam"},
    @{Row=58; Name="Marcus F."; Username="marcus-f-0ba22412a"},
    @{Row=59; Name="Francis Soh"; Username="francis-soh-27771328"},
    @{Row=60; Name="Maivizhi Murugian"; Username="maivizhi-murugian-218844204"},
    @{Row=61; Name="Zee C."; Username="zee-c-538789b6"},
    @{Row=62; Name="Marie-Morgane Le Bras"; Username="marie-morgane-le-bras-684a1925"},
    @{Row=63; Name="Wilman Ng"; Username="wilman-ng-28721758"},
    @{Row=64; Name="Shagun Chand"; Username="shagun-chand-862135159"},
    @{Row=65; Name="Dr. M Hazane"; Username="dr-m-hazane-37a4663"},
    @{Row=66; Name="Dr. George S.T. Khoo"; Username="dr-george-s-t-khoo-97b21b6a"},
    @{Row=67; Name="Tylus Lim"; Username="tylus-lim-7b801b97"},
    @{Row=68; Name="Yeo HQ"; Username="yeo-hq-b93a7"},
    @{Row=69; Name="Dr Ravee Vellu S"; Username="dr-ravee-vellu-s-830351381"},
    @{Row=70; Name="SINGHAM DHARMESH"; Username="singham-dharmesh-a2473243"},
    @{Row=71; Name="Lam Addison"; Username="lam-addison-7339b838"},
    @{Row=72; Name="Adri Bellamy"; Username="adri-bellamy-864373137"},
    @{Row=73; Name="Melvern Chia"; Username="{{CLIENT_LOCAL_USER}}rnchia"},
    @{Row=74; Name="Emmanuel Stroobant"; Username="emmanuel-stroobant-05a39419"},
    @{Row=75; Name="Brett Davey"; Username="brett-davey-14565649"},
    @{Row=76; Name="Alice Lai"; Username="alice-lai-0836174"},
    @{Row=77; Name="Frédéric Colin"; Username="fcolinsbh"},
    @{Row=78; Name="Glenden Khew"; Username="glenden-khew-237a093"},
    @{Row=79; Name="Will Toh"; Username="will-toh-2b0ba8398"},
    @{Row=80; Name="Steven Lim"; Username="steven-lim-71048a7"},
    @{Row=81; Name="Suhaidi Hussin"; Username="suhaidi-hussin-4567aa22"},
    @{Row=82; Name="Jenny Au"; Username="jenny-au-727b9914"},
    @{Row=83; Name="Olivier van Hardenbroek"; Username="olivier-van-hardenbroek"},
    @{Row=84; Name="Ian Wu"; Username="ian-wu-1ab40431"},
    @{Row=85; Name="Saiskanda Bhaskar Guntury"; Username="sisko07"},
    @{Row=86; Name="Aileen Estrellado"; Username="aileen-estrellado-b2a923101"},
    @{Row=87; Name="Magdalene Tang"; Username="magdalene-tang-16ba9a8b"},
    @{Row=88; Name="Jasmine Ong"; Username="jasmineoll"},
    @{Row=89; Name="Leon Lim"; Username="leon-lim-10a171178"},
    @{Row=90; Name="MissNur (NICCHI)"; Username="missnur"},
    @{Row=91; Name="Gerald Png"; Username="gerald-png-65047655"},
    @{Row=92; Name="Sofia Tung"; Username="sofiatung"},
    @{Row=93; Name="Lorraine Tan"; Username="lorraine-tan-9b4353261"},
    @{Row=94; Name="Gee Michaud"; Username="gee-michaud-2ab6221"},
    @{Row=95; Name="Henry Lim"; Username="henry-lim-975a1118"},
    @{Row=96; Name="Timothy Charlton"; Username="tjcharlton"},
    @{Row=97; Name="Andrew Wong"; Username="andrew-wong-3a227158"},
    @{Row=98; Name="Pek Ee Perh Thomas"; Username="pek-ee-perh-thomas-0a673825"},
    @{Row=99; Name="Meng Soon Lim"; Username="meng-soon-lim-8b81131"},
    @{Row=100; Name="Matthew E. Bradley"; Username="matthew-e-bradley-00558855"},
    @{Row=101; Name="Richard Korff"; Username="richardkorff"},
    @{Row=102; Name="Samantha Sun"; Username="samantha-sun-%E5%AD%99%E8%8E%B9%E5%8F%8C-30805536"},
    @{Row=103; Name="Gerard Chuah"; Username="gerard-chuah-63093316"},
    @{Row=104; Name="Dr Fahir Khiard"; Username="fahirkhiard"}
)

# Main menu
Write-ColorOutput "`n=== LinkedIn Activity Scanner ===" -Color Header
Write-ColorOutput "Total Prospects: 50 (Rows #55-104)" -Color Info
Write-ColorOutput ""
Write-ColorOutput "Choose scanning mode:" -Color Info
Write-ColorOutput "1. Batch mode (open 10 profiles at a time)" -Color Highlight
Write-ColorOutput "2. Full scan (open all 50 profiles - NOT RECOMMENDED)" -Color Warning
Write-ColorOutput "3. Custom range (specify start and end row)" -Color Highlight
Write-ColorOutput "4. Single profile (specify row number)" -Color Highlight
Write-ColorOutput "5. Exit" -Color Info
Write-ColorOutput ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        # Batch mode
        Write-ColorOutput "`nBatch Mode Selected" -Color Success
        Write-ColorOutput "This will open profiles in groups of 10 with pauses between batches." -Color Info
        Write-ColorOutput ""

        $batchSize = 10
        $totalBatches = [Math]::Ceiling($prospects.Count / $batchSize)

        Write-ColorOutput "Total batches: $totalBatches" -Color Info
        $startBatch = Read-Host "Start from which batch? (1-$totalBatches)"

        $startBatchNum = [int]$startBatch
        if ($startBatchNum -lt 1 -or $startBatchNum -gt $totalBatches) {
            Write-ColorOutput "Invalid batch number. Exiting." -Color Error
            exit
        }

        for ($batch = $startBatchNum; $batch -le $totalBatches; $batch++) {
            $startIdx = ($batch - 1) * $batchSize
            $endIdx = [Math]::Min($startIdx + $batchSize - 1, $prospects.Count - 1)

            Write-ColorOutput "`n--- Batch $batch of $totalBatches ---" -Color Header
            Write-ColorOutput "Opening profiles $($startIdx + 1) to $($endIdx + 1)..." -Color Info

            for ($i = $startIdx; $i -le $endIdx; $i++) {
                $prospect = $prospects[$i]
                $url = "https://www.linkedin.com/in/$($prospect.Username)/recent-activity/all/"
                Write-ColorOutput "  Row #$($prospect.Row): $($prospect.Name)" -Color Highlight
                Start-Process $url
                Start-Sleep -Milliseconds 500  # Delay between tabs to avoid overwhelming browser
            }

            if ($batch -lt $totalBatches) {
                Write-ColorOutput "`nBatch $batch complete. Review these profiles and mark activity status." -Color Success
                Write-ColorOutput "Press any key when ready for next batch..." -Color Warning
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            }
        }

        Write-ColorOutput "`nAll batches complete!" -Color Success
    }

    "2" {
        # Full scan (not recommended)
        Write-ColorOutput "`nWARNING: This will open 50 LinkedIn tabs at once!" -Color Warning
        $confirm = Read-Host "Are you sure? (yes/no)"

        if ($confirm -eq "yes") {
            Write-ColorOutput "Opening all 50 profiles..." -Color Info
            foreach ($prospect in $prospects) {
                $url = "https://www.linkedin.com/in/$($prospect.Username)/recent-activity/all/"
                Write-ColorOutput "  Row #$($prospect.Row): $($prospect.Name)" -Color Highlight
                Start-Process $url
                Start-Sleep -Milliseconds 300
            }
            Write-ColorOutput "All profiles opened!" -Color Success
        } else {
            Write-ColorOutput "Cancelled." -Color Info
        }
    }

    "3" {
        # Custom range
        Write-ColorOutput "`nCustom Range Mode" -Color Success
        $startRow = Read-Host "Enter start row number (55-104)"
        $endRow = Read-Host "Enter end row number (55-104)"

        $startRowNum = [int]$startRow
        $endRowNum = [int]$endRow

        if ($startRowNum -lt 55 -or $endRowNum -gt 104 -or $startRowNum -gt $endRowNum) {
            Write-ColorOutput "Invalid range. Exiting." -Color Error
            exit
        }

        $filtered = $prospects | Where-Object { $_.Row -ge $startRowNum -and $_.Row -le $endRowNum }

        Write-ColorOutput "`nOpening rows $startRowNum to $endRowNum ($($filtered.Count) profiles)..." -Color Info
        foreach ($prospect in $filtered) {
            $url = "https://www.linkedin.com/in/$($prospect.Username)/recent-activity/all/"
            Write-ColorOutput "  Row #$($prospect.Row): $($prospect.Name)" -Color Highlight
            Start-Process $url
            Start-Sleep -Milliseconds 500
        }
        Write-ColorOutput "Range complete!" -Color Success
    }

    "4" {
        # Single profile
        Write-ColorOutput "`nSingle Profile Mode" -Color Success
        $rowNum = Read-Host "Enter row number (55-104)"

        $prospect = $prospects | Where-Object { $_.Row -eq [int]$rowNum }

        if ($prospect) {
            $url = "https://www.linkedin.com/in/$($prospect.Username)/recent-activity/all/"
            Write-ColorOutput "`nOpening Row #$($prospect.Row): $($prospect.Name)" -Color Highlight
            Start-Process $url
            Write-ColorOutput "Profile opened!" -Color Success
        } else {
            Write-ColorOutput "Invalid row number. Exiting." -Color Error
        }
    }

    "5" {
        Write-ColorOutput "Exiting." -Color Info
        exit
    }

    default {
        Write-ColorOutput "Invalid choice. Exiting." -Color Error
    }
}

Write-ColorOutput "`nDon't forget to update the scan checklist as you review each profile!" -Color Warning
Write-ColorOutput "Checklist location: {{CLIENT_WORKSPACE_ROOT}}\linkedin-core\shared\logs\activity-scan-batch-30jan.md" -Color Info
