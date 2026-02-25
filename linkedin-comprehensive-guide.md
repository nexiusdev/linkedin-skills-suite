# LinkedIn Skills: Comprehensive User Guide
## From Onboarding to Continuous Nurturing

**Complete workflow covering all LinkedIn skills for building and nurturing a prospect pipeline.**

---

## Table of Contents

1. [Phase 1: Onboarding](#phase-1-onboarding) - First-time setup
2. [Phase 2: ICP Definition](#phase-2-icp-definition) - Define your ideal customer profile
3. [Phase 3: ICP Discovery](#phase-3-icp-discovery) - Find prospects
4. [Phase 4: ICP Warming](#phase-4-icp-warming) - Engage with prospects (0→3 touches)
5. [Phase 5: Connection Timing](#phase-5-connection-timing) - Determine when to connect
6. [Phase 6: Connection & DMs](#phase-6-connection--dms) - Send connection requests
7. [Phase 7: Continuous Nurturing](#phase-7-continuous-nurturing) - Daily engagement workflow
8. [Supporting Skills](#supporting-skills) - Content creation and engagement tools
9. [Quick Reference](#quick-reference) - Commands and file locations

---

## Phase 1: Onboarding

**Skill:** `linkedin-onboarding`
**When:** First-time setup BEFORE using any other LinkedIn skills
**Purpose:** Customize all LinkedIn skills for your specific business, ICP, and geography

### What This Does

Collects your business information through 13 guided questions and generates personalized reference files that power all other LinkedIn skills.

### How to Run

Say: **"setup linkedin"** or **"onboard linkedin"** or **"linkedin first time setup"**

### The Onboarding Flow

#### **Phase 1: Business Foundation (Q1-Q3)**

**Q1: Business Identity**
- Your company/business name
- Your LinkedIn profile URL (optional but recommended)

**Q2: Core Positioning**
- In one sentence, what do you help customers achieve?
- Your primary domain/niche (e.g., "AI automation", "B2B SaaS")

**Q3: Target Market**
- Who is your ideal customer? (e.g., "SME founders", "enterprise CTOs")
- What company size do you target? (e.g., "10-200 employees", "500+ employees")

#### **Phase 2: ICP Details (Q4-Q9)**

**Q4: ICP Example Profiles (RECOMMENDED)**
- Provide 2-5 LinkedIn profile URLs of your ideal customers
- These will be analyzed to extract common patterns:
  - Job titles/roles
  - Industries they work in
  - Company sizes
  - Pain points from their posts
  - Geographic locations
- If you don't have URLs, skip to manual ICP definition (Q5-Q8)

**Q5: Target Roles (Decision-Makers)**
- 3-5 job titles of people who can buy/decide
- Examples: CEO, Founder, CFO, Operations Director, Head of Marketing

**Q6: Target Roles (Influencers)**
- 2-4 job titles of people who influence the decision
- Examples: Operations Manager, IT Manager, Business Analyst

**Q7: Target Industries**
- Primary (3-4): Where most of your customers come from
- Adjacent (2-3): Related industries that could benefit

**Q8: Geographic Focus** ⚠️ **CRITICAL**
- What regions do you target? (e.g., "US, UK, Canada" or "APAC" or "Global")
- This becomes the geography filter in linkedin-icp-finder
- Example: "US, UK, Canada" or "Singapore, Malaysia, Thailand" or "Global"

**Q9: Pain Keywords**
- 8-12 keywords your customers commonly mention
- Examples: "manual processes", "scaling issues", "data silos"

#### **Phase 3: Content & Engagement (Q10-Q12)**

**Q10: Content Pillars**
- 2-3 main topics you post about on LinkedIn
- These become profile alignment signals for 360Brew algorithm

**Q11: Peer Signals**
- Keywords that identify fellow builders/peers in your space
- Tools, technologies, communities they follow
- Examples: "React developers", "HubSpot users", "Y Combinator founders"

**Q12: Save-Worthy Assets**
- What practical assets can you create that your audience would save?
- Examples: templates, checklists, frameworks, code snippets, calculators
- 2-3 asset types with descriptions

#### **Phase 4: Timezone (Q13)**

**Q13: Primary Timezone**
- What timezone are you in? (for optimal posting times)
- This adjusts the daily planner time blocks

### Output Files Generated

After completing all questions, onboarding creates these files:

1. **`references/icp-profile.md`** - Target customer criteria, roles, industries, pain keywords
2. **`references/contact-classification.md`** - How to classify contacts (PEER/PROSPECT/THOUGHT LEADER)
3. **`references/connect-request.md`** - Connection request templates
4. **`references/saved-asset.md`** - Save-worthy content examples
5. **`references/linkedin-strategy.md`** - Personalized strategy doc

### After Onboarding

**Next steps:**
1. Review the generated files and adjust any details
2. Run **"start linkedin"** to begin your first session
3. Use **"linkedin-profile-icp"** to further refine your ICP if needed

---

## Phase 2: ICP Definition

**Skill:** `linkedin-profile-icp`
**When:** After onboarding OR when you need to refine your ICP
**Purpose:** Extract ICP targeting criteria from your LinkedIn profile

### What This Does

Analyzes your LinkedIn profile to extract:
- Profile positioning summary
- Target job roles (primary decision-makers + secondary influencers)
- Target industries (primary + adjacent)
- Target company profile (size, stage, geography, tech maturity)
- ICP screening filters (role, industry, company size, pain keywords)
- Posts to engage with (based on pain signals)
- Search keywords (for prospecting)

### How to Run

Say: **"find my ICP"** or provide your LinkedIn profile for ICP analysis

### The ICP Scoring Matrix

The skill uses a scoring system to evaluate prospects:

| Score Range | Classification | Action |
|-------------|----------------|--------|
| 80-100 | HOT | High priority, engage immediately |
| 60-79 | WARM | Good fit, engage when available |
| 40-59 | COOL | Maybe fit, consider if no better options |
| <40 | SKIP | Not a fit, do not pursue |

**Scoring criteria:**
- Geography fit: 25%
- Role match: 25%
- Company size: 20%
- Pain signals: 20%
- Engagement signals: 10%

### Anti-ICP Definition

The skill also identifies who NOT to target:
- Wrong geography (outside your target region)
- Wrong company size (too small or too large)
- Wrong roles (non-decision-makers, job seekers)
- Wrong industries (irrelevant sectors)

### Content Pillars Mapping

Analyzes your content strategy:
- 40% core expertise (your main domain)
- 30% adjacent topics (related areas)
- 20% personal insights (your unique perspective)
- 10% engagement content (community building)

### Output

The skill outputs to **`references/icp-profile.md`** with:
- Complete ICP targeting criteria
- Screening filters for linkedin-icp-finder
- Search keywords for prospecting
- Content engagement guidelines

---

## Phase 3: ICP Discovery

**Skill:** `linkedin-icp-finder`
**When:** To find new prospects to engage with
**Purpose:** Classify contacts and discover ICP prospects using multiple discovery methods

### Discovery Methods

linkedin-icp-finder supports **7 discovery modes**:

#### **1. Traditional Outbound Discovery**
- Competitor comment threads
- Authority post comments
- LinkedIn search results
- Single profile screening

#### **2. Algorithm Training Mode** 🆕
- Systematically visit prospect profiles
- Follow prospects
- Turn on notifications
- Prime LinkedIn feed to show more ICP content

#### **3. Feed Discovery Mode** 🆕
- Scan LinkedIn feed for prospects
- Find prospects posting relevant content
- On-the-fly discovery while browsing

#### **4. Hashtag Discovery Mode** 🆕
- Search posts by hashtag (e.g., hashtags relevant to your niche and geography)
- Find prospects discussing relevant topics
- **Note:** No geography filters available, may have low hit rate

#### **5. Profile Recommendations Discovery** 🆕
- Harvest "People you may know" from prospect profiles
- Algorithmically clustered lookalike prospects
- High-quality matches based on existing ICPs

#### **6. Inbound Signal Discovery**
- Profile viewers
- New followers
- Post reactors
- Connection requests (highest intent)

#### **7. Advanced Discovery Strategies**
- Content re-sharers (highest engagement)
- Competitor commenters (active buyers)
- Shared connections (warm intro paths)
- Group members
- Event attendees

### How to Run

**Traditional discovery:**
- "find prospects" or "classify contacts"
- Provide LinkedIn content for screening

**Algorithm training:**
- "train algorithm" or "train feed" or "prime my feed"

**Feed discovery:**
- "scan feed" or "find prospects in feed"

**Hashtag discovery:**
- "scan hashtag [tag]" or "hashtag discovery"

**Profile recommendations:**
- "harvest recommendations" or "expand from [prospect name]"

**Inbound signals:**
- "check inbound" or "screen inbound"
- "who viewed my profile"
- "check new followers"

### The ICP Screening Process

**Step 0: Blacklist Check** (MANDATORY)
- Check `shared/logs/linkedin-blacklist.md`
- If contact is blacklisted → SKIP entirely

**Step 1: Geography Filter** 🚨 **APPLY FIRST**
- **STRICT**: Only pass if prospect is from your target geography
- Read target countries from `references/icp-profile.md`
- If geography NOT confirmed → SKIP immediately, no exceptions

**Step 2: Role Filter**
- Match against target roles from ICP profile
- Focus on: Managers, Directors, Heads of Departments, C-suite

**Step 3: Company Filter**
- Match against target company profile (size, stage)

**Step 4: Post Engagement Filter**
- Skip job postings/hiring announcements
- Skip posts with comments disabled

**Step 5: Pain Signal Filter**
- Look for specific frustrated questions
- Concrete problem descriptions
- Asks for recommendations
- Uses ICP pain keywords

### Contact Classification

Before ICP screening, classify each contact:

| Category | Criteria | Engagement Priority |
|----------|----------|---------------------|
| **PROSPECT** | ICP match, decision-maker at target company | HIGHEST |
| **PEER** | 1K-10K followers, same niche, fellow builder | HIGH |
| **THOUGHT LEADER** | 10K+ followers, established authority | MEDIUM |
| **GENERAL** | <1K or irrelevant niche | LOW |

### Output Format

For each prospect:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICP SCREENING: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌏 GEOGRAPHY: [✅ CONFIRMED / ❌ SKIP]
Location: [Country/City]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT / ❌ SKIP]

Role: [Title] → [Match assessment]
Company: [Company, size] → [Match assessment]
Pain Signal: [Quote] → [Match vs ICP keywords]

Fit Score: [X/4 criteria met]
```

### Where Prospects Are Saved

**File:** `shared/logs/icp-prospects.md`

All discovered prospects are saved to a single consolidated file with:
- Date Found
- Name, Role, Company, Location
- Classification (PROSPECT/PEER/THOUGHT LEADER)
- Touches (0, 1, 2, 3+)
- Last Touch date
- Touch History
- Connection Status
- Profile URL
- Email (if captured)
- Notes

**Profile Cache** is also maintained to minimize repeat LinkedIn visits:
- Last Checked timestamp
- Activity Status (ACTIVE/MODERATE/INACTIVE)
- Follower count
- Last Post date
- Recent Post URLs (up to 3)
- Engagement Score

### Sales Navigator Strategy

If you have Sales Navigator account:

**🔥 PRIORITY #1: "Posted on LinkedIn" Filter**
- ALWAYS enable this filter when searching
- Ensures every prospect has recent posts to engage with
- Direct workflow: Find → View Post → Comment → Save to prospects

**Saved Searches with Alerts:**
- Create ICP-filtered searches
- Enable daily/weekly alerts
- Always include "Posted on LinkedIn: Yes"

**Lead Recommendations:**
- Save 5-10 best ICP matches as leads
- Check "Similar leads" weekly
- Algorithm learns your preferences

**⚠️ Data Preservation (CRITICAL):**
- Sales Navigator data is LOST when subscription ends
- ALWAYS save leads to local `icp-prospects.md` IMMEDIATELY
- Document saved searches in `linkedin-account-config.md`

---

## Phase 4: ICP Warming

**Skill:** `linkedin-icp-warmer`
**When:** To find engagement opportunities with prospects across the warming pipeline
**Purpose:** Proactively hunt for posts to comment on, progressing prospects from 0→3 touches

### The 2-3 Touch Rule

360Brew monitors "relevance gap" between you and connection targets. Cold requests get flagged as spam. **Solution:** Multi-touch journeys with 2-3 engagements minimum.

| Touch Count | Status | Action Needed |
|-------------|--------|---------------|
| 0 touches | NEW | Find posts → First engagement |
| 1 touch | WARMING | Find new posts → Continue warming |
| 2 touches | ALMOST READY | One more engagement → Ready to connect |
| 3 touches | READY | Move to "Ready to Connect" pipeline |

### How to Run

**Interactive mode:**
- "warm up my ICPs"
- "find posts from prospects"
- "warmup opportunities"

**Autonomous mode (when called from daily planner):**
- Automatically engages all high-priority prospects
- No user prompts, fully automated

### The Warming Workflow

**Step 0: Blacklist Check** (MANDATORY)
- Check `shared/logs/linkedin-blacklist.md`
- If prospect is blacklisted → SKIP entirely

**Step 0a: Cache-First Check** (Minimize LinkedIn Visits)
- Check Profile Cache FIRST before visiting any profile
- Files to check:
  - `shared/logs/icp-prospects.md` → Profile Cache table
  - `shared/logs/inbound-screening-history.md` → Profile Cache section
- If cached data exists (<7 days old) + has Recent Post URLs:
  - USE CACHED DATA
  - Navigate directly to cached post URLs
  - Skip profile visit (saves 2-3 minutes)
- If no cache or stale:
  - Visit LinkedIn profile
  - Extract and cache data
  - Update Profile Cache

**Step 0d: Email Extraction** (Capture When Available)
- Always attempt to extract email when visiting prospect profile
- Sources:
  1. Contact Info section (1st-degree connections only)
  2. About section (sometimes displayed)
  3. Featured/Links section → Company website
- Update `icp-prospects.md` Email column

**Step 1: Read Prospect Sources**

Two sources:
1. **ICP prospects file** (`shared/logs/icp-prospects.md`) - 0-touch prospects
2. **Shared activity log** (`shared/logs/linkedin-activity.md`) - 1-2 touch prospects

**Step 2: Prioritize Prospects**

**🔥 CRITICAL: 1-TOUCH → 2-TOUCH CONVERSION** (Process First)
- 1 touch, last engagement > 3 days ago
- Action: Find second post → Comment → Move to 2-touch
- Target: Convert 3+ prospects from 1→2 touch per day

**🔥 HIGH PRIORITY** (Engage Today)
- 2 touches already (one more = ready to connect)
- Replied to your previous comment
- High-value ICP signal

**🟡 MEDIUM PRIORITY: 0-TOUCH BACKLOG** (Clear Before Discovery)
- 0 touches, oldest first (FIFO)
- Action: Find posts → First comment → Move to 1-touch
- Target: Clear 3+ prospects from 0-touch per day

**🆕 NEW PROSPECTS** (Only After Backlog Under Control)
- Only discover new if 0-touch backlog < 10 prospects

**Step 3: Search for New Posts**

For each prioritized prospect:
1. Navigate to their profile activity: `linkedin.com/in/[username]/recent-activity/all/`
2. Scan for posts from last 7 days:
   - Native posts (not reshares)
   - Posts you haven't commented on
   - Posts with engagement potential (5+ reactions)

**Step 4: Cross-Reference Engagement History**

Check shared log:
- Already commented? → Skip
- Already liked/saved? → Comment opportunity
- Fresh post? → Full opportunity

**Step 5: Output Warmup Opportunities**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICP WARMUP OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: [Date/Time]
Prospects scanned: [X]
Opportunities found: [Y]

🔥 HIGH PRIORITY (2 touches → ready after this)
1. [Name] - [Title] at [Company]
   Current touches: 2
   📝 NEW POST FOUND: [Post URL]
   Topic: [Brief summary]
   Action: Comment → Ready for connection

🟡 MEDIUM PRIORITY (1 touch → need 2 more)
1. [Name] - [Title] at [Company]
   Current touches: 1
   📝 NEW POST FOUND: [Post URL]
   Action: Comment → 2 touches, need 1 more

🆕 FIRST TOUCH NEEDED (0 touches → start warming)
1. [Name] - [Title] at [Company]
   Source: icp-prospects.md
   📝 POST FOUND: [Post URL]
   Action: Comment → Move to Warming Up table

⚪ NO NEW POSTS FOUND
[Name] - Last post: [X days ago] - Monitor
```

**Step 6: Integrate with Comment Generation**

**Autonomous mode (from daily planner):**
- Automatically engage ALL high-priority prospects
- For each: Read post → Generate comment (linkedin-pro-commenter) → Post → Update log
- No user prompts, fully automated

**Interactive mode:**
- Present opportunities
- User selects prospect
- Generate comment with linkedin-pro-commenter
- After comment posted, update shared log

### Comment Hunting (For Inactive Posters)

Some high-value prospects don't post content but actively comment on others' posts.

**When to use:** Prospect marked INACTIVE (no posts 30+ days) but actively comments

**Workflow:**
1. Navigate to prospect's Comments tab: `linkedin.com/in/[username]/recent-activity/comments/`
2. Find recent comments (last 7 days)
3. Look for substantive comments (not one-word reactions)
4. Reply to their comment with additional perspective
5. Update tracking: "Touch X: Reply to comment on [Author]'s post - COMMENT HUNTING"

### Profile Recommendations Discovery

**Strategy:** Leverage LinkedIn's algorithm to find lookalike prospects.

When viewing any prospect's profile, LinkedIn displays similar profiles in right sidebar:
- "More profiles for you"
- "People you may want to know"

**Workflow:**
1. Navigate to existing prospect profile
2. Extract recommendations from right sidebar
3. ICP qualification check (role, company size, location, industry)
4. Save qualified prospects to `icp-prospects.md`

**Efficiency:** 30 seconds per profile, 3-5 prospects per seed

**Best practice:** Use strongest ICP matches (Score 80+) as seeds

### Premium Account Optimization

**FREE Account:**
- Prioritize prospects with cached Recent Post URLs
- Focus on comment-based warming
- Skip prospects with NO_COMMENT flag quickly
- Use profile views sparingly (80/day limit)

**PREMIUM Account:**
- Higher profile view limit (150/day)
- See all profile viewers
- Use private browsing strategically

**SALES NAVIGATOR Account:**
- **🔥 Priority #1:** Use "Posted on LinkedIn" filter for discovery + warming
- InMail for stuck prospects (NO_COMMENT flag)
- Lead tracking
- Engagement insights
- Higher limits (500 profile views/day)

### Shared Activity Log Updates

**After engagement:**

**For 0-touch prospects (first engagement):**
1. Add to "Warming Up" table in shared log
2. Set: First Touch = today, Touches = 1, Needed = 1-2 more
3. Log comment in "Comments Made" table

**For 1-2 touch prospects (continuing warmup):**
1. Increment touch count
2. Update "Last Post Seen" date
3. Move to "Ready to Connect" if now at 3 touches
4. Log comment in "Comments Made" table

---

## Phase 5: Connection Timing

**Skill:** `linkedin-connect-timer`
**When:** To determine who is ready for connection requests
**Purpose:** Analyze past activity to identify prospects ready for connection based on 2-3 Touch Rule

### The 2-3 Touch Timeline

| Timeline | Action | 360Brew Benefit |
|----------|--------|-----------------|
| T-72 hours | Follow profile + Save post | Name enters notification feed |
| T-48 hours | Leave 1st comment (15+ words) | Indexed in "Engagement Graph" |
| T-24 hours | Leave 2nd comment OR like + reply | Strengthens relevance signal |
| T-0 (Now) | Send connection request | High acceptance rate (35%+) |

**Minimum requirement:** 2-3 separate engagements before connecting.

### How to Run

**Check connection pipeline:**
- "who should I connect with"
- "connection timing"
- "ready to connect"
- "check my connection pipeline"

**Update connection status:**
- "sent connection to [Name]"
- "[Name] accepted my connection"
- "update connection status"

### Activity Log (Token Optimization)

The skill maintains a persistent activity log: `linkedin-connect-timer/logs/activity-log.md`

**Incremental read strategy:**
- On each run, read only NEW activities since last timestamp
- Merge with existing prospect records
- Update status based on new engagement timeline
- Save updated log

**Token savings:** After first run, only reads new activities, skipping already-logged data

### The Workflow

**Step 0: Blacklist Check** (MANDATORY)
- Check `shared/logs/linkedin-blacklist.md`
- If prospect is blacklisted → SKIP from connection pipeline

**Step 0a: Load or Initialize Activity Log**
- Check if log exists
- If exists: Extract "Last activity timestamp", set read_from date
- If not exists: Set read_from = NULL (full read)

**Step 1: Access LinkedIn Activity Page** (Incremental)
- Navigate to `linkedin.com/in/[username]/recent-activity/all/`
- Extract only NEW activities (timestamp > read_from)
- Stop when reaching already-logged timestamps

**Step 2: Merge New Activities with Log**
- For each activity: Find or create prospect record
- If prospect exists: Append new engagement, recalculate status
- If new prospect: Create new record, set status = TOO_EARLY
- Update log metadata

**Step 3: Build Engagement Timeline**

For each unique person:
```
PROSPECT: [Name]
Profile: [URL]
Role: [Title]
Company: [Company]

Engagement History:
- [Date/Time] - [Commented/Liked/Saved/Followed]
- [Date/Time] - [Action]

First Touch: [Earliest date]
Latest Touch: [Most recent date]
Touch Count: [Number]
```

**Step 4: Calculate Connection Readiness**

**🟢 READY NOW** (Green Light)
- Minimum 2-3 separate engagements
- At least ONE meaningful comment (15+ words)
- First touch was 48+ hours ago
- Most recent engagement within last 7 days

**🟡 WARMING UP** (Yellow Light)
- Only 1 engagement (need 1-2 more)
- OR has engagements but no comments yet
- OR first touch was <48 hours ago

**🔴 TOO EARLY** (Red Light)
- First touch was <24 hours ago
- Need to wait and build more touches

**⚪ ALREADY CONNECTED**
- Skip if already in network

**Step 5: Output Connection Pipeline**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN CONNECTION PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 LOG STATUS:
- Previous log: [Found/Not found]
- New activities read: [X items]
- Token savings: [Skipped Z cached activities]

🟢 READY TO CONNECT NOW ([Count])
1. [Name] - [Title] at [Company]
   Engagement: [X touches over Y days]
   Last interaction: [Date] - [Action]
   Recommended approach: [BLANK REQUEST / ASSET-LED NOTE]

🟡 WARMING UP - COMMENT FIRST ([Count])
1. [Name] - [Title] at [Company]
   Current status: Only liked/reacted
   Action needed: Leave 15+ word comment
   Ready in: ~24 hours after comment

🔴 TOO EARLY - WAIT ([Count])
1. [Name] - [Title] at [Company]
   First touch: [Date/Time]
   Ready in: [Hours until 48h mark]
```

**Step 6: Determine Request Approach**

**Use BLANK REQUEST when (Recommended):**
- 3+ engagements
- At least one back-and-forth reply
- Last comment was substantive and recent
- Blank requests perform 12% better than templated notes

**Use ASSET-LED NOTE when:**
- Exactly 2 engagements (minimum threshold)
- Their post mentioned specific pain point
- You have relevant asset to offer
- No back-and-forth conversation yet

**Asset-Led Note Template:**
```
Hi [Name], your post on [Topic] caught my eye.

Curious how you're handling [specific challenge]?
Seeing [related observation] across [their industry] in your target geography.
```
(Under 250 characters - authentic question, not solution-offering)

**Step 7: Optimal Timing Recommendation**

**Best Send Windows (your timezone):**
- Tuesday-Thursday: 9:00 AM - 10:30 AM
- Secondary: Tuesday-Thursday: 12:00 PM - 1:00 PM

**Avoid:**
- Mondays (inbox overload)
- Fridays (weekend mindset)
- Weekends (low activity)
- After 6 PM (low response)

**Step 8: Save Updated Activity Log**

After processing:
- Write updated log to `linkedin-connect-timer/logs/activity-log.md`
- Update "Last updated" and "Last activity timestamp"
- Update prospect statuses
- Archive old prospects monthly

### Contact Classification for Prioritization

| Category | Priority | Approach |
|----------|----------|----------|
| **PROSPECT** (ICP match) | HIGH | Asset-led note if pain point visible |
| **PEER** (1K-10K, same niche) | MEDIUM | Blank request (engagement exists) |
| **THOUGHT LEADER** (10K+) | LOWER | Blank request after 3+ engagements |

### Commonality Clusters

360Brew prioritizes "Tribal Relevance." Group prospects by cluster:
- Geographic cluster (your target geography)
- Tech-stack cluster
- Industry cluster

**Benefit:** Once 3-4 people in cluster accept, 360Brew auto-suggests you to the rest.

### Daily Limits & Tracking

**360Brew Safe Limits:**
- Max 15 requests/day (quality over quantity)
- Target acceptance rate: >30%
- If acceptance drops below 25%, pause for 48h

---

## Phase 6: Connection & DMs

**Skills:** `linkedin-connect-timer` (identifies ready prospects) + manual execution
**When:** After prospects have 2-3 touches
**Purpose:** Send connection requests and follow-up DMs

### Connection Request Strategy

**Step 1: Check Connection Pipeline**

Run linkedin-connect-timer to see "Ready to Connect Now" list.

**Step 2: Choose Request Approach**

**Blank Request (Preferred for 3+ touches):**
- No note, just click "Connect"
- 10-15% higher acceptance than templated notes
- Use when you have multiple engagements and comments

**Asset-Led Note (For 2 touches):**
- Keep under 250 characters
- Reference specific pain point from their post
- Genuine curiosity, not sales pitch

**Example:**
```
Hi [Name], your post on [Topic] resonated.

Curious how you're handling [challenge]?
Seeing similar patterns across [their industry] in [geography].
```

**Step 3: Send Connection Request**

**Optimal timing:**
- Tuesday-Thursday: 9:00 AM - 10:30 AM (your timezone)
- Secondary: Tuesday-Thursday: 12:00 PM - 1:00 PM (your timezone)

**Daily limits:**
- Max 15 requests/day
- Target >30% acceptance rate

**Step 4: Update Shared Log**

After sending:
- Update `shared/logs/linkedin-activity.md` → "Connection Requests" table
- Log: Date, Time, Name, Profile URL, Blank/Asset-led, Notes
- Update `icp-prospects.md` → Connection Status column to "pending"

### DM Strategy (After Connection Accepted)

**When:** Within 24 hours of acceptance

**Approach:** Value-first, not sales

**Template 1: Reference Previous Engagement**
```
Hi [Name], thanks for connecting!

Your thoughts on [topic from their post] really resonated.
We're seeing [related insight] in our work with [industry].

Would love to hear how you're approaching [challenge they mentioned].
```

**Template 2: Offer Value/Asset**
```
Hi [Name], appreciate the connect!

Based on your post about [topic], thought you might find
[asset/framework/resource] useful. It's helped a few
[their role] in [their industry] with [specific challenge].

Happy to share if relevant.
```

**Template 3: Genuine Curiosity**
```
Hi [Name], great to connect!

Curious about [specific thing from their profile/posts].
How are you handling [challenge] at [Company]?

We're exploring [related topic] and would value your perspective.
```

**DM Best Practices:**
- Keep under 3-4 lines
- Reference specific context from engagement history
- Ask one clear question
- Offer value before asking anything
- No immediate sales pitch

**Step 5: Update Tracking**

After DM sent:
- Update shared log → "DMs Sent" table
- Log: Date, Time, Name, DM Type, Response Status
- Update `icp-prospects.md` → Notes column with DM summary

### Follow-Up Sequence (If No Response)

**Day 3:** No follow-up needed yet
**Day 7:** Soft check-in (if they viewed but didn't reply)
```
Hi [Name], just circling back - curious if you had
thoughts on [original question]?
```

**Day 14+:** No further follow-up. Focus on continuous nurturing via content engagement.

**If they respond:** Start conversation, focus on understanding their challenges, not pitching.

---

## Phase 7: Continuous Nurturing

**Skill:** `linkedin-daily-planner`
**When:** Daily workflow for ongoing engagement
**Purpose:** Orchestrate daily LinkedIn activities across time blocks

### The Daily Workflow

linkedin-daily-planner divides your day into engagement blocks with specific targets.

### Time Block Strategy

**MORNING BLOCK (Enhanced):**
- 3 PEER + 3 PROSPECT + 3 THOUGHT LEADER (diverse warm-up)
- Activities:
  1. **Feed Discovery** - Find new prospects from feed
  2. **Algorithm Training** - Visit profiles, follow, prime feed
  3. **Hashtag Discovery** - Topic-based prospecting
  4. **Standard engagement** - Comment on posts

**MIDDAY BLOCK:**
- PROSPECT-only engagement
- Focus on warming pipeline (0→3 touches)

**AFTERNOON BLOCK:**
- PROSPECT-only engagement
- Focus on high-priority (2-touch → 3-touch conversion)

**EVENING BLOCK:**
- PROSPECT-only engagement
- Final touchpoints before connection

### How to Run

**Four modes:**

**1. AUTONOMOUS MODE** - "start linkedin"
- Runs full workflow without questions
- AI auto-selects and executes all tasks
- Fully automated daily execution

**2. CREATE PLAN MODE** - "plan my day" or "daily linkedin plan"
- Generates to-do list for the day
- User executes tasks manually

**3. RESUME MODE** - "resume linkedin" or "linkedin status"
- Continue from where you left off

**4. CHECK SCHEDULE MODE** - "what time block am I in" or "when should I post"
- Shows current time block and recommendations

### The 3-3-3 Rule (Minimum Daily Engagement)

**Reference:** `references/contact-classification.md`

- 3 comments on **PEER** posts (1K-10K followers, fellow builders)
- 3 comments on **PROSPECT** posts (ICP, decision-makers)
- 3 comments on **THOUGHT LEADER** posts (10K+ followers)

**Growth Baseline:** 5-15 high-quality comments/day

### Morning Block Workflow

**1. Feed Discovery (10-15 minutes)**
- Scan LinkedIn feed for new prospects
- Look for posts with pain signals
- Screen for ICP fit (geography, role, company, pain)
- Save qualified prospects to `icp-prospects.md`

**2. Algorithm Training (5-10 minutes)**
- Visit 5-10 prospect profiles
- Follow each profile
- Turn on notifications (if ICP match)
- Primes feed to show more ICP content
- Harvest profile recommendations while visiting

**3. Hashtag Discovery (10 minutes)**
- Search posts by relevant hashtag
- Filter for engagement (20+ likes, 10+ comments)
- Filter for individuals only (exclude company pages)
- Screen for ICP fit

**4. Standard Engagement (20 minutes)**
- 3 PEER posts
- 3 PROSPECT posts
- 3 THOUGHT LEADER posts

**Total: 45-55 minutes**

### Midday/Afternoon/Evening Block Workflow

**Each block: 15-20 minutes**

**1. Check Warming Pipeline**
- linkedin-icp-warmer finds opportunities
- Prioritize:
  - 🔥 2-touch → 3-touch (highest priority)
  - 🟡 1-touch → 2-touch (conversion gap)
  - 🆕 0-touch → 1-touch (clear backlog)

**2. Generate Comments**
- linkedin-pro-commenter (autonomous mode)
- AI analyzes post, generates 3 variations, auto-selects best
- Post comment immediately

**3. Update Shared Log**
- `shared/logs/linkedin-activity.md`
- Log all engagement activity

### Golden Hour Rule

**CRITICAL for 360Brew distribution:**

**15 minutes BEFORE posting:**
- Engage with 5-10 posts (comments, not just likes)
- Warms topical relevance

**15 minutes AFTER posting:**
- Engage with 5-10 posts
- Extends distribution window for 4 hours

### Shared Activity Log (Central Hub)

**File:** `shared/logs/linkedin-activity.md`

**Contains:**
- Warming Up table (1-2 touch prospects)
- Ready to Connect table (3+ touches)
- Pending Acceptance table
- Connected (Recent) table
- Comments Made (last 7 days)
- DMs Sent
- Posts Published
- High-Value Interactions
- Feed Insights Cache
- Profile Cache

**On each run:**
1. **Read shared log FIRST** (not LinkedIn page)
2. Check today's activity status
3. Only access LinkedIn if log is stale (>4 hours)
4. **Update shared log AFTER** every action

**Benefits:**
- Token efficiency (reuse cached data)
- Activity history preserved
- Cross-skill coordination
- Quick navigation (Profile URLs + Post URLs saved)

### Browser Automation

linkedin-daily-planner uses two automation stacks:

**Primary:** Chrome DevTools MCP (default)
**Fallback:** Playwright MCP

**Tool mapping documented in the skill file.**

### Profile Cache Optimization

**7-day TTL cache** minimizes LinkedIn visits:
- Last Checked timestamp
- Activity Status
- Follower count
- Last Post date
- Recent Post URLs (up to 3)
- Engagement Score

**After 1 month:** ~70% of prospects will be cached, dramatically reducing screening time.

### Quality Checklist (Daily)

Before ending session:
- [ ] Shared log updated with all activity
- [ ] Profile Cache updated for visited profiles
- [ ] Email captured for any 1st-degree connections
- [ ] icp-prospects.md synced (if using Google Sheets)
- [ ] Activity logged: Comments, DMs, Connections
- [ ] Pipeline health checked (0-touch < 10, 1-touch < 15)

---

## Supporting Skills

### linkedin-pro-commenter

**Purpose:** Generate authentic LinkedIn comments (15-50 words) that prove genuine engagement

**Key Rules:**
- **🛑 ABSOLUTELY NO EM-DASHES (—)** - Instant AI detection signal
- 15-50 word range (STRICT)
- Must prove you read the post
- Add new information/perspective
- Reflect real experience
- Have a point of view

**Engagement Modes:**
1. Extension/Building - "Yes, and here's what connects..."
2. Challenge/Reframe - "I see it differently because..."
3. Question/Probe - "This raises interesting question..."
4. Pattern Recognition - "This matches what I'm seeing..."

**Autonomous Mode (when called from daily planner):**
- AI analyzes post context
- Generates 3 variations
- Auto-selects best comment
- Posts immediately
- No user prompts

**Interactive Mode:**
- User pastes post content
- AI generates 3 variations
- AI auto-selects best with reasoning
- User can override if needed

**360Brew Comment Rules:**
- 15-word minimum (algorithm filters shorter as "low-value")
- 50-word maximum (conciseness)
- Thread depth matters (back-and-forth extends post life 48+ hours)
- Response time boost (reply within 24h = +35% visibility)

**The "Did I Actually Read This?" Test:**
- Could someone write this without reading the post?
- If yes → it's performative garbage, start over

### linkedin-elite-post

**Purpose:** Generate high-performing LinkedIn posts optimized for engagement, thought leadership, conversions

**Key Rules:**
- **⚠️ NO EM-DASHES (—)** - AI detection signal
- **⚠️ NO BOX-DRAWING LINES (━━━)** - Looks AI-generated
- **⚠️ USE UNICODE BOLD, NOT MARKDOWN** - LinkedIn doesn't support `**bold**`
- **CRITICAL: Maximum 2700 characters** (90% of LinkedIn's 3000 limit)

**Unicode Bold Reference:**
```
𝗔 𝗕 𝗖 𝗗 𝗘 𝗙 𝗚 𝗛 𝗜 𝗝 𝗞 𝗟 𝗠 𝗡 𝗢 𝗣 𝗤 𝗥 𝗦 𝗧 𝗨 𝗩 𝗪 𝗫 𝗬 𝗭
𝗮 𝗯 𝗰 𝗱 𝗲 𝗳 𝗴 𝗵 𝗶 𝗷 𝗸 𝗹 𝗺 𝗻 𝗼 𝗽 𝗾 𝗿 𝘀 𝘁 𝘂 𝘃 𝘄 𝘅 𝘆 𝘇
```

**Post Modes:**
1. Thought Leadership - Insights, frameworks, unique perspectives
2. Educational - Teaching, breaking down complexity
3. Engagement - Questions, experiences, community building
4. Lead Generation - Direct, solution-focused
5. **Save-Worthy Asset** - Practical artifacts users save

**360Brew Algorithm Compliance:**
- Profile-to-Post alignment (80% content must match profile keywords)
- "See More" hook (first 2 lines determine expansion)
- Saves > Likes (Save valued 5x more than Like, 2x more than Comment)
- External links penalized (60% reach reduction - use first comment)
- Golden Hour (engage 5-10 posts before/after posting)

**AI Auto-Selection:**
After generating 2-3 variations, AI selects best based on:
- Hook strength (30%)
- 360Brew alignment (25%)
- Content depth (20%)
- Engagement potential (15%)
- Day-content fit (10%)

**Posting Schedule (NEVER POST IMMEDIATELY):**

| Day | Best For | Primary Window (your timezone) |
|-----|----------|---------------------|
| Monday | Week-starters, strategy | 10:00-11:30 AM |
| Tuesday | Major demos, technical | 8:30-10:30 AM |
| Wednesday | Save-worthy assets | 9:00-11:00 AM |
| Thursday | Thought leadership | 10:00 AM-12:00 PM |
| Friday | Reflections, wins | 8:30-10:00 AM |

**MANDATORY: Always use LinkedIn's "Schedule" feature**
- Click clock icon (🕐) in post composer
- Select optimal day + time based on content type
- Click "Schedule" (NOT "Post")

**Image Usage:**
- **Default: Text-only** (single images get 30% less reach)
- Only generate images if user explicitly requests
- Alternatives: PDF carousels, native video, inline text assets

### linkedin-trender

**Purpose:** Analyze LinkedIn feed to identify trending topics for content creation

**How it Works:**

**Autonomous mode (from daily planner):**
- Navigate to LinkedIn feed
- Scroll to load 30-50 posts from past 24h
- Extract feed content
- Parse and filter posts
- Auto-select top trending topic
- Proceed to linkedin-elite-post generation

**Interactive mode:**
- Ask user to paste feed content
- Present trending topics
- User selects topic
- Generate post with linkedin-elite-post

**Filters:**
- Engagement threshold: 20+ likes AND 10+ comments
- Individual authors only (NO company pages, brands, articles)
- Native LinkedIn posts (not reshares)

**Output:**
- Trending topic #1 (Hot Now)
- Trending topic #2 (Rising)
- Trending topic #3 (Your Lane)
- Each with: Evidence, Why It's Working, Your Angle

**360Brew Context:**
- Only recommend topics aligned with profile keywords
- Look for Save-worthy signals
- Focus on quality arguments, not engagement-bait
- Emerging voices valued (not just established influencers)

---

## Quick Reference

### Commands Cheat Sheet

**Onboarding:**
- "setup linkedin" or "onboard linkedin"

**ICP Definition:**
- "find my ICP" or "extract icp"

**ICP Discovery:**
- "find prospects" or "classify contacts"
- "train algorithm" or "prime my feed"
- "scan feed" or "feed discovery"
- "scan hashtag [tag]"
- "harvest recommendations"
- "check inbound"

**ICP Warming:**
- "warm up my ICPs"
- "find posts from prospects"
- "warmup opportunities"

**Connection Timing:**
- "who should I connect with"
- "connection timing"
- "ready to connect"

**Daily Workflow:**
- "start linkedin" (autonomous)
- "plan my day" (create to-do)
- "resume linkedin" (continue)

**Content Creation:**
- "find trending topics" (linkedin-trender)
- "create linkedin post" (linkedin-elite-post)

**Comments:**
- Paste post content → linkedin-pro-commenter

### File Locations

**Configuration:**
- `references/icp-profile.md` - ICP targeting criteria
- `references/contact-classification.md` - Classification framework
- `references/linkedin-strategy.md` - 360Brew rules
- `shared/linkedin-account-config.md` - Account type & features

**Tracking:**
- `shared/logs/icp-prospects.md` - All discovered prospects + Profile Cache
- `shared/logs/linkedin-activity.md` - Shared activity log (central hub)
- `shared/logs/linkedin-blacklist.md` - NEVER engage contacts
- `shared/logs/inbound-screening-history.md` - Inbound signals cache

**Skill-Specific Logs:**
- `linkedin-connect-timer/logs/activity-log.md` - Incremental activity tracking
- `linkedin-icp-warmer/logs/warmup-runs.md` - Warming session history

### 360Brew Algorithm Rules (2026)

**Profile-Content Alignment:**
- 80% of content must align with profile keywords
- Off-topic posts flagged as "Low Authority"

**Engagement Hierarchy:**
- Save = 5x value of Like, 2x value of Comment
- Meaningful comments (15+ words) > reactions
- Thread depth extends post life 48+ hours

**Distribution Rules:**
- "See More" hook (first 2 lines) determines expansion
- Golden Hour (engage 5-10 posts before/after posting)
- External links in post body = 60% reach reduction
- Single images = 30% reach reduction

**Connection Limits:**
- 10-20 requests/day (higher triggers automation detection)
- Target >30% acceptance rate
- 2-3 Touch minimum before connecting

### Workflow Summary

**Weekly Cycle:**

**Monday:**
- Morning: Feed Discovery + Algorithm Training
- Midday/Afternoon: Warming (focus 0→1 touch)
- Evening: Check connection pipeline

**Tuesday:**
- Morning: Post (if scheduled) + Golden Hour engagement
- Midday/Afternoon: Warming (focus 1→2 touch)
- Evening: DM follow-ups

**Wednesday:**
- Morning: Save-worthy asset creation + schedule
- Midday/Afternoon: Warming (focus 2→3 touch)
- Evening: Inbound signal screening

**Thursday:**
- Morning: Feed Discovery + Hashtag Discovery
- Midday/Afternoon: Send connection requests (optimal day)
- Evening: Thought leadership post creation

**Friday:**
- Morning: Post (if scheduled) + Golden Hour engagement
- Midday/Afternoon: Lighter engagement, personal content
- Evening: Weekly review + pipeline health check

**Weekend:**
- Engagement only, no new content
- Monitor notifications, respond to DMs

### Success Metrics

**Pipeline Health:**
- 0-touch prospects: <10 (clear backlog before discovery)
- 1-touch prospects: <15 (conversion gap)
- 2-touch prospects: Growing (healthy pipeline)
- Pending connections: 5-10 active
- Acceptance rate: >30%

**Daily Activity:**
- Comments: 9-15 per day (3-3-3 rule minimum)
- Connection requests: 5-10 per optimal day
- DMs sent: 2-5 per day
- Posts: 3-5 per week

**Profile Cache Efficiency:**
- After 1 month: ~70% of prospects cached
- Reduces profile visits by 50-70%
- Saves 2-3 minutes per prospect

### Troubleshooting

**"ICP not configured"**
→ Run linkedin-onboarding OR linkedin-profile-icp first

**"No prospects found"**
→ Check geography filter (may be too strict)
→ Try different discovery methods (Feed, Hashtag, Inbound)

**"0-touch backlog > 20"**
→ Pause discovery, focus on warming existing prospects
→ Target: Clear 3+ prospects from 0-touch per day

**"Low acceptance rate (<25%)"**
→ Pause connection requests for 48h
→ Review 2-3 Touch Rule compliance
→ Check if using optimal send times

**"Profile Cache not working"**
→ Ensure Profile Cache table exists in icp-prospects.md
→ Update cache on every profile visit
→ Check Last Checked timestamp (<7 days)

---

## Conclusion

This comprehensive guide covers the complete LinkedIn workflow from initial setup through continuous nurturing. The key to success is:

1. **Start with Onboarding** - Configure your ICP and geography filters
2. **Discover Systematically** - Use multiple discovery methods (Feed, Hashtag, Inbound, Recommendations)
3. **Warm Consistently** - Follow 2-3 Touch Rule, never skip touches
4. **Connect Strategically** - Only after proper warming, optimal timing
5. **Nurture Continuously** - Daily engagement via linkedin-daily-planner

**Remember:**
- Geography filter is STRICT (no exceptions)
- Cache-first approach (minimize LinkedIn visits)
- Shared activity log is central hub (read first, update after)
- 360Brew compliance (profile alignment, saves > likes, Golden Hour)
- Quality over quantity (9-15 comments/day, 5-10 connections/optimal day)

**Next Steps:**
1. If not yet onboarded: Run "setup linkedin"
2. If onboarded: Run "start linkedin" for autonomous daily workflow
3. Check shared activity log regularly: `shared/logs/linkedin-activity.md`
4. Monitor pipeline health: Keep 0-touch < 10, 1-touch < 15

Happy prospecting! 🚀
