---
name: skill-updater
description: Safely apply upstream skill updates to client installations without overwriting local modifications. Use when "apply skill update", "sync skills", "update skills", or when an update manifest file is available.
---

# Skill Updater

Reads structured update manifest files, compares against client's current skill files, and intelligently merges changes - showing diffs for approval before writing.

## Trigger

Activate when user says:
- "apply skill update"
- "update skills"
- "sync skills"
- "apply update manifest"
- "check for updates"
- "what version am I on"
- "rollback last update"

## Update Manifest Format

Update manifests are structured markdown files placed in `skill-updater/updates/`. Each manifest describes one versioned update with specific change operations.

```markdown
# Skill Update: [Title]
Version: X.Y
Date: YYYY-MM-DD
Author: [name]

## Changes Summary
- [bullet list of what changed and why]

## File Updates

### File: [relative/path/to/skill.md]

#### Change 1: ADD_SECTION
Location: After section "## [Section Name]"
Description: [What this adds and why]
Content:
~~~
[The actual markdown content to insert]
~~~

#### Change 2: MODIFY_SECTION
Section: "## [Section Name]"
Find: [exact text to locate]
Replace with:
~~~
[replacement content]
~~~

#### Change 3: ADD_TO_LIST
Section: "## [Checklist Name]"
After line containing: "[existing item text]"
Add:
~~~
[new list item(s)]
~~~
```

### Operation Types

| Operation | Description | Conflict Risk |
|-----------|-------------|---------------|
| `ADD_SECTION` | Insert new section after a specified anchor | LOW - new content in new location |
| `MODIFY_SECTION` | Replace specific text within a section | HIGH - client may have modified target area |
| `ADD_TO_LIST` | Append items to an existing list/checklist | LOW - additive by nature |

## Workflow

### Step 1: Read Manifest

```
1. Check skill-updater/updates/ folder for manifest files
   → OR accept path provided by user
2. Parse manifest:
   → Version number
   → Date and author
   → Files affected (list of relative paths)
   → Change operations per file (ADD_SECTION, MODIFY_SECTION, ADD_TO_LIST)
3. Display summary:
   "Update [Version]: [Title] - [X] changes across [Y] files"
```

### Step 2: Version Check

Read `skill-updater/versions.md` to check update history.

```
1. Read skill-updater/versions.md
2. Check if this version has already been applied:
   → If ALREADY APPLIED: Warn user and ask to confirm re-application
   → If NOT APPLIED: Continue
3. Check version ordering:
   → If applying out of order (e.g., v1.2 before v1.1): Warn user
   → Recommend applying in sequence
4. Display: "Last applied: [version] on [date]. This update: [version]"
```

### Step 3: Analyze Changes (Per File)

For each file listed in the manifest:

```
1. READ the client's current version of the file
2. For each change operation in the manifest:

   ADD_SECTION:
   → Verify the "after" anchor section exists in client file
   → Search for the new content already present (idempotency check)
   → If anchor NOT FOUND: Mark as CONFLICT (anchor missing)
   → If content ALREADY EXISTS: Mark as ALREADY_APPLIED
   → If anchor found + content new: Mark as CLEAN

   MODIFY_SECTION:
   → Find the target section in client file
   → Search for the "Find" text
   → If "Find" text matches exactly: Mark as CLEAN
   → If section exists but "Find" text differs: Mark as CONFLICT
     (client has modified this area)
   → If section NOT FOUND: Mark as CONFLICT (section missing)

   ADD_TO_LIST:
   → Find the list/checklist section
   → Verify the anchor item exists
   → Check if new item(s) already present
   → If anchor found + items new: Mark as CLEAN
   → If items ALREADY EXIST: Mark as ALREADY_APPLIED
   → If anchor NOT FOUND: Mark as CONFLICT

3. Classify each change:
   → CLEAN: Can apply safely
   → CONFLICT: Client modified the target area
   → ALREADY_APPLIED: Content already exists
```

### Step 4: Present Diff for Approval

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UPDATE ANALYSIS: [Title] v[Version]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
  CLEAN changes (ready to apply): [X]
  CONFLICTS (need resolution):    [Y]
  ALREADY APPLIED (skipping):     [Z]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLEAN CHANGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] ADD_SECTION to [file]
    After: "## [Section Name]"
    Adding: [brief description]
    Preview: [first 3 lines of new content]...

