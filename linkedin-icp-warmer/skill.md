---
name: linkedin-icp-warmer
description: Proactively find engagement opportunities with ICP prospects across the full warming pipeline (0→3 touches). Reads from ICP prospects files (0-touch) AND shared activity log (1-2 touches), then searches their profiles for posts to engage with. Handles first touch initiation and continued warming. Works with browser automation (Claude for Chrome or DevTools fallback). AUTONOMOUS MODE - when called from linkedin-daily-planner, automatically engages all high-priority prospects without user prompts. INTERACTIVE MODE - presents opportunities for user selection.
---

# LinkedIn ICP Warmer

**Browser automation uses Claude for Chrome if available, otherwise falls back to Chrome DevTools. See linkedin-daily-planner skill for detailed tool mapping.**

Proactively hunt for engagement opportunities with ICP prospects across the complete warming pipeline - from first touch to connection-ready.

## Core Purpose

The 2-3 Touch Rule requires multiple engagements before connecting. This skill handles the COMPLETE warming pipeline:

| Touch Count | Source | Action |
|-------------|--------|--------|
| 0 touches | ICP prospects file | Find posts → First engagement → Add to Warming Up |
| 1-2 touches | Warming Up table | Find new posts → Continue warming |
| 3 touches | - | Move to Ready to Connect |

## Trigger

Activate when user says:
- "warm up my ICPs"
- "find posts from prospects"
- "who needs more engagement"
- "warmup opportunities"
- "continue warming"
- "check prospect posts"
- "find lookalike prospects"
- "harvest profile recommendations"
- "expand from [prospect name]"
- "discover similar prospects"

## Workflow

### Step 0: Blacklist Check (MANDATORY FIRST STEP)

**CRITICAL: Before identifying ANY prospect for warming, check the blacklist.**

**File location:** `shared/logs/linkedin-blacklist.md`

```
BEFORE WARMING ANY PROSPECT:
1. Read linkedin-blacklist.md
2. Check if prospect name OR profile URL appears in blacklist
3. If FOUND → SKIP ENTIRELY, remove from warming pipeline
4. If NOT FOUND → Proceed with warming workflow
```

**This check overrides ALL other criteria. Never engage with blacklisted contacts.**

---

### Step 0a: Cache-First Check (Minimize LinkedIn Visits)

**CRITICAL: Check Profile Cache before visiting ANY LinkedIn profile.**

**File locations (check BOTH):**
- `shared/logs/icp-prospects.md` → Profile Cache table
- `shared/logs/inbound-screening-history.md` → Profile Cache section

**Cross-Check Workflow:** See `shared/references/signal-screening-workflow.md` for complete protocol

```
BEFORE VISITING PROSPECT PROFILE:
1. Check Blacklist FIRST:
   → grep -i "prospect name" shared/logs/linkedin-blacklist.md
   → IF FOUND: SKIP entirely, remove from warming pipeline

2. Check Profile Cache (both files):
   → grep -i "prospect name" shared/logs/inbound-screening-history.md
   → OR check Profile Cache table in icp-prospects.md
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

**Use Cached Data When Available:**
- Recent Post URLs → Engage with these posts directly (no profile visit needed)
- Activity Status → Skip INACTIVE prospects
- Last Post date → Know if they've posted recently

**Update Cache After Each Visit:**
When you DO visit LinkedIn, capture and update:
- Last Checked = current timestamp
- Activity Status = ACTIVE/MODERATE/INACTIVE
- Last Post = date of most recent post
- Recent Post URLs = up to 3 post URLs
- Engagement Score = posts/week estimate
- **Email = extract if visible** (see Email Extraction below)
- **Add to Profile Cache in inbound-screening-history.md** (not just icp-prospects.md)

---

### Step 0d: Email Extraction (Capture When Available)

**ALWAYS attempt to extract email when visiting any prospect profile or website.**

#### LinkedIn Email Sources

1. **Contact Info Section (1st-degree connections only)**
   ```
   WORKFLOW:
   1. Click "Contact info" button on profile
   2. Look for email field in popup
   3. If email found → Update icp-prospects.md Email column
   ```

2. **About Section (sometimes displayed)**
   ```
   WORKFLOW:
   1. Read About section text
   2. Look for email patterns: [text]@[domain].[tld]
   3. Common formats: name@company.com, firstname.lastname@company.com
   ```

3. **Featured/Links Section**
   ```
   WORKFLOW:
   1. Check Featured section for personal website links
   2. Visit company website → Look for team/about page
   3. Extract email from contact page or footer
   ```

#### Company Website Email Discovery

When you have company URL (from Company URL column or discovered):

```
WORKFLOW:
1. Navigate to company website
2. Check these pages in order:
   - /contact or /contact-us
   - /about or /about-us → Team section
   - /team or /our-team
   - Footer (email often in footer)
