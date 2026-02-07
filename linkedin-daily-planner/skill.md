---
name: linkedin-daily-planner
description: Generate a daily LinkedIn outreach to-do list based on the 360Brew algorithm strategy. Four modes - (1) AUTONOMOUS with "start linkedin" - runs full workflow without questions, AI auto-selects and executes all tasks; (2) CREATE plan with "plan my day", "daily linkedin plan"; (3) RESUME with "resume linkedin", "linkedin status"; (4) CHECK SCHEDULE with "what time block am I in", "when should I post". Determines current time block (Morning/Content/Midday/Afternoon/Evening), executes tasks autonomously, logs to shared activity log.
---

# LinkedIn Daily Planner

Generate a structured daily outreach to-do list based on the 360Brew algorithm strategy. Integrates with all LinkedIn skills for seamless execution.

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

## Autonomous Workflow

When user triggers autonomous mode ("start linkedin"):

**AUTONOMOUS MODE RULES:**
- ❌ Do NOT ask which task to start - execute in order
- ❌ Do NOT ask user to select variations - AI auto-selects
- ❌ Do NOT wait for confirmation - proceed automatically
- ✅ Execute all tasks for current time block
- ✅ Use Claude for Chrome for all LinkedIn actions
- ✅ Log everything to shared activity log
- ✅ Move to next task immediately after completion

### Autonomous Execution Flow

