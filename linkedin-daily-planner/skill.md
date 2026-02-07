---
name: linkedin-daily-planner
description: Generate a daily LinkedIn outreach to-do list based on the 360Brew algorithm strategy. MORNING BLOCK ENHANCED - (1) Feed Discovery (find new prospects from feed), (2) Algorithm Training (visit profiles, follow, prime feed), (3) Hashtag Discovery (topic-based prospecting), (4) Standard engagement (Peers/Prospects/Thought Leaders). OTHER BLOCKS engage PROSPECT-only (Midday, Evening). Four modes - (1) AUTONOMOUS with "start linkedin" - runs full workflow without questions, AI auto-selects and executes all tasks; (2) CREATE plan with "plan my day", "daily linkedin plan"; (3) RESUME with "resume linkedin", "linkedin status"; (4) CHECK SCHEDULE with "what time block am I in", "when should I post". Determines current time block, executes tasks autonomously, trains algorithm to surface prospect content, logs to shared activity log.
---

# LinkedIn Daily Planner

Generate a structured daily outreach to-do list based on the 360Brew algorithm strategy. Integrates with all LinkedIn skills for seamless execution.

## Commenting Strategy by Time Block

**STANDARD ENGAGEMENT STRATEGY**

| Time Block | Who to Comment On | Target | Strategy |
|------------|-------------------|--------|----------|
| **Morning Block** | 3 PEER + 3 PROSPECT + 3 THOUGHT LEADER | 9 comments | Diverse warm-up (see Morning Block Strategy below) |
| **Midday Block** | PROSPECT posts ONLY | 5-10 comments | Golden Hour engagement (see PROSPECT-Only Strategy below) |
| **Afternoon Block** | PROSPECT posts ONLY (warming) | 3-5 comments | 2-3 Touch Rule warm-up (see PROSPECT-Only Strategy below) |
| **Evening Block** | PROSPECT posts ONLY (inbound) | 3-7 comments | Inbound signal follow-up (see PROSPECT-Only Strategy below) |

**Rationale:**
- **Morning Block (Diverse):** Warm topical relevance with balanced engagement across contact types before posting
- **Midday/Afternoon/Evening (PROSPECT-Only):** Focus on ICP pipeline building after content posted
- **Thought Leadership:** Built through YOUR posts (Content Block), not commenting on others
- **Efficiency:** Standardized finding methods for each contact type, clear fallback sequence

## Trigger

**Create new plan:**
- "plan my day"
- "daily linkedin plan"
- "linkedin to-do"
- "what should I do on linkedin today"
- "create my daily outreach plan"

**Resume existing plan:**
- "resume linkedin"
- "continue linkedin"
- "what's next on linkedin"
- "open my linkedin to-do"
- "linkedin status"
- "check my linkedin progress"

**Check schedule/timing:**
- "what time block am I in"
- "check my linkedin schedule"
- "when should I post"
- "what's the posting window"
- "linkedin timing"

**Autonomous execution:**
- "start linkedin"
- "run linkedin autonomously"
- "execute linkedin workflow"

## Browser Automation Setup

**LinkedIn skills require browser automation. Two options available:**

### Primary: Claude for Chrome

Use Claude for Chrome extension tools when available:
- `mcp__claude-in-chrome__tabs_context_mcp` - Get tab context
- `mcp__claude-in-chrome__navigate` - Navigate to URLs
- `mcp__claude-in-chrome__read_page` - Read page accessibility tree
- `mcp__claude-in-chrome__computer` - Click, type, scroll actions
- `mcp__claude-in-chrome__find` - Find elements by natural language

**Detection:** Call `mcp__claude-in-chrome__tabs_context_mcp` first. If it returns "Browser extension is not connected", fall back to DevTools.

### Fallback: Chrome DevTools

Use Chrome DevTools MCP server when Claude for Chrome is unavailable:
- `mcp__chrome-devtools__list_pages` - List open tabs
- `mcp__chrome-devtools__navigate_page` - Navigate to URLs
- `mcp__chrome-devtools__take_snapshot` - Get page snapshot (accessibility tree)
- `mcp__chrome-devtools__click` - Click elements by uid
- `mcp__chrome-devtools__fill` - Type into input fields

**Key Differences:**
- DevTools uses `uid` from snapshots for element selection (e.g., `uid=1_42`)
- DevTools requires `take_snapshot` before interacting with elements
- DevTools requires explicit page selection with `select_page` when switching tabs

**Tool Mapping:**

| Claude for Chrome | Chrome DevTools Equivalent |
|-------------------|----------------------------|
| `tabs_context_mcp` | `list_pages` |
| `navigate` | `navigate_page` |
| `read_page` | `take_snapshot` |
| `computer` (click) | `click` (with uid) |
| `computer` (type) | `fill` (with uid) |
| `find` | Parse `take_snapshot` output |

**Workflow Pattern (DevTools):**
```
1. list_pages → Get available tabs/pages
2. navigate_page → Go to LinkedIn URL
3. take_snapshot → Get page structure with uids
4. click/fill → Interact with elements by uid
5. Repeat steps 3-4 as needed
```

## Profile Cache Strategy

**Purpose:** Minimize LinkedIn profile visits by caching recent post URLs locally (7-day TTL).

### Cache Location

`shared/logs/icp-prospects.md` → **Profile Cache** table (separate from Main Prospects table)

### Cache Structure

```markdown
| # | Profile URL | Last Checked | Activity Status | Followers | Last Post | Recent Post URLs | Engagement Score |
|---|-------------|--------------|-----------------|-----------|-----------|------------------|------------------|
| 37 | /in/name/ | 28Jan 08:14 | ACTIVE | 3K | 27Jan | url1, url2, url3 | HIGH |
```

### How to Extract Post URLs from Snapshot

When visiting a prospect's activity page (`/in/{profile-path}/recent-activity/all/`):

**Step 1: Take snapshot**
```
snapshot = take_snapshot()
```

**Step 2: Search snapshot for post URLs**

Look for lines containing: `url="https://www.linkedin.com/feed/update/urn:li:activity:XXXXXXXXXXXXX/"`

**Example snapshot output:**
```
uid=52_404 link "Post content preview..." url="https://www.linkedin.com/feed/update/urn:li:activity:7421711052880642048/"
uid=52_405 link "Another post preview..." url="https://www.linkedin.com/feed/update/urn:li:activity:7420261502747811841/"
```

**Step 3: Extract URLs using grep or parsing**

```bash
# Save snapshot to temp file
echo "$snapshot" > temp_snapshot.txt

# Extract post URLs (up to 3 most recent)
grep -o 'url="https://www.linkedin.com/feed/update/urn:li:activity:[^"]*' temp_snapshot.txt | \
  sed 's/url="//' | \
  head -3
```

**Step 4: Determine Activity Status**

Based on snapshot content:
- Look for post date indicators (e.g., "1 week ago", "2 days ago", "3 hours ago")
- **ACTIVE** = Posted within last 7 days
- **MODERATE** = Posted 7-30 days ago
- **INACTIVE** = No posts in 30+ days → **SKIP this prospect**

**Step 5: Extract Follower Count**

Look for pattern: `"X followers"` or `"X,XXX followers"` in snapshot

**Step 6: Update Profile Cache IMMEDIATELY**

```markdown
| 37 | /in/prospect-name/ | 28Jan 08:14 | ACTIVE | 3K | 27Jan | https://...url1, https://...url2, https://...url3 | HIGH |
```

Save `icp-prospects.md` **before** proceeding to comment.

### Cache Usage Decision Tree

```
Check Profile Cache for prospect:

IF Last Checked < 7 days AND has Recent Post URLs:
  → USE CACHE (skip profile visit)
  → Navigate directly to cached URLs
  → Update "Last Checked" = today (extends cache freshness)
  → Comment on fresh posts

ELSE IF Last Checked >= 7 days OR no Recent Post URLs:
  → REFRESH CACHE (visit profile)
  → Extract post URLs from snapshot
  → Update entire cache row
  → Save file
  → Comment on first post

IF Activity Status = INACTIVE:
  → SKIP entirely (don't waste time on inactive prospects)
```

### ROI: Time Savings

- **Without cache:** 2-3 minutes per prospect (profile visit + scroll + find post)
- **With cache:** 45 seconds per prospect (direct URL navigation)
- **Efficiency gain:** 60% time reduction on prospect engagement

## Autonomous Workflow

When user triggers autonomous mode ("start linkedin"):

**AUTONOMOUS MODE RULES:**
- ❌ Do NOT ask which task to start - execute in order
- ❌ Do NOT ask user to select variations - AI auto-selects
- ❌ Do NOT wait for confirmation - proceed automatically
- ✅ Execute all tasks for current time block
- ✅ Use browser automation (Claude for Chrome or DevTools fallback)
- ✅ Log everything to shared activity log
- ✅ Move to next task immediately after completion
- ✅ Use sub-agents for research tasks to save tokens (see Sub-Agent Optimization below)

### 🚀 SUB-AGENT OPTIMIZATION (Token Efficiency)

**Purpose:** Offload research-heavy tasks to sub-agents to reduce main context token usage by ~66%.

**When to use sub-agents:**
- File analysis tasks (filtering large prospect lists)
- Batch duplicate checking
- Feed classification tasks
- Cross-file validation
- Metrics calculation

**Sub-agent types available:**
- `Explore` - For research, file reading, filtering (most common)
- `Haiku` - For quick calculations, simple checks (faster, cheaper)

#### MORNING BLOCK Sub-Agents

**1. Prospect Cache Analysis** (saves ~35K tokens)
```
Task (Explore): "Read shared/logs/icp-prospects.md and return ONLY prospects matching:
- Last Touch > 7 days (or > 3 days if Connection Status != 'connected')
- Activity Status = 'ACTIVE'
- Has Recent Post URLs in cache
- NOT on blacklist (check shared/logs/linkedin-blacklist.md)
Return max 5 as JSON: [{name, profile_url, post_urls, last_touch, touches}]"
```

**2. Feed Classification** (saves ~5K tokens)
```
Task (Explore): "Analyze this feed snapshot and classify each post author:
- PROSPECT: ICP match (read criteria from `references/icp-profile.md`)
- PEER: 1K-10K followers, AI/automation niche
- THOUGHT LEADER: 10K+ followers
Return categorized list: {prospects: [], peers: [], thought_leaders: []}
Include: author name, post preview (50 chars), follower count estimate"
```

**3. Batch Duplicate Check** (saves ~10K tokens)
```
Task (Explore): "Check shared/logs/linkedin-activity.md for these authors: [list]
Return which ones are SAFE to engage (not commented in last 30 days)
Format: {safe: [names], skip: [{name, last_commented, reason}]}"
```

**4. Unfollowed 0-Touch Prospect Filter** (saves ~35K tokens)
```
Task (Explore): "Read shared/logs/icp-prospects.md and return unfollowed 0-touch prospects:
Filter criteria:
- Touches = 0 (never engaged)
- Notes does NOT contain 'Followed' (not yet followed)
- NOT on blacklist (check shared/logs/linkedin-blacklist.md)

Sort by Date Found (oldest first - FIFO)
Return max 15 as JSON: [{name, profile_url, date_found, notes}]"
```

**5. INACTIVE Comment Check Rotation Filter** (saves ~35K tokens)
```
Task (Explore): "Read shared/logs/icp-prospects.md and return INACTIVE prospects due for comment check:
Filter criteria:
- Notes contains 'INACTIVE' (flagged as inactive poster)
- Notes does NOT contain 'Comment Check' with a date within the last 14 days
- NOT on blacklist (check shared/logs/linkedin-blacklist.md)

Sort by Date Found (oldest unchecked first)
Return max 5 as JSON: [{name, profile_url, date_found, notes, last_comment_check}]"
```

#### CONTENT BLOCK Sub-Agents

**4. 12-Hour Rule Check** (saves ~5K tokens)
```
Task (Haiku, model=haiku): "Read shared/logs/linkedin-activity.md
Find the most recent entry in 'Posts Published' table
Calculate hours since that timestamp
Return: {can_post: bool, hours_since_last: X, next_valid_time: timestamp}"
```

**5. Trending Topic Analysis** (saves ~15K tokens)
```
Task (Explore): "Analyze feed for trending topics suitable for your niche positioning (from `references/icp-profile.md`).
Filter for: 50+ reactions, individual authors (not company pages), AI/automation/business topics
Return top 3: [{topic, author, reactions, comments, sme_angle_suggestion}]"
```

#### MIDDAY/AFTERNOON BLOCK Sub-Agents

**6. Touch Conversion Filter** (saves ~30K tokens)
```
Task (Explore): "Read shared/logs/icp-prospects.md and find prospects ready for touch conversion:
- 0→1 conversion: Touches=0, Activity Status=ACTIVE, has posts
- 1→2 conversion: Touches=1, Last Touch > 3 days, Connection Status='none'
Return prioritized list (max 5 each): {zero_touch: [], one_touch: []}
Include: name, profile_url, cached_post_urls, date_found"
```

**7. DM Research** (saves ~15K tokens - run in background)
```
Task (Explore, run_in_background=true): "Research these 3 PROSPECT connections for Value DMs:
[names and profile URLs]
For each, find: recent posts, profile highlights, previous comment interactions
Return DM context: [{name, recent_topic, shared_interest, dm_hook_suggestion}]"
```

#### EVENING BLOCK Sub-Agents

**8. Three-File Cross-Check** (saves ~50K tokens)
```
Task (Explore): "Cross-check these inbound signals against 3 files:
Signals: [list of names/profile URLs from notifications]

Check order:
1. shared/logs/linkedin-blacklist.md → If found, mark SKIP
2. shared/logs/inbound-screening-history.md → If found, use cached classification
3. shared/logs/icp-prospects.md → Check gap rules (7 days connected, 3 days warming)

Return: [{name, classification, action, reason}]
Classifications: PROSPECT/PEER/THOUGHT_LEADER/NON_ICP/BLACKLISTED"
```

**9. Daily Metrics Calculation** (saves ~10K tokens)
```
Task (Haiku, model=haiku): "Read shared/logs/linkedin-activity.md
Calculate today's totals: comments, connections, DMs, likes, profile views
Return formatted Daily Limits Status table with remaining counts"
```

#### Sub-Agent Execution Pattern

```
BLOCK START:
    ↓
    ├── Launch research sub-agents (parallel where possible)
    │   ├── Task (Explore) → Prospect filtering
    │   ├── Task (Explore) → Duplicate checking
    │   └── Task (Haiku) → Quick calculations
    │
    ├── WAIT for sub-agent results (they return summarized data)
    │
    └── Main thread → Execute browser actions with pre-filtered targets
        (No need to read large files - sub-agents already did filtering)
```

#### Token Savings Summary

| Block | Without Sub-Agents | With Sub-Agents | Savings |
|-------|-------------------|-----------------|---------|
| Morning | ~60K tokens | ~20K tokens | 67% |
| Content | ~25K tokens | ~10K tokens | 60% |
| Midday | ~45K tokens | ~15K tokens | 67% |
| Afternoon | ~55K tokens | ~20K tokens | 64% |
| Evening | ~80K tokens | ~25K tokens | 69% |
| **Daily Total** | ~265K tokens | ~90K tokens | **66%** |

#### When NOT to Use Sub-Agents

