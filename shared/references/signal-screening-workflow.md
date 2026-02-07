# Signal Screening Cross-Check Workflow

Efficient multi-file workflow to avoid unnecessary steps when screening LinkedIn inbound signals.

## File Relationships

```
┌─────────────────────────────────────┐
│   NEW SIGNAL DETECTED               │
│   (Post reaction, comment, etc.)    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  STEP 1: linkedin-blacklist.md      │
│  grep "Contact Name"                │
└──────────────┬──────────────────────┘
               │
         FOUND?│
      ┌────────┴────────┐
      │ YES             │ NO
      ▼                 ▼
  ⛔ SKIP         Continue
  IMMEDIATELY          │
                       ▼
        ┌──────────────────────────────┐
        │  STEP 2: Profile Cache       │
        │  inbound-screening-history   │
        │  grep "Contact Name"         │
        └──────────────┬───────────────┘
                       │
                 FOUND?│
          ┌────────────┴─────────────┐
          │ YES                      │ NO
          ▼                          ▼
    Use Cached                  Go to STEP 4
    Classification              (Full screening)
          │
          │
    ┌─────┴──────────────┐
    │                    │
    │ PEER/TL/NON-ICP?  │ PROSPECT?
    │                    │
    ▼                    ▼
  SKIP              Continue
  (Evening Block)        │
                         ▼
          ┌─────────────────────────────┐
          │  STEP 3: icp-prospects.md   │
          │  grep "Contact Name"        │
          └──────────────┬──────────────┘
                         │
                   FOUND?│
          ┌──────────────┴────────────┐
          │ YES                       │ NO
          ▼                           ▼
    Check Last Touch           New PROSPECT
    Apply Gap Rules            (0 touches)
          │                           │
          │                           │
    ┌─────┴─────┐              Can engage
    │           │              (First touch)
    │ Too soon? │ OK?               │
    │           │                   │
    ▼           ▼                   │
  SKIP      Can engage              │
  (Gap rule) (Update touches)       │
                │                   │
                └───────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  ENGAGE WITH POST   │
              │  (Comment/Like/etc) │
              └─────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  UPDATE ALL FILES   │
              │  - Activity log     │
              │  - ICP prospects    │
              │  - Profile cache    │
              └─────────────────────┘
```

## Quick Reference: What Each File Does

### 1. linkedin-blacklist.md (VETO FILE)
**Purpose:** Absolute blocklist - never engage under any circumstances

**When to check:** ALWAYS FIRST, before any other checks

**What it tells you:** This contact is permanently blocked

**Action:** SKIP immediately, log as "Blacklisted"

**Update frequency:** Only when user explicitly adds someone

---

### 2. inbound-screening-history.md - Profile Cache (CLASSIFICATION FILE)
**Purpose:** Cache contact classifications to avoid re-screening

**When to check:** Before visiting LinkedIn profile

**What it tells you:**
- Classification: PROSPECT/PEER/THOUGHT LEADER/NON-ICP
- Location, followers, role
- Why they were classified that way

**Action:**
- PEER/THOUGHT LEADER/NON-ICP → SKIP in Evening Block
- PROSPECT → Check engagement rules (Step 3)
- Not found → Need full screening (Step 4)

**Update frequency:** After every new contact screening

---

### 3. icp-prospects.md (ENGAGEMENT TRACKER)
**Purpose:** Track prospect touch history and engagement timing

**When to check:** After confirming contact is PROSPECT (from cache or after screening)

**What it tells you:**
- Last Touch date (for gap rules)
- Total Touches (for 2-3 touch rule)
- Connection Status (for connected vs warming gap rules)
- Touch History (types of engagement)

**Action:**
- Check gap rules:
  - Connected + Last Touch < 7 days → SKIP (too recent)
  - Warming + Last Touch < 3 days → SKIP (too recent)
  - Otherwise → OK to engage
- After engagement → Update: Touches +1, Last Touch = today

**Update frequency:** After every prospect engagement

---

## Efficiency Comparison

### WITHOUT Cross-Checking (Old Way):
```
New Signal: "Sarah Chen reacted"
  → Visit LinkedIn profile (2-3 mins, 1 profile view)
  → Extract location, followers, role
  → Classify as PEER
  → Realize Evening Block = PROSPECT-only
  → SKIP

Result: Wasted 3 minutes + 1 profile view
```

### WITH Cross-Checking (New Way):
```
New Signal: "Sarah Chen reacted"
  → grep "sarah chen" blacklist (0.5 sec) → Not found ✅
  → grep "sarah chen" profile cache (0.5 sec) → Found: PEER
  → Evening Block = PROSPECT-only → SKIP

Result: 1 second, 0 profile views, same outcome
```