```
1. Determine current time block (based on system time)
2. Read account config → `shared/linkedin-account-config.md` → Get account type
3. Read shared activity log → Get today's progress AND daily limits status
4. Read icp-prospects.md → Profile Cache table → Check for cached data
5. Read/create today's to-do file
6. For current block, execute each pending task WITH LIMIT CHECKS:

   CACHE-FIRST RULE (applies to ALL blocks):
   → Before visiting ANY LinkedIn profile:
     - Check Profile Cache for prospect
     - If Last Checked < 7 days AND has Recent Post URLs → USE CACHE
     - If Activity Status = INACTIVE → SKIP prospect
     - Only visit LinkedIn if cache is stale or missing
   → After visiting LinkedIn profile:
     - Update Profile Cache with all captured data
     - Record: Last Checked, Activity Status, Last Post, Recent Posts

   COMMENT DEDUP RULE (applies to ALL commenting across ALL blocks):
   **ONE COMMENT PER POST - NEVER comment on the same post twice.**
   (Replying to your own comment thread on a post is OK. Posting a new top-level comment is NOT.)

   → PRE-FLIGHT (once per session, before any commenting starts):
     1. Navigate to /in/melverick/recent-activity/comments/
     2. Scroll to load all visible entries (at least 30-50 entries)
     3. Extract "already commented" set: { author_slug + first_60_chars_of_post_text }
     4. Store this set in memory for the entire session
     5. This takes ~30 seconds and prevents all duplicate comments

   → BEFORE EACH COMMENT:
     1. Build post identifier: author_slug + first_60_chars_of_post_text
     2. Check against "already commented" set
     3. If MATCH FOUND → SKIP this post, find a replacement post
     4. If NO MATCH → Proceed with commenting

   → AFTER EACH COMMENT:
     1. Add the post identifier to the "already commented" set (in-memory)
     2. Log to shared activity log with: Author, Post URL, Post Topic, Comment Preview
     3. This ensures subsequent comments in the same session also check correctly

   MORNING BLOCK:
   → CHECK: Comments today < 30 limit? If not, skip commenting
   → RUN COMMENT DEDUP PRE-FLIGHT (scrape comments activity page → build dedup set)
   → Find 9 posts to comment on (3 Peer, 3 Prospect, 3 Thought Leader)
   → For each comment:
     - CHECK: Still under 30 comment limit?
     - CHECK: Post NOT in "already commented" set (COMMENT DEDUP RULE)
     - If duplicate detected → Skip post, find replacement
     - Generate comment using linkedin-pro-commenter (AI auto-selects)
     - Post comment via Claude for Chrome
     - Update "already commented" set with new post identifier
     - Update daily limits: Comments +1
   → Log all comments to shared activity log

   CONTENT BLOCK:
   → CHECK: Posts today < 2 limit? If not, skip posting
   → Check last post time from shared log
   → Apply 12-HOUR RULE:
     - If last post < 12 hours ago → Calculate next valid window
     - If last post >= 12 hours ago → Can post in current window
   → If posting allowed: Run linkedin-trender → Get trending topic
   → Run linkedin-elite-post → AI auto-selects best variation
   → Run linkedin-image-generator → Generate image via Gemini
   → Schedule post for valid window (respecting 12h minimum gap)
   → Update daily limits: Posts +1
   → Log to shared activity log with scheduled time

   MIDDAY BLOCK:
   → Check notifications for comments on your post
   → For each reply:
     - CHECK: Still under 30 comment limit?
     - Reply to comment (replies to comments on YOUR post are OK, not subject to dedup)
     - Update daily limits: Comments +1
   → Golden Hour engagement (5-10 posts):
     - CHECK: Comments + Likes within limits?
     - CHECK: Post NOT in "already commented" set (COMMENT DEDUP RULE)
     - If already commented on post → Like only, skip commenting
     - Engage with posts (comments and/or likes)
     - Update "already commented" set after each new comment
     - Update daily limits after each action
   → Log engagement to shared activity log

   AFTERNOON BLOCK:
   → Check for connection acceptances → Move to Connected table
   → Classify each new connection: PROSPECT / PEER / THOUGHT LEADER
   → For Value DMs (1-2 day old connections):
     - **ONLY DM PROSPECTS** (skip Peers and Thought Leaders)
     - CHECK: DMs today < 25 limit?
     - Send Value DM to PROSPECT connections only
     - Update daily limits: DMs +1
   → **WARM UP existing prospects (2-3 Touch Rule):**
     - Read icp-prospects.md → Filter for 0-1 touch prospects
     - Run linkedin-icp-warmer → Find their recent posts
     - CHECK: Post NOT in "already commented" set (COMMENT DEDUP RULE)
     - Comment on posts to build touches (+1 touch per comment)
     - Update "already commented" set after each new comment
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
   → Run full inbound audit:
     - Post engagement (commenters, likers)
     - Comment likes and replies
     - Profile views (CHECK: < 80 limit before viewing back)
     - New followers
   → Screen each for ICP fit
   → **SAVE all ICP matches to icp-prospects.md** with source noted
   → For ICP matches needing engagement:
     - CHECK: Comments/Likes/Profile Views within limits?
     - Execute engagement action
     - Update daily limits
   → Log all to shared activity log
   → **COMMENT REPLY AUDIT (Scan last 7-14 days of posts for unreplied comments):**
     - Navigate to own activity page (/in/melverick/recent-activity/all/)
     - For each post from last 14 days with comments:
       * Open post → Scan ALL comments (load more if needed)
       * Identify comments without a reply from Melverick/Nexius Labs
       * Reply to unreplied comments (prioritize 1st degree > 2nd degree > company pages)
       * CHECK: Comments today < 30 limit before each reply
     - Log: "Comment Reply Audit: X unreplied found, Y replied"
     - This catches comments that arrive days after posting (especially on viral posts)
   → Update weekly metrics
   → Update Daily Limits Status table with final counts

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
[09:02] ✓ Found 9 posts to comment on
[09:03] ✓ Comment 1/9: [Author] - [Topic] - Posted
[09:04] ✓ Comment 2/9: [Author] - [Topic] - Posted
...
[09:15] ✓ All 9 comments posted
[09:15] ✓ Logged to shared activity log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ MORNING BLOCK COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Comments: 9/9
Time: 14 minutes
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

### Time Blocks (SGT)

| Time | Block | Duration | Focus |
|------|-------|----------|-------|
| Before 10:00 AM | Morning Block | 15 mins | Pre-posting warm-up, 9 comments (3 Peer, 3 Prospect, 3 Thought Leader) |
| 10:00 AM - 12:00 PM | Content Block | Varies | Create and SCHEDULE post (use linkedin-elite-post) |
| 12:00 PM - 3:00 PM | Midday Block | 15 mins | Golden Hour (60-90 min) engagement, reply to comments on your post |
| 3:00 PM - 6:00 PM | Afternoon Block | 15 mins | Connection requests, DMs, outreach |
| After 6:00 PM | Evening Block | 10 mins | Daily audit, metrics check, inbound engagement review |

### Posting Windows by Day (SGT)

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
Last post: Today 10:30 SGT
Current time: 16:00 SGT
Hours since last: 5.5 hours

⚠️ 12-HOUR MINIMUM NOT MET
Next valid posting: Today 22:30 SGT
Nearest posting window: Tomorrow 08:30 SGT (Tuesday Primary)

Action: Scheduling for Tomorrow 08:30 SGT
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
Current time: [HH:MM] SGT
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
Primary: [Time range] SGT
Secondary: [Time range] SGT (if available)
Best content type: [Type for today]
Window status: [In window / Missed / Upcoming in X mins]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ 12-HOUR POSTING RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last post: [Date HH:MM SGT or "None in last 24h"]
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
Current time: [HH:MM] SGT
Blocks passed: Morning Block, Content Block

FLEXIBLE TASKS (still do today):
- [ ] 9 comments (Peer/Prospect/Thought Leader) - can do now
- [ ] Connection requests - can do now

TIME-SENSITIVE (check status):
- [ ] Post: Primary window MISSED, Secondary at [Time] SGT
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
Current time: 15:00 SGT (Monday)

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
- [ ] Comment on 3 peer posts (fellow builders in Agentic AI/SME space)
```