- Browser automation tasks (must run in main thread)
- Sequential dependent operations
- Tasks requiring immediate user interaction
- Simple single-file reads (overhead not worth it)

### ⚠️ TASK COMPLETION ENFORCEMENT (MANDATORY)

**CRITICAL: Do NOT stop until ALL tasks for the current block are completed.**

This enforcement rule prevents premature termination of autonomous workflows. The AI must complete every task in the current block before stopping or reporting completion.

**ENFORCEMENT RULES:**

1. **NO EARLY EXITS:** Do not stop execution after completing one task. Check if there are remaining tasks in the current block.

2. **TASK LIST TRACKING:** After completing each task:
   - Mark it complete in the to-do file
   - Check: "Are there more tasks in this block?"
   - If YES → Execute next task immediately
   - If NO → Block is complete, report summary

3. **BLOCK COMPLETION CHECKLIST:**
   ```
   MORNING BLOCK:
   [ ] Feed Discovery (2-3 prospects)
   [ ] Algorithm Training (5-7 profiles + 10-20 lookalike prospects discovered)
   [ ] Bulk Follow Sprint (10-15 unfollowed 0-touch prospects)
   [ ] 0-Touch Warming Sprint (3 prospects)
   [ ] INACTIVE Comment Monitor (5 prospects' comment tabs checked)
   [ ] Standard Engagement (9 comments: 3+3+3)
   → Only report "MORNING BLOCK COMPLETE" when ALL boxes are checked

   CONTENT BLOCK:
   [ ] 12-Hour Rule checked
   [ ] Trending topic found (or backup used)
   [ ] Post generated
   [ ] Image generated (if needed)
   [ ] Post scheduled
   → Only report "CONTENT BLOCK COMPLETE" when ALL boxes are checked

   MIDDAY BLOCK:
   [ ] Comment replies processed
   [ ] 5-10 PROSPECT engagements
   → Only report "MIDDAY BLOCK COMPLETE" when ALL boxes are checked

   AFTERNOON BLOCK:
   [ ] Connection acceptances checked
   [ ] Value DMs sent (to PROSPECT connections only)
   [ ] 0-1 touch prospects warmed
   [ ] Connection requests sent (2+ touch only)
   [ ] NEW prospects discovered (linkedin-icp-finder)
   → Only report "AFTERNOON BLOCK COMPLETE" when ALL boxes are checked

   EVENING BLOCK:
   [ ] Three-file cross-check executed
   [ ] Inbound signals screened
   [ ] ICP matches saved
   [ ] Bulk Follow progress tracked (X/203 prospects followed)
   [ ] INACTIVE Comment Monitor progress tracked (X prospects checked today, Y COMMENT_ACTIVE found)
   [ ] Daily metrics logged
   [ ] Weekly metrics updated (if Friday)
   → Only report "EVENING BLOCK COMPLETE" when ALL boxes are checked
   ```

4. **PARTIAL COMPLETION HANDLING:**
   - If a task cannot be completed (e.g., no qualifying prospects found), log the reason and proceed to next task
   - "Partial completion" is acceptable ONLY if:
     * Task was attempted with multiple strategies
     * Reason for non-completion is logged
     * All OTHER tasks in the block ARE completed
   - NEVER stop at a partial task without attempting remaining tasks

5. **BLOCK TRANSITION RULE:**
   - After completing ALL tasks in a block, check if user requested multiple blocks
   - If user said "start linkedin" with no time qualifier → Execute current block only, then report
   - If user specified "run full day" → Continue to next block
   - Always report which block(s) were completed

6. **RESUMPTION AFTER INTERRUPTION:**
   - If session was interrupted (context limit, error, etc.), on resume:
     * Read to-do file → Find incomplete tasks
     * Continue from FIRST incomplete task
     * Complete remaining tasks before reporting

**ENFORCEMENT OUTPUT:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[BLOCK NAME] TASK PROGRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task 1: [Description] - COMPLETE
✅ Task 2: [Description] - COMPLETE
⏳ Task 3: [Description] - IN PROGRESS
⬜ Task 4: [Description] - PENDING
⬜ Task 5: [Description] - PENDING

Progress: 2/5 tasks complete
Status: CONTINUING...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**VIOLATION DETECTION:**
If you catch yourself about to stop before all tasks are done, ask:
1. "Have I completed ALL tasks listed for this block?"
2. "Are there pending tasks I haven't attempted?"
3. "Did I skip any task without logging a valid reason?"

If any answer is NO → Continue execution until complete.

### Autonomous Execution Flow

