# Skill Updates Needed - Cross-Checking Workflow Integration

## Status: NOT YET UPDATED

The cross-checking workflow (`signal-screening-workflow.md`) has been created but NOT yet integrated into skill files.

---

## Skills Requiring Updates

### 1. linkedin-daily-planner/skill.md

**Location:** Line 449-480 (EVENING BLOCK section)

**Add BEFORE line 450 ("→ Run full inbound audit:"):**

```markdown
   EVENING BLOCK:
   → **THREE-FILE CROSS-CHECK (Efficiency System):**
     Reference: `shared/references/signal-screening-workflow.md`

     **For EACH inbound signal, check in this order:**

     1. **Blacklist Check (MANDATORY FIRST)** ⛔
        - `grep -i "contact name" shared/logs/linkedin-blacklist.md`
        - IF FOUND → SKIP IMMEDIATELY, log as "Blacklisted"
        - IF NOT FOUND → Continue to Step 2

     2. **Profile Cache Check (Skip Profile Visit)** 🚀
        - `grep -i "contact name" shared/logs/inbound-screening-history.md`
        - IF FOUND:
          * PEER/THOUGHT LEADER/NON-ICP → SKIP (Evening = PROSPECT-only)
          * PROSPECT → Continue to Step 3
        - IF NOT FOUND → Full screening needed (Step 4)

     3. **ICP Prospects Check (Engagement Gap Rules)** 📊
        - `grep -i "contact name" shared/logs/icp-prospects.md`
        - IF FOUND:
          * Check Last Touch date
          * Apply gap rules (connected: 7 days, warming: 3 days)
          * IF too soon → SKIP
          * IF OK → Can engage
        - IF NOT FOUND → New prospect (0 touches)

     4. **Full Profile Screening (Only if not cached)**
        - Visit LinkedIn profile
        - Extract location, followers, role
        - Classify: PROSPECT/PEER/THOUGHT LEADER/NON-ICP
        - Add to Profile Cache (inbound-screening-history.md)
        - If PROSPECT: Add to icp-prospects.md with 0 touches

     **Efficiency:** This workflow saves 70% of profile visits after 1 month of cache building.

   → Run full inbound audit:
     [existing content continues...]
```

**Also add at end of Evening Block (line 480, after "Update Daily Limits Status"):**

```markdown
   → **Update Signal Screening Log:**
     - Add day's screening results to `shared/logs/inbound-screening-history.md`
     - Add NEW contacts to Profile Cache section
     - Track PROSPECT vs PEER vs NON-ICP ratios for content strategy analysis
```

---

### 2. linkedin-icp-warmer/skill.md

**Location:** After "Step 0a: Cache-First Check" section

**Update the existing Cache-First Check section (around line 35-60) to reference:**

```markdown
### Step 0a: Cache-First Check (Minimize LinkedIn Visits)

**CRITICAL: Check Profile Cache before visiting ANY LinkedIn profile.**

**File location:** `shared/logs/inbound-screening-history.md` → Profile Cache table

**Cross-Check Workflow:** See `shared/references/signal-screening-workflow.md`

```
BEFORE VISITING PROSPECT PROFILE:
1. Check Blacklist FIRST:
   → grep -i "prospect name" shared/logs/linkedin-blacklist.md
   → IF FOUND: SKIP entirely, remove from warming pipeline

2. Check Profile Cache:
   → grep -i "prospect name" shared/logs/inbound-screening-history.md
   → IF FOUND + cached < 7 days + has Recent Post URLs:
     - USE CACHED DATA (skip profile visit)
     - Navigate directly to cached post URLs
     - Comment on fresh posts
   → IF NOT FOUND or cache stale:
     - Visit LinkedIn profile
     - Extract and cache: Location, followers, role, recent post URLs
     - Update Profile Cache in inbound-screening-history.md
     - Save file BEFORE proceeding
```

**When cache used:** Saved 2-3 minutes + 1 profile view (150/day limit)

**After 1 month:** 70% of prospects will be cached, dramatically reducing screening time.
```

---

### 3. linkedin-icp-finder/skill.md

**Location:** At the beginning of the main workflow, before profile screening

**Add new Step 0:**

```markdown
## Step 0: Pre-Screening Cross-Check (Efficiency Filter)

**Reference:** `shared/references/signal-screening-workflow.md`

Before screening ANY new contact, perform three-file cross-check:

### Blacklist Check (Mandatory)
```bash
grep -i "contact name" shared/logs/linkedin-blacklist.md
```

- **IF FOUND:** SKIP immediately, do not screen or engage
- **IF NOT FOUND:** Continue

### Profile Cache Check
```bash
grep -i "contact name" shared/logs/inbound-screening-history.md
```

- **IF FOUND:** Use cached classification
  - Already classified as PEER/PROSPECT/etc
  - Skip LinkedIn profile visit
  - Use cached data for classification output
- **IF NOT FOUND:** New contact, proceed with full screening

### ICP Prospects Check
```bash
grep -i "contact name" shared/logs/icp-prospects.md
```

- **IF FOUND:** Already tracked prospect
  - Note current touch count
  - Note last engagement date
  - Include in output with existing data
- **IF NOT FOUND:** New prospect, will be added after screening

**Efficiency Gain:** After 1 month, ~70% of contacts will be pre-classified, reducing redundant profile visits.

---

## Existing Workflow (Step 1+)
[Continue with existing ICP finder workflow...]
```

---

## Implementation Priority

1. **HIGH:** linkedin-daily-planner (most impactful - used daily in autonomous mode)
2. **MEDIUM:** linkedin-icp-warmer (frequent use, big efficiency gains)
3. **LOW:** linkedin-icp-finder (used less frequently, but still valuable)

---

## Testing Checklist

After updating each skill:

- [ ] linkedin-daily-planner updated
  - [ ] Evening Block references three-file cross-check
  - [ ] Autonomous mode uses blacklist/cache/prospects checks
  - [ ] Updates inbound-screening-history.md after screening

- [ ] linkedin-icp-warmer updated
  - [ ] Cache-first checking referenced
  - [ ] Blacklist check added before warming
  - [ ] Profile Cache updated after visits

- [ ] linkedin-icp-finder updated
  - [ ] Pre-screening cross-check added
  - [ ] Blacklist check prevents screening bad contacts
  - [ ] Uses cached classifications when available

---

## Validation

Run one full Evening Block screening session and verify:

1. **Blacklist blocks** blacklisted contacts immediately
2. **Profile Cache** prevents redundant profile visits for cached contacts
3. **ICP Prospects** gap rules prevent over-engagement
4. **All three files** are updated after screening

Expected result: **70% reduction in profile visits for repeat engagers** after 1 month of use.
