#!/usr/bin/env bash
# LinkedIn Skills Suite — Pull updates safely
# Stashes local changes, pulls latest, restores your changes.
# Reports conflicts if your skill edits clash with upstream updates.

set -e

echo ""
echo "LinkedIn Skills Suite - Update"
echo "=============================="
echo ""

# Check for uncommitted changes
has_changes=false
if [ -n "$(git status --porcelain)" ]; then
    has_changes=true
fi

if [ "$has_changes" = true ]; then
    echo "  Stashing your local changes..."
    git stash push -m "pre-update-backup-$(date +%Y-%m-%d-%H%M%S)"
    echo "  Stashed."
else
    echo "  No local changes to stash."
fi

# Pull latest
echo ""
echo "  Pulling latest updates..."
if ! git pull; then
    echo "  ERROR: git pull failed."
    if [ "$has_changes" = true ]; then
        echo "  Your changes are safe in git stash. Run 'git stash pop' to restore."
    fi
    exit 1
fi
echo "  Pull complete."

# Restore stashed changes
if [ "$has_changes" = true ]; then
    echo ""
    echo "  Restoring your local changes..."

    if ! git stash pop 2>&1 | tee /dev/stderr | grep -q "CONFLICT"; then
        echo "  Restored. No conflicts."
    else
        echo ""
        echo "  CONFLICTS DETECTED"
        echo "  Some of your skill edits clash with upstream updates."
        echo ""
        echo "  What to do:"
        echo "    1. Open the conflicted files (look for <<<<<<< markers)"
        echo "    2. Keep the parts you want, delete the conflict markers"
        echo "    3. Or run 'git checkout --theirs <file>' to accept the upstream version"
        echo "    4. Or run 'git checkout --ours <file>' to keep your version"
        echo ""
        git diff --name-only --diff-filter=U 2>/dev/null | while read -r f; do
            echo "    CONFLICT: $f"
        done
        echo ""
        exit 1
    fi
fi

echo ""
echo "Update complete! All skill updates applied, your changes preserved."
echo ""