[2] ADD_TO_LIST in [file]
    List: "## [Checklist Name]"
    Adding: [new items]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONFLICTS (Require Decision)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[3] MODIFY_SECTION in [file]
    Section: "## [Section Name]"

    UPSTREAM VERSION:
    [new content from manifest]

    YOUR VERSION:
    [client's current content]

    Options:
    (a) Apply upstream version (overwrite your changes)
    (b) Keep your version (skip this change)
    (c) Manual merge (I'll show both, you edit)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALREADY APPLIED (Skipping)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[4] ADD_SECTION to [file] - Content already present
[5] ADD_TO_LIST in [file] - Items already in list

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceed with [X] clean changes? (Y/N)
For conflicts, choose resolution per item.
```

### Step 5: Apply Approved Changes

```
1. BACKUP: Before any writes, copy affected files to:
   skill-updater/backups/[version]/[original-filename]

2. APPLY: For each approved change:
   → ADD_SECTION: Insert content after anchor section
   → MODIFY_SECTION: Replace "Find" text with new content
   → ADD_TO_LIST: Insert new items after anchor item

3. VERIFY: Re-read each modified file to confirm changes applied correctly

4. UPDATE VERSION TRACKING:
   → Add row to skill-updater/versions.md:
     | [Version] | [Today] | [Title] | [applied count]/[total] | [skipped count] |

5. LOG: Add entry to shared/logs/skill-changes.md:
   → Category: ENHANCEMENT
   → Title: "Skill Update [Version]: [Title]"
   → Changes: List of what was applied
   → Files Modified: List of affected files

6. DISPLAY RESULT:
   "Update [Version] applied successfully.
    [X] changes applied, [Y] skipped, [Z] conflicts resolved.
    Backups saved to skill-updater/backups/[version]/"
```

## Version Tracking

**File:** `skill-updater/versions.md`

Tracks which updates have been applied to this installation:

```markdown
# Skill Versions

| Version | Date Applied | Update Title | Changes Applied | Changes Skipped |
|---------|-------------|--------------|-----------------|-----------------|
| 1.0     | 06Feb2026   | Passive Prospect Monitoring | 8/8 | 0 |
```

Read this file to answer "what version am I on" - the latest row is the current version.

## Creating Update Manifests (For Skill Author)

When you (the skill author) make changes and want to distribute them:

```
1. After making changes to skill files, run:
   "create update manifest for [version]"

2. The skill will:
   → Read git diff or recent changes
   → Identify affected files and sections
   → Auto-generate manifest in correct format
   → Classify each change as ADD_SECTION, MODIFY_SECTION, or ADD_TO_LIST
   → Save to skill-updater/updates/update-YYYYMMDD.md

3. Review the generated manifest for accuracy

4. Share with clients:
   → Copy the manifest file to client's skill-updater/updates/ folder
   → Client runs "apply skill update" to process it
```

### Manifest Creation Workflow

```
FOR EACH modified file in git diff:
  1. Identify which sections changed
  2. For each section:
     → New section added? → ADD_SECTION operation
     → Existing section modified? → MODIFY_SECTION operation
     → Items added to list? → ADD_TO_LIST operation
  3. Capture the exact new/changed content
  4. Write to manifest with proper anchors and descriptions
```

## Conflict Resolution Strategies

| Operation | Conflict Likelihood | Resolution Strategy |
|-----------|-------------------|---------------------|
| ADD_SECTION | LOW | Almost never conflicts - new content in new location. Only conflicts if anchor section was renamed/removed by client. |
| MODIFY_SECTION | HIGH | Most likely to conflict. Show both versions side-by-side. Ask client to choose: upstream, keep theirs, or manual merge. |
| ADD_TO_LIST | LOW | Rarely conflicts - additive by nature. Only conflicts if anchor item was removed by client. |

### Conflict Tips

- If client renamed a section, the anchor won't match. Solution: Update the anchor in the manifest to match client's section name.
- If client heavily customized a section, prefer "keep client's" and manually apply relevant parts from upstream.
- ADD_SECTION is safest for distributing new features (no existing content to conflict with).

## Rollback

**Trigger:** "rollback last update" or "undo skill update"

```
ROLLBACK WORKFLOW:
1. Read skill-updater/versions.md for last applied update
2. Check skill-updater/backups/[version]/ for backup files
3. For each backed-up file:
   → Show diff between current and backup
   → Confirm rollback per file
4. Restore files from backup
5. Remove version entry from versions.md
6. Log rollback to shared/logs/skill-changes.md
```

**Backup location:** `skill-updater/backups/[version]/`

Before applying ANY changes in Step 5, the workflow copies every affected file to the backup folder. This ensures safe rollback if something goes wrong.

## Edge Cases

**No manifest files found:**
```
No update manifests found in skill-updater/updates/

Options:
1. Provide a path to a manifest file
2. Check if manifest was placed in correct folder
3. Download latest manifest from skill author
```

**Manifest references file that doesn't exist:**
```
File not found: [path]

This file may not be part of your installation.
Options:
1. Create the file with manifest content (treats all changes as ADD)
2. Skip all changes for this file
```

**Multiple manifests available:**
```
Multiple update manifests found:
1. update-20260206.md (v1.0 - Passive Prospect Monitoring)
2. update-20260215.md (v1.1 - Algorithm Training Update)

Apply in order? (Recommended: apply oldest first)
```

## Quality Checklist

Before applying any update:
- [ ] Manifest parsed successfully (version, files, operations)
- [ ] Version check completed (not already applied, correct order)
- [ ] All affected files read and analyzed
- [ ] Each change classified (CLEAN / CONFLICT / ALREADY_APPLIED)
- [ ] Diff preview shown to user
- [ ] Conflicts resolved (upstream / keep / manual merge)
- [ ] Backups created before any writes
- [ ] Changes applied and verified
- [ ] versions.md updated
- [ ] skill-changes.md logged

## Integration with Other Skills

| Scenario | Skill |
|----------|-------|
| After update applied | Check affected skills still work as expected |
| New skill added via update | `linkedin-onboarding` may need re-run |
| Version history query | Read `skill-updater/versions.md` directly |
