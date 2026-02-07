# Skill Update Guide (For Clients)

This guide explains how to receive and apply updates to your LinkedIn skill suite without losing any local customizations you've made.

---

## First-Time Setup

Make sure you have the `skill-updater/` folder in your skills directory:

```
your-skills-folder/
  skill-updater/
    skill.md          ← the updater skill
    versions.md       ← tracks which updates you've applied
    updates/           ← where update files go
    backups/           ← automatic backups before changes
```

If you don't have this folder, ask your skill author for it.

---

## Applying an Update

### 1. Receive the update file

Your skill author will send you a file like `update-20260206.md`. This is the update manifest - it describes exactly what changed and why.

### 2. Drop it in the updates folder

Copy the file to:

```
skill-updater/updates/update-20260206.md
```

### 3. Tell Claude to apply it

Say any of these:

> "apply skill update"
> "update skills"
> "sync skills"

### 4. Review the changes

Claude will analyze every change against YOUR current files and show:

| Status | Meaning | Action |
|--------|---------|--------|
| **CLEAN** | Safe to apply, no conflicts | Auto-applied with your approval |
| **CONFLICT** | You modified the same area the update touches | You choose: keep yours, take upstream, or merge both |
| **ALREADY APPLIED** | You already have this change | Skipped automatically |

### 5. Approve and done

Your files are **backed up automatically** before any changes are written. If something goes wrong, you can always rollback.

---

## Other Commands

| Say this | What happens |
|----------|-------------|
| "what version am I on" | Shows your last applied update version |
| "check for updates" | Scans the updates folder for unapplied manifests |
| "rollback last update" | Restores your files from the pre-update backup |

---

## What Happens to My Customizations?

**They're safe.** The updater is designed to preserve your local changes:

- **New sections** (most updates) are inserted without touching your existing content
- **Modified sections** are flagged as conflicts if you've changed the same area - you decide what to keep
- **New list items** are appended without removing your additions
- **Backups** are saved to `skill-updater/backups/` before every update

---

## FAQ

**Q: What if I apply updates out of order?**
Claude will warn you and recommend applying in sequence. You can proceed anyway, but sequential is safest.

**Q: Can I apply the same update twice?**
Claude will detect it's already applied and skip duplicate changes. Safe to re-run.

**Q: What if I haven't customized anything?**
Even simpler - all changes will show as CLEAN and apply directly.

**Q: Where are my backups?**
In `skill-updater/backups/[version]/` - one folder per update, containing your pre-update files.

**Q: How do I know what changed?**
Open the manifest file (`skill-updater/updates/update-XXXXXXXX.md`) - it lists every change with descriptions of what was added and why.
