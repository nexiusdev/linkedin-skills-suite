# LinkedIn Skills Suite — Pull updates safely
# Stashes local changes, pulls latest, restores your changes.
# Reports conflicts if your skill edits clash with upstream updates.

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "LinkedIn Skills Suite - Update" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Check for uncommitted changes
$status = git status --porcelain
$hasChanges = $status.Length -gt 0

if ($hasChanges) {
    Write-Host "  Stashing your local changes..." -ForegroundColor Yellow
    git stash push -m "pre-update-backup-$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR: Failed to stash changes. Aborting." -ForegroundColor Red
        exit 1
    }
    Write-Host "  Stashed." -ForegroundColor Green
} else {
    Write-Host "  No local changes to stash." -ForegroundColor DarkGray
}

# Pull latest
Write-Host ""
Write-Host "  Pulling latest updates..." -ForegroundColor Yellow
git pull
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: git pull failed." -ForegroundColor Red
    if ($hasChanges) {
        Write-Host "  Your changes are safe in git stash. Run 'git stash pop' to restore." -ForegroundColor Yellow
    }
    exit 1
}
Write-Host "  Pull complete." -ForegroundColor Green

# Restore stashed changes
if ($hasChanges) {
    Write-Host ""
    Write-Host "  Restoring your local changes..." -ForegroundColor Yellow
    git stash pop 2>&1 | Out-String | Tee-Object -Variable popOutput | Out-Null

    if ($LASTEXITCODE -ne 0 -or $popOutput -match "CONFLICT") {
        Write-Host ""
        Write-Host "  CONFLICTS DETECTED" -ForegroundColor Red
        Write-Host "  Some of your skill edits clash with upstream updates." -ForegroundColor Red
        Write-Host ""
        Write-Host "  What to do:" -ForegroundColor Yellow
        Write-Host "    1. Open the conflicted files (look for <<<<<<< markers)"
        Write-Host "    2. Keep the parts you want, delete the conflict markers"
        Write-Host "    3. Or run 'git checkout --theirs <file>' to accept the upstream version"
        Write-Host "    4. Or run 'git checkout --ours <file>' to keep your version"
        Write-Host ""
        git diff --name-only --diff-filter=U 2>$null | ForEach-Object {
            Write-Host "    CONFLICT: $_" -ForegroundColor Red
        }
        Write-Host ""
        exit 1
    }

    Write-Host "  Restored. No conflicts." -ForegroundColor Green
}

Write-Host ""
Write-Host "Update complete! All skill updates applied, your changes preserved." -ForegroundColor Green
Write-Host ""
