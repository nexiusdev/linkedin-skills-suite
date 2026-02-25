---
name: codex-skills-maintainer
description: Safely update skills installed directly in ~/.codex/skills (or %USERPROFILE%\\.codex\\skills) by backing up client state, reinstalling from GitHub, and restoring local config/logs. Use when user says "update installed skills", "upgrade .codex skills", "refresh skills from GitHub", or asks how to update non-git skill installs.
---

# Codex Skills Maintainer

Use this skill when the user installed skills directly into `$CODEX_HOME/skills` and needs updates from a GitHub repository.

## When to Use

Use this skill for:
- direct `.codex/skills` installs (not a local git clone)
- safe upgrades that preserve local client files
- reinstalling selected skill folders from a repo/ref

Do not use this skill when the user is updating a local git clone. In that case, use the repo `update.ps1` / `update.sh` flow.

## What It Does

The updater script performs:
1. Detect/update target skills in `$CODEX_HOME/skills`
2. Backup local client state paths (references/logs/config)
3. Remove old skill folders
4. Reinstall latest skill folders from GitHub
5. Restore backed up local state
6. Print a summary and backup location

## Script

`scripts/update_codex_installed_skills.py`

## Recommended Command

```bash
python "$CODEX_HOME/skills/codex-skills-maintainer/scripts/update_codex_installed_skills.py" --repo <owner>/<repo> --ref main
```

## Common Options

```bash
# Dry-run first
python "$CODEX_HOME/skills/codex-skills-maintainer/scripts/update_codex_installed_skills.py" --repo <owner>/<repo> --dry-run

# Update only selected skills
python "$CODEX_HOME/skills/codex-skills-maintainer/scripts/update_codex_installed_skills.py" --repo <owner>/<repo> --skills linkedin-core linkedin-daily-planner

# Include updating this maintainer skill itself
python "$CODEX_HOME/skills/codex-skills-maintainer/scripts/update_codex_installed_skills.py" --repo <owner>/<repo> --include-self
```

## Defaults

- Destination: `$CODEX_HOME/skills` (defaults to `~/.codex/skills`)
- Ref: `main`
- Backup root: `$CODEX_HOME/backups/skills-update-<timestamp>`
- State paths backed up/restored by default:
  - `linkedin-core/references`
  - `linkedin-core/shared/logs`
  - `linkedin-core/shared/linkedin-account-config.md`
  - `references`
  - `shared/logs`

## Notes

- Requires network access to GitHub.
- Requires the system installer script at:
  - `$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py`
- Restart Codex after update so refreshed skills are loaded.
