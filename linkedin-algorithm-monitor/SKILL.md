---
name: linkedin-algorithm-monitor
description: Search for LinkedIn algorithm changes (last 7 days), analyze findings against current strategy parameters, propose changes with full details for review, and make approved modifications to skill files. Use when user says "check linkedin algorithm", "linkedin algorithm update", "scan for algorithm changes", or "linkedin strategy audit".
---

# LinkedIn Algorithm Monitor

Scan for recent LinkedIn algorithm changes and keep your strategy files up to date. All changes require explicit user approval before implementation.

## Trigger

- "check linkedin algorithm"
- "linkedin algorithm update"
- "scan for algorithm changes"
- "linkedin strategy audit"
- "update linkedin strategy"

## Workflow Overview

```
Phase 1: RESEARCH (Last 7 Days)
├─ Web search for LinkedIn algorithm updates
├─ Search official sources + trusted researchers
└─ Output: List of potential changes with sources

Phase 2: ANALYSIS
├─ Compare findings against current strategy parameters
├─ Read linkedin-core/references/LINKEDIN-OUTREACH-STRATEGY.md for current values
└─ Output: Gap analysis - what's changed vs current config

Phase 3: PROPOSAL (Requires Approval)
├─ Generate detailed change proposal
├─ Show complete proposal to user
└─ STOP and wait for explicit "proceed" approval

Phase 4: IMPLEMENTATION (After Approval Only)
├─ Update affected files
├─ Log all changes with timestamps
└─ Output: Change log with before/after values
```

---

## Phase 1: Research

### Search Window
Last 7 days only (quick scan for recent updates)

### Search Sources

**Primary Sources (Official/Trusted):**
1. LinkedIn Official Blog - blog.linkedin.com
2. LinkedIn Engineering Blog - engineering.linkedin.com
3. independent LinkedIn algorithm researcher (360Brew) - LinkedIn algorithm researcher
4. LinkedIn Help Center updates

**Secondary Sources:**
1. Social Media Today
2. HubSpot LinkedIn updates
3. Hootsuite LinkedIn reports
4. Marketing professionals on LinkedIn

### Search Queries

Execute these web searches in sequence:

```
1. "LinkedIn algorithm update [current month] 2026"
2. "LinkedIn algorithm changes this week"
3. "360Brew algorithm update 2026"
4. "independent LinkedIn algorithm researcher LinkedIn 2026"
5. "LinkedIn reach changes 2026"
6. "LinkedIn posting best practices [current month] 2026"
7. "LinkedIn engagement changes 2026"
```

### Research Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN ALGORITHM SCAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Search period: [Date] to [Date] (7 days)
Sources checked: [X]

FINDINGS:
1. [Finding 1]
   Source: [URL]
   Date: [Publication date]

2. [Finding 2]
   Source: [URL]
   Date: [Publication date]

[Continue for all findings...]

NO CHANGES FOUND: [List areas with no updates]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 2: Analysis

### Current Strategy Parameters

Read the master strategy file to get current values:
- `{{CLIENT_WORKSPACE_ROOT}}\linkedin-core/references/LINKEDIN-OUTREACH-STRATEGY.md`

### Parameters to Compare

| Parameter | Current Value | Check Against |
|-----------|---------------|---------------|
| Post limit | 1-2/day, 12h gap | Any changes to posting frequency |
| Comment limit | 30/day max | New comment limits or quality signals |
| Comment length | 15-50 words | Word count requirements |
| Connection limit | 15/day max | Connection request thresholds |
| DM limit | 25/day max | DM limitations |
| Posting windows | Day-specific {{CLIENT_TIMEZONE}} | Optimal timing updates |
| Golden Hour | 5-10 posts before/after | Engagement timing changes |
| Response boost | +35% within 1h | Reply impact on reach |
| Save multiplier | 5x Likes | Save value changes |
| Link penalty | -50% in body | External link handling |
| 2-3 Touch Rule | Min 2-3 touches | Connection warmup requirements |
| Blank request bonus | 10-15% better | Connection note effectiveness |

