---
name: linkedin-connect-timer
description: Analyze past LinkedIn activity to determine optimal timing for connection requests based on the 360Brew "Semantic Bridge" strategy. Use when user says "who should I connect with", "connection timing", "ready to connect", or wants to identify prospects ready for connection requests. Applies the 2-3 Touch Rule (minimum 2-3 engagements before connecting). Reads from shared activity log first, then LinkedIn if needed. Outputs prioritized list of prospects ready for connection, recommended approach (blank for 3+ touches, asset-led for 2 touches), and optimal send times.
---

# LinkedIn Connect Timer

Analyze your LinkedIn activity history to identify prospects who are "warmed up" and ready for connection requests based on the 360Brew Semantic Bridge strategy.

## Core Strategy: The 2-3 Touch Rule

360Brew monitors the "relevance gap" between you and connection targets. Cold requests get flagged as spam. The solution: **multi-touch journeys with 2-3 engagements minimum**.

| Timeline | Action | 360Brew Benefit |
|----------|--------|-----------------|
| T-72 hours | Follow profile + Save their post | Name enters their notification feed |
| T-48 hours | Leave 1st comment (15+ words) | Indexed in "Engagement Graph" |
| T-24 hours | Leave 2nd comment OR like + meaningful reply | Strengthens relevance signal |
| T-0 (Now) | Send connection request | High acceptance rate (35%+) |

**Minimum requirement: 2-3 separate engagements before connecting.**

## Trigger

**Check connection pipeline:**
- "who should I connect with"
- "connection timing"
- "ready to connect"
- "check my connection pipeline"
- "analyze my linkedin activity"
- "connection request timing"

**Update connection status:**
- "sent connection to [Name]"
- "[Name] accepted my connection"
- "connected with [Name]"
- "mark [Name] as connected"
- "update connection status"

## Activity Log (Token Optimization)

To minimize token usage, this skill maintains a persistent activity log that tracks previously read engagements.

**Log file location:**
```
linkedin-connect-timer/logs/activity-log.md
```

### Log File Structure

```markdown
# LinkedIn Activity Log

Last updated: [YYYY-MM-DD HH:MM {{CLIENT_TIMEZONE}}]
Last activity timestamp: [YYYY-MM-DD HH:MM]

## Engagement Records

### [Prospect Name]
- Profile: [URL]
- Role: [Title]
- Company: [Company]
- Status: [READY/WARMING/TOO_EARLY/CONNECTED/REQUEST_SENT]
- First touch: [YYYY-MM-DD HH:MM]
- Engagements:
  - [YYYY-MM-DD HH:MM] - [Commented/Liked/Saved/Followed] - [Post URL or description]
  - [YYYY-MM-DD HH:MM] - [Action] - [Details]
- Connection sent: [Date if sent, or "Not yet"]
- Accepted: [Yes/No/Pending]

### [Next Prospect Name]
...
```

### Incremental Read Strategy

**On each run:**

1. **Check for existing log file**
   - If exists: Read `Last activity timestamp`
   - If not exists: Create new log, do full read

2. **Read only NEW activities**
   - Navigate to `https://www.linkedin.com/in/{{CLIENT_LINKEDIN_HANDLE}}/recent-activity/all/`
   - Only extract activities NEWER than `Last activity timestamp`
   - Stop scrolling when reaching already-logged timestamps

3. **Merge with existing data**
   - Add new engagements to existing prospect records
   - Create new prospect records for first-time engagements
   - Update status based on new engagement timeline

4. **Save updated log**
   - Update `Last updated` timestamp
   - Update `Last activity timestamp` to newest activity found

## Workflow

### Step 0: Load or Initialize Activity Log

```
Check: linkedin-connect-timer/logs/activity-log.md exists?

IF EXISTS:
  → Read log file
  → Extract "Last activity timestamp"
  → Set read_from = Last activity timestamp
  → Load existing prospect records into memory

IF NOT EXISTS:
  → Create logs/ directory
  → Set read_from = NULL (full read)
  → Initialize empty prospect records
```

### Step 1: Access LinkedIn Activity Page (Incremental)

Navigate to user's recent activity:
```
https://www.linkedin.com/in/{{CLIENT_LINKEDIN_HANDLE}}/recent-activity/all/
```

Use Chrome DevTools MCP (default; Playwright fallback) to read the activity feed.

**Incremental Read Logic:**
```
WHILE scrolling through activity feed:
  FOR each activity item:
    Extract timestamp of activity

    IF timestamp <= read_from:
      → STOP reading (already logged)
      → Break out of loop

    ELSE:
      → Extract engagement data:
        - Prospect name and profile URL
        - Action type (Commented/Liked/Saved/Followed)
        - Post URL or content snippet
        - Timestamp
      → Add to new_activities list

RETURN new_activities
```