**After:**
```markdown
- [x] Comment on 3 peer posts (fellow builders in Agentic AI/SME space) ✓ 09:15
```

---

## Step 1: Determine Day of Week

Get the current date and day of week to customize the plan:

| Day | Content Focus | Post Type |
|-----|--------------|-----------|
| Monday | Evidence content | Demo, Schema, JSON import |
| Tuesday | Strategy content | High-level AI shifts for SMEs |
| Wednesday | Evidence content | Demo, Schema, JSON import |
| Thursday | Strategy content | High-level AI shifts for SMEs |
| Friday | Reflection | Personal story from teaching/hackathons |
| Saturday/Sunday | Engagement only | No posting required |

## Step 2: Generate Daily To-Do List

Create the to-do file with this structure:

```markdown
# LinkedIn Daily Outreach Plan - [Day, DD MMM YYYY]

## Morning Block (15 mins) - Pre-Posting Warm-Up

The 15/15 Rule: Engage BEFORE posting to warm your topical relevance.

### Commenting Tasks (use linkedin-pro-commenter + linkedin-icp-finder)

**Contact Classification:** See `references/contact-classification.md`

- [ ] Comment on 3 **PEER** posts (1K-10K followers, fellow builders in AI/automation)
- [ ] Comment on 3 **PROSPECT** posts (ICP match - use linkedin-icp-finder to classify)
- [ ] Comment on 3 **THOUGHT LEADER** posts (10K+ followers, visibility boost)

**Comment Rules:**
- Minimum 15 words per comment
- Maximum 50 words
- Must add POV or insight
- Ask a question to encourage thread depth

---

## Content Block ([Day-specific])

[Insert day-specific content task - see Day Matrix below]

---

## Midday Block (15 mins) - Post-Content Engagement

### Golden Hour Tasks
- [ ] Engage with 5-10 posts immediately after publishing (warms topical relevance for 4 hours)
- [ ] Reply to ALL comments on your post within 1 hour (35% reach boost)
- [ ] Save 2-3 high-quality posts from your feed (360Brew values Saves 5x more than Likes)

### Post Commenter Engagement (HIGHEST priority inbound signal)
- [ ] For each commenter on your post: Quick ICP screen
- [ ] If ICP match: Note for Evening Block follow-up (find their posts, comment back)
- [ ] Reply builds thread depth even if not ICP (extends post reach 48+ hours)

---

## Afternoon Block (15 mins) - Outreach

### Check Connection Acceptances (do this FIRST)
- [ ] Check "My Network" for new connection acceptances
- [ ] For each acceptance: Move from "Pending" → "Connected" table in shared log
- [ ] **Classify each connection: PROSPECT / PEER / THOUGHT LEADER**
- [ ] Schedule Value DM for **PROSPECTS ONLY** (24-48h after acceptance)
- [ ] ⚠️ **DO NOT schedule DMs for Peers or Thought Leaders** (engage via comments instead)

### Send Value DMs (for PROSPECT acceptances from 1-2 days ago)
- [ ] Check "Connected (Recent)" table for pending Value DMs
- [ ] **FILTER: Only send DMs to contacts marked as PROSPECT**
- [ ] Skip Peers and Thought Leaders (they don't need DMs - continue engaging on their content)
- [ ] Send personalized Value DM to PROSPECTS (see templates in shared log)
- [ ] NO external links, NO pitch, reference their content
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

**DM Template (Anti-Pitch):**
> "Hey [Name], enjoyed your post on [Topic]. I just finished a workflow for [Pain Point]. Happy to share the logic diagram if useful—no strings attached."

### CRM Auto-Sync (end of Afternoon Block)
- [ ] After all Afternoon Block tasks complete → call `crm_sync_all`
- [ ] This captures: new prospects, connection status updates, touch history changes
- [ ] Log sync result (created/updated/skipped counts) to activity log

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
- [ ] For ICP commenters: Find their posts → Comment back (use linkedin-pro-commenter)
- [ ] For ICP likers: Find their posts → Comment
- [ ] Log to shared activity log → "Post Engagement Received" table

**Comment Engagement (on your comments):**
- [ ] Check LinkedIn notifications for comment likes received
- [ ] Check for replies to your comments
- [ ] For ICP matches: Find their posts → Comment to reciprocate
- [ ] Reply to comment replies (builds thread depth = algorithm boost)

### Comment Reply Audit (Scan Older Posts - MANDATORY)

**Problem this solves:** Comments on posts from 1-2 weeks ago are invisible in notifications. Viral posts (30+ comments) keep getting new comments for days. Without this audit, those comments go unreplied, damaging engagement and credibility.

**Execution:**
- [ ] Navigate to own activity page (`/in/melverick/recent-activity/all/`)
- [ ] Check posts from last 14 days that have comments (skip 0-comment posts)
- [ ] For each post with comments:
  - Open the post detail page
  - Load ALL comments (click "Load more comments" if needed)
  - Scan each comment: Does it have a reply from Melverick or Nexius Labs?
  - If UNREPLIED: Reply with genuine, substantive response (under 50 words)
  - CHECK: Comments today < 30 limit before each reply
- [ ] Log to activity log: "Comment Reply Audit: X unreplied found across Y posts, Z replied"

**Priority Order:**
1. 1st degree connections (strongest signal, most visible)
2. 2nd degree connections with substantive comments (potential prospects)
3. Company pages and generic comments (lowest priority)

**Skip:**
- Emoji-only comments (👏🔥) - no reply needed
- Spam/promotional comments - no reply needed
- Comments older than 14 days - diminishing returns

**Time Budget:** 5-10 minutes max. If >10 unreplied found, reply to top 5 by priority and carry forward the rest to tomorrow.

**Weekly Target:** 100% reply rate on 1st degree comments, 80%+ on substantive 2nd degree comments.

**Profile & Follower Signals:**
- [ ] **Check profile views** (linkedin.com/me/profile-views/)
- [ ] **Check new followers** (linkedin.com/mynetwork/network-manager/people-follow/followers/)

**For all inbound signals:**
- [ ] Quick ICP screen (ASEAN? Decision-maker? SME?)
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
- ✅ Location: Singapore, Malaysia, Thailand, Indonesia, Philippines
- ✅ Role: Manager, Director, Head of, CEO, Founder, COO, CFO
- ✅ Company: SME (10-500 employees), not enterprise/MNC
- ❌ Skip: Non-ASEAN, junior roles, large corporations, recruiters

### CRM Auto-Sync (end of Evening Block)
- [ ] After all Evening Block tasks complete → call `crm_sync_all`
- [ ] This captures: inbound audit results, new ICP matches from followers/viewers
- [ ] Log sync result (created/updated/skipped counts) to activity log

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
| Sync prospects to CRM | `hubspot-crm` (MCP: `crm_sync_all`) |

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
  → CHECK DEDUP: Is this post in the "already commented" set?
  → If YES: SKIP post, log "Already commented on this post - skipping"
  → If NO: Proceed with comment

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
→ Example: "AI Singapore" AND (CEO OR founder) → Find relevant posts

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
  - High-level AI shifts for SMEs
- [ ] Ensure opening hook is a "Topic Signal"
- [ ] Put any external links in FIRST COMMENT, not post body
- [ ] **Schedule for: 10:00 AM - 11:30 AM SGT (Primary) or 4:00 PM - 5:30 PM SGT (Secondary)**
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
- [ ] **Schedule for: 8:30 AM - 10:30 AM SGT (Primary) or 12:00 PM - 1:30 PM SGT (Secondary)**
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
- [ ] **Schedule for: 9:00 AM - 11:00 AM SGT (Primary) or 3:00 PM - 5:00 PM SGT (Secondary)**
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
- [ ] **Schedule for: 10:00 AM - 12:00 PM SGT (Primary) or 1:00 PM - 2:30 PM SGT (Secondary)**
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
  - Lesson from recent SME hackathon
  - Teaching moment from training non-coders
  - Personal journey insight
  - Build-in-public update with learnings
  - Team highlights or wins
- [ ] Use first-person narrative for "Human-in-the-loop" trust signal
- [ ] Connect story back to Agentic AI/SME positioning
- [ ] **Schedule for: 8:30 AM - 10:00 AM SGT ONLY (No afternoon slot on Friday)**
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
- [ ] Screen against ICP criteria (ASEAN SME decision-maker)
- [ ] Add 5-10 new ICP matches to `shared/logs/icp-prospects.md`
- [ ] Capture LinkedIn profile URLs during screening
- [ ] Note source in each prospect: "Source: Sales Nav: [Search Name]"

**Saved Searches to Rotate Weekly:**
```
Week 1: ASEAN SME Decision Makers + Singapore Operations Leaders
Week 2: Finance Decision Makers ASEAN + Recent Job Changers
Week 3: SME Founders Singapore + [Your choice]
Week 4: All searches quick scan
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
- **CHECK COMMENT DEDUP** → Is this post in the "already commented" set? If yes → SKIP
- After action → Update Daily Limits Status immediately
- After comment → Update "already commented" set with new post identifier
- After comment → Log to shared activity log with Post URL
- **After visiting LinkedIn profile** → Update Profile Cache with new data

**Comment Dedup Pre-flight (once per session):**
- Must run BEFORE any commenting block starts
- Navigate to /in/melverick/recent-activity/comments/
- Build "already commented" set: { author_slug + first_60_chars_of_post }
- This set persists for the entire session across all blocks

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