3. Look for prospect's name + email
4. If no direct email, note email pattern: format@company.com
```

#### Email Pattern Detection

If you can't find direct email but find company email pattern:

```
COMMON PATTERNS:
- firstname@company.com
- firstname.lastname@company.com
- f.lastname@company.com
- firstnamelastname@company.com

SAVE AS:
- If certain: actual email
- If pattern-based: "[likely] firstname@company.com"
```

#### Update icp-prospects.md

After extracting email:

```
LOCATE prospect row in icp-prospects.md
UPDATE Email column:
- From: TBD
- To: actual.email@company.com

ALSO UPDATE Notes:
- Append: "Email captured [date] from [source: LinkedIn/Website/Pattern]"
```

---

---

### Step 0c: Premium Account Optimization

**Read account config:** `shared/linkedin-account-config.md`

#### FREE Account Warming Strategy

**Constraints:** Limited profile views, no InMail

```
WARMING OPTIMIZATION (FREE):
1. Prioritize prospects with cached Recent Post URLs
   → Engage directly without profile visit

2. Focus on comment-based warming
   → Comments visible to non-connections
   → Build public relationship first

3. Skip prospects with NO_COMMENT flag quickly
   → Cannot warm via comments
   → Move to next prospect

4. Use profile views sparingly (80/day limit)
   → Only visit when cache is stale (>7 days)
```

#### PREMIUM Account Warming Strategy

**Advantages:** More profile views, see all viewers

```
WARMING OPTIMIZATION (PREMIUM):
1. Higher profile view limit (150/day)
   → Can check more prospect activity feeds

2. See all profile viewers
   → Check if prospects viewed YOU after engagement
   → Strong signal they noticed your comment

3. Use private browsing mode strategically
   → Research competitors without alerting them
   → Turn OFF when warming prospects (you WANT them to see you)
```

#### SALES_NAVIGATOR Warming Strategy

**Advantages:** InMail, lead tracking, engagement insights

```
WARMING OPTIMIZATION (SALES NAVIGATOR):

🔥 PRIORITY #1: "POSTED ON LINKEDIN" FILTER (ALWAYS ENABLE FIRST)

When searching for NEW prospects to warm, ALWAYS use the "Posted on LinkedIn"
filter in Sales Navigator. This is THE most efficient way to find warm-able
prospects because every search result has recent posts to engage with.

WORKFLOW FOR NEW PROSPECT DISCOVERY + WARMING:
1. Open Sales Navigator saved search (with ICP filters)
2. Enable "Posted on LinkedIn" filter (under Spotlight section)
3. For each prospect found:
   → View their recent post directly in Sales Navigator
   → Click to open full post on LinkedIn
   → Comment using linkedin-pro-commenter
   → Save prospect to icp-prospects.md with 1 touch
4. Result: Every prospect discovered is immediately engaged

WHY THIS IS PRIMARY STRATEGY:
→ Eliminates inactive prospects from search results
→ Guaranteed engagement opportunity with each prospect
→ Combines discovery + first touch in one workflow
→ Most efficient use of Sales Navigator features

2. INMAIL FOR STUCK PROSPECTS:
   If prospect has NO_COMMENT flag (non-connections blocked):
   → Use InMail to bypass comment restriction
   → Template: "Saw your post on [topic]. Quick question: [relevant question]?"
   → Counts as a touch in warming pipeline

3. LEAD TRACKING:
   → Save warming prospects as "Leads" in Sales Navigator
   → Track all your activity on them in one place
   → See when they post new content (notifications)

4. ENGAGEMENT INSIGHTS:
   → Sales Navigator shows when lead was last active
   → Prioritize recently active leads
   → Skip leads inactive for 30+ days

5. HIGHER LIMITS:
   → Profile views: 500/day
   → Can warm many more prospects per session
```

---

### Step 1: Read Prospect Sources

The skill reads from TWO sources to cover the complete warming pipeline (0→3 touches).

#### Step 1A: Read ICP Prospects File (0-touch prospects)

**File location:** `shared/logs/icp-prospects.md`

Single consolidated file containing all discovered prospects with Date Found column.

```
FROM ICP prospects file, find:
1. All prospects not yet in Warming Up table
2. Check each prospect's Profile URL against Warming Up table
3. If NOT in Warming Up → This is a 0-touch prospect