Extract from NEW activities only:
- Posts the user has **commented** on (with timestamps)
- Posts the user has **liked/reacted** to (with timestamps)
- Posts the user may have **saved** (if visible)
- People the user has **followed** recently

### Step 2: Merge New Activities with Log

```
FOR each activity in new_activities:
  prospect = Find or create prospect record by name/URL

  IF prospect exists in log:
    → Append new engagement to prospect.engagements
    → Recalculate prospect.status based on updated timeline

  ELSE (new prospect):
    → Create new prospect record
    → Set first_touch = activity timestamp
    → Set status = TOO_EARLY (initial)

Update log metadata:
  → Last updated = NOW
  → Last activity timestamp = newest activity timestamp
```

### Step 3: Build Engagement Timeline

For each unique person found in activity (from log), create an engagement record:

```
PROSPECT: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Profile: [URL]
Role: [Title if visible]
Company: [Company if visible]

Engagement History:
- [Date/Time] - [Action: Commented/Liked/Saved/Followed]
- [Date/Time] - [Action]

First Touch: [Earliest engagement date]
Latest Touch: [Most recent engagement date]
Touch Count: [Number of interactions]
```

### Step 4: Calculate Connection Readiness

Apply the 2-3 Touch Rule to classify each prospect:

**🟢 READY NOW** (Green Light)
- **Minimum 2-3 separate engagements** (comments, likes, saves, follows)
- At least ONE meaningful comment (15+ words)
- First touch was 48+ hours ago
- Most recent engagement within last 7 days

**🟡 WARMING UP** (Yellow Light)
- Only 1 engagement so far (need 1-2 more)
- OR has engagements but no comments yet
- OR first touch was less than 48 hours ago
- Action needed: Add more engagements before connecting

**🔴 TOO EARLY** (Red Light)
- First touch was less than 24 hours ago
- Need to wait and build more touches
- Shows countdown and touches needed

**⚪ ALREADY CONNECTED**
- Skip if already in network

### Step 5: Output Connection Pipeline

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN CONNECTION PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: [Current Date/Time]
Activity Period Analyzed: [Date range]

📊 LOG STATUS:
- Previous log: [Found/Not found]
- New activities read: [X items]
- Loaded from cache: [Y prospects]
- Token savings: [Skipped Z cached activities]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 READY TO CONNECT NOW ([Count])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Name] - [Title] at [Company]
   Profile: [URL]
   Engagement: [X touches over Y days]
   Last interaction: [Date] - [Action]

   Recommended approach: [BLANK REQUEST / ASSET-LED NOTE]
   [If asset-led, provide template based on their content]

2. [Name] - [Title] at [Company]
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟡 WARMING UP - COMMENT FIRST ([Count])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Name] - [Title] at [Company]
   Profile: [URL]
   Current status: Only liked/reacted
   Action needed: Leave 15+ word comment
   Ready in: ~24 hours after comment

   Suggested comment topic: [Based on their recent post]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 TOO EARLY - WAIT ([Count])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Name] - [Title] at [Company]
   First touch: [Date/Time]
   Ready in: [Hours until 48h mark]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ready now: [X]
Warming up: [Y]
Too early: [Z]
Daily limit remaining: [15 - requests sent today]
```

### Step 6: Determine Request Approach

For each "Ready" prospect (must have 2-3+ engagements), recommend approach:

**Use BLANK REQUEST when (Recommended):**
- You have 3+ engagements with them
- At least one back-and-forth reply exchange
- Your last comment was substantive and recent (within 48h)
- Their content aligns with your profile keywords
- Blank requests perform 12% better than templated notes

**Use ASSET-LED NOTE when:**
- Exactly 2 engagements (minimum threshold)
- Their post mentioned a specific pain point you can address
- You have a relevant PRD/schema/asset to offer
- No back-and-forth conversation yet

**Asset-Led Note Template:**
```
Hi [Name], caught your post on [Topic].

I'm mapping out an Agentic [ERP/CRM/workflow] for [Their Industry] to automate [Pain Point from their post].

Happy to share the schema if useful.
```
(Keep under 250 characters)

### Step 7: Optimal Timing Recommendation

**Best Send Windows ({{CLIENT_TIMEZONE}}):**
- Tuesday-Thursday: 9:00 AM - 10:30 AM
- Secondary: Tuesday-Thursday: 12:00 PM - 1:00 PM

**Avoid:**
- Mondays (inbox overload)
- Fridays (weekend mindset)
- Weekends (low activity)
- After 6 PM (low response)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ OPTIMAL SEND TIME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current time: [Time] {{CLIENT_TIMEZONE}}
Day: [Day of week]

Recommendation: [SEND NOW / WAIT UNTIL [Time]]

Next optimal window: [Day], [Time range] {{CLIENT_TIMEZONE}}
```