```
1. Determine current time block (based on system time)

2. LAUNCH SUB-AGENTS FOR RESEARCH (Token Optimization)
   ┌─────────────────────────────────────────────────────────────────┐
   │ Launch these sub-agents IN PARALLEL at block start:            │
   │                                                                 │
   │ Task (Explore) → "Prospect Cache Analysis"                     │
   │   - Filter icp-prospects.md for qualifying prospects           │
   │   - Returns: pre-filtered list (5-10 prospects max)            │
   │                                                                 │
   │ Task (Explore) → "Batch Duplicate Check"                       │
   │   - Check activity log for recent engagements                  │
   │   - Returns: safe-to-engage list                               │
   │                                                                 │
   │ Task (Haiku) → "Daily Limits Check"                            │
   │   - Calculate remaining limits from activity log               │
   │   - Returns: {comments: X/30, connections: X/15, ...}          │
   │                                                                 │
   │ ⏱️ Wait for all sub-agents to return (typically <30 seconds)   │
   │ 📉 Token savings: ~50K by not loading full files into context  │
   └─────────────────────────────────────────────────────────────────┘

3. QUICK READS (Small files only - sub-agents handle large files)
   3a. Read `shared/linkedin-account-config.md` → Get account type (small file)
   3b. Read `references/autonomous-optimization.md` → Auto-selection logic (if needed)
   3c. Read `references/evergreen-topics.md` → Backup content (if Content Block)

4. Read/create today's to-do file

5. BLACKLIST CHECK (Via sub-agent results)
   - Sub-agent already filtered out blacklisted contacts
   - Double-check before ANY engagement action
   - If contact is blacklisted → SKIP entirely, move to next contact
6. For current block, execute each pending task WITH LIMIT CHECKS:

   CACHE-FIRST RULE (applies to ALL blocks):
   → Before visiting ANY LinkedIn profile:
     - Check Profile Cache table in icp-prospects.md for prospect
     - If Last Checked < 7 days AND has Recent Post URLs → USE CACHE (skip profile visit)
     - If Activity Status = INACTIVE → SKIP prospect entirely (no point engaging if they don't post)
     - Only visit LinkedIn profile if cache is stale (>7 days) or missing
   → **After visiting LinkedIn profile (MANDATORY - before commenting):**
     - Take snapshot of activity page
     - Parse snapshot to extract:
       * 1-3 recent post URLs (feed/update/urn:li:activity:XXXXX format)
       * Follower count
       * Last post date
       * Activity status (ACTIVE if posted <7 days, MODERATE if 7-30 days, INACTIVE if 30+ days)
       * **Connection Status (MANDATORY):** Check for "Message" button = connected, "Follow"/"Connect" button = none, "Pending" = pending
     - **IMMEDIATELY update Profile Cache table with extracted data**
     - **IMMEDIATELY update Connection Status column** if observed status differs from stored value
     - Save icp-prospects.md file
     - THEN proceed to comment on first post

   → **CONNECTION STATUS OBSERVATION RULE (applies to ALL profile visits):**
     - **Every time you visit ANY prospect's LinkedIn profile for ANY reason** (Bulk Follow, Algorithm Training, commenting, warming, screening):
       * Observe the primary action button: "Message" = connected, "Follow"/"Connect" = none, "Pending" = pending
       * Compare with stored Connection Status in icp-prospects.md
       * If different: **UPDATE IMMEDIATELY** before proceeding with the task
     - This prevents stale Connection Status data from accumulating
     - This saves future sessions from redundant profile checks
   → **When using fresh cache (no profile visit):**
     - Update "Last Checked" timestamp to today (extends cache freshness)
     - Keeps 7-day rolling window active

   MORNING BLOCK:
   → CHECK: Comments today < 30 limit? If not, skip commenting
   → **⚠️ DUPLICATE CHECK RULE (MANDATORY - SEE FULL PROTOCOL ABOVE):**
     - **EXECUTE FULL DUPLICATE CHECK PROTOCOL** before EVERY comment
     - Check 1: grep -i "author_name" shared/logs/linkedin-activity.md
     - Check 2: grep -i "urn:li:activity:POST_ID" shared/logs/linkedin-activity.md
     - Check 3: grep -i "topic_keyword" shared/logs/linkedin-activity.md (if similar topic within 7 days)
     - If ANY check returns match: **SKIP THIS POST IMMEDIATELY**
     - See "MANDATORY DUPLICATE CHECK PROTOCOL" section above for full decision tree
     - ONLY re-engage if there's a REPLY to your comment (check notifications)
   → **PROSPECT ENGAGEMENT TRACKING (CRITICAL):**
     - After commenting on ANY prospect's post:
       * Update icp-prospects.md → Find this prospect by name
       * Update "Last Touch" = today's date
       * Update "Touches" = increment by +1
       * Update "Touch History" = append "comment"
     - Before commenting on a prospect:
       * Check icp-prospects.md → Last Touch date AND Connection Status
       * **NEW GAP RULES:**
         - If Connection Status = "connected" AND Last Touch < 7 days ago: SKIP (too recent for connected)
         - If Connection Status = "none" or "pending" AND Last Touch < 3 days ago: SKIP (too recent for warming)
         - If Last Touch >= 3 days (warming) or >= 7 days (connected): OK to engage
       * Find different prospect if too recent
     - **All future engagement with this prospect = linkedin-icp-warmer process**
     - This prevents over-engagement while enabling faster warming (3-day cycle vs 7-day)
   → **SCAN Sales Navigator notifications (if account = SALES_NAVIGATOR):**
     - Navigate to Sales Navigator notifications
     - Check for posts from last 24 hours
     - Screen each author against ICP criteria (from `references/icp-profile.md`)
     - For ICP matches:
       * **⚠️ EXECUTE MANDATORY DUPLICATE CHECK** (grep author + post URL in activity log)
       * If YES: SKIP, move to next
       * Save to icp-prospects.md if not already there
       * Navigate to full LinkedIn post
       * **LIKE the post** (click Like/reaction button)
       * Generate comment using linkedin-pro-commenter
         - AUTO-SELECT using weighted algorithm (see autonomous-optimization.md)
         - If all comments score <40 → Regenerate with "make more specific and concise"
       * Click into comment field, type comment text
       * **CLICK "Post" button to submit** (DO NOT skip this step)
       * Wait for confirmation comment posted
       * Update touches and last touch in icp-prospects.md
       * Update daily limits: Comments +1
     - Log all new ICPs and comments to shared activity log
   **═══════════════════════════════════════════════════════════════**
   **MORNING BLOCK STANDARD STRATEGY: 9 Comments (Diverse Engagement)**
   **═══════════════════════════════════════════════════════════════**

   **🎯 TARGET: 3 PEER + 3 PROSPECT + 3 THOUGHT LEADER = 9 comments**
   **⏱️ TIME: 25-30 minutes total (including discovery & algorithm training)**
   **📊 GOAL: Discover prospects + Train algorithm + Warm topical relevance**

   **EXECUTION SEQUENCE:**

   **═══════════════════════════════════════════════════════════════**
   **NEW: DISCOVERY & ALGORITHM TRAINING (First 10 minutes)**
   **═══════════════════════════════════════════════════════════════**

   **─── STEP 0A: Feed Discovery (5 minutes) ───**

   **PURPOSE:** Discover NEW prospects directly from feed while engaging

   1. Navigate to LinkedIn feed (home page)
   2. Scan first 10-15 posts visible without scrolling
   3. For each post, quick ICP filter:
      ✓ Author from your target geography (from `references/icp-profile.md`) - MANDATORY
      ✓ Decision-maker role (from `references/icp-profile.md`)
      ✓ Target market size signals in headline (from `references/icp-profile.md`)
      ✓ Post discusses pain points or challenges
   4. Identify 2-3 HIGH FIT prospects (stop when found)
   5. For each prospect found:
      → Blacklist check (skip if blacklisted)
      → Duplicate check (skip if already commented)
      → Like post
      → Generate comment (linkedin-pro-commenter)
      → Post comment
      → Add to icp-prospects.md:
        * Source = "Feed Discovery"
        * Algorithm Trained = ⏳ PENDING
        * Touches = 1
        * Last Touch = today + "comment"
      → Log to shared activity log
      → Update daily limits: Comments +1
   6. **TIME LIMIT:** Stop at 5 minutes even if <3 prospects found

   **FALLBACK:** If feed has <2 ICP prospects, skip to Step 0B immediately

   **─── STEP 0B: Algorithm Training (5 minutes) ───**

   **PURPOSE:** Train LinkedIn to surface prospect content in feed

   1. Read icp-prospects.md → Filter for:
      ✓ Algorithm Trained = ❌ NO or ⏳ PENDING
      ✓ Priority: Connection Status = "connected" > Touches >=2 > Touches <2
   2. Select 5-7 prospects to train (prioritize HIGH fit)
   3. For each prospect:
      → Navigate to profile URL
      → Scroll profile slowly (30-45 seconds dwell time)
      → Check Following status:
        * If NOT following → Click "Follow" button
      → Bell notifications (HIGH priority only - skip for most):
        * Only if: Connected + High-value + Active poster
        * Click bell icon → Select "All"
      → Navigate to recent activity (/recent-activity/all/)
      → Save 1-2 most recent posts (bookmark icon)
      → **Email Extraction (if connected):**
        * Click "Contact info" button on profile
        * If email visible → Capture email address
        * Check About section for email patterns
        * If Company URL visible → Note for later website check
      → **Profile Recommendations Harvesting (NEW - High Priority):**
        * Scroll to right sidebar on profile page
        * Look for "More profiles for you" OR "People you may want to know"
        * For each recommended profile (scan 3-5 recommendations):
          → Extract: Name, Role, Company, Location, Profile URL
          → Quick ICP check (decision-maker role + target market + target geography + relevant industry — from `references/icp-profile.md`)
          → If QUALIFIED:
            * Check NOT in icp-prospects.md already (scan by name)
            * Check NOT in linkedin-blacklist.md
            * Add to prospects_to_add queue (batch save at end)
            * Source = "LinkedIn Profile Rec from [Current Prospect Name]"
        * Result: 2-4 new qualified prospects per training session (10-20 per morning block)
      → Update icp-prospects.md:
        * Algorithm Trained = ✅ YES
        * Last Trained = today
        * Email = [captured email or keep TBD]
        * Notes += "Followed" (or "Followed + Bell ON")
        * Notes += "Email captured [date]" (if email found)
      → Wait 10-15 seconds (appear human)
   4. Log training session to shared activity log:
      → Section: "Algorithm Training"
      → List prospects trained
      → Actions: Follow/Bell/Save counts
   5. **TIME LIMIT:** Stop at 5 minutes (train 5-7 prospects max)
   6. **BATCH SAVE NEW PROSPECTS (from recommendations):**
      → Read prospects_to_add queue
      → For each new prospect:
        * Add row to icp-prospects.md table
        * Include: Name, Date Found (today), Role, Company, Location
        * Classification = PROSPECT
        * Touches = 0
        * Source = "LinkedIn Profile Rec from [Seed Prospect]"
        * Assign ICP Score based on fit (70-90 range)
      → Save icp-prospects.md
      → Log to activity log: "Discovered X new prospects via profile recommendations"

   **RESULT:**
   - Within 2-4 weeks, feed will be dominated by trained prospect content
   - 10-20 new qualified prospects added to pipeline per morning block
   - Lookalike network effect compounds over time

   **─── STEP 0C: Hashtag Discovery (OPTIONAL - 5 minutes) ───**

   **PURPOSE:** Find prospects discussing specific topics

   **USE WHEN:** Feed Discovery found <2 prospects OR weekly deep dive

   **Hashtag rotation (daily):**
   ```
   Read hashtag rotation from `references/linkedin-strategy.md`
   Monday: [hashtag 1]
   Tuesday: [hashtag 2]
   Wednesday: [hashtag 3]
   Thursday: [hashtag 4]
   Friday: [hashtag 5]
   ```

   1. Navigate to LinkedIn search:
      ```
      https://www.linkedin.com/search/results/content/?keywords=%23[today's hashtag]
      ```
   2. Filter: "Posts" + "Past 24 hours"
   3. Scan first 10-15 posts
   4. For each post, quick ICP filter (same as Feed Discovery)
   5. Identify 1-2 HOT prospects (specific pain signals in post)
   6. For each:
      → Blacklist + Duplicate check
      → Like post
      → Generate comment (reference their specific pain point)
      → Post comment
      → Visit author profile:
        * Follow them (algorithm training)
        * Save 1-2 recent posts
      → Add to icp-prospects.md:
        * Source = "Hashtag: #[tag]"
        * Algorithm Trained = ✅ YES (profile visited + followed)
        * Touches = 1
        * Last Touch = today + "comment on #[tag] post"
        * Notes = "Pain: [specific challenge mentioned]"
      → Update Profile Cache
      → Log to shared activity log
      → Update daily limits: Comments +1
   7. **TIME LIMIT:** Stop at 5 minutes

   **─── STEP 0D: Bulk Follow Sprint (5 minutes) ───**

   **PURPOSE:** Follow every 0-touch prospect so their posts appear in your feed automatically. LinkedIn does the monitoring for you - no need to manually check profiles.

   **WHY THIS IS SEPARATE FROM ALGORITHM TRAINING:**
   - Algorithm Training (Step 0B) = Full profile visit + save posts + harvest recommendations (5-7 profiles)
   - Bulk Follow Sprint = FAST follow-only pass: visit profile, click Follow, move on (10-15 profiles)
   - At 10-15/day, all 200+ prospects followed within ~15 days

   **🚀 USE SUB-AGENT FOR PROSPECT FILTERING:**
   ```
   Task (Explore): "Read shared/logs/icp-prospects.md and return unfollowed 0-touch prospects:
   Filter criteria:
   - Touches = 0 (never engaged)
   - Notes does NOT contain 'Followed' (not yet followed)
   - NOT on blacklist (check shared/logs/linkedin-blacklist.md)

   Sort by Date Found (oldest first - FIFO)
   Return max 15 as JSON: [{name, profile_url, date_found, notes}]"
   ```

   **EXECUTION:**
   1. Sub-agent returns filtered unfollowed prospects
   2. Select 10-15 from returned list
   3. For each prospect:
      → Navigate to profile URL
      → Click "Follow" button (if not already following)
      → DO NOT: save posts, scroll profile, harvest recommendations (that's Algorithm Training)
      → Update icp-prospects.md Notes: append "Followed [date]"
      → Wait 3-5 seconds (appear human)
      → Move to next profile immediately
   4. Log to shared activity log: "Bulk Follow Sprint: Followed X prospects"

   **TIME LIMIT:** 5 minutes strict. Move fast - this is a volume play.
   **DAILY TARGET:** 10-15 follows
   **COMPLETION TARGET:** All 0-touch prospects followed within ~15 days

   **SKIP THIS STEP IF:**
   - All 0-touch prospects already have "Followed" in Notes
   - Sub-agent returns 0 unfollowed prospects

   **═══════════════════════════════════════════════════════════════**
   **🔥 PRIORITY: 0-TOUCH WARMING SPRINT (5 minutes) - BEFORE Standard Engagement**
   **═══════════════════════════════════════════════════════════════**

   **PURPOSE:** Clear the 0-touch backlog before discovering more prospects.

   **WHY THIS MATTERS:** Pipeline analysis shows 64% of prospects stuck at 0-touch.
   Discovery without warming creates a top-heavy pipeline that never converts.

   **RATIO RULE: 70% Warming / 30% Discovery**
   - Until 0-touch backlog < 10 prospects, prioritize warming over discovery
   - Only add 2-3 new prospects per day (not 5-10)
   - Focus energy on moving existing prospects through the funnel

   **EXECUTION (Sub-Agent Optimized - saves ~25K tokens):**

   **🚀 USE SUB-AGENT FOR PROSPECT FILTERING:**
   ```
   Task (Explore): "Read shared/logs/icp-prospects.md and return 0-touch prospects:
   Filter criteria:
   - Touches = 0 (never engaged)
   - Connection Status = 'none' (not yet connected)
   - Activity Status != 'INACTIVE' (has posts to engage with)
   - NOT on blacklist (check shared/logs/linkedin-blacklist.md)

   Sort by Date Found (oldest first - FIFO)
   Return max 5 as JSON: [{name, profile_url, cached_post_urls, date_found, fit_score}]"
   ```

   **Main thread receives pre-filtered list - no need to read 40K+ token file.**

   1. ✅ Sub-agent returns filtered 0-touch prospects (already sorted)
   2. Select 3 oldest from returned list
   4. For each prospect:
      → Check Profile Cache for Recent Post URLs
      → If cached: Navigate directly to post URL
      → If not cached: Visit profile → Extract posts → Update cache
      → Blacklist + Duplicate check
      → Like post → Generate comment → Post comment
      → Update icp-prospects.md:
        * Touches: 0 → 1
        * Last Touch = today
        * Touch History = "comment"
      → Log to activity log
   5. **RESULT:** 3 prospects moved from 0-touch → 1-touch

   **DAILY TARGET:** Convert 3+ prospects from 0-touch → 1-touch
   **WEEKLY TARGET:** Clear 15-20 from 0-touch backlog

   **SKIP THIS STEP ONLY IF:**
   - 0-touch count < 10 prospects (backlog cleared)
   - All 0-touch prospects are INACTIVE (no posts to engage)

   **═══════════════════════════════════════════════════════════════**
   **INACTIVE COMMENT MONITOR (5 minutes) - Daily Rotation**
   **═══════════════════════════════════════════════════════════════**

   **PURPOSE:** Systematically rotate through INACTIVE prospects checking their comment tabs for engagement opportunities. Detects prospects who don't post but actively comment on others' posts.

   **WHY THIS MATTERS:** Many high-value ICP prospects are active commenters but infrequent posters. Standard warming (comment on their posts) doesn't work. Comment Hunting via their comment tab reveals hidden engagement opportunities.

   **🚀 USE SUB-AGENT FOR PROSPECT FILTERING:**
   ```
   Task (Explore): "Read shared/logs/icp-prospects.md and return INACTIVE prospects due for comment check:
   Filter criteria:
   - Notes contains 'INACTIVE' (flagged as inactive poster)
   - Notes does NOT contain 'Comment Check' with a date within the last 14 days
   - NOT on blacklist (check shared/logs/linkedin-blacklist.md)

   Sort by Date Found (oldest unchecked first)
   Return max 5 as JSON: [{name, profile_url, date_found, notes, last_comment_check}]"
   ```

   **EXECUTION:**
   1. Sub-agent returns filtered INACTIVE prospects due for rotation
   2. Select up to 5 from returned list
   3. For each prospect:
      → Navigate to comment tab: `https://www.linkedin.com/in/[username]/recent-activity/comments/`
      → Scan for substantive comments in last 14 days
      → **IF ACTIVE COMMENTER (has substantive comments):**
        * Find best comment to reply to (technical insight, question, or strong opinion)
        * Use linkedin-pro-commenter to generate reply (30-50 words max)
        * Post reply via browser automation
        * Update icp-prospects.md:
          - Touches: increment +1
          - Last Touch = today
          - Touch History: append "comment reply (Comment Hunting)"
          - Notes: replace "INACTIVE" with "COMMENT_ACTIVE"
          - Notes: append "Comment Monitor [date]: Active commenter - replied to comment on [Author]'s post"
        * Log to activity log
      → **IF NO COMMENTS (inactive in all ways):**
        * Update icp-prospects.md Notes: append "Comment Check [date]: No activity"
        * After 3 consecutive "No activity" checks → Update Notes: replace "INACTIVE" with "INACTIVE_VERIFIED"
        * Move to next prospect
      → Wait 5-10 seconds between profiles

   **DAILY TARGET:** Check 5 INACTIVE prospects
   **ROTATION:** ~100 INACTIVE prospects checked every 20 days (full cycle)

   **SKIP THIS STEP IF:**
   - No INACTIVE prospects exist in pipeline
   - All INACTIVE prospects checked within last 14 days
   - Sub-agent returns 0 prospects

   **═══════════════════════════════════════════════════════════════**
   **STANDARD ENGAGEMENT: 9 Comments (3+3+3) - Next 15 minutes**
   **═══════════════════════════════════════════════════════════════**

   **─── PHASE 1: Find 3 PROSPECT Posts (5-7 minutes) ───**

   **Method 1A: Profile Cache Mining (Primary - Fastest)**
   1. Read `shared/logs/icp-prospects.md` → Profile Cache table
   2. Filter prospects:
      ✓ Last Checked <7 days (fresh cache)
      ✓ Has Recent Post URLs (not empty)
      ✓ Activity Status = ACTIVE
      ✓ Last Touch >7 days (gap rule)
   3. Navigate directly to cached post URLs (3 prospects max)
   4. For each: Blacklist → Duplicate check → Like → Comment → Post → Log
   5. Update: Last Checked = today, Touches +1, Last Touch = today

   **Method 1B: Targeted Search (If cache <3 prospects)**
   Navigate to:
   ```
   https://www.linkedin.com/search/results/content/?keywords=[decision-maker roles from references/icp-profile.md] AND [target market keywords from references/icp-profile.md] AND [target geography from references/icp-profile.md]&origin=GLOBAL_SEARCH_HEADER
   ```
   Filter: Posted in last 24 hours
   Screen first 10 results → Engage with 3 ICP matches
   For each: Extract URL → Duplicate check → Like → Comment → Post → Log → Save to icp-prospects.md

   **─── PHASE 2: Find 3 THOUGHT LEADER Posts (5-7 minutes) ───**

   **Method 2A: Feed Scrolling (Primary)**
   1. Navigate to LinkedIn feed
   2. Scroll and visually identify:
      ✓ 10K+ followers (check profile badge/count)
      ✓ High engagement (50+ reactions)
      ✓ Topics relevant to your niche (from `references/icp-profile.md`)
      ✓ Posted within 48 hours
   3. Extract post URL → Duplicate check
   4. Engage with 3 THOUGHT LEADER posts
   5. Mark as "THOUGHT LEADER" in activity log

   **Method 2B: Hashtag Search (If feed has few thought leaders)**
   Navigate to:
   ```
   https://www.linkedin.com/search/results/content/?keywords=[hashtags from references/linkedin-strategy.md]&origin=GLOBAL_SEARCH_HEADER
   ```
   Filter: Sort by Recent
   Visually identify: 10K+ follower authors
   Engage with 3 posts from thought leaders

   **─── PHASE 3: Find 3 PEER Posts (5-7 minutes) ───**

   **Method 3A: Hashtag Search (Primary)**
   Navigate to:
   ```
   https://www.linkedin.com/search/results/content/?keywords=[hashtags from references/linkedin-strategy.md]&origin=GLOBAL_SEARCH_HEADER
   ```
   Filter: Sort by Recent
   Visually identify:
      ✓ 1K-10K followers (PEER range)
      ✓ Individual builders/founders (not company pages)
      ✓ Your niche topics (from `references/icp-profile.md`)
   Extract URLs → Duplicate check → Engage with 3 PEER posts
   Mark as "PEER" in activity log

   **Method 3B: Comment Thread Mining (Alternative)**
   Find 1 high-engagement post from a thought leader
   Check commenters → Screen for 1K-10K followers
   Find their recent posts → Engage with 3 PEER posts

   **═══════════════════════════════════════════════════════════════**
   **QUALITY GATES (Every Engagement)**
   **═══════════════════════════════════════════════════════════════**

   **Before commenting:**
   - [ ] Blacklist check: Author NOT on linkedin-blacklist.md
   - [ ] Duplicate check: Post URL NOT in linkedin-activity.md
   - [ ] Contact type verified: PEER (1K-10K) / PROSPECT (ICP) / THOUGHT LEADER (10K+)
   - [ ] Daily limit: Comments <30

   **After commenting:**
   - [ ] Log to linkedin-activity.md with contact type classification
   - [ ] If PROSPECT: Update icp-prospects.md (Touches +1, Last Touch = today)
   - [ ] Update daily limits: Comments +1

   **═══════════════════════════════════════════════════════════════**
   **EXPECTED OUTCOMES**
   **═══════════════════════════════════════════════════════════════**

   **90% of days:** 15-20 mins → 9 comments (3+3+3) ✅
   **If time-constrained:** Minimum 6 comments (2+2+2) in 10-12 mins
   **Prioritize:** PROSPECTS if choosing (pipeline building)

   CONTENT BLOCK:
   → CHECK: Posts today < 2 limit? If not, skip posting
   → Check last post time from shared log
   → Apply 12-HOUR RULE:
     - If last post < 12 hours ago → Calculate next valid window
     - If last post >= 12 hours ago → Can post in current window
   → If posting allowed: Run linkedin-trender → Get trending topic
     - AUTO-SELECT using weighted algorithm (see autonomous-optimization.md)
     - If no topics score >60 → USE evergreen backup (see evergreen-topics.md)
   → Run linkedin-elite-post → AI auto-selects best variation
     - AUTO-SELECT using weighted algorithm (see autonomous-optimization.md)
     - If all variations score <50 → Regenerate with "make more concise and actionable"
   → Run linkedin-image-generator → Generate image via Gemini
   → Schedule post for valid window (respecting 12h minimum gap)
   → Update daily limits: Posts +1
   → Log to shared activity log with scheduled time

   **═══════════════════════════════════════════════════════════════**
   **MIDDAY/EVENING/AFTERNOON PROSPECT-ONLY STRATEGY**
   **═══════════════════════════════════════════════════════════════**

   **🎯 TARGET: 5-10 PROSPECT engagements (Midday), 3-7 (Evening), 3-5 (Afternoon)**
   **⏱️ TIME: 10-15 minutes per block**
   **📊 GOAL: Build ICP pipeline through targeted PROSPECT engagement**

   **APPLIES TO:**
   - Midday Block (Golden Hour engagement)
   - Evening Block (Inbound signal follow-up)
   - Afternoon Block (Warm up prospects 0-1 touches)

   **═══════════════════════════════════════════════════════════════**
   **🎯 PRIORITY PHASE 0: FORCE 1→2 TOUCH CONVERSION (MANDATORY FIRST)**
   **═══════════════════════════════════════════════════════════════**

   **PURPOSE:** Pipeline analysis shows gap between 1-touch (18%) and 2-touch (7%).
   This phase forces systematic 1→2 conversion before random engagement.

   **BEFORE engaging with ANY new posts, FIRST:**

   **🚀 USE SUB-AGENT FOR TOUCH CONVERSION FILTERING (saves ~30K tokens):**
   ```
   Task (Explore): "Read shared/logs/icp-prospects.md and find prospects ready for touch conversion:

   1→2 CONVERSION candidates:
   - Touches = 1 (exactly one touch)
   - Last Touch > 3 days ago (gap rule for warming)
   - Connection Status = 'none' (not pending/connected)
   - Activity Status = 'ACTIVE' (has recent posts)
   - NOT on blacklist

   Return max 5 as JSON: [{
     name, profile_url, touches, last_touch,
     cached_post_urls, date_found, fit_score
   }]
   Sort by: fit_score DESC, last_touch ASC (oldest first)"
   ```

   1. ✅ Sub-agent returns pre-filtered 1-touch prospects
   2. Select 2-3 prospects from returned list
   3. For each prospect:
      → Navigate to their Recent Activity page
      → Find a post you haven't commented on yet
      → Blacklist + Duplicate check
      → Like → Comment → Post → Log
      → Update icp-prospects.md:
        * Touches: 1 → 2
        * Last Touch = today
        * Touch History += ", comment"
      → **If Touches now = 2:** Prospect is WARM, ready for asset-led connection
   4. Log conversions to activity log

   **DAILY TARGET:** Convert 2-3 prospects from 1-touch → 2-touch
   **WEEKLY TARGET:** All 1-touch prospects moved to 2-touch within 2 weeks

   **SKIP THIS PHASE ONLY IF:**
   - No 1-touch prospects meet criteria (all too recent or pending)
   - Already completed 1→2 conversions earlier today

   **THEN proceed to Phase 1 below for remaining engagement quota**

   **═══════════════════════════════════════════════════════════════**

   **EXECUTION SEQUENCE (Use until target reached):**

   **─── PHASE 1: Profile Cache Mining (Always Start Here) ───**
   **Time**: 5-7 minutes | **Expected**: 5-7 engagements

   1. Read `shared/logs/icp-prospects.md` → Profile Cache table
   2. Filter prospects:
      ✓ Last Checked <7 days (fresh cache)
      ✓ Has Recent Post URLs (not empty)
      ✓ Activity Status = ACTIVE (posted <7 days)
      ✓ Last Touch >7 days (gap rule for connected) OR >3 days (gap rule for warming)
      ✓ Connection Status ≠ pending
   3. For each cached prospect (max 10):
      → Navigate directly to cached post URL
      → Execute: Blacklist check → Duplicate check → Like → Comment → Post → Log
      → Update: Last Checked = today, Touches +1, Last Touch = today, Touch History += "comment"
   4. STOP when you hit target OR run out of fresh cache

   **If Phase 1 yielded ≥5 engagements → DONE, skip to logging**
   **If Phase 1 yielded <5 engagements → Continue to Phase 2**

   **─── PHASE 2: Targeted LinkedIn Search (Primary Fallback) ───**
   **Time**: 10-15 minutes | **Expected**: 5-10 engagements

   1. Navigate to LinkedIn search
   2. Use Boolean query:
      ```
      [decision-maker roles from references/icp-profile.md] AND
      [target market keywords from references/icp-profile.md] AND
      [target geography from references/icp-profile.md]
      ```
   3. Add filters:
      → Content type: Posts
      → Posted: Past 24 hours
      → Sort by: Recent
   4. Screen first 15 results:
      → Quick ICP check against criteria from `references/icp-profile.md`
      → Post quality check: Not job posting, not promotional spam
      → Extract post URL
   5. For each ICP match:
      → Blacklist check → Duplicate check (post URL)
      → Navigate to post → Like → Comment → Post → Log
      → Add to icp-prospects.md with 1 touch
   6. STOP when total engagements ≥target OR searched 15 results

   **If Phase 1+2 yielded ≥5 engagements → DONE, skip to logging**
   **If total engagements <5 → Continue to Phase 3**

   **─── PHASE 3: Comment Thread Mining (Secondary Fallback) ───**
   **Time**: 10-15 minutes | **Expected**: 3-5 engagements

   1. Find 1-2 seed posts:
      → Search hashtags from `references/linkedin-strategy.md`
      → Filter: High engagement (50+ likes, 20+ comments)
      → From thought leaders (10K+ followers)
      → Posted in last 48 hours
   2. Open comment thread on seed post
   3. Screen first 20-30 commenters:
      → Quick profile check: Name, headline, location
      → ICP criteria from `references/icp-profile.md`
      → Skip: Consultants, recruiters, students, large enterprises
   4. For each ICP match:
      → Click profile → Recent activity
      → Find their latest post (24-48h old)
      → Blacklist check → Duplicate check
      → Navigate → Like → Comment → Post → Log
      → Add to icp-prospects.md with 1 touch
   5. STOP when total engagements ≥target

   **If Phase 1+2+3 yielded ≥5 engagements → DONE, skip to logging**
   **If total engagements <3 → Continue to Phase 4 (rare)**

   **─── PHASE 4: Emergency Fallback (Rarely Needed) ───**
   **Time**: 15-20 minutes | **Expected**: 2-4 engagements

   **Use only when Phases 1-3 yielded <3 total:**

   1. **Feed Scrolling:**
      → Scroll LinkedIn feed
      → Visual ICP screening (profile photo, headline, company)
      → Engage with qualifying posts

   2. **Notification Mining:**
      → Check notifications for post reactors/commenters
      → Screen for ICP
      → Find their recent posts → Engage

   3. **Accept partial completion if:**
      → Already spent 30+ minutes
      → Search quota exhausted
      → No more qualifying prospects visible
      → Log partial completion, resume tomorrow

   **═══════════════════════════════════════════════════════════════**
   **DECISION TREE**
   **═══════════════════════════════════════════════════════════════**

   ```
   START Block
       ↓
   Check Daily Limits: Comments < 30?
       ↓ YES
   PHASE 1: Profile Cache Mining
       ↓
   Found ≥5 prospects?
       ↓ YES → ENGAGE → LOG → DONE ✅
       ↓ NO (0-4)
   PHASE 2: Targeted LinkedIn Search
       ↓
   Total ≥5?
       ↓ YES → LOG → DONE ✅
       ↓ NO (0-4)
   PHASE 3: Comment Thread Mining
       ↓
   Total ≥5?
       ↓ YES → LOG → DONE ✅
       ↓ NO (0-4)
   PHASE 4: Emergency Fallback
       ↓
   Reach 5 OR 30 mins → LOG → DONE ⚠️
   ```

   **═══════════════════════════════════════════════════════════════**
   **QUALITY GATES (Every Engagement)**
   **═══════════════════════════════════════════════════════════════**

   **Before commenting:**
   - [ ] Blacklist check: Author NOT on linkedin-blacklist.md
   - [ ] Duplicate check: Post URL NOT in linkedin-activity.md
   - [ ] Gap rule: Last Touch >7 days (connected) OR >3 days (warming)
   - [ ] Daily limit: Comments <30
   - [ ] Post freshness: Posted within 7 days (not stale)

   **After commenting:**
   - [ ] linkedin-activity.md: Add entry with post URL
   - [ ] icp-prospects.md: Update Last Touch, Touches +1, Touch History
   - [ ] Profile Cache: Update Last Checked = today (if using cache)
   - [ ] Daily Limits: Increment comment count

   **═══════════════════════════════════════════════════════════════**
   **EXPECTED OUTCOMES BY PHASE**
   **═══════════════════════════════════════════════════════════════**

   | Phase | Time | Expected ROI | When to Use |
   |-------|------|--------------|-------------|
   | **Phase 1: Cache** | 5-7 mins | 5-7 engagements | **Every block (always start here)** |
   | **Phase 2: Search** | 10-15 mins | 5-10 engagements | When cache <5 |
   | **Phase 3: Comments** | 10-15 mins | 3-5 engagements | When search quota low |
   | **Phase 4: Emergency** | 15-20 mins | 2-4 engagements | When all else fails |

   **90% of blocks:** Phase 1 only → 5-7 mins → 5-7 engagements ✅
   **9% of blocks:** Phase 1+2 → 15-20 mins → 7-10 engagements ✅
   **1% of blocks:** All phases → 25-30 mins → 5-8 engagements ⚠️

   **═══════════════════════════════════════════════════════════════**

   **MIDDAY BLOCK SPECIFIC ADDITIONS:**
   → Check notifications for comments on your post
   → For each reply to post commenters:
     - CHECK: Still under 30 comment limit?
     - Navigate to the post with comments
     - Find the specific comment to reply to
     - **LIKE the comment** (click like icon on the comment)
     - Click "Reply" on that comment
     - Type reply text in reply field
     - **CLICK "Reply" button to submit** (DO NOT skip this step)
     - Wait for confirmation reply posted
     - Update daily limits: Comments +1
   → THEN proceed with Golden Hour PROSPECT engagement using strategy above

   **AFTERNOON BLOCK SPECIFIC ADDITIONS:**
   → Check for connection acceptances → Move to Connected table
   → Classify each new connection: PROSPECT / PEER / THOUGHT LEADER
   → For PROSPECT connections ONLY: Schedule Value DMs (1-2 day old)
   → Warm up 0-1 touch prospects using strategy above
   → Send connection requests to 2+ touch prospects ONLY

   **EVENING BLOCK SPECIFIC ADDITIONS:**
   → THREE-FILE CROSS-CHECK for inbound signals (see Evening Block section)
   → Screen: Post engagement, comment likes, profile views, new followers
   → Save ICP matches to icp-prospects.md
   → Engage using strategy above

   AFTERNOON BLOCK:
   → Check for connection acceptances → Move to Connected table
   → Classify each new connection: PROSPECT / PEER / THOUGHT LEADER
   → For Value DMs (1-2 day old connections):
     - **ONLY DM PROSPECTS** (skip Peers and Thought Leaders)
     - CHECK: DMs today < 25 limit?
     - Read DM framework: `references/dm-framework.md`
     - Research prospect: recent posts, profile, previous comments
     - Choose pattern: Specific Curiosity / Thoughtful Question / Shared Observation / Acknowledge Insight
     - Write authentic DM (under 50 words, genuine curiosity, NO solution offers)
     - Send DM via Claude for Chrome
     - Update daily limits: DMs +1
   → **WARM UP existing prospects (2-3 Touch Rule):**
     - Read icp-prospects.md → Filter for 0-1 touch prospects
     - Run linkedin-icp-warmer → Find their recent posts
     - For each prospect post to comment on:
       * **⚠️ EXECUTE MANDATORY DUPLICATE CHECK** (grep author + post URL in activity log)
       * If ALREADY COMMENTED: SKIP, find different post from this prospect
       * Navigate to their LinkedIn post
       * **LIKE the post** (click Like/reaction button)
       * Generate comment using linkedin-pro-commenter
       * Click into comment field, type comment text
       * **CLICK "Post" button to submit** (DO NOT skip this step)
       * Wait for confirmation comment posted
       * Update touches +1 per comment in icp-prospects.md
     - Update Touch History in icp-prospects.md
   → **ONLY send connection requests to 2+ touch prospects:**
     - Filter icp-prospects.md for Touches >= 2
     - CHECK: Connections today < 15 limit?
     - Send connection request (blank for 3+ touches, asset-led for 2 touches)
     - Update Connection Status to "pending"
     - Update daily limits: Connections +1
   → Run linkedin-icp-finder for NEW prospects (discovery only):
     - Screen results against ICP Scoring Matrix
     - **SAVE qualifying prospects (60+) to icp-prospects.md as 0-touch**
     - Do NOT send connection requests to 0-touch prospects
   → Log all to shared activity log

   EVENING BLOCK:
   → **THREE-FILE CROSS-CHECK WORKFLOW (Sub-Agent Optimized):**
     **Reference:** `shared/references/signal-screening-workflow.md`
     **Token Savings:** ~50K tokens by using sub-agent instead of sequential reads

     **🚀 USE SUB-AGENT FOR BATCH CROSS-CHECK:**
     ```
     Task (Explore): "Cross-check these inbound signals against 3 files:

     Signals to check: [list names/profile URLs from notifications]

     Files to check (in order):
     1. shared/logs/linkedin-blacklist.md → If found, mark SKIP (blacklisted)
     2. shared/logs/inbound-screening-history.md → If found, use cached classification
     3. shared/logs/icp-prospects.md → Check gap rules (7 days connected, 3 days warming)

     Return JSON for each signal:
     [{
       name: string,
       profile_url: string,
       classification: PROSPECT|PEER|THOUGHT_LEADER|NON_ICP|BLACKLISTED,
       action: ENGAGE|SKIP|NEEDS_SCREENING,
       reason: string,
       gap_ok: bool (if PROSPECT),
       last_touch: date (if tracked)
     }]"
     ```

     **Sub-agent handles all 3 checks in one pass - main thread receives pre-filtered results.**

     **For signals marked NEEDS_SCREENING (not in any file):**
     4️⃣ **Full Profile Screening (Only for unknown contacts)**
        - Visit LinkedIn profile
        - Extract: location, followers, role, company
        - Classify: PROSPECT/PEER/THOUGHT LEADER/NON-ICP
        - **Add to Profile Cache** in inbound-screening-history.md
        - If PROSPECT: Add to icp-prospects.md with 0 touches

   → Run full inbound audit:
     - Post engagement (commenters, likers)
     - Comment likes and replies
     - Profile views (CHECK: < 80 limit before viewing back)
     - New followers
   → Screen each using THREE-FILE CROSS-CHECK above
   → **SAVE all ICP matches to icp-prospects.md** with source noted
   → For ICP matches needing engagement:
     - **⚠️ EXECUTE MANDATORY DUPLICATE CHECK** (see protocol - grep author + post URL)
     - If ALREADY COMMENTED: SKIP, only re-engage if they replied to your comment
     - **CHECK: If prospect, Last Touch < 7 days? (check icp-prospects.md)**
     - If RECENT PROSPECT: SKIP, use linkedin-icp-warmer process instead
     - CHECK: Comments/Likes/Profile Views within limits?
     - If engaging via comment on their post:
       * Navigate to their post
       * **LIKE the post**
       * Generate comment, type in field
       * **CLICK "Post" button to submit**
       * Wait for confirmation
       * **Update icp-prospects.md (Last Touch, Touches +1, Touch History)**
     - If engaging via reply to their comment:
       * Navigate to post with their comment
       * **LIKE their comment**
       * Click "Reply", type reply text
       * **CLICK "Reply" button to submit**
       * Wait for confirmation
       * **Update icp-prospects.md (Last Touch, Touches +1, Touch History)**
     - Update daily limits after each action
   → Log all to shared activity log
   → Update weekly metrics
   → Update Daily Limits Status table with final counts
   → **Update Signal Screening Log:**
     - Add screening session to `shared/logs/inbound-screening-history.md`
     - Add NEW contacts to Profile Cache section with: Name, Location, Classification, Profile Description, Followers, Screened Date
     - Track daily PROSPECT vs PEER vs NON-ICP ratios for content strategy optimization