FILTER for:
- Classification = PROSPECT (skip THOUGHT LEADER for first touch)
- Not already in Warming Up table (check by Profile URL)
- Not already Connected or Pending Acceptance
```

#### Step 1B: Read Shared Activity Log (1-2 touch prospects)

**Log location:** `shared/logs/linkedin-activity.md`

```
FROM shared log, find:
1. "Warming Up" pipeline → Prospects with 1-2 touches
2. "Comments Made" (last 7 days) → Authors you've engaged with once
3. "High-Value Interactions" → Warm leads needing follow-up

FILTER for:
- Touches < 3 (not yet ready for connection)
- Last engagement > 24 hours ago (give time for new content)
- Not already in "Pending Acceptance" or "Connected"

FILTER OUT prospects with Flags (check "Flags" column in Warming Up table):
- ⚠️ NO_COMMENT → Cannot comment on their posts (non-connections blocked)
- ⚠️ INACTIVE → Low priority (no recent posts to engage with)
- Any other flag starting with ⚠️ → Skip and note reason
```

### Step 2: Prioritize Prospects

**⚠️ PIPELINE HEALTH CHECK FIRST (Before Prioritizing)**

Before ranking by touch count, check pipeline health:

```
READ icp-prospects.md AND COUNT:
- 0-touch prospects: __
- 1-touch prospects: __
- 2-touch prospects: __
- Pending connections: __

IF 0-touch > 20:
  → PAUSE discovery mode
  → Focus 70% on warming 0-touch prospects
  → Only add 2-3 new prospects max

IF 1-touch > 15:
  → Focus on 1→2 conversion
  → Target: Move 3-5 prospects from 1→2 touch today

HEALTHY PIPELINE:
  → 0-touch < 10, 1-touch < 15, 2-touch growing
  → Normal prioritization applies
```

---

Rank prospects by warmup priority:

**🔥 CRITICAL: 1-TOUCH → 2-TOUCH CONVERSION (Process First)**
- 1 touch so far, last engagement > 3 days ago
- **Why priority:** Pipeline analysis shows 1-touch → 2-touch is biggest gap
- Action: Find second post to comment on → Move to 2-touch (warm)
- **Target:** Convert 3+ prospects from 1→2 touch per day

**🔥 HIGH PRIORITY (Engage Today)**
- 2 touches already (one more = ready to connect)
- Replied to your previous comment
- High-value ICP signal (decision-maker, pain points visible)

**🟡 MEDIUM PRIORITY: 0-TOUCH BACKLOG (Clear Before Discovery)**
- 0 touches, oldest first (FIFO - first in, first out)
- **Why priority:** 64% of pipeline stuck at 0-touch = discovery without warming
- Action: Find their posts → First comment → Move to 1-touch
- **Target:** Clear 3+ prospects from 0-touch per day

**🆕 NEW PROSPECTS (Only After Backlog Under Control)**
- 0 touches (from ICP prospects file)
- Strong ICP match (decision-maker at SME)
- Has recent posts to engage with
- **NOTE:** Only discover new if 0-touch backlog < 10 prospects

**🟢 COMMENT_ACTIVE (Warm via Comment Hunting)**
- Prospect flagged COMMENT_ACTIVE by Scheduled Comment Monitoring
- Doesn't post but actively comments on others' posts
- Strategy: Find their comments → Reply with substance → Counts as touch
- Check `/in/[username]/recent-activity/comments/` for reply opportunities

**⚪ LOW PRIORITY (Monitor)**
- 1 touch, no recent posts
- Unclear ICP fit
- INACTIVE poster (pending Scheduled Comment Monitoring rotation)
- INACTIVE_VERIFIED (confirmed zero activity - monthly check only)

### Step 3: Search for New Posts

For each prioritized prospect:

1. **Navigate to their profile activity:**
   ```
   https://www.linkedin.com/in/[username]/recent-activity/all/
   ```

2. **Scan for posts from last 7 days:**
   - Native posts (not reshares)
   - Posts you haven't commented on yet
   - Posts with engagement potential (5+ reactions = active discussion)

3. **Record opportunities found:**
   - Post URL
   - Post topic/summary
   - Post age (days)
   - Current engagement level

### Step 4: Cross-Reference Engagement History

For each new post found, check shared log:
- Have you already commented on this post? → Skip
- Have you liked/saved this post? → Comment opportunity (adds touch)
- Fresh post, no engagement? → Full opportunity

### Step 5: Output Warmup Opportunities

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICP WARMUP OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: [Date/Time]
Prospects scanned: [X]
Opportunities found: [Y]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 HIGH PRIORITY (2 touches → ready after this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Name] - [Title] at [Company]
   Profile: [Profile URL]
   Current touches: 2

   📝 NEW POST FOUND:
   Post URL: [URL]
   Topic: [Brief summary]
   Posted: [X days ago]
   Engagement: [Y reactions, Z comments]

   Action: Comment → Then ready for connection request
   Suggested angle: [Based on post content + your positioning]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟡 MEDIUM PRIORITY (1 touch → need 2 more)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Name] - [Title] at [Company]
   Profile: [Profile URL]
   Current touches: 1

   📝 NEW POST FOUND:
   Post URL: [URL]
   Topic: [Brief summary]
   Posted: [X days ago]

   Action: Comment → 2 touches, need 1 more after

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆕 FIRST TOUCH NEEDED (0 touches → start warming)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Name] - [Title] at [Company]
   Profile: [Profile URL]
   Source: icp-prospects.md (found [Date Found])
   Current touches: 0

   📝 POST FOUND:
   Post URL: [URL]
   Topic: [Brief summary]
   Posted: [X days ago]
   Engagement: [Y reactions, Z comments]

   Action: Comment → Adds to Warming Up table with 1 touch
   Suggested angle: [Based on post content + your positioning]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚪ NO NEW POSTS FOUND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Name] - Last post: [X days ago] - Monitor for new content
[Name] - Last post: [X days ago] - Monitor for new content

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚫 SKIPPED (Flagged Prospects)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Name] - Flag: NO_COMMENT (non-connections blocked)
[Name] - Flag: INACTIVE (no recent posts)

Note: These prospects have limitations that prevent standard warmup.
Alternative warmup: Likes, saves, or wait for them to post/allow comments.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
High priority (2 touches): [X]
Medium priority (1 touch): [Y]
First touch needed (0 touches): [Z]
Prospects with no new posts: [N]
Skipped (flagged): [M]

Recommended: Start with high priority, then first touches to expand pipeline
```