**Time saved:** 2-3 minutes per cached contact
**Profile views saved:** 1 per cached contact

### Cache Hit Rate Projection:
- **Week 1:** 0% cached (all new contacts)
- **Week 2:** ~30% cached (repeat engagers)
- **Week 4:** ~50% cached (regular community)
- **Month 3:** ~70% cached (stable community)

## Manual Cross-Check (Current Session)

When screening a new signal manually, follow this checklist:

```markdown
**New Signal:** [Contact Name]

**Step 1: Blacklist** ⛔
- [ ] `grep -i "[name]" linkedin-blacklist.md`
- Result: [ ] Not found (continue) / [ ] FOUND (SKIP)

**Step 2: Profile Cache** 🚀
- [ ] `grep -i "[name]" inbound-screening-history.md`
- Result: [ ] Not cached (continue) / [ ] Cached as [CLASSIFICATION]
- If cached as PEER/TL/NON-ICP: SKIP (Evening Block)
- If cached as PROSPECT: Continue to Step 3

**Step 3: ICP Prospects** 📊
- [ ] `grep -i "[name]" icp-prospects.md`
- Result: [ ] Not found (new prospect) / [ ] Found
- If found:
  - Last Touch: [date]
  - Days since: [X days]
  - Connection Status: [connected/pending/none]
  - Gap rule check: [ ] Too soon (SKIP) / [ ] OK (engage)

**Step 4: Full Screening** 🔍
- [ ] Visit LinkedIn profile
- [ ] Classify: [PROSPECT/PEER/TL/NON-ICP]
- [ ] Add to Profile Cache
- [ ] If PROSPECT: Add to icp-prospects.md
```

## Automated Cross-Check (Script)

Use the helper script for faster checking:

```bash
cd shared/scripts
./check-contact.sh "Sarah Chen"
```

Output will show results from all three files with recommended action.

---

## File Update Checklist

After engaging with a contact, update files in this order:

1. **linkedin-activity.md** (Daily activity log)
   - Add comment/engagement to appropriate table
   - Update Daily Limits Status

2. **icp-prospects.md** (If PROSPECT)
   - Update: Touches +1
   - Update: Last Touch = today
   - Update: Touch History append engagement type

3. **inbound-screening-history.md** (If new contact)
   - Add to Profile Cache section
   - Include: Name, Location, Classification, Profile Description, Screened Date

---

## Common Scenarios

### Scenario 1: Repeat Engager (PEER)
```
Signal: "Darryl WONG reacted to post"
→ Blacklist: Not found ✅
→ Cache: PEER (co-founder) ✅
→ Evening Block: PROSPECT-only
→ Action: SKIP (cached as PEER)
→ Time: 1 second
```

### Scenario 2: Known PROSPECT (Recent Touch)
```
Signal: "Sarah Chen commented"
→ Blacklist: Not found ✅
→ Cache: PROSPECT ✅
→ ICP Prospects: Last Touch = 2 days ago (warming, pending)
→ Gap Rule: Warming + < 3 days = Too soon
→ Action: SKIP (gap rule)
→ Time: 2 seconds
```

### Scenario 3: Known PROSPECT (Ready to Engage)
```
Signal: "John Tan liked post"
→ Blacklist: Not found ✅
→ Cache: PROSPECT ✅
→ ICP Prospects: Last Touch = 5 days ago, 1 touch, warming
→ Gap Rule: 5 days > 3 days = OK
→ Action: ENGAGE (find his posts, comment)
→ After: Update touches to 2, Last Touch = today
→ Time: Screening = 2 sec, Full workflow = 5-10 mins
```

### Scenario 4: Brand New Contact
```
Signal: "Emma Wong reacted"
→ Blacklist: Not found ✅
→ Cache: Not found ❌
→ Action: Full screening needed
→ Visit profile → Target geography, COO at target-sized company → PROSPECT ✅
→ Add to Cache + ICP Prospects (0 touches)
→ Find her posts → Comment → Update to 1 touch
→ Time: 10-15 minutes (full workflow)
```

---

## Monthly Maintenance

**Profile Cache Cleanup (Optional):**
- Review contacts cached >6 months ago
- If no recent engagement: Archive to separate file
- Keeps cache file manageable size

**ICP Prospects Cleanup:**
- Review prospects with 0 touches from >3 months ago
- Consider moving to "Stale Prospects" section
- Re-engagement campaign opportunity