5. Mark tasks complete in to-do file with timestamps
6. Report summary when block complete
```

### Autonomous Output Format

During execution, show minimal progress updates:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AUTONOMOUS MODE - [Block Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[09:01] Starting Morning Block...
[09:02] ✓ Feed Discovery → Found 2 new prospects from feed
[09:03] ✓ Algorithm Training → Visiting 5 prospect profiles...
[09:04] ✓ Profile 1/5: Didi Gan → Followed, Saved 2 posts, Harvested 3 recommendations
[09:05] ✓ Profile 2/5: Bryan Oh → Followed, Saved 2 posts, Harvested 4 recommendations
[09:06] ✓ Profile 3/5: Jaslyn Lee → Followed, Saved 2 posts, Harvested 2 recommendations
[09:07] ✓ Profile 4/5: Jennifer Zhang → Followed, Saved 2 posts, Harvested 3 recommendations
[09:08] ✓ Profile 5/5: Quek Siu Rui → Followed, Saved 2 posts, Harvested 4 recommendations
[09:09] ✓ Discovered 16 new lookalike prospects → Saved to icp-prospects.md
[09:09] ✓ Bulk Follow Sprint → Followed 12 unfollowed 0-touch prospects (87/203 total)
[09:10] ✓ 0-Touch Warming Sprint → Engaged 3 prospects with first touch
[09:12] ✓ INACTIVE Comment Monitor → Checked 5 INACTIVE prospects: 1 COMMENT_ACTIVE found, 4 no activity
[09:05] ✓ Comment 1/9: [Author - PROSPECT] - [Topic] - Posted (from cache)
[09:06] ✓ Comment 2/9: [Author - PROSPECT] - [Topic] - Posted (from cache)
[09:07] ✓ Comment 3/9: [Author - PROSPECT] - [Topic] - Posted (from cache)
[09:08] ✓ Scrolling feed → Identifying THOUGHT LEADERS (10K+) and PEERS (1K-10K)
[09:10] ✓ Comment 4/9: [Author - THOUGHT LEADER] - [Topic] - Posted
[09:11] ✓ Comment 5/9: [Author - THOUGHT LEADER] - [Topic] - Posted
...
[09:15] ✓ All 9 comments posted
[09:15] ✓ Logged to shared activity log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ MORNING BLOCK COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Comments: 9/9
New Prospects Discovered: 16 (via profile recommendations)
Algorithm Training: 5 profiles followed
Bulk Follow Sprint: 12 prospects followed (87/203 total)
INACTIVE Comment Monitor: 5 checked, 1 COMMENT_ACTIVE found
Time: 18 minutes
Next block: Content Block at 10:00

📊 DAILY LIMITS STATUS:
| Activity | Used | Limit | Remaining |
|----------|------|-------|-----------|
| Comments | 9 | 30 | 21 ✅ |
| Connections | 0 | 15 | 15 ✅ |
| DMs | 0 | 25 | 25 ✅ |
| Posts | 0 | 2 | 2 ✅ |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Late Start - Autonomous Handling

If started late, autonomously compress tasks:

```
[15:00] Late start detected - Afternoon Block
[15:00] Checking missed blocks...
[15:00] ⚠️ Morning Block: 0/9 comments (FLEXIBLE - doing now)
[15:00] ⚠️ Content Block: No post (Secondary window at 16:00)
[15:01] Executing compressed plan:
        → 9 comments (quick)
        → Schedule post for 16:00
        → Then Afternoon Block tasks