### Step 6: Integrate with Comment Generation

**AUTONOMOUS MODE (when called from linkedin-daily-planner):**
- Automatically engage with ALL high-priority (🔥) prospects first
- Then engage with medium-priority (🟡) prospects until daily comment limit
- For each prospect:
  1. Read the post content
  2. Invoke linkedin-pro-commenter with post context (AI auto-selects)
  3. Post comment via Claude for Chrome
  4. Update shared log with new touch
  5. Move to next prospect immediately
- No user prompts, no confirmations, fully automated

**INTERACTIVE MODE (when called directly by user):**

After presenting opportunities, offer:

```
Which prospect would you like to engage with?

I'll use linkedin-pro-commenter to generate a comment for their post.

Or say "engage all high priority" to generate comments for all 🔥 posts.
```

When user selects a prospect:
1. Read the post content
2. Invoke linkedin-pro-commenter with post context
3. After comment is posted, update shared log with new touch

## Shared Activity Log Integration

**Log location:** `shared/logs/linkedin-activity.md`

### On Each Run:
1. **Read shared log first** to identify warming prospects
2. **Only access LinkedIn profiles** for prospects needing warmup
3. **Update shared log** after finding opportunities:
   - Add new posts found to prospect records
   - Update "Last Post Seen" dates

### After Engagement:
When a warmup comment is posted:

**For 0-touch prospects (first engagement):**
1. Add prospect to "Warming Up" table in shared log with:
   - Name, Profile URL from prospects file
   - First Touch = today's date + engagement type (Comment)
   - Touches = 1
   - Needed = 1-2 more
   - Flags = (empty unless issue discovered)
2. Log the comment in "Comments Made" table
3. Prospect now appears in future warmer runs as 1-touch

**For 1-2 touch prospects (continuing warmup):**
1. Update prospect's touch count in shared log (increment by 1)
2. Update "Last Post Seen" date
3. Move to "Ready to Connect" if now at 3 touches
4. Log the comment in "Comments Made" table

### What to Log:
**Warmup runs:**
```
| Date | Prospects Scanned | Opportunities Found | Comments Made | Moved to Ready |
```

## Contact Classification Context

**Reference:** `references/contact-classification.md`