### Analysis Process

1. **Read current strategy file** for baseline values
2. **Compare each finding** against the parameter table
3. **Identify gaps** where research suggests different values
4. **Classify changes** by confidence level:
   - HIGH: Official LinkedIn announcement
   - MEDIUM: Multiple trusted sources agree
   - LOW: Single source or speculation

### Analysis Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GAP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHANGES DETECTED: [X]

CHANGE 1: [Parameter name]
├─ Current value: [From strategy file]
├─ New value: [From research]
├─ Source: [URL]
├─ Confidence: [HIGH/MEDIUM/LOW]
└─ Reason: [Why this matters]

CHANGE 2: [Parameter name]
...

NO CHANGE NEEDED:
- [Parameter]: Still accurate per [source]
- [Parameter]: Still accurate per [source]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 3: Proposal

### Files That May Be Modified

Upon approval, the following files can be updated:

1. `{{CLIENT_WORKSPACE_ROOT}}\linkedin-core/references/LINKEDIN-OUTREACH-STRATEGY.md` (master strategy)
2. `{{CLIENT_WORKSPACE_ROOT}}\linkedin-daily-planner\SKILL.md`
3. `{{CLIENT_WORKSPACE_ROOT}}\linkedin-elite-post\SKILL.md`
4. `{{CLIENT_WORKSPACE_ROOT}}\linkedin-pro-commenter\SKILL.md`
5. `{{CLIENT_WORKSPACE_ROOT}}\linkedin-connect-timer\SKILL.md`
6. `{{CLIENT_WORKSPACE_ROOT}}\linkedin-icp-warmer\SKILL.md`
7. `{{CLIENT_WORKSPACE_ROOT}}\linkedin-icp-finder\SKILL.md`
8. `{{CLIENT_WORKSPACE_ROOT}}\linkedin-core\references\linkedin-strategy.md`

### Proposal Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHANGE PROPOSAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Changes found: [X]

CHANGE 1:
├─ Parameter: [Name]
├─ Current: [Value]
├─ Proposed: [New Value]
├─ Source: [URL]
├─ Confidence: [HIGH/MEDIUM/LOW]
├─ Impact: [Description of what this affects]
└─ Files to modify:
   - [File 1]: [Section to update]
   - [File 2]: [Section to update]

CHANGE 2:
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APPROVAL REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type "proceed" to apply ALL changes
Type "proceed 1,3" to apply specific changes (by number)
Type "skip" to cancel without changes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### CRITICAL: Wait for Approval

**DO NOT proceed to Phase 4 without explicit user approval.**

Valid approval responses:
- "proceed" - Apply all changes
- "proceed 1,3" - Apply only specified changes
- "yes" - Apply all changes
- "skip" - Cancel, no changes made

---

## Phase 4: Implementation

### Update Process

For each approved change:

1. **Read the target file** to find the exact section
2. **Edit the specific value** (not the entire file)
3. **Log the change** to algorithm-changes.md
4. **Confirm** the edit was successful

### Change Log Entry Format

Add to `{{CLIENT_WORKSPACE_ROOT}}\linkedin-core\shared\logs\algorithm-changes.md`:

```markdown
## [Date] - Algorithm Update

### Source
[URL of the source that prompted this change]

### Changes Made

| Parameter | Old Value | New Value | Files Modified |
|-----------|-----------|-----------|----------------|
| [Param 1] | [Old] | [New] | [file1.md, file2.md] |
| [Param 2] | [Old] | [New] | [file1.md] |

### Rollback Reference
If needed, restore these old values:
- [Parameter 1]: [Old value]
- [Parameter 2]: [Old value]

---
```

### Implementation Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHANGES APPLIED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files modified: [X]