```

## Schedule Check Workflow

When user asks about timing or schedule:

### Time Blocks (your timezone)

> **Read timezone from `references/linkedin-strategy.md`** and apply to all time references below.

| Time | Block | Duration | Focus |
|------|-------|----------|-------|
| Before 10:00 AM | Morning Block | 15 mins | Pre-posting warm-up, 9 comments (3 Peer, 3 Prospect, 3 Thought Leader) - DIVERSE ENGAGEMENT |
| 10:00 AM - 12:00 PM | Content Block | Varies | Create and SCHEDULE post (use linkedin-elite-post) |
| 12:00 PM - 3:00 PM | Midday Block | 15 mins | Golden Hour engagement (PROSPECT POSTS ONLY), reply to comments on your post |
| 3:00 PM - 6:00 PM | Afternoon Block | 15 mins | Connection requests, DMs, outreach |
| After 6:00 PM | Evening Block | 10 mins | Daily audit, metrics check, inbound PROSPECT engagement review |

### Posting Windows by Day (your timezone)

| Day | Primary Window | Secondary Window | Best Content |
|-----|----------------|------------------|--------------|
| Monday | 10:00 - 11:30 AM | 4:00 - 5:30 PM | Strategy, planning frameworks |
| Tuesday | 8:30 - 10:30 AM | 12:00 - 1:30 PM | **Technical demos** (peak reach) |
| Wednesday | 9:00 - 11:00 AM | 3:00 - 5:00 PM | Save-worthy assets (schemas, SQL) |
| Thursday | 10:00 AM - 12:00 PM | 1:00 - 2:30 PM | Thought leadership |
| Friday | 8:30 - 10:00 AM | None | Reflections, personal stories |
| Weekend | Avoid posting | - | Engagement only |

### 12-Hour Posting Rule

**Minimum 12 hours between posts.** This prevents algorithm fatigue and ensures each post gets full distribution.

**Check before scheduling:**
```
1. Read shared log → Posts Published table → Get last post timestamp
2. Calculate: hours_since_last = current_time - last_post_time
3. If hours_since_last < 12:
   → next_valid_time = last_post_time + 12 hours
   → Find posting window ON OR AFTER next_valid_time
4. If hours_since_last >= 12:
   → Can post in current window
```

**Scheduling Logic:**

| Last Post Time | Current Time | Action |
|----------------|--------------|--------|
| Yesterday 18:00 | Today 09:00 | ✅ OK - 15 hours gap, use morning window |
| Today 08:00 | Today 10:00 | ❌ Wait - only 2h gap, schedule for 20:00+ |
| Today 10:00 | Today 16:00 | ❌ Wait - only 6h gap, schedule for 22:00+ |
| 2+ days ago | Any | ✅ OK - post immediately in current window |

**Autonomous Output When Delayed:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ POST SCHEDULING - 12H RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last post: Today 10:30 (your timezone)
Current time: 16:00 (your timezone)
Hours since last: 5.5 hours

⚠️ 12-HOUR MINIMUM NOT MET
Next valid posting: Today 22:30 (your timezone)
Nearest posting window: Tomorrow 08:30 (your timezone) (Tuesday Primary)

Action: Scheduling for Tomorrow 08:30 (your timezone)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Weekend Exception:**
- If next valid time falls on weekend → Schedule for Monday morning
- Weekend = engagement only, no posting

### Schedule Check Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ LINKEDIN SCHEDULE CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current time: [HH:MM] (your timezone)
Day: [Day of week]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 CURRENT BLOCK: [Block Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Focus: [What to do in this block]
Time remaining: [X mins/hours until next block]

Tasks for this block:
- [ ] [Task 1]
- [ ] [Task 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 TODAY'S POSTING WINDOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary: [Time range] (your timezone)
Secondary: [Time range] (your timezone) (if available)
Best content type: [Type for today]
Window status: [In window / Missed / Upcoming in X mins]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ 12-HOUR POSTING RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last post: [Date HH:MM (your timezone) or "None in last 24h"]
Hours since last: [X hours]
Status: [✅ OK to post / ⚠️ Wait until HH:MM]
Next valid window: [Day, Time range]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏭️ UPCOMING BLOCKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Next block]: Starts at [Time]
[Following block]: Starts at [Time]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 TODAY'S PROGRESS (from shared log)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Comments: [X]/9 target
Post: [Scheduled/Not yet/Posted]
Connections: [X]/10 target
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Quick Actions by Current Block

**If Morning Block:**
- "Run linkedin-pro-commenter to draft comments"
- "Run linkedin-post-finder to find posts to engage"

**If Content Block:**
- "Run linkedin-elite-post to create today's post"
- "Run linkedin-trender to find trending topics"
- "Run linkedin-image-generator for post visual"

**If Midday Block:**
- "Check notifications for comments on your post"
- "Reply to all comments (35% reach boost)"

**If Afternoon Block:**
- "Run linkedin-connect-timer to check connection pipeline"
- "Run linkedin-icp-warmer to find warmup opportunities"

**If Evening Block:**
- "Check inbound engagement (comment likes, replies, profile views, new followers)"
- "Review new followers at linkedin.com/mynetwork/network-manager/people-follow/followers/"
- "Review profile views at linkedin.com/me/profile-views/"
- "Screen followers/viewers for ICP fit - fast-track ICP followers"
- "Update shared activity log with today's metrics"

### Late Start Handling

**Tasks are categorized as TIME-SENSITIVE or FLEXIBLE:**

| Task Type | Time-Sensitive? | If Missed |
|-----------|-----------------|-----------|
| Commenting (9 comments) | ❌ Flexible | Can do anytime, carry forward |
| Post scheduling | ✅ Yes | Check if secondary window available |
| Golden Hour engagement | ✅ Yes | Only if you posted today |
| Connection requests | ❌ Flexible | Can do anytime |
| Inbound audit | ❌ Flexible | Can do anytime |

**When starting late (after Morning Block):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ LATE START DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current time: [HH:MM] (your timezone)
Blocks passed: Morning Block, Content Block

FLEXIBLE TASKS (still do today):
- [ ] 9 comments (Peer/Prospect/Thought Leader) - can do now
- [ ] Connection requests - can do now

TIME-SENSITIVE (check status):
- [ ] Post: Primary window MISSED, Secondary at [Time] (your timezone)
- [ ] Golden Hour: Only if post scheduled

CURRENT BLOCK: [Block Name]
Focus on: [Prioritized tasks for remaining day]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Adjusted workflow for late starts:**

1. **Check posting window status:**
   - If Primary missed but Secondary available → Schedule for Secondary
   - If both missed → Skip posting for today (or post anyway with lower reach)
   - If weekend → No posting needed

2. **Carry forward flexible tasks:**
   - Commenting can be done in any block
   - Connections can be done in any block
   - Compress into remaining time

3. **Skip time-sensitive tasks if window passed:**
   - Golden Hour only matters if you posted
   - Don't stress about missed windows - focus on what's still possible

**Example: Starting at 3 PM on Monday:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ADJUSTED PLAN - Late Start
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current time: 15:00 (your timezone) (Monday)

❌ MISSED:
- Morning Block (commenting warm-up)
- Content Block (primary posting window 10:00-11:30)

✅ STILL AVAILABLE:
- Secondary posting window: 4:00 - 5:30 PM (in 1 hour!)
- Commenting: Do now (before posting for Golden Hour effect)
- Connections: Do after posting

📍 ADJUSTED PRIORITY:
1. NOW: 9 comments quickly (15-20 mins)
2. 4:00 PM: Schedule post (secondary window)
3. 4:15 PM: Golden Hour engagement
4. 5:00 PM: Connection requests
5. Evening: Audit and log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Resume Workflow

When user triggers a resume command:

### Step R1: Find Today's To-Do File

Look for existing to-do file with today's date:
```
to-do_DDMMYYYY.md
```

**If file exists:** Load it and proceed to Step R2.
**If file doesn't exist:** Ask user if they want to create a new plan for today.

### Step R2: Parse Progress

Read the file and identify:
1. **Completed tasks:** Lines with `[x]`
2. **Pending tasks:** Lines with `[ ]`
3. **Current time block:** Based on current time
   - Before 10am → Morning Block
   - 10am-12pm → Content Block
   - 12pm-3pm → Midday Block
   - 3pm-6pm → Afternoon Block
   - After 6pm → Evening Block

### Step R3: Show Status Summary

Display progress summary:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN PROGRESS - [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Progress: [X/Y tasks completed]

✅ COMPLETED:
- [List completed tasks]

⏳ CURRENT BLOCK: [Block Name]
- [ ] [Next pending task in current block]
- [ ] [Other pending tasks in block]

📋 REMAINING:
- [Count of tasks in later blocks]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step R4: Offer Next Action

```
What would you like to do?

1. Execute next task: "[Next pending task description]"
2. Skip to a specific block
3. Mark a task as complete
4. See full to-do list

Or just tell me what you've completed and I'll update the list.
```

---

## Task Completion Tracking

### Marking Tasks Complete

When a task is completed (either by execution or user confirmation):

1. **Read** the current to-do file
2. **Find** the matching task line (by task description)
3. **Update** `[ ]` to `[x]`
4. **Add timestamp** after the task: `[x] Task description ✓ HH:MM`
5. **Save** the updated file
6. **Confirm** completion to user and show next task

### Auto-Complete After Skill Execution

When a LinkedIn skill completes successfully, automatically mark the related task:

| Skill Completed | Auto-Mark Task |
|-----------------|----------------|
| linkedin-pro-commenter | "Comment on X posts" |
| linkedin-elite-post | "Create a [type] post" |
| linkedin-trender | "Run linkedin-trender" |
| linkedin-icp-finder | "Screen ICP prospects" / "Send connection requests" |
| linkedin-post-finder | "Find high-engagement posts" |

### Manual Completion

User can mark tasks done by saying:
- "done with morning comments"
- "finished the post"
- "completed [task description]"
- "mark [task] as done"

Update the file immediately when user confirms completion.

### Completion Update Format

When updating the to-do file:

**Before:**
```markdown
- [ ] Comment on 3 peer posts (fellow builders in your niche — from `references/icp-profile.md`)
```

**After:**
```markdown
- [x] Comment on 3 peer posts (fellow builders in your niche — from `references/icp-profile.md`) ✓ 09:15
```

---

## Step 1: Determine Day of Week

Get the current date and day of week to customize the plan:

| Day | Content Focus | Post Type |
|-----|--------------|-----------|
| Monday | Evidence content | Demo, Schema, JSON import |
| Tuesday | Strategy content | Strategy content for your target market |
| Wednesday | Evidence content | Demo, Schema, JSON import |
| Thursday | Strategy content | Strategy content for your target market |
| Friday | Reflection | Personal story from teaching/hackathons |
| Saturday/Sunday | Engagement only | No posting required |

## Step 2: Generate Daily To-Do List

Create the to-do file with this structure:

```markdown
# LinkedIn Daily Outreach Plan - [Day, DD MMM YYYY]

## Morning Block (15 mins) - Pre-Posting Warm-Up

The 15/15 Rule: Engage BEFORE posting to warm your topical relevance.

### Sales Navigator Notification Scan (if account = SALES_NAVIGATOR)

**Read account type from:** `shared/linkedin-account-config.md`

**ONLY do this step if Account Type = SALES_NAVIGATOR**

- [ ] Navigate to Sales Navigator → Click notifications bell
- [ ] Check for posts created in last 24 hours
- [ ] For each notification, screen author against ICP criteria:
  - ✅ Target geography (from `references/icp-profile.md`)
  - ✅ Decision-maker role (from `references/icp-profile.md`)
  - ✅ Target market company size (from `references/icp-profile.md`)