### Step 8: Save Updated Activity Log

After processing, save the updated log file:

```
Write to: linkedin-connect-timer/logs/activity-log.md

Content:
- Updated "Last updated" timestamp
- Updated "Last activity timestamp"
- All prospect records (existing + new)
- Updated statuses for all prospects

Also update prospect status when:
- Connection request sent → Status = REQUEST_SENT, Connection sent = [Date]
- Connection accepted → Status = CONNECTED, Accepted = Yes
- Connection declined/withdrawn → Status = DECLINED
```

**Log Maintenance:**
- Keep prospects for 30 days after connection sent
- Archive old/connected prospects to `logs/archive-YYYYMM.md` monthly
- Delete prospects with no engagement for 60+ days

## Contact Classification for Prioritization

**Reference:** See `linkedin-core/references/contact-classification.md` for full criteria.

When prioritizing connection requests, consider contact type:

| Category | Priority | Approach |
|----------|----------|----------|
| **PROSPECT** (ICP match) | HIGH | Asset-led note if pain point visible |
| **PEER** (1K-10K, same niche) | MEDIUM | Blank request (engagement context exists) |
| **THOUGHT LEADER** (10K+) | LOWER | Blank request after 3+ engagements |

**Prioritization Logic:**
1. Prospects with confirmed pain signals → Send first
2. Peers with mutual engagement → High acceptance rate
3. Thought Leaders → Only after sustained engagement (harder to convert)

## Commonality Clusters

360Brew prioritizes "Tribal Relevance." Group prospects by cluster:

**Singapore SME Cluster:**
- People in same local industry group
- Commented on same SME-focused posts

**Tech-Stack Cluster:**
- Followers of n8n, Supabase, Agentic AI content
- Engaged with similar technical posts

**Benefit:** Once 3-4 people in a cluster accept, 360Brew auto-suggests you to the rest.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 CLUSTER OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cluster: [Name, e.g., "Singapore Finance SMEs"]
Members ready: [Names]
Recommendation: Connect with all in same session for cluster boost
```

## Daily Limits & Tracking

**360Brew Safe Limits:**
- Max 15 requests/day (quality over quantity)
- Target acceptance rate: >30%
- If acceptance drops below 25%, pause for 48h

**Track in daily to-do:**
```
Connection Requests Today: [X/15]
Acceptance rate this week: [Y%]
```

## Integration with Other Skills

| After This Skill | Use |
|------------------|-----|
| Need to comment first | `linkedin-pro-commenter` |
| Check ICP fit | `linkedin-icp-finder` |
| Create asset for note | `linkedin-elite-post` |
| Update daily to-do | `linkedin-daily-planner` |

## Shared Activity Log (Token Optimization)

**ALWAYS read from the shared log first before accessing LinkedIn.**

**Log location:** `linkedin-core/shared/logs/linkedin-activity.md`

### On Each Run:
1. **Read shared log first** to check:
   - Existing prospect pipeline (Warming Up, Ready to Connect, Pending)
   - Today's connection requests count (respect 15/day limit)
   - Recent engagement history with prospects
2. **Only access LinkedIn** if log data is stale (>4 hours) or user explicitly requests fresh data
3. **Update shared log** after every action:
   - Connection requests sent → Add to "Connection Requests" table
   - Connection accepted → Move to "Connected (Recent)" table
   - New prospect identified → Add to appropriate pipeline section

### What to Log:
```
| HH:MM | Name | Profile URL | SENT/ACCEPTED/DECLINED/BLOCKED | Blank/Asset-led | Notes |
```
**Always capture Profile URL** for quick navigation later.

## Quality Checklist

Before sending connection requests:
- [ ] Shared log read first (not LinkedIn page)
- [ ] **Minimum 2-3 separate engagements with prospect**
- [ ] At least one 15+ word comment exists
- [ ] Prospect has 48+ hours of engagement history
- [ ] Current day is Tuesday-Thursday
- [ ] Current time is 9:00-10:30 AM {{CLIENT_TIMEZONE}} (or secondary window)
- [ ] Daily limit not exceeded (<15 requests)
- [ ] Request approach determined (blank for 3+, asset-led for 2)
- [ ] Note is under 250 characters (if using note)
- [ ] Cluster opportunities identified
- [ ] Shared log updated after actions