1. linkedin-core/references/LINKEDIN-OUTREACH-STRATEGY.md
   └─ [Parameter]: [Old] → [New]

2. linkedin-daily-planner/SKILL.md
   └─ [Parameter]: [Old] → [New]

3. linkedin-pro-commenter/SKILL.md
   └─ [Parameter]: [Old] → [New]

Change log updated: linkedin-core/shared/logs/algorithm-changes.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ROLLBACK INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
If issues occur, old values are logged in:
linkedin-core/shared/logs/algorithm-changes.md

Or use git to revert:
git checkout HEAD~1 -- [file]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Execution Instructions

When triggered, execute this workflow:

### Step 1: Research Phase

```
1. Get current date to calculate 7-day window
2. Execute web searches using WebSearch tool:
   - "LinkedIn algorithm update January 2026"
   - "LinkedIn algorithm changes this week"
   - "360Brew algorithm update 2026"
   - "independent LinkedIn algorithm researcher LinkedIn 2026"
   - "LinkedIn reach changes 2026"
3. For each search result, extract:
   - The specific change mentioned
   - The source URL
   - The publication date
4. Filter for changes within last 7 days
5. Output Research Summary
```

### Step 2: Analysis Phase

```
1. Read linkedin-core/references/LINKEDIN-OUTREACH-STRATEGY.md
2. Extract current values for each parameter:
   - Post limits (Daily Limits section)
   - Comment rules (Engagement Strategy section)
   - Connection rules (Connection Request Strategy section)
   - Posting windows (Content Strategy section)
   - Golden Hour rules (Engagement Strategy section)
3. Compare research findings to current values
4. Identify discrepancies
5. Output Gap Analysis
```

### Step 3: Proposal Phase

```
1. For each identified gap:
   - Document current vs proposed value
   - Cite the source
   - Assess confidence level
   - List all files that contain this parameter
2. Output complete Proposal
3. STOP and wait for user approval
4. Do NOT proceed without explicit "proceed" response
```

### Step 4: Implementation Phase (Only After Approval)

```
1. For each approved change:
   - Read the target file
   - Locate the exact section with the parameter
   - Edit only the specific value
   - Verify the edit
2. Log all changes to algorithm-changes.md:
   - Date and source
   - Old and new values
   - Files modified
   - Rollback instructions
3. Output Implementation Summary
```

---

## No Changes Scenario

If research finds no algorithm updates:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN ALGORITHM SCAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Search period: [Date] to [Date] (7 days)
Sources checked: 7

RESULT: No significant algorithm changes detected

Your current strategy parameters remain valid:
- Post limit: 1-2/day (12h gap) ✓
- Comment limit: 30/day max ✓
- Comment length: 15-50 words ✓
- Connection limit: 15/day max ✓
- Golden Hour: 5-10 posts ✓
- Response boost: +35% within 1h ✓

Last confirmed: [Date]
Next recommended scan: [Date + 7 days]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Safety Rules

1. **Never auto-apply changes** - Always require explicit approval
2. **Always log old values** - Enable rollback if needed
3. **Verify sources** - Prioritize official LinkedIn announcements
4. **Conservative approach** - When uncertain, flag for manual review
5. **Single parameter edits** - Don't rewrite entire files

---

## Quality Checklist

**Research Phase:**
- [ ] All 7 search queries executed
- [ ] Results filtered to last 7 days
- [ ] Sources cited with URLs
- [ ] Publication dates noted

**Analysis Phase:**
- [ ] Current strategy file read
- [ ] All parameters compared
- [ ] Gaps clearly identified
- [ ] Confidence levels assigned

**Proposal Phase:**
- [ ] All changes documented
- [ ] Files to modify listed
- [ ] Impact described
- [ ] Waiting for explicit approval

**Implementation Phase:**
- [ ] Only approved changes applied
- [ ] Each edit verified
- [ ] Change log updated
- [ ] Rollback instructions provided