- [ ] For ICP matches found:
  - Save to `shared/logs/icp-prospects.md` if not already there
  - Note source: "Source: Sales Nav: Notifications"
  - Navigate to full LinkedIn post
  - Use linkedin-pro-commenter to generate comment
  - Post comment
  - Update prospect: Touches +1, Last Touch = today, Touch History += "comment"
  - Log to shared activity log
- [ ] Continue until all notifications scanned or comment limit approached

### Commenting Tasks (use linkedin-pro-commenter + linkedin-icp-finder)

**Contact Classification:** See `references/contact-classification.md`

---

## ⚠️ MANDATORY DUPLICATE CHECK PROTOCOL (CANNOT BE BYPASSED)

**CRITICAL: Before commenting on ANY post, you MUST execute this duplicate check. Failure to check = duplicate comment = wasted engagement.**

### Why This Matters
- LinkedIn algorithm penalizes duplicate behavior
- Re-commenting on same post damages credibility
- Wastes daily comment limit (30/day)
- Breaks touch tracking accuracy

### 🔴 SESSION-LEVEL DUPLICATE PREVENTION (NEW - CRITICAL)

**Problem:** Within a single autonomous session, the same post can appear multiple times in feed/search results. Without session-level tracking, you may comment on the same post 2-3 times before it's logged.

**Solution: Maintain a SESSION COMMENT TRACKER in memory during autonomous execution.**

**SESSION TRACKER FORMAT:**
```
SESSION_COMMENTED_POSTS = []  # List of post URLs commented this session
```

**ENFORCEMENT RULES:**
1. **BEFORE generating any comment:**
   - Check if post URL is in SESSION_COMMENTED_POSTS
   - If YES → SKIP IMMEDIATELY (already commented this session)
   - If NO → Continue to activity log check

2. **IMMEDIATELY after posting comment:**
   - Add post URL to SESSION_COMMENTED_POSTS
   - This happens BEFORE moving to next post
   - Do not wait for activity log file save

3. **Session tracker persists until:**
   - Session ends
   - User says "reset session"
   - New time block starts

**VISUAL CHECK: Before commenting, output:**
```
🔍 Session Check: [POST_URL]
   - Session tracker: [NOT FOUND / FOUND - SKIP]
   - Activity log: [checking...]
```

**This prevents the scenario where:**
- Post A appears at position 3 in feed → Comment posted
- Post A appears again at position 12 → BLOCKED by session tracker
- Post A appears in search results → BLOCKED by session tracker

### Post URL: The Single Source of Truth

**CRITICAL: Every post on LinkedIn has a unique URL (urn:li:activity:XXXXXXXXXXXXX). This is your duplicate prevention key.**

Why URL-based checking is superior:
- 100% accurate - same URL = same post
- Works regardless of author, topic, or post age
- Prevents re-commenting even if you engaged months ago
- Simple binary check: URL in log = SKIP, URL not in log = OK to comment

**Mandatory: Always log the Post URL in activity log**

Every comment entry MUST include the full post URL in this format:
```
| Time | Author | Category | Profile URL | Post URL | Topic | Comment | Status |
| 08:45 | John Doe | PROSPECT | /in/johndoe | linkedin.com/feed/update/urn:li:activity:7421711052880642048/ | Topic | "Comment..." | ✅ Posted |
```

### How to Extract Post URLs

**Method 1: From LinkedIn Page URL (Most Reliable)**
When you navigate to a post, the browser URL contains the post ID:
```
https://www.linkedin.com/feed/update/urn:li:activity:7421711052880642048/
```
Extract the full URL including the `urn:li:activity:XXXXXXXXXXXXX` part.

**Method 2: From Snapshot/Accessibility Tree**
Search snapshot for links containing `feed/update/urn:li:activity:`:
```bash
grep -o 'url="https://www.linkedin.com/feed/update/urn:li:activity:[^"]*' snapshot.txt | \
  sed 's/url="//' | head -1
```

**Method 3: From JavaScript (DevTools)**
```javascript
window.location.href  // Returns current post URL
```

**If you cannot extract the URL:**
- Click on the post timestamp or "..." menu
- Navigate to the standalone post page
- Capture the URL from the browser address bar
- Then proceed with duplicate checking

**CRITICAL: Never comment without capturing the Post URL first. No URL = Cannot verify duplicates.**

### Duplicate Check Steps (Execute BEFORE Every Comment)

**Step 1: Check Author Name**
```bash
grep -i "[AUTHOR_NAME]" "shared/logs/linkedin-activity.md"
```

If author name found → Read the matching lines → Check dates
- If commented within last 30 days → **SKIP THIS AUTHOR**
- If commented > 30 days ago → Can re-engage (verify different post)

**Step 2: Check Post URL (if available)**
```bash
grep -i "urn:li:activity:[POST_ID]" "shared/logs/linkedin-activity.md"
```

If post URL found → **SKIP THIS POST IMMEDIATELY** (already commented)

**Step 3: Check Post Topic**

Even if author is different, check if you commented on identical topic recently:
```bash
grep -i "[KEY_TOPIC_PHRASE]" "shared/logs/linkedin-activity.md"
```

Examples:
- "[Location] [Topic] Governance" → Check for "[Location].*Governance"
- "GEO enterprise capability" → Check for "GEO.*enterprise"

If very similar topic found within 7 days → Consider skipping (avoid repetitive positioning)

### Decision Tree

```
FOR EACH POST BEFORE COMMENTING:

STEP 1: EXTRACT POST URL (MANDATORY)
   → Navigate to the post detail page
   → Extract the full post URL: linkedin.com/feed/update/urn:li:activity:XXXXXXXXXXXXX/
   → If you cannot get the URL, you CANNOT comment (must find it first)

STEP 2: CHECK POST URL IN ACTIVITY LOG (PRIMARY DUPLICATE CHECK)
   → Run: grep "urn:li:activity:XXXXXXXXXXXXX" "shared/logs/linkedin-activity.md"
   → FOUND? → **SKIP IMMEDIATELY** - Already commented on this exact post
   → NOT FOUND? → Continue to step 3

STEP 3: CHECK AUTHOR NAME (SECONDARY CHECK)
   → Run: grep -i "author_name" "shared/logs/linkedin-activity.md"
   → FOUND + within 30 days? → **SKIP** - Recently engaged with this author
   → NOT FOUND? → Continue to step 4

STEP 4: CHECK TOPIC SIMILARITY (OPTIONAL)
   → Run: grep -i "main_topic_keyword" "shared/logs/linkedin-activity.md"
   → Similar topic within 7 days? → Consider skipping (avoid repetitive positioning)
   → No similar topic? → Continue to step 5

STEP 5: SAFE TO COMMENT
   → Like post
   → Generate comment (40-50 words)
   → Post comment
   → **IMMEDIATELY LOG TO ACTIVITY LOG WITH POST URL**

STEP 6: UPDATE ACTIVITY LOG (MANDATORY)
   → Add new row with: Time | Author | Category | Profile URL | **POST URL** | Topic | Comment | Status
   → Verify post URL is captured correctly
   → Save activity log file
```

**The Golden Rule: If the Post URL is in the activity log, NEVER comment again.**

### Examples of Proper Checking

**Example 1: Found a post by Jamshed Wadia**
```bash
# STEP 1: Extract post URL from LinkedIn page
# Navigate to post → URL bar shows:
# https://www.linkedin.com/feed/update/urn:li:activity:7421711052880642048/
POST_URL="7421711052880642048"

# STEP 2: Check if this exact post URL is in activity log (PRIMARY CHECK)
grep "urn:li:activity:7421711052880642048" "C:\Users\melve\.claude\skills\shared\logs\linkedin-activity.md"

# Output shows line? → SKIP THIS POST (already commented)
# No output? → Continue to step 3

# STEP 3: Check author name (SECONDARY CHECK)
grep -i "jamshed" "C:\Users\melve\.claude\skills\shared\logs\linkedin-activity.md"

# Output shows recent comment? → SKIP (engaged recently)
# No output? → SAFE TO COMMENT

# STEP 4: Comment, then log with URL
# After posting comment, add to activity log:
# | 09:15 | Jamshed Wadia | THOUGHT LEADER | /in/jamshedwadia | linkedin.com/feed/update/urn:li:activity:7421711052880642048/ | Topic | "Comment..." | ✅ Posted |
```

**Example 2: Found a post by Tom Edwards on GEO**
```bash
# STEP 1: Extract post URL
POST_URL="7422345678901234567"

# STEP 2: Check post URL (PRIMARY - most important check)
grep "urn:li:activity:7422345678901234567" "C:\Users\melve\.claude\skills\shared\logs\linkedin-activity.md"

# No output? → Continue

# STEP 3: Check author
grep -i "tom edwards" "C:\Users\melve\.claude\skills\shared\logs\linkedin-activity.md"

# No output? → SAFE TO COMMENT (post URL is the definitive check)
```

**Example 3: Discovered you already commented**
```bash
# STEP 1: Extract URL
grep "urn:li:activity:7420988849025261568" "C:\Users\melve\.claude\skills\shared\logs\linkedin-activity.md"

# Output returns:
# | 17:10 | Alva Chew | PEER | linkedin.com/in/alvachew | linkedin.com/feed/update/urn:li:activity:7420988849025261568/ | Cold outreach roast | "Comment..." | ✅ Posted |

# ACTION: SKIP THIS POST IMMEDIATELY
# Find a different post from a different author
```

### Fail-Safe Rule

**When in doubt, SKIP the post.** Better to miss one engagement than damage credibility with duplicate comments.

---

**EFFICIENT POST-FINDING STRATEGY:**

**Step 1: Find 3 PROSPECT posts (Cache-First)**
- [ ] Open `shared/logs/icp-prospects.md` → Profile Cache table + Main Prospects table
- [ ] Filter for prospects with Last Touch > 7 days, Connection Status ≠ pending
- [ ] For each prospect: Check if cache is fresh (Last Checked < 7 days AND has Recent Post URLs)
- [ ] **IF cache empty/stale:**
  - Navigate to `/in/{profile-path}/recent-activity/all/`
  - Take snapshot
  - Extract 1-3 post URLs (feed/update/urn:li:activity:XXXXX)
  - **IMMEDIATELY update Profile Cache table** (Last Checked, Activity Status, Followers, Last Post, Recent Post URLs)
  - Save icp-prospects.md
  - Navigate to first post URL
- [ ] **IF cache fresh:**
  - Navigate directly to cached post URLs
  - Update "Last Checked" timestamp to today
- [ ] Verify not already commented (check activity log by Post URL)
- [ ] Like post → Comment → Update touch tracking
- [ ] Repeat for 3 PROSPECT posts total

**Step 2: Find 3 THOUGHT LEADER posts (Feed Scrolling)**
- [ ] Scroll LinkedIn feed or search your niche hashtags (from `references/linkedin-strategy.md`)
- [ ] Visually identify 10K+ followers = THOUGHT LEADER
- [ ] Verify not already commented (check activity log by Author Name)
- [ ] Comment on 3 fresh THOUGHT LEADER posts

**Step 3: Find 3 PEER posts (Feed Scrolling)**
- [ ] Continue scrolling LinkedIn feed
- [ ] Visually identify 1K-10K followers + AI/automation niche = PEER
- [ ] Verify not already commented (check activity log by Author Name)
- [ ] Comment on 3 fresh PEER posts

**Comment Rules:**
- Minimum 15 words per comment
- Maximum 50 words
- Must add POV or insight
- Ask a question to encourage thread depth
- LIKE the post before commenting
- CLICK "Post" button to submit (do not skip!)

**⚠️ CRITICAL: NO EM-DASHES (—) IN COMMENTS OR REPLIES**
- Em-dashes (—) are a STRONG AI-detection signal on LinkedIn
- NEVER use em-dashes in any comment, reply, or post text
- Use commas, periods, or colons instead
- Use "and" or rewrite the sentence if needed
- Before posting: Search your text for "—" and REPLACE if found
- Examples of BAD → GOOD:
  - BAD: "systems—the orchestration layer" → GOOD: "systems. The orchestration layer"
  - BAD: "builders—fellow SG" → GOOD: "builders, fellow SG"
  - BAD: "AI agents—and why" → GOOD: "AI agents and why"

---

## Content Block ([Day-specific])

[Insert day-specific content task - see Day Matrix below]

---

## Midday Block (15 mins) - Post-Content Engagement

### Golden Hour Tasks
- [ ] Engage with 5-10 PROSPECT posts ONLY (warms topical relevance for 4 hours)
- [ ] Reply to ALL comments on your post within 1 hour (35% reach boost)
- [ ] Save 2-3 high-quality posts from your feed (360Brew values Saves 5x more than Likes)

**IMPORTANT: Only comment on PROSPECT posts during Midday Block. Morning Block is the only time to engage with Peers and Thought Leaders.**

### Post Commenter Engagement (HIGHEST priority inbound signal)
- [ ] For each commenter on your post: Quick ICP screen
- [ ] If PROSPECT match: Note for Evening Block follow-up (find their posts, comment back)
- [ ] Reply builds thread depth even if not PROSPECT (extends post reach 48+ hours)
- [ ] **Note: Only comment back on PROSPECT posts. Peers and Thought Leaders are engaged with in Morning Block only.**

---

## Afternoon Block (15 mins) - Outreach

### Check Connection Acceptances (do this FIRST)
- [ ] Check "My Network" for new connection acceptances
- [ ] For each acceptance: Move from "Pending" → "Connected" table in shared log
- [ ] **Classify each connection: PROSPECT / PEER / THOUGHT LEADER**
- [ ] Schedule Value DM for **PROSPECTS ONLY** (24-48h after acceptance)
- [ ] ⚠️ **DO NOT schedule DMs for Peers or Thought Leaders** (engage via comments instead)

### 🔔 DAILY DM CHECK (MANDATORY - Do Not Skip)

**Problem identified:** Only 2 Value DMs sent in past week. Target is 5-10/week.

**BEFORE any other Afternoon Block tasks:**
1. Check icp-prospects.md → Filter for:
   ✓ Connection Status = "connected"
   ✓ Classification = PROSPECT
   ✓ "dm_sent" NOT in Touch History
   ✓ Connection date = 24-48 hours ago
2. If matches found → These MUST get Value DMs today
3. Log as "DM Pending" if not sent immediately

**Weekly DM Target:** 5-10 Value DMs to new PROSPECT connections
**Current gap:** Most new connections not receiving DMs within 48h window

