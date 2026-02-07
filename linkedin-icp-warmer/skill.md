---
name: linkedin-icp-warmer
description: Proactively find engagement opportunities with ICP prospects across the full warming pipeline (0→3 touches). Reads from ICP prospects files (0-touch) AND shared activity log (1-2 touches), then searches their profiles for posts to engage with. Handles first touch initiation and continued warming. Outputs prioritized list of warmup opportunities with post URLs for quick action.
---

# LinkedIn ICP Warmer

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

## Workflow

### Step 0: Cache-First Check (Minimize LinkedIn Visits)

**CRITICAL: Check Profile Cache before visiting ANY LinkedIn profile.**

**File location:** `shared/logs/icp-prospects.md` → Profile Cache table

```
BEFORE VISITING PROSPECT PROFILE:
1. Read Profile Cache table in icp-prospects.md
2. Find prospect by Profile URL
3. Check "Last Checked" column:
   → If < 7 days old AND has Recent Post URLs → USE CACHED DATA
   → If >= 7 days old OR no Recent Posts → VISIT LINKEDIN
4. Check "Activity Status" column:
   → If INACTIVE → SKIP (no posts in 30+ days)
   → If ACTIVE/MODERATE → Proceed
```

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

---

### Step 0b: Premium Account Optimization

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

1. INMAIL FOR STUCK PROSPECTS:
   If prospect has NO_COMMENT flag (non-connections blocked):
   → Use InMail to bypass comment restriction
   → Template: "Saw your post on [topic]. Quick question: [relevant question]?"
   → Counts as a touch in warming pipeline

2. LEAD TRACKING:
   → Save warming prospects as "Leads" in Sales Navigator
   → Track all your activity on them in one place
   → See when they post new content (notifications)

3. ENGAGEMENT INSIGHTS:
   → Sales Navigator shows when lead was last active
   → Prioritize recently active leads
   → Skip leads inactive for 30+ days

4. "POSTED ON LINKEDIN" FILTER:
   → When scanning for warmup opportunities
   → Use filter to only see prospects who posted recently
   → Saves time vs. visiting inactive profiles

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

Rank prospects by warmup priority:

**🔥 HIGH PRIORITY (Engage Today)**
- 2 touches already (one more = ready to connect)
- Replied to your previous comment
- High-value ICP signal (decision-maker, pain points visible)

**🟡 MEDIUM PRIORITY (Engage This Week)**
- 1 touch so far (need 2 more)
- No reply yet but strong ICP fit
- Posted actively in last 7 days

**🆕 NEW PROSPECTS (First Touch Needed)**
- 0 touches (from ICP prospects file)
- Strong ICP match (decision-maker at SME)
- Has recent posts to engage with
- Initiating first engagement starts the warming process

**⚪ LOW PRIORITY (Monitor)**
- 1 touch, no recent posts
- Unclear ICP fit
- Inactive poster

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

### Step 4: Cross-Reference Engagement History (COMMENT DEDUP CHECK)

**ONE COMMENT PER POST - NEVER comment on the same post twice.**

For each new post found, check BOTH sources:

**Source 1: "Already Commented" Set (in-memory, built during session pre-flight)**
- This set is built at session start by scraping /in/melverick/recent-activity/comments/
- Contains: { author_slug + first_60_chars_of_post_text } for all recent comments
- If post is in this set → SKIP (already commented)

**Source 2: Shared Activity Log (persistent)**
- Check `shared/logs/linkedin-activity.md` → Comments Made table
- Search by Post URL or author_slug + topic match
- If found → SKIP (already commented)

**Decision Matrix:**
- Already commented (either source) → SKIP this post entirely
- Only liked/saved this post → Comment opportunity (adds touch)
- Fresh post, no engagement → Full opportunity

**After commenting on a post:**
- Add to "already commented" set immediately
- Log to shared activity log with: Author, Post URL, Post Topic, Comment Preview

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
2. Find their comments on others' posts to engage with
3. Check back monthly for new activity
```

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