Warmup priority should consider contact type:

| Category | Warmup Priority | Rationale |
|----------|-----------------|-----------|
| PROSPECT (ICP) | HIGHEST | Direct lead generation value |
| PEER (1K-10K) | HIGH | Collaboration potential, mutual engagement |
| THOUGHT LEADER (10K+) | MEDIUM | Visibility benefit, harder to convert |

## Quality Checklist

Before presenting warmup opportunities:
- [ ] **ICP prospects file read** (shared/logs/icp-prospects.md) for 0-touch prospects
- [ ] **Shared log read** for 1-2 touch prospects
- [ ] **Flags column checked** - skip prospects with NO_COMMENT, INACTIVE flags
- [ ] 0-touch prospects not already in Warming Up table
- [ ] 1-2 touch prospects: last engagement was 24+ hours ago
- [ ] Posts are from last 7 days
- [ ] Posts not already engaged with
- [ ] Profile URLs included for quick navigation
- [ ] Post URLs included for quick access
- [ ] Touch count accurate (0, 1, or 2)
- [ ] Priority correctly assigned (🔥, 🟡, 🆕, ⚪)
- [ ] **Flagged prospects listed in "Skipped" section with reason**
- [ ] **0-touch prospects listed in "First Touch Needed" section**

After warmup engagement:
- [ ] **0-touch: Added to Warming Up table** with touch count = 1
- [ ] **1-2 touch: Touch count incremented** in Warming Up table
- [ ] **3 touches: Moved to Ready to Connect**
- [ ] Comments Made table updated
- [ ] Warmup run logged

## Edge Cases

**No ICP prospects file found:**
```
ICP prospects file not found at shared/logs/icp-prospects.md

Options:
1. Run linkedin-icp-finder to discover new prospects
2. Manually create icp-prospects.md with prospects
3. Continue with Warming Up table prospects only
```

**All 0-touch prospects already in Warming Up:**
```
All ICP prospects from icp-prospects.md are already in Warming Up table.

This means first touch has been completed for all discovered prospects.
Continue warming existing prospects or run linkedin-icp-finder for new ones.
```

**No warming prospects in log (and no 0-touch prospects):**
```
No prospects currently in warmup phase (0, 1, or 2 touches).

Options:
1. Run linkedin-icp-finder to discover new prospects
2. Check if recent engagements need to be logged
3. Review "Comments Made" for potential prospects to track
```

**Prospect has no new posts:**
```
[Name] hasn't posted in [X] days.

Options:
1. Engage with their comments on others' posts
2. Save one of their older posts (counts as touch)
3. Wait and check again in a few days
```

**All prospects already at 3+ touches:**
```
All tracked prospects are ready for connection!

Run linkedin-connect-timer to see who to connect with today.
```

**Prospect doesn't allow non-connection comments:**
```
[Name] has comment restrictions (non-connections cannot comment).

Action: Add flag to Warming Up table:
| Name | ... | Flags |
| [Name] | ... | ⚠️ NO_COMMENT (non-connections blocked) |

Alternative warmup methods:
1. Like their posts instead (weaker signal but still counts)
2. Save their posts (private, no notification to them)
3. Wait until connected to comment
4. Engage with their comments on others' posts (if visible)
```

**Prospect is inactive (no posts in 30+ days):**
```
[Name] hasn't posted in 30+ days.

Action: Add flag to Warming Up table:
| Name | ... | Flags |
| [Name] | ... | ⚠️ INACTIVE (last post 30+ days ago) |

Options:
1. Lower priority in warmup queue
2. **🎯 COMMENT HUNTING** - Find their comments on others' posts (see below)
3. Check back monthly for new activity
```

---

### Comment Hunting: Warming INACTIVE Posters Who Actively Comment

**Problem:** Some high-value ICP prospects don't post content but actively comment on others' posts. Standard warming (comment on their posts) doesn't work because they have no posts to comment on.

**Solution:** Find their comments on others' posts and reply to those comments. This creates a touchpoint while they're actively engaged.

#### When to Use Comment Hunting

| Prospect Status | Activity Pattern | Use Comment Hunting? |
|-----------------|------------------|---------------------|
| INACTIVE (no posts 30+ days) | Actively comments on others | ✅ YES - Primary strategy |
| INACTIVE | No comments visible | ❌ NO - Wait or deprioritize |
| ACTIVE (posts regularly) | N/A | ❌ NO - Use standard warming |

#### Comment Hunting Workflow