### Send Value DMs (for PROSPECT acceptances from 1-2 days ago)
- [ ] Check "Connected (Recent)" table for pending Value DMs
- [ ] **FILTER: Only send DMs to contacts marked as PROSPECT**
- [ ] Skip Peers and Thought Leaders (they don't need DMs - continue engaging on their content)
- [ ] **Read DM framework:** `references/dm-framework.md` for patterns and examples
- [ ] Research each prospect: recent posts, profile details, your previous comments on their content
- [ ] Choose DM pattern based on context (Specific Curiosity / Thoughtful Question / Shared Observation / Acknowledge Insight)
- [ ] Write personalized DM using framework (under 50 words, genuine curiosity, NO solution offers)
- [ ] NO external links, NO pitch, NO "happy to share" phrases
- [ ] Mark "Value DM Sent = Yes" in log

### Warm Up Existing Prospects (2-3 Touch Rule)
- [ ] Read `shared/logs/icp-prospects.md` → Filter for 0-1 touch prospects
- [ ] Run linkedin-icp-warmer to find their recent posts
- [ ] Comment on 3-5 prospect posts (builds +1 touch per comment)
- [ ] Update Touch History column in icp-prospects.md after each engagement

**2-3 Touch Rule:**
| Touches | Status | Action |
|---------|--------|--------|
| 0 | Cold | **Do NOT connect** - find their posts and comment |
| 1 | Warming | Continue engagement - comment on another post |
| 2 | Warm | Can connect with asset-led note |
| 3+ | Hot | Can connect with blank request (10-15% better) |

### Send Connection Requests (2+ Touches ONLY)
- [ ] Filter icp-prospects.md for prospects with Touches >= 2
- [ ] Send connection requests ONLY to warmed prospects (max 15/day)
- [ ] For 2-touch prospects: Use asset-led note
- [ ] For 3+ touch prospects: Send blank request (performs better)
- [ ] Update Connection Status to "pending" in icp-prospects.md

### Discover NEW Prospects (use linkedin-icp-finder)
- [ ] Run linkedin-icp-finder to search for new prospects
- [ ] Screen each result against ICP Scoring Matrix (80+ = HOT, 60-79 = WARM)
- [ ] **Save all qualifying prospects to `shared/logs/icp-prospects.md` as 0-touch**
- [ ] ⚠️ **Do NOT send connection requests** - warm up first!

**Prospect Saving Rule:**
```
IF prospect scores 60+ on ICP matrix:
  → Save to shared/logs/icp-prospects.md
  → Set Touches = 0, Connection Status = "none"
  → Include: Name, Role, Company, Profile URL
  → Note: "Source: Outbound search [date]"
  → Next step: Find their posts and comment (warming)
```

**Email Capture:**
- Click "Contact info" on prospect's profile (below their headline)
- If email is visible → Add to Email column in prospects file
- If email not visible → Leave blank (will be available after connection)
- Common visibility: ~30% of profiles show email to non-connections

**Value DM Framework (Genuine Curiosity - NO Solutions Offered):**

**CRITICAL: Never offer workflows, frameworks, or solutions in first DMs. Build relationship through genuine curiosity.**

Choose ONE of these patterns based on prospect context:

**Pattern 1: Specific Curiosity**
> "Saw your work at [Company] [specific detail from their profile]. Curious how you [specific challenge related to their role]? We're seeing [related observation] in your target geography (from `references/icp-profile.md`) [their industry]."

**Pattern 2: Thoughtful Question**
> "Your focus on [their area] caught my eye. What's the biggest [mindset shift/challenge/friction point] you see companies struggle with when [relevant transition/problem]?"

**Pattern 3: Shared Observation**
> "Read your take on [specific post topic]. We're noticing the same pattern with [relevant detail] - especially around [specific angle]. How are you approaching [their challenge]?"

**Pattern 4: Acknowledge Insight**
> "Your point about [specific thing they said] resonates. Seeing this play out differently across [geography/industry] - have you noticed [interesting pattern/question]?"

**Rules:**
- Reference something SPECIFIC from their profile/post (not generic)
- Ask a REAL question you're genuinely curious about
- Share an observation WITHOUT offering a solution
- Keep under 50 words
- NO "happy to share", NO "let me know if", NO offers
- Goal: Start a conversation, not pitch anything

---

## Evening Block (10 mins) - Audit

### Daily Metrics Check
- [ ] Count comments made today (target: 9-15 high-quality)
- [ ] Count connection requests sent (target: 5-10)
- [ ] Note any high-engagement posts for tomorrow's follow-up
- [ ] Log any ICP leads identified

### Inbound Engagement Audit (Check Notifications)

**Post Engagement (on YOUR posts) - HIGHEST priority:**
- [ ] Review who commented on your posts today
- [ ] Review who liked/reacted to your posts (focus on ICP screening)
- [ ] **PROSPECT commenters ONLY:** Find their posts → Comment back (use linkedin-pro-commenter)
- [ ] **PROSPECT likers ONLY:** Find their posts → Comment
- [ ] **SKIP Peers and Thought Leaders** - only engage with them in Morning Block
- [ ] Log to shared activity log → "Post Engagement Received" table

**Comment Engagement (on your comments):**
- [ ] Check LinkedIn notifications for comment likes received
- [ ] Check for replies to your comments
- [ ] **PROSPECT matches ONLY:** Find their posts → Comment to reciprocate
- [ ] Reply to comment replies (builds thread depth = algorithm boost)
- [ ] **SKIP Peers and Thought Leaders** - only engage with them in Morning Block

**Profile & Follower Signals:**
- [ ] **Check profile views** (linkedin.com/me/profile-views/)
- [ ] **Check new followers** (linkedin.com/mynetwork/network-manager/people-follow/followers/)

**For all inbound signals:**
- [ ] Quick ICP screen (criteria from `references/icp-profile.md`)
- [ ] **Save ICP matches to `shared/logs/icp-prospects.md`**
- [ ] Log ICP matches to `shared/logs/linkedin-activity.md` → "Inbound Engagement" section
- [ ] Add ICP matches to "Warming Up" pipeline with note (signal type)

**Inbound Prospect Saving Rule:**
```
IF inbound signal passes ICP screen:
  → Save to shared/logs/icp-prospects.md
  → Include: Name, Role, Company, Profile URL
  → **Check "Contact Info" on profile → Capture Email if visible**
  → Note: "Source: [Signal Type] [date]" (e.g., "Source: Profile View 22Jan")
  → Fast-track warmth: Profile view = 1-2, Follower = 2, Reactor = 1
```

**New Followers = VERY Strong Signal (prioritize over profile views):**
- [ ] Review new followers today
- [ ] Screen each follower against ICP criteria
- [ ] If ICP match: **Save to icp-prospects file** → Follow back → Find their posts → Comment
- [ ] **Fast-track:** ICP followers only need 1-2 touches before connecting
- [ ] Log to shared activity log → "New Followers Received" table

**Profile Views = Strong Buying Signal:**
- [ ] Review who viewed your profile today
- [ ] Screen each viewer against ICP criteria
- [ ] If ICP match: **Save to icp-prospects file** → View their profile back → Find their posts → Comment
- [ ] Log to shared activity log → "Profile Views Received" table

**ICP Fit Quick Check:**
- ✅ Location: Your target geography (from `references/icp-profile.md`)
- ✅ Role: Decision-maker roles (from `references/icp-profile.md`)
- ✅ Company: Target market size (from `references/icp-profile.md`)
- ❌ Skip: Outside target geography, junior roles, excluded company types, recruiters (from `references/icp-profile.md`)

---

## Skills Integration

| Task | Skill to Use |
|------|--------------|
| Find trending topics | `linkedin-trender` |
| Create post content | `linkedin-elite-post` |
| Generate images for posts | `linkedin-image-generator` |
| Write comments | `linkedin-pro-commenter` |
| Find high-engagement posts | `linkedin-post-finder` |
| Screen ICP prospects | `linkedin-icp-finder` |
| Warm up existing prospects | `linkedin-icp-warmer` |
| Check connection readiness | `linkedin-connect-timer` |
| Audit profile alignment | `linkedin-profile-icp` |

## Reference Files

| Reference | Location | Purpose |
|-----------|----------|---------|
| **DM Framework** | `references/dm-framework.md` | Value DM patterns for new PROSPECT connections (genuine curiosity, NO solution-offering) |
| **Autonomous Optimization** | `references/autonomous-optimization.md` | Auto-selection algorithms, fail-safe mechanisms, performance targets for zero-interaction execution |
| **Evergreen Topics** | `references/evergreen-topics.md` | Backup content topics (12 topics across 4 tiers) when trending analysis fails |
| **Account Config** | `shared/linkedin-account-config.md` | Account type, limits, feature availability |
| **ICP Prospects** | `shared/logs/icp-prospects.md` | Master prospect list with touch tracking |
| **Activity Log** | `shared/logs/linkedin-activity.md` | Daily engagement tracking and limits |

### Account-Conditional Features

**Read account type from:** `shared/linkedin-account-config.md`

| Account Type | Additional Features |
|--------------|---------------------|
| FREE | Standard workflow only |
| PREMIUM_CAREER | Enhanced search, see all profile viewers |
| PREMIUM_BUSINESS | Above + InMail (5-15/month) |
| SALES_NAVIGATOR | Above + Saved Searches, Lead tracking, 50 InMails, Weekly pipeline refresh |

**If SALES_NAVIGATOR:** Include Friday "Sales Navigator Pipeline Refresh" in weekly audit

---

## 360Brew Reminders

- 80% of content must align with profile keywords
- Saves > Likes (5x value)
- No external links in posts or first DMs
- Hashtags are obsolescent
- First 2 lines of post = "Topic Signal" for algorithm
```

## Daily Engagement Limits (360Brew Safe)

**CRITICAL: Exceeding these limits triggers LinkedIn's Automation Detection System (ADS).**

### Limit Reference Table

| Activity | Daily Limit | Target | Notes |
|----------|-------------|--------|-------|
| **Posts** | 1-2 max | 1 | 12-hour minimum between posts |
| **Comments** | 30 max | 9-15 | Quality > quantity; 15-50 words each |
| **Connection Requests** | 100-200/week (~15-20/day) | 5-10 | Rolling 7-day window; blank requests preferred |
| **DMs (New Conversations)** | 25 max | 5-10 | No links in first DM |
| **DM Follow-ups** | 50 max | As needed | Existing conversations only |
| **Likes/Reactions** | 100 max | 20-50 | Don't mass-like |
| **Profile Views (outbound)** | 80 max | 20-30 | Quality screening only |
| **Follows** | 20 max | 5-10 | Follow-for-follow is flagged |

### Limit Check Logic (Autonomous Mode)

Before each action, check the shared activity log:

```
BEFORE COMMENTING:
  → Read today's comment count from shared log
  → If count >= 30: STOP, log "Daily comment limit reached"
  → If count >= 25: WARN "Approaching comment limit (25/30)"

BEFORE SENDING CONNECTION:
  → Read this week's connection request count (rolling 7-day window)
  → If weekly count >= 100: STOP, log "Weekly connection limit reached"
  → Daily guidance: ~15-20/day max, but weekly total matters more
  → If acceptance rate < 30%: Reduce volume, improve targeting

BEFORE SENDING DM:
  → Read today's new DM count from shared log
  → If count >= 25: STOP, log "Daily DM limit reached"
  → If count >= 20: WARN "Approaching DM limit (20/25)"

BEFORE LIKING:
  → Read today's like count from shared log
  → If count >= 100: STOP, log "Daily like limit reached"

BEFORE VIEWING PROFILE:
  → Read today's profile view count from shared log
  → If count >= 80: STOP, log "Daily profile view limit reached"
```

### Autonomous Output When Limit Reached

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ DAILY LIMIT REACHED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Activity: Comments
Current: 30/30
Status: LIMIT REACHED - Skipping remaining comments

Remaining tasks for today:
- Connection requests: 8/15 (7 remaining)
- DMs: 3/25 (22 remaining)

Action: Moving to next task type
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Warning Signs of Over-Engagement

If you see these, STOP immediately:
- LinkedIn shows "Something went wrong" errors
- Comments fail to post
- Connection requests get "pending" status instantly
- Profile shows "restricted" warnings
- Temporary action blocks (24-72 hours)

**Recovery Protocol:**
1. Stop ALL engagement for 24 hours
2. Resume at 50% of normal limits for 3 days
3. Gradually return to normal limits over 1 week

### Limit Tracking in Shared Log

Update daily metrics after EACH action:

```markdown
## Daily Limits Status - [Date]

| Activity | Count | Limit | Remaining |
|----------|-------|-------|-----------|
| Posts | 1 | 2 | 1 |
| Comments | 12 | 30 | 18 |
| Connections | 4 | 15 | 11 |
| DMs (new) | 2 | 25 | 23 |
| Likes | 15 | 100 | 85 |
| Profile Views | 8 | 80 | 72 |
```

---

## Premium Account Workflow Optimization

**Read account config:** `shared/linkedin-account-config.md`

### Account-Specific Daily Limits

| Activity | FREE | PREMIUM | SALES NAVIGATOR |
|----------|------|---------|-----------------|
| Searches | ~10/day safe | Unlimited | Unlimited |
| Profile views | 80/day | 150/day | 500/day |
| Connection requests | 15-20/day | 25/day | 50/day |
| InMails | 0 | 5-15/month | 50/month |

### FREE Account Daily Workflow

```
MORNING BLOCK (Optimized for FREE):
→ Rely on cached Recent Post URLs for commenting
→ Avoid searching for new posts (uses search quota)
→ Use inbound signals: notifications, tagged posts

AFTERNOON BLOCK (Optimized for FREE):
→ Check profile viewers (limited to last 5 on free)
→ Use icp-finder INBOUND mode instead of searches
→ Maximize competitor comment thread mining (1 search = many prospects)

EVENING BLOCK (Optimized for FREE):
→ Focus on engagement audit (no searches needed)
→ Cache all data from profile visits
→ Queue prospects for tomorrow instead of searching now
```

### PREMIUM Account Daily Workflow

```
MORNING BLOCK (Premium Advantages):
→ Use Boolean search for finding posts to comment on
→ Example: "[your niche] [target geography]" AND (CEO OR founder) → Find relevant posts

AFTERNOON BLOCK (Premium Advantages):
→ Check ALL profile viewers (90 days available)
→ Use enhanced search filters for prospect discovery
→ Save up to 5 search queries for reuse

EVENING BLOCK (Premium Advantages):
→ Screen all profile viewers from last 90 days
→ Use private browsing when researching competitors
→ Higher profile view limit allows more screening
```

### SALES_NAVIGATOR Daily Workflow

```
MORNING BLOCK (Sales Navigator Advantages):
→ Check Saved Search alerts for new ICP matches (delivered to inbox)
→ View Lead Recommendations for new prospects
→ Use "Posted on LinkedIn recently" filter for active prospects

AFTERNOON BLOCK (Sales Navigator Advantages):
→ Use InMail for NO_COMMENT flagged prospects (bypasses restriction)
→ Check TeamLink for warm intro paths before cold outreach
→ Save all engaged prospects to Lead Lists for tracking

EVENING BLOCK (Sales Navigator Advantages):
→ Review Lead activity timeline (see all your interactions)
→ Check which Leads viewed your profile (engagement tracking)
→ Export weekly leads to CRM if integrated

PASSIVE PROSPECTING (Sales Navigator):
→ Saved searches with alerts do the work for you
→ Check email daily for new ICP matches
→ Algorithm-suggested leads improve over time
```

### InMail Strategy (Premium/Sales Navigator Only)

**When to use InMail (50 credits/month on Sales Navigator):**
- Prospect has NO_COMMENT flag (can't comment on their posts)
- High-value ICP that's hard to reach via comments
- Time-sensitive opportunity

**InMail Template (Value-First):**
```
Subject: Quick question about [their recent post topic]

Hi [Name],

Saw your post on [topic] - really resonated with the point about [specific detail].

Quick question: [relevant question that shows you understand their challenge]

Happy to share what's worked for others in [their industry] if helpful.

[Your name]
```

**InMail Rules:**
- Keep under 100 words
- Reference something specific (shows research)
- Ask a genuine question (not a pitch)
- No attachments or links in first InMail

---

## Day-Specific Content Tasks

Insert the appropriate content task based on day of week.
**Reference:** See `linkedin-elite-post` skill for full posting schedule.

**Monday (Strategy/Planning Day):**
```markdown
## Content Block (Monday)

### 12-Hour Check (ALWAYS do first)
- [ ] Check shared log → Posts Published → Get last post time
- [ ] Calculate hours since last post
- [ ] If < 12 hours: Note next valid posting time (last_post + 12h)

### Post Creation (use linkedin-elite-post + linkedin-trender)
- [ ] Run linkedin-trender to find trending topics in your lane
- [ ] Create a "Week-starter" post:
  - Strategy framework or planning methodology
  - Week ahead predictions or focus areas
  - Strategy content for your target market (from `references/icp-profile.md`)
- [ ] Ensure opening hook is a "Topic Signal"
- [ ] Put any external links in FIRST COMMENT, not post body
- [ ] **Schedule for: 10:00 AM - 11:30 AM (your timezone) (Primary) or 4:00 PM - 5:30 PM (your timezone) (Secondary)** — read timezone from `references/linkedin-strategy.md`
- [ ] **If 12h rule blocks current window → Schedule for next valid window**
```

**Tuesday (Technical Demo Day - PEAK REACH):**
```markdown
## Content Block (Tuesday)

### 12-Hour Check (ALWAYS do first)
- [ ] Check shared log → Posts Published → Get last post time
- [ ] Calculate hours since last post
- [ ] If < 12 hours: Note next valid posting time (last_post + 12h)

### Post Creation (use linkedin-elite-post + linkedin-trender)
- [ ] Run linkedin-trender to find trending topics in your lane
- [ ] Create a "Technical Demo" post (Tuesday = peak technical reach):
  - Video demo of Agentic ERP/CRM prototype
  - Technical walkthrough with screenshots
  - Architecture diagram with explanation
- [ ] Use clear structure for 360Brew semantic reasoning
- [ ] Include specific examples from real implementations
- [ ] **Schedule for: 8:30 AM - 10:30 AM (your timezone) (Primary) or 12:00 PM - 1:30 PM (your timezone) (Secondary)** — read timezone from `references/linkedin-strategy.md`
- [ ] **If 12h rule blocks current window → Schedule for next valid window**
```

**Wednesday (Save-Worthy Asset Day):**
```markdown
## Content Block (Wednesday)

### 12-Hour Check (ALWAYS do first)
- [ ] Check shared log → Posts Published → Get last post time
- [ ] Calculate hours since last post
- [ ] If < 12 hours: Note next valid posting time (last_post + 12h)

### Post Creation (use linkedin-elite-post + linkedin-trender)
- [ ] Run linkedin-trender to find trending topics in your lane
- [ ] Create a "Save-Worthy Asset" post:
  - SQL schema or database structure
  - JSON import logic for automation
  - PRD framework or template
- [ ] Ensure opening hook is a "Topic Signal"
- [ ] Put any external links in FIRST COMMENT, not post body
- [ ] **Schedule for: 9:00 AM - 11:00 AM (your timezone) (Primary) or 3:00 PM - 5:00 PM (your timezone) (Secondary)** — read timezone from `references/linkedin-strategy.md`
- [ ] **If 12h rule blocks current window → Schedule for next valid window**
```

**Thursday (Thought Leadership Day):**
```markdown
## Content Block (Thursday)

### 12-Hour Check (ALWAYS do first)
- [ ] Check shared log → Posts Published → Get last post time
- [ ] Calculate hours since last post
- [ ] If < 12 hours: Note next valid posting time (last_post + 12h)

### Post Creation (use linkedin-elite-post + linkedin-trender)
- [ ] Run linkedin-trender to find trending topics in your lane
- [ ] Create a "Thought Leadership" post:
  - "Frontier Firm" perspective on AI trends
  - Contrarian take on industry trend
  - Prediction about agentic AI future
  - Framework or methodology breakdown
- [ ] Use clear structure (bullet points, headings) for 360Brew semantic reasoning
- [ ] Include specific examples from real implementations
- [ ] **Schedule for: 10:00 AM - 12:00 PM (your timezone) (Primary) or 1:00 PM - 2:30 PM (your timezone) (Secondary)** — read timezone from `references/linkedin-strategy.md`
- [ ] **If 12h rule blocks current window → Schedule for next valid window**
```

**Friday (Reflection Day):**
```markdown
## Content Block (Friday)

### 12-Hour Check (ALWAYS do first)
- [ ] Check shared log → Posts Published → Get last post time
- [ ] Calculate hours since last post
- [ ] If < 12 hours: Note next valid posting time (last_post + 12h)

### Post Creation (use linkedin-elite-post)
- [ ] Create a "Reflection/Story" post:
  - Lesson from a recent industry event or hackathon
  - Teaching moment from training non-coders
  - Personal journey insight
  - Build-in-public update with learnings
  - Team highlights or wins
- [ ] Use first-person narrative for "Human-in-the-loop" trust signal
- [ ] Connect story back to your niche positioning (from `references/icp-profile.md`)
- [ ] **Schedule for: 8:30 AM - 10:00 AM (your timezone) ONLY (No afternoon slot on Friday)** — read timezone from `references/linkedin-strategy.md`
- [ ] **If 12h rule blocks morning window → Skip posting today (no secondary Friday window)**
```

**Saturday/Sunday (Engagement Only):**
```markdown
## Content Block (Weekend - Engagement Focus)

### No Posting Required
- [ ] Focus on commenting and engagement only
- [ ] Optional: Save high-quality posts for Monday content ideas
- [ ] Optional: Draft content for next week
```

## Step 3: Save the To-Do File

Save the generated to-do list with filename format:

```
to-do_DDMMYYYY.md
```

Example: `to-do_19012026.md`

**Save location:** Current working directory or user-specified location.

## Step 4: Offer Execution Support

After creating the to-do, offer to help execute:

```
Your daily LinkedIn plan is ready: to-do_[DATE].md

Would you like me to help you execute any of these tasks now?

1. Run linkedin-trender to find today's trending topics
2. Run linkedin-elite-post to create your content
3. Run linkedin-icp-finder to identify prospects to engage
4. Run linkedin-pro-commenter to draft comments

Which task would you like to start with?
```

## Weekly Audit (Friday Addition)

On Fridays, add a weekly audit section:

```markdown
## Weekly Audit (Friday)

### SSI Score Check
- [ ] Check Social Selling Index at linkedin.com/sales/ssi
- [ ] Target: Score above 75

### Weekly Metrics Review
- [ ] Total posts this week (target: 3-5)
- [ ] Total comments this week (target: 45-75)
- [ ] Total connection requests (target: 50-100)
- [ ] Notable leads or conversations started

### 📊 Pipeline Movement Metrics (NEW - Track Weekly)

**Purpose:** Ensure prospects are moving through the funnel, not just accumulating.

**Read icp-prospects.md and calculate:**

| Metric | This Week | Target | Status |
|--------|-----------|--------|--------|
| 0→1 touch conversions | __ | 10+ | ✅/⚠️/❌ |
| 1→2 touch conversions | __ | 5+ | ✅/⚠️/❌ |
| 2→3 touch conversions | __ | 3+ | ✅/⚠️/❌ |
| Connection requests sent | __ | 10-15 | ✅/⚠️/❌ |
| Connections accepted | __ | 3-5 | ✅/⚠️/❌ |
| Value DMs sent | __ | 5-10 | ✅/⚠️/❌ |

**Pipeline Health Check:**
- [ ] 0-touch backlog count: __ (target: <10)
- [ ] 1-touch backlog count: __ (target: <15)
- [ ] Pending connections >7 days: __ (may not convert)
- [ ] Pending connections >14 days: __ (deprioritize)

**If 0-touch > 20:** PAUSE discovery, focus on warming
**If 1-touch > 15:** PAUSE new touches, focus on 1→2 conversion
**If Pending > 10:** Review connection request quality

### Pending Connection Tracking

**Check icp-prospects.md for pending connections:**
- [ ] Count prospects with Connection Status = "pending"
- [ ] For each: Calculate days since connection request sent
- [ ] Flag 7+ days pending (may need follow-up touch)
- [ ] Flag 14+ days pending (likely won't convert - reduce priority)

**Action for stale pending:**
- Continue touching their posts (shows persistence)
- Do NOT resend connection request (spam signal)
- After 30 days: Consider removing from active pipeline

### Profile Alignment Check (use linkedin-profile-icp)
- [ ] Run linkedin-profile-icp to audit 360Brew compliance
- [ ] Update headline if needed (entity keywords)
- [ ] Update About section if pillars have shifted
- [ ] Check top skills alignment

### 🔍 Sales Navigator Pipeline Refresh (if Account Type = SALES_NAVIGATOR)

**Check account type in:** `shared/linkedin-account-config.md`

**ONLY show this section if Account Type = SALES_NAVIGATOR**

- [ ] Check email for Sales Navigator Saved Search alerts (new ICP matches this week)
- [ ] Open Sales Navigator → Saved Searches → Run 1-2 searches
- [ ] Review top 10-15 results from each search
- [ ] Screen against ICP criteria (from `references/icp-profile.md`)
- [ ] Add 5-10 new ICP matches to `shared/logs/icp-prospects.md`
- [ ] Capture LinkedIn profile URLs during screening
- [ ] Note source in each prospect: "Source: Sales Nav: [Search Name]"

**Saved Searches to Rotate Weekly:**
```
Week 1: [Target market] Decision Makers + [Target geography] Operations Leaders
Week 2: Finance Decision Makers [Target geography] + Recent Job Changers
Week 3: [Target market] Founders [Target geography] + [Your choice]
Week 4: All searches quick scan

> Read target market and geography from `references/icp-profile.md` to populate the search rotation above.
```

**Quick Links (from linkedin-account-config.md):**
- Check Saved Searches section for direct URLs

### ⚠️ Sales Navigator Data Export (CRITICAL - if using Sales Navigator)
- [ ] Export all NEW leads from this week to `icp-prospects.md`
- [ ] Copy any Lead Notes from Sales Navigator to local Notes column
- [ ] Update Profile Cache for all prospects engaged this week
- [ ] Log all InMails sent to `linkedin-activity.md`
- [ ] Document any NEW Saved Searches in `linkedin-account-config.md`
- [ ] Verify all prospect Profile URLs are saved locally

**Why:** Sales Navigator data is DELETED when subscription ends. Local files are your backup.
```

## Shared Activity Log (Token Optimization)

**ALWAYS read from the shared log for daily metrics instead of re-reading LinkedIn.**

**Log location:** `shared/logs/linkedin-activity.md`

### On Each Run:
1. **Read shared log first** to get:
   - Today's comment count (for progress tracking)
   - Today's connection requests count
   - Today's post status
   - High-value interactions needing follow-up
2. **After completing tasks**, update shared log:
   - Update "Today's Summary" section with new activities
   - Update "Weekly Metrics" table
   - Add any new high-value interactions

### For Daily Audit:
Instead of reading LinkedIn activity page, read from shared log:
- Comments Made table → Count and impressions
- Connection Requests table → Sent count
- Posts Published table → Content status
- High-Value Interactions → Follow-up priorities

### What to Log:
All task completions should update the shared log, not just the to-do file.

## Quality Checklist

**Creating new plan:**
- **Account config read** (`shared/linkedin-account-config.md` → Account Type)
- Shared log read first for current metrics
- **Profile Cache read** (icp-prospects.md → Profile Cache table)
- Daily Limits Status table checked
- Correct day of week identified
- Day-specific content task included
- All time blocks present (Morning, Content, Midday, Afternoon, Evening)
- Skills integration table included
- Filename follows to-do_DDMMYYYY.md format
- Friday includes weekly audit section
- **If SALES_NAVIGATOR:** Friday includes "Sales Navigator Pipeline Refresh" section

**Resuming existing plan:**
- Shared log read first for progress data
- Daily Limits Status table checked
- Today's to-do file found and loaded
- Progress accurately parsed (completed vs pending)
- Current time block identified
- Status summary displayed
- Next action offered

**Task completion:**
- Task marked with `[x]` immediately after completion
- Timestamp added (HH:MM format)
- Shared log updated with activity
- **Daily Limits Status updated** (increment count, update remaining)
- File saved after each update
- Next pending task shown to user

**Before EACH engagement action:**
- **CHECK Profile Cache first** → Use cached Recent Post URLs if available
- **SKIP if Activity Status = INACTIVE** (no posts in 30+ days)
- CHECK limit for that action type
- If at limit → Skip and log "Limit reached"
- If approaching limit (80%+) → Warn in output
- After action → Update Daily Limits Status immediately
- **After visiting LinkedIn profile** → Update Profile Cache with new data

## Automation Setup

Single command to run entire workflow autonomously.

### Quick Start

**Option 1: Run directly in Claude Code**
```
start linkedin
```

**Option 2: Run via PowerShell script**
```powershell
.\start-linkedin.ps1
```

**Option 3: Set up alias for easy access**
```powershell
# Add to your PowerShell profile
Set-Alias startlinkedin "C:\Users\melve\.claude\skills\linkedin-daily-planner\scripts\start-linkedin.ps1"

# Then just run:
startlinkedin
```

### Scripts Location

```
linkedin-daily-planner/scripts/
├── start-linkedin.ps1    # Single autonomous trigger
├── daily-launcher.ps1    # Block-specific launcher (optional)
└── setup-scheduler.md    # Windows Task Scheduler setup
```

### Schedule with Windows Task Scheduler

Set up a single daily trigger:

```powershell
# Run once daily at 9:00 AM - AI handles all blocks based on time
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"C:\Users\melve\.claude\skills\linkedin-daily-planner\scripts\start-linkedin.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable
Register-ScheduledTask -TaskName "LinkedIn-Daily" -Action $action -Trigger $trigger -Settings $settings -Description "LinkedIn autonomous workflow"
```

Or run multiple times per day:
```powershell
# Morning, Midday, Afternoon, Evening triggers
@("09:00","12:30","15:00","18:30") | ForEach-Object {
    $time = $_
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"C:\Users\melve\.claude\skills\linkedin-daily-planner\scripts\start-linkedin.ps1`""
    $trigger = New-ScheduledTaskTrigger -Daily -At $time
    Register-ScheduledTask -TaskName "LinkedIn-$time" -Action $action -Trigger $trigger
}
```

### How Autonomous Mode Works

1. **Single trigger** starts Claude Code
2. **AI determines** current time block automatically
3. **AI executes** all tasks for that block without questions
4. **AI auto-selects** best variations for posts/comments
5. **AI logs** everything to shared activity log
6. **AI reports** summary when complete

### What Runs Autonomously

| Block | Autonomous Actions |
|-------|-------------------|
| Morning | Find posts → Generate comments → Post all 9 → Log |
| Content | Find trend → Create post → Generate image → Schedule → Log |
| Midday | Reply to comments → Engage 5-10 posts → Log |
| Afternoon | Check acceptances → Send DMs → Send connections → Log |
| Evening | Full audit → Screen ICPs → Update log → Weekly metrics |

### Late Start Handling

AI automatically detects late starts and compresses tasks:
- Flexible tasks (comments, connections) are done immediately
- Time-sensitive tasks check for secondary windows
- Everything logged regardless of timing
