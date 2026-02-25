# LinkedIn Activity Scan - Complete Guide

## Overview

This scanning system helps you efficiently identify ACTIVE and MODERATE prospects from 50 newly added LinkedIn profiles (rows #55-104 in icp-prospects.md). The goal is to focus algorithm training efforts on prospects who are actively posting on LinkedIn.

## Why Activity Status Matters

**ACTIVE prospects** (posted within 7 days) are:
- Currently engaging with their network
- More likely to see and respond to your engagement
- Best candidates for algorithm training
- Highest ROI for warming efforts

**MODERATE prospects** (posted 7-30 days ago) are:
- Secondary targets when ACTIVE pool is exhausted
- Still viable but lower priority
- May require more touches to warm up

**INACTIVE prospects** (no posts in 30+ days) are:
- Not worth warming effort
- Algorithm won't surface your content to them
- Better to skip and focus on active profiles

## Files Created

### 1. Activity Scan Checklist
**Location:** `{{CLIENT_WORKSPACE_ROOT}}\shared\logs\activity-scan-batch-30jan.md`

**Purpose:** Main working document for manual scanning

**Contains:**
- All 50 prospects with profile URLs
- Recent activity URLs pre-populated
- Checkboxes for activity classification
- Fields for last post date and notes
- Summary statistics section

**How to use:**
1. Open this file in your editor
2. Work through each prospect one by one
3. Visit their recent activity page
4. Check appropriate activity status box
5. Record last post date and any notes

### 2. Workflow Guide
**Location:** `{{CLIENT_WORKSPACE_ROOT}}\shared\logs\activity-scan-workflow.md`

**Purpose:** Step-by-step process guide

**Contains:**
- Setup instructions
- 5-step scanning process per prospect
- Keyboard shortcuts for efficiency
- Date reference guide (what "1w ago" means)
- Expected outcome statistics
- Troubleshooting tips

**How to use:**
1. Read once before starting
2. Keep open as reference during scanning
3. Follow the 5-step process for each prospect

### 3. PowerShell Profile Opener
**Location:** `{{CLIENT_WORKSPACE_ROOT}}\shared\scripts\open-linkedin-profiles.ps1`

**Purpose:** Automate opening LinkedIn profiles in batches

**Features:**
- Batch mode (10 profiles at a time)
- Custom range mode (specify row numbers)
- Single profile mode
- Pauses between batches for review

**How to use:**
```powershell
cd {{CLIENT_WORKSPACE_ROOT}}\shared\scripts
.\open-linkedin-profiles.ps1
```
Choose mode:
- **Recommended:** Batch mode (opens 10 profiles, pause, next 10, etc.)
- Custom range if you want specific rows
- Single profile for spot checks

### 4. CSV Results Template
**Location:** `{{CLIENT_WORKSPACE_ROOT}}\shared\logs\activity-scan-results-template.csv`

**Purpose:** Structured data capture for easy import

**Contains:**
- Pre-populated with all 50 prospect names and usernames
- Empty columns for Activity_Status, Last_Post_Date, Followers, Engagement_Score, Notes
- Ready to import into Excel or database

**How to use:**
1. Open in Excel or Google Sheets
2. Fill in data as you scan each prospect
3. Use for data analysis and filtering
4. Import results back into icp-prospects.md

## Recommended Workflow

### Option A: Fully Manual (Most Thorough)
1. Open `activity-scan-batch-30jan.md` in your editor
2. Open LinkedIn in browser
3. For each prospect:
   - Copy recent activity URL from checklist
   - Paste into browser
   - Check activity status
   - Record results in checklist
4. Update summary statistics when complete

**Time estimate:** 100-150 minutes (2-3 min per prospect)

### Option B: PowerShell-Assisted (Faster)
1. Run `open-linkedin-profiles.ps1`
2. Choose batch mode (10 profiles at a time)
3. Script opens 10 LinkedIn tabs
4. Review all 10 tabs quickly
5. Record results in checklist
6. Press any key for next batch

**Time estimate:** 60-90 minutes (1-2 min per prospect)

### Option C: CSV Export (Best for Analysis)
1. Open `activity-scan-results-template.csv` in Excel
2. Use PowerShell script for batch opening
3. Fill CSV as you review each prospect
4. Sort/filter by activity status when complete
5. Copy ACTIVE prospects to priority list

**Time estimate:** 60-90 minutes + analysis time

## Classification Rules

### ACTIVE
- Posted within last 7 days (23-30 Jan 2026)
- LinkedIn shows: "1d ago", "3d ago", "1w ago"
- These are your TOP priority targets

### MODERATE
- Posted 7-30 days ago (31 Dec 2025 - 22 Jan 2026)
- LinkedIn shows: "2w ago", "3w ago", "1mo ago"
- Secondary targets for warming

### INACTIVE
- No posts in 30+ days (before 31 Dec 2025)
- LinkedIn shows: "2mo ago", "1y ago", or "No posts yet"
- SKIP these prospects - not worth the effort

## Expected Results

Based on typical SME owner activity rates:

| Status | Expected Count | Percentage |
|--------|---------------|------------|
| ACTIVE | 5-10 | 10-20% |
| MODERATE | 8-13 | 15-25% |
| INACTIVE | 30-37 | 60-70% |

**Key Metric:** You should find 13-23 prospects worth warming (ACTIVE + MODERATE)

## After Scan Completion

### Immediate Actions
1. Count totals: ACTIVE, MODERATE, INACTIVE
2. Create prioritized list of ACTIVE prospects
3. Update Profile Cache in `icp-prospects.md`
4. Flag INACTIVE prospects to skip

### Profile Cache Update Format
For each prospect, add to Profile Cache table:

```
| # | Profile URL | Last Checked | Activity Status | Followers | Last Post | Recent Post URLs | Engagement Score |
|---|-------------|--------------|-----------------|-----------|-----------|------------------|------------------|
| 55 | /in/birch-sio-177164b/ | 30Jan 14:30 | ACTIVE | ~1K | 28Jan | URL1, URL2 | HIGH |
```

### Next Steps
1. Focus algorithm training on ACTIVE prospects only
2. Use linkedin-icp-warmer skill with ACTIVE prospect list
3. Reserve MODERATE prospects for later warming cycles
4. Remove INACTIVE prospects from daily workflow

## Troubleshooting

### "Profile shows limited activity"
- May be privacy settings or connection requirement
- Mark as "Unknown - requires connection"
- Lower priority, attempt connection first

### "LinkedIn rate limiting"
- Take 15-minute break
- Clear browser cookies
- Use incognito window
- Resume scanning

### "Can't find recent activity page"
- Profile may be restricted
- Try main profile URL instead
- Mark as "Activity hidden" in notes

### "Post dates are confusing"
- Use date reference guide in workflow document
- When in doubt, open the post to see exact date
- LinkedIn shows relative time ("2w ago"), not exact dates

## Data Quality Tips

### What to Record in Notes
- Follower count (approximate)
- Post frequency (e.g., "posts 2x per week")
- Content topics (e.g., "AI, leadership, SME growth")
- Engagement level (e.g., "posts get 50+ likes")
- Red flags (e.g., "all posts are job listings")

### Good vs. Bad ACTIVE Prospects

**Good ACTIVE Prospects:**
- Posts about business challenges, industry insights
- Genuine engagement with comments
- Mix of personal and professional content
- Followers in the 500-5K range

**Bad ACTIVE Prospects:**
- Only posts company news/job listings
- No engagement on posts (0-5 likes)
- Clearly automated/scheduled content
- Massively high follower count (spam/bot)

## Time Management

### Single Session (2-3 hours)
- Scan all 50 prospects in one go
- Use PowerShell batch mode
- Take 5-minute break every 15 prospects

### Multiple Sessions (30 min each)
- Session 1: Rows 55-64 (10 prospects)
- Session 2: Rows 65-74 (10 prospects)
- Session 3: Rows 75-84 (10 prospects)
- Session 4: Rows 85-94 (10 prospects)
- Session 5: Rows 95-104 (10 prospects)

### Best Times to Scan
- Morning (8-10am): Fresh mind, better attention to detail
- Afternoon (2-4pm): Good for routine tasks
- Avoid: Late evening when tired

## Success Metrics

After completing the scan, you should have:
- [ ] All 50 prospects classified (ACTIVE/MODERATE/INACTIVE)
- [ ] Last post date recorded for ACTIVE and MODERATE prospects
- [ ] Prioritized list of 5-10 ACTIVE prospects
- [ ] Updated Profile Cache in icp-prospects.md
- [ ] CSV export with all data (optional)
- [ ] Clear action plan for algorithm training

## Integration with Existing Skills

### linkedin-icp-warmer
- Use ACTIVE prospect list as input
- Automatically finds their recent posts
- Generates engagement comments
- Logs activity to shared activity log

### linkedin-daily-planner
- Morning Block: Feed Discovery + Algorithm Training
- Focus training on ACTIVE prospects only
- 3-day gap rule before re-engaging
- Auto-prioritizes based on activity status

### linkedin-connect-timer
- Only suggests connections for 2-3 touch prospects
- Factors in activity status (ACTIVE = higher priority)
- Recommends blank requests for 3+ touches on ACTIVE prospects

---

**Created:** 30 January 2026
**Purpose:** Activity scanning for rows #55-104 in icp-prospects.md
**Expected Duration:** 60-150 minutes depending on method
**Expected Output:** 13-23 viable prospects (ACTIVE + MODERATE)