**Step 1: Navigate to Prospect's Comments Tab**
```
https://www.linkedin.com/in/[username]/recent-activity/comments/
```

**Step 2: Find Recent Comments (Last 7 Days)**
- Look for comments on posts with active discussions
- Prefer comments where prospect shared substantive insight
- Skip one-word reactions ("Great!", "Agreed", "Thanks")

**Step 3: Assess Comment Quality for Reply**

| Comment Type | Reply Potential | Action |
|--------------|-----------------|--------|
| Substantive insight (technical, strategic) | HIGH | Reply with additional perspective |
| Question asked | HIGH | Answer or add related insight |
| Opinion/take on topic | MEDIUM | Agree + extend OR respectfully contrast |
| Simple agreement | LOW | Skip - find better comment |

**Step 4: Generate and Post Reply**

Use linkedin-pro-commenter with these adjustments:
- Reference their specific point (shows you read it)
- Add YOUR expertise angle (positions you as peer)
- Keep concise (30-50 words max for replies)
- End with insight, not question (replies don't need thread-driving)

**Example Reply Structure:**
```
"Your [specific point] resonates - [why]. We're seeing [related observation/data point].
The [topic] angle you mentioned is especially relevant for [your ICP context]."
```

**Step 5: Update Tracking**

After successful comment reply:
```
icp-prospects.md:
- Touches: increment +1
- Last Touch: today's date
- Touch History: append "comment reply"
- Notes: append "Touch X: Reply to comment on [Author]'s [Topic] post - COMMENT HUNTING"
```

#### Comment Hunting Example

**Prospect:** Dr. Andrew Ang (INACTIVE - hasn't posted in 30+ days)
**Found:** His comment on Rod Askarov's post about Meta's $2B Manus acquisition
**His comment:** Discussed TRL (Technology Readiness Levels) for AI agent maturity
**Your reply:** "Your TRL analogy is spot on. The leap from TRL 4-6 (demonstration) to TRL 7-9 (production) is where most AI tools fail. Especially true for enterprise agentic systems needing audit trails and rollback capabilities."

**Result:** 1 touch added without needing prospect to post anything.

#### Efficiency Considerations

| Method | Time per Touch | Reliability | Best For |
|--------|---------------|-------------|----------|
| Standard (comment on their post) | 2-3 mins | HIGH | ACTIVE prospects |
| Comment Hunting (reply to their comment) | 5-7 mins | MEDIUM | INACTIVE prospects with visible comments |
| InMail (Sales Navigator) | 3-5 mins | MEDIUM | NO_COMMENT flagged prospects |

**When to deprioritize INACTIVE prospects:**
- No visible comments in last 30 days
- Comments are low-quality (one-word only)
- Time investment exceeds value (many other prospects available)

#### Best Comment Topics for Reply

| Topic in Original Post | Your Reply Angle |
|------------------------|------------------|
| AI strategy/trends | SME implementation perspective |
| Technical architecture | Practical considerations from builds |
| Enterprise adoption | Decision-maker challenges you've observed |
| Industry predictions | Data/evidence from your experience |

---

### Scheduled Comment Monitoring (Daily Rotation)

**Problem:** 200+ INACTIVE prospects sitting in pipeline with no way to detect when they become active commenters. Comment Hunting is currently manual/reactive - this section formalizes it into a scheduled daily rotation.

**Goal:** Systematically rotate through ALL INACTIVE prospects' comment tabs to find hidden engagement opportunities and accurately classify prospect activity patterns.

#### Rotation Schedule

| Metric | Target |
|--------|--------|
| **Daily check** | 5 INACTIVE prospects |
| **Full cycle** | ~100 INACTIVE prospects every 20 days |
| **Recheck interval** | Every 14 days per prospect |
| **Time per check** | ~1 minute per prospect |
| **Total daily time** | ~5 minutes |

#### Comment Check Workflow (Per Prospect)

```
1. Navigate to: https://www.linkedin.com/in/[username]/recent-activity/comments/
2. Scan for comments in last 14 days
3. Classify result:

IF substantive comments found (technical, strategic, question):
   → STATUS: COMMENT_ACTIVE
   → ACTION: Execute Comment Hunting reply workflow (see above)
   → UPDATE icp-prospects.md Notes:
     - Replace "INACTIVE" with "COMMENT_ACTIVE"
     - Append: "Comment Monitor [date]: Active commenter found - [topic area]"
   → This prospect is now elevated in warming priority

IF only low-quality comments ("Great!", "Thanks", emoji-only):
   → STATUS: INACTIVE (unchanged)
   → UPDATE Notes: append "Comment Check [date]: Low-quality comments only"
   → Recheck in 14 days

IF no comments visible:
   → STATUS: INACTIVE (unchanged)
   → UPDATE Notes: append "Comment Check [date]: No activity"
   → After 3 consecutive "No activity" checks:
     - Replace "INACTIVE" with "INACTIVE_VERIFIED"
     - Deprioritize in rotation (check monthly instead of bi-weekly)
```

#### Status Transitions

```
INACTIVE (default for 30+ day non-posters)
    │
    ├──→ COMMENT_ACTIVE (found substantive comments)
    │       → Elevated priority in warming pipeline
    │       → Use Comment Hunting for touches
    │       → Recheck every 14 days to confirm continued activity
    │
    ├──→ INACTIVE (still no posts, but comments found are low-quality)
    │       → Keep in rotation, recheck in 14 days
    │
    └──→ INACTIVE_VERIFIED (3 consecutive "No activity" checks)
            → Deprioritize to monthly rotation
            → Consider removing from pipeline after 3 months
```

#### Priority Ranking (Updated)

| Status | Warming Priority | Strategy |
|--------|-----------------|----------|
| ACTIVE (posts regularly) | HIGHEST | Standard warming (comment on posts) |
| **COMMENT_ACTIVE** (doesn't post but comments) | **HIGH** | **Comment Hunting (reply to their comments)** |
| MODERATE (posts 7-30 days) | MEDIUM | Standard warming when posts appear |
| INACTIVE (not yet checked or recently active) | LOW | Scheduled Comment Monitoring rotation |
| INACTIVE_VERIFIED (confirmed zero activity) | LOWEST | Monthly check, consider pipeline removal |

#### Tracking Format

In `icp-prospects.md` Notes column, append structured check results:

```
Comment Check 06Feb: Active commenter - AI strategy topics → COMMENT_ACTIVE
Comment Check 06Feb: Low-quality comments only
Comment Check 06Feb: No activity [1/3]
Comment Check 20Feb: No activity [2/3]
Comment Check 06Mar: No activity [3/3] → INACTIVE_VERIFIED
```

#### Integration with Morning Block

The linkedin-daily-planner runs this rotation as "INACTIVE Comment Monitor" in the Morning Block:
- Sub-agent filters INACTIVE prospects due for check (not checked in 14 days)
- Returns max 5, sorted by oldest unchecked first
- Main thread executes browser navigation and comment scanning
- Results logged to icp-prospects.md and activity log

---

## Profile Recommendations Discovery (NEW)

**Strategy:** Leverage LinkedIn's algorithm to find lookalike prospects from profile recommendations.

When viewing any prospect's profile, LinkedIn displays similar profiles in a right sidebar section labeled:
- "More profiles for you" OR
- "People you may want to know"

These recommendations are algorithmically clustered by role, industry, location, and network - making them high-probability ICP matches.

### Discovery Workflow

**Step 1: Navigate to Existing Prospect Profile**
```
When warming any prospect (0, 1, or 2 touches):
→ Navigate to their LinkedIn profile
→ Look for right sidebar recommendations section
```

**Step 2: Extract Recommendation Data**

For each recommended profile, capture:
- Name
- Role/Title
- Company name
- Location
- Profile URL
- Follower count (if visible)
- Connection degree (1st, 2nd, 3rd)

**Step 3: ICP Qualification Check**

Evaluate against core criteria:

| Criteria | Check |
|----------|-------|
| **Role** | Founder, CEO, COO, Operations Director, CFO, CTO (decision-makers) |
| **Company Size** | SME (20-500 employees typically) |
| **Location** | Your target geography (from `references/icp-profile.md`) |
| **Industry** | Your target industries (from `references/icp-profile.md`) |
| **Pain Signals** | Manual processes, scaling challenges, operational inefficiency visible in headline/about |

**Step 4: Save Qualified Prospects**

Add to `icp-prospects.md`:
```
| # | Name | Date Found | Role | Company | Company URL | Location | Classification | Touches | Last Touch | Touch History | Connection Status | Profile URL | Email | Notes |
|---|------|------------|------|---------|-------------|----------|----------------|---------|------------|---------------|-------------------|-------------|-------|-------|
| X | [Name] | [DDMon] | [Title] | [Company] | TBD | [City, Country] | PROSPECT | 0 | - | - | none | [LinkedIn URL] | TBD | Source: LinkedIn Profile Rec from [Original Prospect Name] \| [Brief ICP fit reasoning] \| Score: [X/100] |
```

**Source notation format:**
`Source: LinkedIn Profile Rec from [Original Prospect Name]`

**Step 5: Iterate Through Seed Prospects**

Use existing high-quality prospects as seeds:
- Start with strongest ICP matches (Score 80+)
- Harvest recommendations from their profiles
- Create a "lookalike network" of similar decision-makers

### Integration Points

**During ICP Warming:**
- When visiting prospect profile for engagement
- Also harvest profile recommendations
- Saves time: 1 profile visit = warming + discovery

**During Algorithm Training (Morning Block):**
- Visit 5-10 prospect profiles to prime feed
- Extract recommendations from each
- Expand pipeline while training algorithm

**Dedicated Discovery Sessions:**
- Pick 3-5 seed prospects (high ICP fit)
- Systematically harvest all recommendations
- Can discover 15-30 new prospects per session

### Efficiency Metrics

| Method | Time per Prospect | Quality | Yield |
|--------|-------------------|---------|-------|
| Profile Recommendations | 30 sec/profile | HIGH (algorithm clustered) | 3-5 prospects per seed |
| Manual LinkedIn Search | 2-3 min/search | MEDIUM (broad results) | Variable |
| Sales Navigator "Posted on LinkedIn" | 1-2 min/prospect | HIGH (active posters) | High but limited to active |

**Best Practice:** Combine methods
1. Use Sales Navigator "Posted on LinkedIn" for immediate engagement opportunities
2. Use Profile Recommendations for pipeline expansion
3. Prioritize prospects discovered via recommendations from your best ICP matches

### Example Workflow

```
SEED PROSPECT: Didi Gan (N&E Innovations Founder, Score 80/100)

Visit profile → Right sidebar shows:
1. Jaslyn Lee (N&E Innovations CTO) → Already in pipeline ✓
2. Chen Wei (GreenTech Co-Founder) → NEW, similar sustainability SME → ADD
3. Sarah Tan (EcoSolutions CEO) → NEW, F&B waste management → ADD
4. Michael Lim (BioCircular Founder) → NEW, circular economy focus → ADD

RESULT: 3 new high-quality prospects from 1 profile visit
```

### Quality Checklist

Before adding recommended profile to prospect list:
- [ ] Decision-maker role confirmed
- [ ] SME company size (check "About" section for employee count)
- [ ] Target geography location (from `references/icp-profile.md`)
- [ ] Relevant industry for your positioning
- [ ] No red flags (job seeker, student, consultant without company)
- [ ] Not already in icp-prospects.md (check by name)
- [ ] Not in blacklist (check shared/logs/linkedin-blacklist.md)

### When to Use This Method

**HIGH PRIORITY - Use Profile Recommendations:**
- After engaging with a strong ICP match (warm them + expand from them)
- During morning algorithm training visits
- When 0-touch backlog < 10 (actively growing pipeline)
- When you have 10+ strong seed prospects to expand from

**LOW PRIORITY - Skip Profile Recommendations:**
- When 0-touch backlog > 20 (focus on warming existing)
- When seed prospect is weak ICP fit (recommendations likely also weak)
- When time-constrained (focus on engagement only)

---

## Integration with Other Skills

| After This Skill | Use |
|------------------|-----|
| Found warmup opportunity | `linkedin-pro-commenter` to generate comment |
| Prospect reached 3 touches | `linkedin-connect-timer` to send request |
| Need more prospects | `linkedin-icp-finder` to discover new ICPs |
| Plan daily warmup | `linkedin-daily-planner` to schedule |

## Logging

**Log file:** `linkedin-icp-warmer/logs/warmup-runs.md`

Track each warmup search:
```
## Warmup Run - [Date]

ICP Prospects File: shared/logs/icp-prospects.md
0-Touch Prospects Found: [Y]

Warming Up Table Scanned:
1-2 Touch Prospects: [Z]

Prospects scanned: [Total]
- [Name]: 0 touches (NEW), [Post found / No posts]
- [Name]: 1 touch, [New post found / No new posts]
- [Name]: 2 touches, [New post found / No new posts]

Opportunities found: [Y]
- First touch needed: [A]
- Continued warming: [B]

Comments generated: [Z]
Added to Warming Up: [N] (0→1 touch)
Moved to Ready: [M] (2→3 touches)
```

Also update `shared/logs/linkedin-activity.md` with any new engagement data.
