# How to Get Skill Updates

When new skill updates are available, follow these steps to update your copy without losing any of your personal settings or data.

## Step 1: Open a terminal in your skills folder

**Windows:** Open PowerShell, then type:
```
cd C:\path\to\linkedin-skills-suite
```
Replace `C:\path\to\` with wherever you cloned the repo (e.g. `C:\Users\YourName\Desktop\CLI`).

**Mac/Linux:** Open Terminal, then type:
```
cd ~/path/to/linkedin-skills-suite
```

## Step 2: Run the update script

**Windows (PowerShell):**
```
.\update.ps1
```

**Mac/Linux:**
```
bash update.sh
```

## Step 3: Check the result

You'll see one of three outcomes:

**A) No local changes — clean update**
```
  No local changes to stash.
  Pulling latest updates...
  Pull complete.
  Update complete! All skill updates applied, your changes preserved.
```
You're done. Everything updated.

**B) You had local edits — no conflicts**
```
  Stashing your local changes...
  Stashed.
  Pulling latest updates...
  Pull complete.
  Restoring your local changes...
  Restored. No conflicts.
  Update complete! All skill updates applied, your changes preserved.
```
You're done. Your edits and the new updates merged cleanly.

**C) You had local edits — conflicts found**
```
  CONFLICTS DETECTED
  Some of your skill edits clash with upstream updates.

    CONFLICT: linkedin-elite-post/skill.md
```
This means you edited the same part of a file that was also updated upstream. See Step 4.

## Step 4: Fixing conflicts (only if Step 3 showed outcome C)

You have three options — pick whichever is easiest:

**Option 1: Keep the author's version (discard your edit)**
```
git checkout --theirs linkedin-elite-post/skill.md
```
This throws away your change and uses the new update.

**Option 2: Keep your version (ignore the update for this file)**
```
git checkout --ours linkedin-elite-post/skill.md
```
This keeps your edit and skips the author's change.

**Option 3: Merge both manually**

Open the conflicted file in any text editor. You'll see something like:
```
<<<<<<< Updated upstream
name: linkedin-elite-posts-v2
=======
name: linkedin-elite-posts-CLIENT-CUSTOMIZED
>>>>>>> Stashed changes
```
- The top section (between `<<<<<<<` and `=======`) is the **author's new version**
- The bottom section (between `=======` and `>>>>>>>`) is **your version**
- Delete the lines you don't want, delete the `<<<<<<<`, `=======`, and `>>>>>>>` markers, and save

## What's safe and what's not

| File type | Updated by pull? | Your data safe? |
|-----------|-----------------|-----------------|
| Skill files (`skill.md`) | Yes | Stashed and restored automatically |
| Your config (`references/`) | Never touched | Always safe |
| Your activity logs (`shared/logs/`) | Never touched | Always safe |
| Your account settings | Never touched | Always safe |

## If something goes wrong

Your local changes are always saved in git's stash with a timestamp. To see them:
```
git stash list
```
To restore them manually:
```
git stash pop
```
