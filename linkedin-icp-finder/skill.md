---
name: linkedin-icp-finder
description: Contact classification, ICP discovery, and algorithm training for LinkedIn engagement in your target markets. Classifies contacts as PEER/THOUGHT LEADER/PROSPECT/CUSTOMER. NEW MODES - (1) Train Algorithm - systematically visit profiles, follow, turn on notifications to prime LinkedIn feed; (2) Feed Discovery - scan LinkedIn feed for new prospects on-the-fly; (3) Hashtag Discovery - find prospects discussing relevant topics. Traditional modes - classify contacts from various sources (competitor comments, inbound signals, group members, etc.). Works with browser automation (Claude for Chrome or DevTools fallback). AUTONOMOUS MODE - auto-executes without questions. INTERACTIVE MODE - presents findings for user selection. Solves core challenge: finding prospects' posts to engage with.
---

# LinkedIn Contact Classifier & ICP Finder

**Browser automation uses Claude for Chrome if available, otherwise falls back to Chrome DevTools. See linkedin-daily-planner skill for detailed tool mapping.**

Classify LinkedIn contacts and find prospects using the Digital Breadcrumb Strategy. Supports three contact types with tailored engagement approaches.

**Reference:** `references/contact-classification.md` for full classification criteria.

**STRICT GEOGRAPHY FILTER: Read target countries from `references/icp-profile.md`. If not configured, skip geography filter.**

**HARD RULE: If a prospect's location is not clearly one of your target countries (from `references/icp-profile.md`), SKIP IMMEDIATELY. Do not proceed with any further screening. No exceptions.**

## Trigger

**Outbound Mode (default):**
- "start icp" or "find prospects"
- "classify contacts" or "who should I engage with"
- Provides LinkedIn content (comment threads, search results, profile info) for screening

**Inbound Mode (lurker detection):**
- "check inbound" or "screen inbound"
- "who viewed my profile" or "check profile views"
- "screen my followers" or "check new followers"
- "who liked my posts" or "check post reactions"
- "find lurker ICPs" or "lurker prospects"

**Advanced Discovery Strategies:**
- "find resharers" or "who reshared my posts" → Content Re-sharers (🥇 highest)
- "check competitor comments" or "monitor competitors" → Competitor Commenters (🥈)
- "check shared connections" or "2nd degree prospects" → Shared Connections (🥉)
- "screen group members" or "check groups" → Group Members
- "screen event attendees" or "check event" → Event Attendees

**Algorithm Training & Discovery Modes (NEW):**
- "train algorithm" or "train feed" or "prime my feed" → Train Algorithm Mode
- "scan feed" or "find prospects in feed" or "feed discovery" → Feed Discovery Mode
- "scan hashtag [tag]" or "hashtag discovery" → Hashtag Discovery Mode
- "harvest recommendations" or "find lookalike prospects" or "expand from [prospect]" → Profile Recommendations Discovery Mode

## Step 0: Blacklist Check (MANDATORY FIRST STEP)

**CRITICAL: Before ANY contact classification or engagement, check the blacklist.**

**File location:** `shared/logs/linkedin-blacklist.md`

```
BEFORE CLASSIFYING ANY CONTACT:
1. Read linkedin-blacklist.md
2. Check if contact name OR profile URL appears in blacklist
3. If FOUND → SKIP ENTIRELY, move to next contact
4. If NOT FOUND → Proceed with classification
```

**This check overrides ALL other criteria. Never engage with blacklisted contacts.**

---

## Contact Classification (Apply FIRST)

Before ICP screening, classify each contact into one of three categories.

**Reference:** See `references/contact-classification.md` for full criteria and flowchart.

### Classification Criteria

| Category | Follower Range | Key Signals |
|----------|---------------|-------------|
| **PEER** | 1K - 10K | Same niche (AI/automation), content creator, builder |
| **THOUGHT LEADER** | 10K+ | Established authority, high engagement, Top Voice |
| **PROSPECT** | Any | Decision-maker at target company type, ICP role match, pain signals |

### Quick Classification Logic

```
1. Check if PROSPECT first (role-based, not follower-based):
   → Is this person a potential CUSTOMER?
   → Decision-maker at target company type? Pain points you solve?
   → If YES → PROSPECT (proceed to ICP screening)

2. If NOT a prospect, check followers:
   → 10K+ followers → THOUGHT LEADER
   → 1K-10K + same niche/builder → PEER
   → <1K or irrelevant niche → GENERAL (lower priority)
```

### Classification Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTACT CLASSIFICATION: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORY: [PEER / THOUGHT LEADER / PROSPECT / GENERAL]

Followers: [X]K
Niche Match: [Yes/No - specify niche]
Role: [Title]
Builder Signals: [Yes/No - what they create/ship]

Engagement Strategy: [See category-specific approach below]
```

### Category-Specific Engagement

**PEER (1K-10K, same niche):**
- Comment tone: Collaborative, share complementary insights
- Goal: Build relationship, potential collaboration
- Comment strategy: "Yes, and..." extension, shared experiences

**THOUGHT LEADER (10K+):**
- Comment tone: Add unique POV, thoughtful questions
- Goal: Visibility boost, credibility by association
- Comment strategy: Challenge/reframe or insightful question

**PROSPECT (ICP match):**
- Comment tone: Mirror & Add, demonstrate expertise
- Goal: Plant seeds, establish credibility for future connection
- Comment strategy: Empathy + insight, low-friction question
- → Proceed to full ICP screening (Step 2)

## Step 0: Pre-Screening Cross-Check (Efficiency Filter)

**Reference:** `shared/references/signal-screening-workflow.md` for complete protocol

**CRITICAL: Before screening ANY new contact, perform three-file cross-check.**

### Three-File Cross-Check Hierarchy

```
BEFORE SCREENING ANY CONTACT:

1️⃣ BLACKLIST CHECK (MANDATORY) ⛔
   → grep -i "contact name" shared/logs/linkedin-blacklist.md
   → IF FOUND: SKIP immediately, do not screen or engage
   → IF NOT FOUND: Continue to step 2

2️⃣ PROFILE CACHE CHECK (Skip Profile Visit) 🚀
   Check BOTH cache locations:
   → grep -i "contact name" shared/logs/inbound-screening-history.md
   → OR check Profile Cache table in shared/logs/icp-prospects.md

   IF FOUND:
   → Use cached classification (PROSPECT/PEER/THOUGHT LEADER/NON-ICP)
   → Skip LinkedIn profile visit
   → Use cached data for classification output

   IF NOT FOUND:
   → New contact, proceed with full screening (Step 1+)

3️⃣ ICP PROSPECTS CHECK (Engagement Rules) 📊
   → grep -i "contact name" shared/logs/icp-prospects.md

   IF FOUND:
   → Already tracked prospect
   → Note current touch count
   → Note last engagement date
   → Include in output with existing data

   IF NOT FOUND:
   → New prospect, will be added after screening
```

**Efficiency Gain:** After 1 month, ~70% of contacts will be pre-classified, reducing redundant profile visits.

### Pre-Search Checklist (After Cross-Check)

```
ONLY SEARCH LINKEDIN IF:
1. Contact passed blacklist check (not blacklisted)
2. Contact NOT in Profile Cache (no cached classification)
3. OR cache data > 7 days old
4. OR specific new data needed (email, recent posts)
```

### Data to Capture Per Profile Visit

**When you visit a LinkedIn profile, capture ALL of this data in ONE visit:**

| Data Point | Where to Store | Why Capture |
|------------|----------------|-------------|
| Name, Role, Company | Prospects table | Core identification |
| Profile URL (full) | Prospects table | Deduplication key |
| Connection degree (1st/2nd/3rd) | Prospects table → Degree | Email visibility, DM access |
| Email (if visible) | Prospects table → Email | Direct outreach |
| Follower count | Profile Cache → Followers | Classification (Peer/Leader) |
| Last post date | Profile Cache → Last Post | Activity status |
| Recent post URLs (up to 3) | Profile Cache → Recent Posts | Warming opportunities |
| Activity status | Profile Cache → Activity Status | Skip inactive prospects |

### Update Profile Cache on Every Visit

**After visiting ANY prospect profile, immediately update the Profile Cache table:**

```markdown
| # | Profile URL | Last Checked | Activity Status | Followers | Last Post | Recent Post URLs | Engagement Score |
|---|-------------|--------------|-----------------|-----------|-----------|------------------|------------------|
| X | /in/[username]/ | [DDMon HH:MM] | [ACTIVE/MODERATE/INACTIVE] | [~XK] | [DDMon] | [url1, url2, url3] | [LOW/MED/HIGH] |
```

**Activity Status Rules:**
- `ACTIVE` = Posted within last 7 days
- `MODERATE` = Posted within 7-30 days
- `INACTIVE` = No posts in 30+ days (skip warming)

### Deduplication Check (MANDATORY)

**Before adding ANY new prospect:**

```
1. Read icp-prospects.md → Prospects table
2. Search for match by:
   - Profile URL (primary key)
   - Name + Company (fallback if URL missing)
3. If MATCH FOUND:
   → Do NOT add duplicate
   → Update cache data if visiting profile
   → Log: "Duplicate skipped: [Name] already in row #X"
4. If NO MATCH:
   → Add new prospect
   → Update Profile Cache
```

---

## Step 0b: Load ICP Profile

**Always start by reading `references/icp-profile.md`** to load current ICP criteria.

**If ICP not configured** (shows "[Not configured]"):

**AUTONOMOUS MODE (when called from linkedin-daily-planner):**
- Skip ICP discovery entirely
- Log warning to shared activity log: "ICP not configured - skipping prospect discovery"
- Return to calling workflow without blocking

**INTERACTIVE MODE (when called directly by user):**
1. Ask user: "I don't have an ICP profile configured yet. Would you like to:"
   - Provide your ICP criteria now (roles, company size, pain points)
   - Run linkedin-profile-icp on your LinkedIn profile first
   - Describe who your ideal customers are
2. Once user provides info, update `references/icp-profile.md` with the new criteria
3. Then proceed with screening

**If ICP is configured**: Proceed to Step 0c.

---

## Step 0c: Check Account Type & Optimize Search Strategy

**Read account config:** `shared/linkedin-account-config.md`

Check the Account Type and use the appropriate search strategy:

### FREE Account Search Strategy

**Constraints:** ~100 searches/month, limited filters, 5 profile viewers visible

```
SEARCH OPTIMIZATION (FREE):
1. Use specific keywords to reduce wasted searches:
   - "[Target Role] [Target Geography] [Target Industry]" instead of just "[Target Role]" (read values from `references/icp-profile.md`)
   - "[Industry] founder" instead of just "founder"

2. Rely more on INBOUND signals (no search cost):
   - Profile viewers (limited but free)
   - Post reactors
   - New followers
   - Comment threads

3. Search sparingly - prefer:
   - Competitor comment threads (one search, many prospects)
   - Group member lists (one access, many prospects)
   - Event attendee lists (one access, many prospects)

4. ALWAYS cache data - cannot afford repeat searches
```

### PREMIUM Account Search Strategy

**Advantages:** Unlimited searches, all profile viewers, Boolean search

```
SEARCH OPTIMIZATION (PREMIUM):
1. Use Boolean operators for precise targeting:
   Example: ([Target Role 1] OR [Target Role 2] OR [Target Role 3]) AND [Target Geography] AND ([Target Company Type])
   → Read target roles, geography, and company types from `references/icp-profile.md`

2. Check ALL profile viewers (90 days available):
   → linkedin.com/me/profile-views/
   → Screen each viewer for ICP fit
   → Higher volume of inbound signals

3. Use enhanced filters:
   - Industry filter
   - Specific company filter
   - Location with radius
   - School filter

4. Save up to 5 searches for quick re-access
```

### SALES_NAVIGATOR Search Strategy

**Advantages:** 25+ advanced filters, lead recommendations, saved search alerts

```
SEARCH OPTIMIZATION (SALES NAVIGATOR):

🔥 PRIORITY #1: "POSTED ON LINKEDIN" FILTER (ALWAYS ENABLE)

When searching for NEW ICP prospects in Sales Navigator, ALWAYS enable the
"Posted on LinkedIn" filter FIRST. This ensures every prospect you find has
recent posts you can engage with via comments.

WHY THIS MATTERS:
→ Prospects with recent posts = immediate engagement opportunity
→ Can comment on their posts to start warming (first touch)
→ No wasted discovery of inactive prospects
→ Direct path: Find → View Post → Comment → Save to prospects

HOW TO USE:
1. Go to Sales Navigator search
2. Enable "Posted on LinkedIn" filter (under Spotlight section)
3. Combine with your ICP filters (company size, seniority, geography)
4. Each result is now a WARM-ABLE prospect with content to engage

WORKFLOW:
Search with "Posted on LinkedIn" → Find ICP match → View their recent post
→ Comment using linkedin-pro-commenter → Save to icp-prospects.md

1. BUILD SAVED SEARCHES WITH ALERTS:
   Create these searches and enable daily/weekly alerts:

   ⚠️ IMPORTANT: Always include "Posted on LinkedIn: Yes" in ALL searches
   to ensure prospects have recent content for engagement.

   Search 1: "Target Market Decision Makers"
   ├─ Company size: (from `references/icp-profile.md` target company size)
   ├─ Seniority: (from `references/icp-profile.md` target roles)
   ├─ Geography: (from `references/icp-profile.md` target countries)
   └─ 🔥 Posted on LinkedIn: Yes (REQUIRED for engagement)

   Search 2: "[Function] Leaders in [Target Geography]"
   ├─ Function: (from `references/icp-profile.md` target functions)
   ├─ Seniority: Manager, Director, VP
   ├─ Geography: (from `references/icp-profile.md` - primary market)
   ├─ Company size: (from `references/icp-profile.md`)
   └─ 🔥 Posted on LinkedIn: Yes (REQUIRED for engagement)

   Search 3: "Recent Job Changers (ICP Roles)"
   ├─ Changed jobs: Last 90 days
   ├─ Seniority: Director, VP, CXO
   ├─ Geography: (from `references/icp-profile.md` target countries)
   ├─ Function: (from `references/icp-profile.md` target functions)
   └─ 🔥 Posted on LinkedIn: Yes (REQUIRED for engagement)

2. USE ADVANCED FILTERS (replaces manual screening):
   → Company Size filter = auto-screen target company type
   → Seniority filter = auto-screen decision-makers
   → Function filter = auto-screen relevant roles
   → "Posted recently" = auto-screen active users

3. LEAD RECOMMENDATIONS:
   → Save 5-10 best ICP matches as leads
   → Check "Similar leads" weekly
   → Algorithm learns your preferences

4. TEAMLINK (if team has Sales Navigator):
   → Before cold outreach, check for warm intro paths
   → See team members' connections to prospect

5. SAVED LEADS LIST:
   → Save all qualifying prospects to a Lead List
   → Export for CRM integration
   → Track engagement within Sales Navigator

6. ⚠️ DATA PRESERVATION (CRITICAL):
   → Sales Navigator data is LOST when subscription ends
   → ALWAYS save leads to local icp-prospects.md IMMEDIATELY
   → Copy Lead Notes to local Notes column
   → Document Saved Searches in linkedin-account-config.md
   → See: shared/linkedin-account-config.md → Data Preservation section
```

### Sales Navigator Data Export Rule

**MANDATORY: Every lead found in Sales Navigator must be saved locally.**

```
FOR EACH SALES NAVIGATOR LEAD:
1. Add to icp-prospects.md (Prospects table) with ALL fields
2. Update Profile Cache with: Followers, Activity Status, Last Post
3. In Notes column, include:
   - Source: "Sales Nav: [search name]"
   - Any Tags: "#tag1 #tag2"
   - Lead Notes: Copy verbatim from Sales Navigator
4. Log any InMail/engagement to linkedin-activity.md
```

**Why:** If subscription ends, all Sales Navigator data is deleted. Local files are your permanent backup.

### Account-Specific Search Limits

| Account | Daily Search Limit | Recommendation |
|---------|-------------------|----------------|
| FREE | ~10 searches/day safe | Use inbound-heavy strategy |
| PREMIUM | Unlimited | Search freely, use Boolean |
| SALES_NAVIGATOR | Unlimited | Use saved searches + alerts |

---

## Step 1: Identify Content Source

Determine what the user has provided:
- **Competitor Gripe Thread**: Comments on competitor/legacy vendor posts
- **Authority Post Comments**: Comments on thought leader posts
- **Search Results**: LinkedIn search for pain-related keywords
- **Single Profile/Comment**: Individual prospect to screen

## Step 2: ICP Screening (3-Second Scan)

For each prospect, evaluate against the **loaded ICP criteria** from `references/icp-profile.md`:

### 🚨 MANDATORY: Geography Filter (APPLY FIRST - NO EXCEPTIONS)

**ONLY PASS if prospect is CLEARLY from one of your target countries (loaded from `references/icp-profile.md`).**

**IMMEDIATELY SKIP if:**
- Prospect is from a country NOT in your target geography list
- Location field shows a non-target country
- Company is headquartered outside your target countries (even if prospect claims target location)
- Geography is unclear, ambiguous, or not specified

**Geography verification (check in order):**
1. Profile location field (must explicitly show one of your target countries)
2. "Based in [target location]" in headline/about
3. Current company location

**If geography cannot be confirmed as one of your target countries, SKIP. Do not guess. Do not proceed with caution. Just skip.**

### Role Filter
Match against Target Roles table from ICP profile.

**Focus on Management Roles**: Prioritize managers, directors, team leads, and heads of departments over strictly C-suite/Founder roles. Management-level professionals often have direct pain points with operations, processes, and systems. Accept any role with "Manager", "Director", "Head of", or "Lead" in the title if they're discussing relevant business challenges.

### Company Filter
Match against Target Company Profile from ICP profile.

### Post Engagement Filter (APPLY BEFORE PAIN SIGNAL)

**IMMEDIATELY SKIP if the post is:**
- ❌ **Job posting or hiring announcement** (e.g., "We're hiring", "Join our team", "Open role", job descriptions)
- ❌ **Comments are disabled** on the post (cannot engage meaningfully)

**Why skip job posts:** Job announcements don't reveal pain points or business challenges. Commenting on hiring posts appears opportunistic rather than genuine engagement.

**Why skip disabled comments:** No engagement opportunity exists. Move to next prospect.

### Pain Signal Filter

| ✅ High Signal | ❌ Low Signal |
|----------------|---------------|
| Specific frustrated question | "Great post!" |
| Describes concrete problem | Generic agreement |
| Asks for recommendations | Tagging colleagues |
| Vents about specific software | One-word reactions |
| Uses ICP pain keywords | Off-topic comments |
| | Job postings/hiring announcements |

## Step 3: Output ICP Screening Verdict

For each prospect:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICP SCREENING: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌏 GEOGRAPHY: [✅ CONFIRMED TARGET GEO / ❌ NON-TARGET GEO / ❌ UNCONFIRMED - SKIP]
Location: [Country/City - must match target countries from icp-profile.md]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT / ❌ SKIP - NOT TARGET GEO / ❌ SKIP - JOB POST / ❌ SKIP - COMMENTS DISABLED]

Role: [Title] → [Match assessment vs ICP roles]
Company: [Company, size if visible] → [Match assessment vs ICP company profile]
Pain Signal: [Quote/paraphrase] → [Match vs ICP pain keywords]

Fit Score: [X/4 criteria met] (Geography + Role + Company + Pain)
```

**If ❌ NON-TARGET GEO or ❌ UNCONFIRMED**: Stop screening immediately. Do not evaluate role, company, or pain signals. Output only geography verdict and move to next prospect. No exceptions.

## Step 4: Breadcrumb Engagement Plan

**PREREQUISITE: Only proceed to this step if prospect has ✅ CONFIRMED TARGET GEO (matches countries in `references/icp-profile.md`).**

For ✅ HIGH FIT or ⚠️ MEDIUM FIT prospects with confirmed target geography:

**A. Recommended Reaction**
- **Save their post** (360Brew values a Save at 5x more than a Like, 2x more than a Comment)
- "Insightful" (💡) for intellectual/strategic comments
- "Support" (❤️) for frustrated/struggling comments

**B. Mirror & Add Comment Draft (15-50 words)**

**360Brew Comment Rules:**
- Minimum 15 words (shorter comments filtered as "low-value")
- Maximum 50 words (conciseness is key)
- Must add Point of View (POV) or insight
- Comments with follow-up questions extend post life 48+ hours

Framework: Acknowledge pain + Relevant insight + Low-friction question

```
MIRROR & ADD COMMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Comment text]

(Word count: X/50)

Why this works:
- Mirrors: [Pain acknowledged]
- Adds: [Insight contributed]
- Opens: [Question asked]
```

**C. Connection Request Strategy (After They Reply)**

Wait 24 hours, then send connection request.

**360Brew Connection Rules (2026):**
- Blank requests perform 10-15% better than templated notes UNLESS note is 100% bespoke
- If using a note, keep it under 2 sentences
- Max 10-20 requests/day (higher volume triggers "Automation Detection")
- If comment generated meaningful reply, blank request is fine (context already established)

```
CONNECTION REQUEST NOTE (Only if bespoke)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hi [Name], enjoyed our exchange on [Author]'s post about [Topic].

I work on [relevant area] and would love to keep in touch.

(Under 300 characters)
```

**Alternative: Blank Request** (Often better if prior engagement exists)

---

## Inbound Mode: Lurker ICP Detection

**For ICPs who consume content but don't post or comment.**

Lurkers leave signals when they engage passively with your content. This mode screens those inbound signals for ICP matches.

### Inbound Signal Sources (Priority Order)

| Signal | URL | ICP Value | Why High Value |
|--------|-----|-----------|----------------|
| **Connection Requests** | My Network → Invitations | 🔥🔥🔥 HIGHEST | They reached out first |
| **Profile Views** | linkedin.com/me/profile-views/ | 🔥🔥 VERY HIGH | Actively researched you |
| **New Followers** | linkedin.com/mynetwork/network-manager/people-follow/followers/ | 🔥🔥 VERY HIGH | Want ongoing access to your content |
| **Post Reactions** | Notifications → Who liked your posts | 🔥 HIGH | Engaged with specific content |

### Inbound Screening Workflow

```
STEP I1: Navigate to Inbound Source
         ↓
STEP I2: For each person, apply filters:
         ├─ Geography: Target countries only (from `references/icp-profile.md`)
         ├─ Role: Decision-maker, Manager+
         ├─ Company: Target company size (from `references/icp-profile.md`)
         └─ Engagement context: What triggered them?
         ↓
STEP I3: Output verdict (same as outbound)
         ↓
STEP I4: Save to icp-prospects file OR Warming Up table
```

### Step I1: Navigate to Inbound Sources

**Connection Requests (check first):**
```
linkedin.com/mynetwork/invitation-manager/
```
- Inbound requests = they want to connect with YOU
- Highest intent signal
- Screen before accepting

**Profile Views:**
```
linkedin.com/me/profile-views/
```
- Shows who viewed in last 90 days
- Premium shows all viewers; Free shows limited
- Note: Some viewers browse anonymously

**New Followers:**
```
linkedin.com/mynetwork/network-manager/people-follow/followers/
```
- People following without connecting
- Often lurkers who want your content
- Sort by "Recently added" for new followers

**Post Reactions:**
```
Click on reaction count on your recent posts
```
- See who liked/celebrated/supported
- Cross-reference with non-commenters = lurkers
- High-engagement posts attract more lurkers

### Step I2: Screen Each Inbound Signal

Apply the same ICP filters as outbound:

```
🚨 GEOGRAPHY FIRST (NO EXCEPTIONS)
├─ ✅ PASS: Target countries only (from `references/icp-profile.md`)
└─ ❌ SKIP: All others, unclear = immediate skip

👤 ROLE CHECK
├─ ✅ Decision-maker, Manager, Director, Head of, C-suite
└─ ❌ Skip: Junior, Individual Contributor, Student

🏢 COMPANY CHECK
├─ ✅ Target company size (from `references/icp-profile.md`)
└─ ❌ Skip: Outside target company profile

🔥 ENGAGEMENT CONTEXT (Lurker-specific)
├─ What content triggered them? (profile view after which post?)
├─ How recent? (last 24h = hot, last week = warm)
└─ Repeat viewer? (multiple views = very high intent)
```

### Step I3: Inbound Screening Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INBOUND ICP SCREENING: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SOURCE: [Profile View / New Follower / Post Reaction / Connection Request]
SIGNAL DATE: [When they engaged]
CONTEXT: [What content may have triggered this]

🌏 GEOGRAPHY: [✅ CONFIRMED TARGET GEO / ❌ SKIP]
Location: [Country]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company, size] → [Match assessment]
Lurker Signal: [What action they took + when]

ENGAGEMENT RECOMMENDATION:
[Based on signal type - see table below]
```

### Engagement Strategy by Signal Type

| Signal Type | They Did | You Should Do | Timeline |
|-------------|----------|---------------|----------|
| **Connection Request** | Sent you request | Screen → Accept if ICP → Send value DM | Accept within 24h |
| **Profile View** | Viewed your profile | View them back → Find their content → Comment | Within 48h |
| **New Follower** | Followed you | Follow back → Find their posts → Engage | Within 48h |
| **Post Reaction** | Liked your post | Find their posts → Comment → Build touches | Within 1 week |

### Lurker Fast-Track Rule

**Inbound signals = warmer than cold outbound.**

| Source | Starting "Warmth" | Touches to Connect |
|--------|-------------------|-------------------|
| Cold outbound (you found them) | 0 | Need 2-3 touches |
| Post reaction (they liked you) | 1 | Need 1-2 more |
| Profile view (they researched you) | 1-2 | Need 1-2 more |
| New follower (they subscribed) | 2 | Need 1 more |
| Connection request (they reached out) | 3 | Accept + DM |

**Lurker ICPs can be fast-tracked** because they've already shown intent.

### Inbound Batch Screening

When screening multiple inbound signals at once:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INBOUND ICP SCREENING BATCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: [Profile Views / Followers / Post Reactions]
Date range: [Last 24h / Last 7 days]
Total screened: [X]

✅ ICP MATCHES (High Fit):
1. [Name] - [Role] at [Company] - [Signal] - [Action]
2. [Name] - [Role] at [Company] - [Signal] - [Action]

⚠️ MEDIUM FIT (Review):
1. [Name] - [Role] at [Company] - [Why medium]

❌ SKIPPED:
- [X] Non-target geography
- [X] Junior roles
- [X] Enterprise/MNC
- [X] Unclear profile

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED ACTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Name]: [Specific action based on signal]
2. [Name]: [Specific action based on signal]
```

### Step I4: Save Inbound Prospects

Same rules as outbound:
- **0 touches** → Save to `icp-prospects-[date].md` (source: "Profile Views" or "New Followers")
- **Already engaged** → Add to Warming Up table with touch count

**Inbound prospects get special notation in the file:**

```markdown
## Session 2 - 14:30 - Inbound: Profile Views

Found via profile viewer screening.

| # | Name | Role | Company | Location | Classification | Profile URL | Notes |
|---|------|------|---------|----------|----------------|-------------|-------|
| 9 | [Name] | COO | [Company] | [Target Country] | PROSPECT | [URL] | 🔥 INBOUND: Viewed after automation post, 2x viewer |
| 10 | [Name] | Director Ops | [Company] | [Target Country] | PROSPECT | [URL] | 🔥 INBOUND: New follower, liked 3 posts |
```

---

## Advanced Discovery Strategies

Beyond standard search and inbound signals, these strategies find ICPs through behavioral signals.

### Strategy Priority Ranking

| Rank | Strategy | Why Effective | Trigger |
|------|----------|---------------|---------|
| 🥇 1 | **Content Re-sharers** | Highest engagement - they amplified YOU | "find resharers" |
| 🥈 2 | **Competitor Commenters** | Active buyers evaluating solutions | "check competitor comments" |
| 🥉 3 | **Shared Connections** | Warm intro path via mutual connections | "check shared connections" |
| 4 | **Group Members** | Self-selected into relevant topic | "screen group members" |
| 5 | **Event Attendees** | Concentrated interest in topic | "screen event attendees" |

---

### 🥇 Strategy 1: Content Re-sharers

**Why #1:** Someone who reshares your content is doing FREE marketing for you. They found it valuable enough to stake their reputation on it.

**How to Find:**
```
1. Go to your recent posts (last 30 days)
2. Look for "X reposts" under engagement stats
3. Click to see who reshared
4. Screen each resharer for ICP fit
```

**URL Pattern:**
```
Your post → Click "X reposts" link
```

**Screening Priority:**
- Reshared with added commentary → 🔥🔥🔥 HIGHEST (they added POV)
- Reshared to their feed → 🔥🔥 HIGH (public endorsement)
- Reshared to groups → 🔥 MEDIUM (targeted sharing)

**Engagement Action:**
```
1. Comment on THEIR post thanking them for sharing
2. Check their recent content → Comment on 1-2 posts
3. If ICP match: Already at 2 touches (reshare + your thank you)
4. One more touch → Ready for connection
```

**Output Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESHARER ICP SCREENING: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNAL: Reshared your post on [Date]
POST RESHARED: [Your post topic]
RESHARE TYPE: [With commentary / Direct repost / To group]

🌏 GEOGRAPHY: [✅ CONFIRMED TARGET GEO / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

WARMTH LEVEL: 2 touches (reshare = strong endorsement)
ACTION: Thank them + 1 comment on their content → Connect
```

**File Notation:**
```
| 11 | [Name] | [Role] | [Company] | [Target Country] | PROSPECT | [URL] | 🔄 RESHARER: Shared my [topic] post with commentary |
```

---

### 🥈 Strategy 2: Competitor Commenters

**Why #2:** People commenting on competitor posts are **actively evaluating solutions**. They have the problem NOW.

**How to Find:**
```
1. Identify competitor accounts (vendors in your space)
2. Find their recent posts about pain points you solve
3. Read the comments - look for:
   - Frustrated questions
   - "We tried this and..."
   - "Looking for alternatives..."
   - Specific pain descriptions
4. Screen commenters for ICP fit
```

**Competitor Types to Monitor:**
- Direct competitors (same solution space)
- Legacy vendors (ERP, CRM providers)
- Consultants in your niche
- Industry analysts/commentators

**High-Value Comment Signals:**
```
✅ HIGH SIGNAL (prioritize):
- "We've been struggling with..."
- "Any recommendations for..."
- "Switched from X because..."
- Asking specific technical questions
- Describing concrete problems

❌ LOW SIGNAL (skip):
- "Great post!"
- Tagging colleagues without context
- Generic agreement
- Promotional comments
```

**Engagement Action:**
```
1. DO NOT pitch in competitor's comments
2. Note the prospect's pain point
3. Find THEIR content → Comment with relevant insight
4. Build touches naturally, then connect
```

**Output Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPETITOR COMMENTER: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FOUND ON: [Competitor name]'s post about [topic]
COMMENT DATE: [Date]
PAIN SIGNAL: "[Quote their comment]"

🌏 GEOGRAPHY: [✅ CONFIRMED TARGET GEO / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

PAIN CATEGORY: [Which ICP pain this maps to]
ACTION: Find their posts → Comment with relevant insight → Build touches
```

**File Notation:**
```
| 12 | [Name] | [Role] | [Company] | [Target Country] | PROSPECT | [URL] | 🎯 COMPETITOR: Commented on [Vendor] about [pain] |
```

---

### 🥉 Strategy 3: Shared Connections

**Why #3:** 2nd-degree connections through your best clients = similar profile + warm intro path.

**How to Find:**
```
1. Identify your best clients/connections (ICP matches you've converted)
2. View their profile → "X mutual connections" or "X connections"
3. Click to see their network
4. Filter by role keywords (CEO, COO, Director, etc.)
5. Screen for ICP fit
```

**Best Source Connections:**
- Converted clients (highest signal - birds of a feather)
- Active engagers who match ICP
- Industry peers who know decision-makers

**Warm Intro Potential:**
```
If screening [Prospect] found via [Mutual Connection]:

INTRO PATH OPTIONS:
1. Ask [Mutual] for introduction (if relationship is strong)
2. Mention mutual in connection request: "I see we both know [Name]..."
3. Comment on content [Mutual] engaged with (natural touchpoint)
```

**Output Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHARED CONNECTION: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FOUND VIA: [Mutual Connection Name]'s network
MUTUAL RELATIONSHIP: [Client / Peer / Engager]

🌏 GEOGRAPHY: [✅ CONFIRMED TARGET GEO / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

WARM INTRO PATH: [Yes - can ask mutual / No - engage directly]
ACTION: [Ask for intro / Mention mutual in request / Engage content first]
```

**File Notation:**
```
| 13 | [Name] | [Role] | [Company] | [Target Country] | PROSPECT | [URL] | 🤝 SHARED: Via [Mutual Name], can request intro |
```

---

### Strategy 4: Group Members (Low Priority)

**Why Lower:** Groups can be noisy, but members self-selected into relevant topics.

**How to Find:**
```
1. Join groups relevant to your ICP:
   - Local business groups in your target geography (from `references/icp-profile.md`)
   - Regional business/trade groups
   - Industry-specific groups (from your ICP industry focus)
   - Operations/Finance professional groups
2. Go to Group → Members
3. Filter/search by role keywords
4. Screen for ICP fit
```

**Best Groups for Your ICPs (discover based on your target market):**
- Local business federations/chambers of commerce in your target geography
- Regional entrepreneur networks
- Industry-specific groups relevant to your niche and geography (from `references/icp-profile.md`)

**Group Engagement Strategy:**
```
1. Don't DM group members directly (feels spammy)
2. Engage with their posts IN the group first
3. Comment on group discussions they participate in
4. Build visibility, then connect
```

**Output Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GROUP MEMBER: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GROUP: [Group Name]
MEMBER ACTIVITY: [Active poster / Occasional / Lurker]

🌏 GEOGRAPHY: [✅ CONFIRMED TARGET GEO / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

ACTION: Engage in group discussions first → Then connect
```

**File Notation:**
```
| 14 | [Name] | [Role] | [Company] | [Target Country] | PROSPECT | [URL] | 👥 GROUP: [Group Name] member, active poster |
```

---

### Strategy 5: Event Attendees (Low Priority)

**Why Lower:** Events are periodic, but attendees have concentrated interest in topic.

**How to Find:**
```
1. Search LinkedIn Events for relevant topics:
   - "[Your niche] [Target Geography]" (e.g., relevant industry events in your market)
   - "[Target Company Type] Digital Transformation"
   - "Operations Excellence [Target Geography]"
   → Use topics and geography from `references/icp-profile.md`
2. Click event → View attendees
3. Screen attendees for ICP fit
```

**Event Types to Monitor:**
- Webinars on topics you solve
- Industry conferences (virtual or in-person) in your target geography
- Networking events for leaders in your target company type
- Relevant niche events in your target geography

**Event Engagement Strategy:**
```
1. Attend the same event (if possible)
2. Comment on event posts
3. Connect with context: "Also attending [Event]..."
4. Follow up after event with value-add
```

**Output Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVENT ATTENDEE: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EVENT: [Event Name]
EVENT DATE: [Date]
EVENT TOPIC: [Relevant topic]

🌏 GEOGRAPHY: [✅ CONFIRMED TARGET GEO / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

ACTION: Connect with event context → Follow up with value-add
```

**File Notation:**
```
| 15 | [Name] | [Role] | [Company] | [Target Country] | PROSPECT | [URL] | 📅 EVENT: Attending [Event Name] on [Date] |
```

---

### Advanced Strategy Triggers

| Trigger Command | Strategy |
|-----------------|----------|
| "find resharers" / "who reshared my posts" | Content Re-sharers |
| "check competitor comments" / "monitor competitors" | Competitor Commenters |
| "check shared connections" / "2nd degree prospects" | Shared Connections |
| "screen group members" / "check groups" | Group Members |
| "screen event attendees" / "check event" | Event Attendees |

---

## Algorithm Training & Discovery Modes

**PURPOSE:** Train the LinkedIn algorithm to surface your prospects' content in your feed by systematically visiting profiles, following, and engaging. These modes solve the core challenge: finding prospects' posts to engage with.

**STRATEGY:** LinkedIn's algorithm feeds you content based on engagement signals. By training it to understand who matters to you, your feed will naturally surface prospect content within 2-4 weeks.

---

### Mode 1: Train Algorithm 🎯

**Trigger:** `"train algorithm"`, `"train feed"`, `"prime my feed"`

**Purpose:** Systematically train LinkedIn to surface content from your existing ICP prospects by visiting profiles, following, and turning on notifications.

**When to use:**
- You have prospects in icp-prospects.md but their posts don't appear in your feed
- You want to prime the algorithm to show you relevant content
- Starting a new LinkedIn account or after long inactivity period

**Workflow:**

```
STEP T1: Read icp-prospects.md → Get prospects with Algorithm Trained = ❌ NO or ⏳ PENDING

STEP T2: Filter by priority:
         → HIGH priority: Connection Status = "connected" (warm relationships)
         → MEDIUM priority: Touches >= 2 (warming pipeline)
         → LOW priority: Touches = 0-1 (cold prospects)

STEP T3: For each prospect (5-10 per session to avoid spam detection):

         A. Navigate to profile URL

         B. Dwell time training:
            → Scroll profile slowly (30-45 seconds)
            → Read headline, about section (algorithm tracks dwell time)
            → Scroll to recent activity section

         C. Check Following status:
            → If NOT following → Click "Follow" button
            → Wait for confirmation
            → LinkedIn now prioritizes their content in your feed

         D. Bell notifications (HIGH priority only):
            → Click bell icon next to Follow button
            → Select "All" notifications
            → Use sparingly (only top 10-15 prospects)

         E. Save recent posts:
            → Navigate to recent activity (/recent-activity/all/)
            → Save 1-2 most recent posts (click bookmark icon)
            → 360Brew values Saves 5x more than Likes

         F. Update icp-prospects.md IMMEDIATELY:
            → Set Algorithm Trained = ✅ YES
            → Set Last Trained = today's date (DDMon format)
            → Add to Notes: "Followed + Bell ON" (if bell enabled)

         G. Wait 10-15 seconds between profiles (appear human)

STEP T4: Log all actions to shared activity log:
         → Section: "Algorithm Training"
         → List prospects trained
         → Timestamp
         → Actions taken (Follow/Bell/Save)

STEP T5: Output summary:
         "Trained algorithm on X prospects. Expected results:
         - Week 1: Occasional posts in feed
         - Week 2-3: Regular appearance
         - Week 4+: Feed dominated by trained prospects

         Next: Engage with their posts when they appear to reinforce the signal."
```

**Algorithm Training Checklist (per prospect):**

```
□ Profile visited (30-45 seconds dwell time)
□ Profile scrolled (signals interest)
□ Followed (if not already following)
□ Bell notification enabled (HIGH priority only)
□ 1-2 posts saved (strong interest signal to 360Brew)
□ Recent activity page visited (shows intent to see their content)
□ icp-prospects.md updated (Algorithm Trained = ✅ YES)
□ Shared activity log updated
```

**Re-training Protocol:**

Train algorithm every 30 days to maintain feed priority:
- Check Last Trained date
- If > 30 days → Re-train (visit profile, save recent post)
- Update Last Trained timestamp

**Bell Notification Strategy (Use Sparingly):**

Only enable for TOP 10-15 prospects:
- Connected prospects (1st degree)
- High-value accounts (>$10K potential)
- Active posters (post 3+ times per week)
- Strategic relationships

**Output Format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALGORITHM TRAINING SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: [Date]
Session: [Morning/Afternoon/Evening]

PROSPECTS TRAINED: 7

HIGH PRIORITY (Bell enabled):
1. [Name] - [C-level Role], [Company] - Followed + Bell ON + 2 posts saved
2. [Name] - [C-level Role], [Company] - Already following, Bell ON, 1 post saved

MEDIUM PRIORITY:
3. [Name] - CFO, [Company] - Followed + 2 posts saved
4. [Name] - COO, [Company] - Followed + 1 post saved
5. [Name] - Director Ops, [Company] - Followed + 2 posts saved

LOW PRIORITY:
6. [Name] - Manager, [Company] - Followed
7. [Name] - Director, [Company] - Followed

ACTIONS SUMMARY:
- Profiles visited: 7
- New follows: 5
- Bell notifications enabled: 2
- Posts saved: 11

UPDATED FILES:
- icp-prospects.md (Algorithm Trained column)
- shared/logs/linkedin-activity.md (training log)

EXPECTED RESULTS:
✓ Week 1-2: Start seeing trained prospects in feed
✓ Week 3-4: Regular appearance of their content
✓ Ongoing: Engage when you see their posts (reinforces signal)

NEXT SESSION: [Date + 30 days] (re-training maintenance)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Integration with Daily Workflow:**

Morning Block (new addition):
```
1. Feed Discovery (5 min) → Find new prospects
2. Algorithm Training (5 min) → Train on 5-7 pending prospects
3. Standard Engagement (10 min) → Comment on peer/prospect/leader posts
```

---

### Mode 2: Feed Discovery 🔍

**Trigger:** `"scan feed"`, `"find prospects in feed"`, `"feed discovery"`

**Purpose:** Discover NEW prospects directly from your LinkedIn feed by scanning visible posts and classifying authors on-the-fly. Fastest prospecting method.

**Why this works:**
- LinkedIn already surfaced this content to you (relevance signal)
- Zero profile visits needed initially (saves time)
- Immediate engagement opportunity (post is right there)
- Discover prospects you didn't know existed

**Workflow:**

```
STEP F1: Navigate to LinkedIn feed
         → URL: https://www.linkedin.com/feed/
         → Wait for feed to load

STEP F2: Take snapshot of visible posts
         → Capture first 10-15 posts in feed
         → Extract for each post:
           * Author name
           * Author title/headline
           * Author company
           * Author location (if visible)
           * Follower count (if visible)
           * Post URL
           * Post content preview (first 100 words)

STEP F3: Quick ICP filtering (per post author):

         A. Geography check (MANDATORY FIRST):
            → Is location clearly one of your target countries (from `references/icp-profile.md`)?
            → If NO or UNCLEAR → SKIP immediately

         B. Role check:
            → Does title indicate decision-maker?
            → Manager, Director, Head of, C-suite, Founder?
            → If junior/IC role → SKIP

         C. Company size signals:
            → Headline mentions target company type keywords (from `references/icp-profile.md`)?
            → Company name suggests size?
            → If enterprise/MNC → SKIP

         D. Content relevance:
            → Post discusses pain points you solve?
            → Topics: automation, operations, scaling, efficiency?
            → If irrelevant topic → SKIP

         E. Engagement signals:
            → Can you add value with a comment?
            → Is this a job posting? (SKIP if yes)
            → Are comments disabled? (SKIP if yes)

STEP F4: Classify matches:
         → For each ICP match found:
           * PROSPECT = Decision-maker at target company type
           * PEER = Builder in same niche (1K-10K followers)
           * THOUGHT LEADER = Authority (10K+ followers)

STEP F5: Output screening results:
         Present findings to user with:
         - Name, role, company, location
         - Classification (Prospect/Peer/Leader)
         - Post topic summary
         - Recommended engagement approach

STEP F6: User selects prospects to engage:
         (In AUTONOMOUS mode: AI auto-selects top 3-5)

         For each selected:
         A. Navigate to post URL
         B. Read full post content
         C. Generate comment using linkedin-pro-commenter
         D. Like/react to post
         E. Post comment
         F. Add to icp-prospects.md:
            → Source = "Feed Discovery"
            → Algorithm Trained = ⏳ PENDING (engaged but not profile-trained yet)
            → Touches = 1
            → Last Touch = today + "comment"
         G. Add to shared activity log (Comments Made section)

STEP F7: Follow-up algorithm training:
         → Schedule these prospects for next "train algorithm" session
         → Will visit profile + follow + save to complete training
```

**Output Format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FEED DISCOVERY SCAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: [Date]
Posts scanned: 15

ICP MATCHES FOUND: 4

✅ PROSPECT #1: [Name]
Role: CFO at [Company]
Location: [Target Country]
Followers: ~2K
Post topic: Struggling with manual invoice reconciliation
Engagement opportunity: HIGH (discusses automation pain point)
Post URL: [URL]

✅ PROSPECT #2: [Name]
Role: Operations Director at [Company]
Location: [Target Country]
Followers: ~1.5K
Post topic: Scaling challenges without adding headcount
Engagement opportunity: HIGH (core ICP pain point)
Post URL: [URL]

🤝 PEER #3: [Name]
Role: Founder at [Company]
Location: [Target Country]
Followers: 3K
Post topic: Building workflows for target company type
Engagement opportunity: MEDIUM (collaboration potential)
Post URL: [URL]

💡 THOUGHT LEADER #4: [Name]
Role: VP Product at [BigCo]
Location: [Target Country]
Followers: 15K
Post topic: Future of AI in operations
Engagement opportunity: LOW (visibility play, not ICP)
Post URL: [URL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDED ACTIONS:
1. Engage with Prospects #1-2 (high pain signals)
2. Engage with Peer #3 (network building)
3. Skip Thought Leader #4 (focus on ICP this session)

Select prospects to engage (or type 'all' for top 3):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Feed Discovery Optimization:**

**Best times to scan feed:**
- Morning (7-9am): Fresh overnight posts
- Lunch (12-2pm): Midday posts
- Evening (5-7pm): End-of-day posts

**Scroll strategy:**
- Scan first 15 posts only (high-quality threshold)
- Don't scroll endlessly (diminishing returns)
- Run 2-3x per day for best coverage

**Quality vs Quantity:**
- 3-5 high-fit prospects > 20 mediocre matches
- Only engage if you can add genuine value
- Skip if comment would be generic

---

### Mode 3: Hashtag Discovery 🏷️

**Trigger:** `"scan hashtag [tag]"`, `"hashtag discovery"`, `"find prospects by topic"`

**Purpose:** Find prospects actively discussing relevant topics via hashtag monitoring. Highly targeted prospecting.

**Why this works:**
- Self-selected interest (they're posting about your topic)
- Pain points visible (post content shows challenges)
- Natural conversation starter (context for engagement)
- Topic-based clustering (find similar prospects)

**Default Hashtag Rotation:**

Generate hashtags based on your domain, target market, and ICP pain points from `references/icp-profile.md`. Example structure:

```
Monday: #[YourDomain]Automation
Tuesday: #DigitalTransformation
Wednesday: #[TargetRole]Challenges
Thursday: #[RelevantTech]Implementation
Friday: #OperationsExcellence
Saturday: #BusinessAutomation
Sunday: #ScalingChallenges
```

**Workflow:**

```
STEP H1: Determine hashtag to scan
         → User provides hashtag (e.g., "#[YourDomain]Automation")
         → OR use default rotation based on day of week

STEP H2: Navigate to LinkedIn search
         → URL: https://www.linkedin.com/search/results/content/?keywords=%23[hashtag]
         → Example: keywords=%23[YourHashtag]
         → Apply filters:
           * Content type: "Posts"
           * Date posted: "Past 24 hours" (or "Past Week" for low-volume tags)

STEP H3: Take snapshot of search results
         → Capture first 10-15 posts
         → Extract for each:
           * Author details (name, title, company, location, followers)
           * Post URL
           * Post content (full text if visible)
           * Engagement metrics (likes, comments)
           * Date posted

STEP H4: ICP screening (per author):

         A. Geography check (MANDATORY):
            → Target countries only (from `references/icp-profile.md`)
            → SKIP if non-target geography or unclear

         B. Role + Company check:
            → Decision-maker at target company type?
            → Manager+ at relevant company?
            → SKIP if junior or enterprise

         C. Content analysis (pain signals):
            → Does post describe a problem you solve?
            → Asking for recommendations?
            → Frustrated with current solution?
            → Specific technical challenge?

            High-signal phrases:
            ✓ "struggling with..."
            ✓ "looking for alternatives to..."
            ✓ "manual process taking..."
            ✓ "need to automate..."
            ✓ "scaling challenges with..."

            Low-signal (skip):
            ✗ Generic motivational content
            ✗ Job postings
            ✗ Promotional posts
            ✗ Reshares without commentary

         D. Engagement check:
            → Can you add specific value?
            → Is this post old/stale?
            → Are comments disabled?

STEP H5: Classify and prioritize:
         → Grade each prospect:
           * 🔥🔥🔥 HOT: High pain signal + recent post + active engagement
           * 🔥🔥 WARM: Medium pain signal + relevant content
           * 🔥 COLD: Low pain signal but ICP match

         → Output ordered list (HOT prospects first)

STEP H6: User selects prospects to engage:
         (In AUTONOMOUS mode: AI selects top 3 HOT prospects)

         For each selected:
         A. Navigate to post
         B. Read full content + existing comments (avoid repetition)
         C. Generate comment using linkedin-pro-commenter
            → Reference specific pain point they mentioned
            → Add insight or question
            → Keep under 50 words
         D. Like/react to post
         E. Post comment
         F. Visit author profile:
            → Follow them (algorithm training)
            → Check recent activity
            → Save 1-2 recent posts
         G. Add to icp-prospects.md:
            → Source = "Hashtag: #[tag]"
            → Algorithm Trained = ✅ YES (profile visited + followed)
            → Touches = 1
            → Last Touch = today + "comment on #[tag] post"
            → Notes = "Pain point: [specific challenge mentioned]"
         H. Update Profile Cache with post URLs
         I. Log to shared activity log

STEP H7: Track hashtag performance:
         → Which hashtags yield highest ICP matches?
         → Best posting times for each tag?
         → Adjust rotation based on results
```

**Output Format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HASHTAG DISCOVERY: #[YourHashtag]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: [Date]
Posts scanned: 12
Time range: Past 24 hours

PROSPECT MATCHES: 5

🔥🔥🔥 HOT PROSPECT #1: [Name]
Role: COO at [Company]
Location: [Target Country]
Followers: ~2K
Post date: 4 hours ago
Pain signal: "[Describes pain point relevant to your ICP]"
Engagement: 15 likes, 8 comments (active discussion)
Post URL: [URL]
→ RECOMMENDATION: Comment with specific insight about their pain point

🔥🔥 WARM PROSPECT #2: [Name]
Role: Finance Director at [Company]
Location: [Target Country]
Followers: ~1K
Post date: Yesterday
Pain signal: "[Asks for recommendations relevant to your solution space]"
Engagement: 8 likes, 3 comments
Post URL: [URL]
→ RECOMMENDATION: Share observation about relevant workflows

🔥 COLD PROSPECT #3: [Name]
Role: Operations Manager at [Company]
Location: [Target Country]
Followers: ~800
Post date: 2 days ago
Pain signal: Generic post about "digital transformation journey"
Engagement: 5 likes, 1 comment (low)
Post URL: [URL]
→ RECOMMENDATION: Lower priority, engage only if time permits

❌ SKIPPED: 7 posts
- 3 non-target geography authors
- 2 job postings
- 1 vendor promotional post
- 1 junior role (intern)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HASHTAG PERFORMANCE:
#[YourHashtag] → 5 ICP matches from 12 posts (42% hit rate) ✅ GOOD
Recommendation: Keep in rotation, scan 2x per week

Select prospects to engage (1, 2, 3, or 'all'):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Hashtag Strategy Tips:**

**High-value hashtags (test in your market):**
```
Generate hashtags based on your domain and target market from `references/icp-profile.md`:

Core pain points:
#[YourDomain]Automation, #DigitalTransformation, #ProcessAutomation

Role-specific:
#[TargetRole]Challenges, #OperationsExcellence, #[Function]Automation

Tech stack:
#[RelevantTech]Implementation, #CRMIntegration, #WorkflowAutomation

Growth stage:
#ScalingChallenges, #[CompanyType]Growth, #BusinessEfficiency

Geographic:
#[TargetCity][CompanyType], #[TargetRegion]Business, #[TargetRegion]Tech
```

**Hashtag testing protocol:**
1. Test new hashtag for 1 week
2. Track: Posts scanned, ICP matches, engagement rate
3. Calculate hit rate (ICP matches / total posts)
4. Keep if hit rate > 30%, discard if < 15%

**Avoid low-value hashtags:**
- ❌ #MondayMotivation (generic, no pain signals)
- ❌ #Hiring (job postings only)
- ❌ #Grateful (sentiment, not pain)
- ❌ #Excited (announcements, not challenges)

---

### Mode 4: Profile Recommendations Discovery 🔗

**Trigger:** `"harvest recommendations"`, `"find lookalike prospects"`, `"expand from [prospect name]"`, `"discover similar prospects"`

**Purpose:** Systematically expand pipeline using LinkedIn's algorithmic profile recommendations

**Strategy:** Use existing high-quality prospects as "seeds" to discover lookalike prospects from LinkedIn's "More profiles for you" / "People you may want to know" sidebar recommendations.

**Why this works:**
- LinkedIn algorithmically clusters similar profiles by role, industry, network
- If Prospect A is a strong ICP match, LinkedIn's recommendations will be similar
- Creates "lookalike network effect" - compounds over time

#### Dedicated Discovery Session Workflow

**STEP R1: Select Seed Prospects (2-3 min)**

```
Target: 5-10 seed prospects (high-quality ICPs)

Selection criteria:
✓ ICP Score >= 80/100 (strongest matches)
✓ Classification = PROSPECT
✓ Target geography confirmed (from `references/icp-profile.md`)
✓ Decision-maker role (Founder/CEO/COO/CFO/CTO)
✓ Target company size (from `references/icp-profile.md`)
✓ Relevant industry for your positioning

Priority order:
1. Connected prospects (1st degree) - best recommendations
2. 2-3 touch prospects (high engagement) - strong signals
3. Recently discovered prospects (fresh, active) - current patterns

Read icp-prospects.md:
→ Sort by ICP Score (highest first)
→ Filter for Score >= 80
→ Select 5-10 for this session
```

**STEP R2: Visit Each Seed Profile & Harvest (15-20 min)**

```
For each seed prospect:

1. Navigate to LinkedIn profile URL
2. Scroll profile (30 sec dwell - appear human)
3. Locate right sidebar recommendations:
   → "More profiles for you" OR
   → "People you may want to know"
4. For EACH recommendation (scan 3-5 per profile):

   EXTRACT:
   - Name
   - Role/Title
   - Company name
   - Location
   - Profile URL
   - Follower count (if visible)
   - Connection degree (1st/2nd/3rd)

   QUICK ICP CHECK (3-second scan):
   ✓ Decision-maker role? (Founder/CEO/COO/etc.)
   ✓ Target company size? (check "About" for employee count, per `references/icp-profile.md`)
   ✓ Target geography? (STRICT - skip if unclear, per `references/icp-profile.md`)
   ✓ Relevant industry? (matches your positioning)

   IF ALL YES:
   → Add to discoveries_queue (batch save at end)
   → Check NOT already in icp-prospects.md (duplicate check)
   → Check NOT in linkedin-blacklist.md

   IF ANY NO:
   → Skip, move to next recommendation

5. Wait 10-15 seconds before next profile (appear human)

Result per seed: 2-4 qualified prospects
Result per session: 10-40 new qualified prospects
```

**STEP R3: Batch Qualification & Scoring (3-5 min)**

```
For each prospect in discoveries_queue:

ASSIGN ICP SCORE (0-100):
+25 pts: Decision-maker role (C-level/Founder)
+20 pts: Target company size (from `references/icp-profile.md`)
+15 pts: Primary target market location (or +10 for secondary target markets)
+15 pts: High-fit industry (automation/tech/operations)
+10 pts: Pain signals visible in headline/about
+10 pts: Active poster (recent activity visible)
+5 pts: Connected to other prospects (network cluster)

Score ranges:
90-100 = EXCELLENT (immediate priority)
80-89 = STRONG (high priority)
70-79 = GOOD (standard pipeline)
60-69 = MODERATE (lower priority)
<60 = SKIP (doesn't meet threshold)

MINIMUM THRESHOLD: 70/100
```

**STEP R4: Save to icp-prospects.md (2-3 min)**

```
For each qualified prospect (Score >= 70):

Add new row to icp-prospects.md:
| # | Name | Date Found | Role | Company | Company URL | Location | Classification | Touches | Last Touch | Touch History | Connection Status | Profile URL | Email | Notes |
| X | [Name] | [DDMon] | [Title] | [Company] | TBD | [Location] | PROSPECT | 0 | - | - | none | [URL] | TBD | Source: LinkedIn Profile Rec from [Seed Prospect Name] \| [Industry/Pain Signal] \| Score: [X]/100 |

Source format: "LinkedIn Profile Rec from [Seed Prospect Name]"

Example:
"Source: LinkedIn Profile Rec from [Seed Prospect] | [Industry] [Company Type] | Score: 85/100"
```

**STEP R5: Log Discovery Session (1 min)**

```
Update shared/logs/linkedin-activity.md:

Section: "Discovery Sessions"

| Date | Mode | Seed Prospects | Profiles Scanned | Recommendations Extracted | Qualified Prospects | Avg ICP Score | Time |
|------|------|----------------|------------------|---------------------------|---------------------|---------------|------|
| 06Feb | Profile Recs | 7 | 7 | 24 | 18 | 78/100 | 22 min |

Notes:
- Best performing seed: [Prospect Name] → 5 qualified prospects
- Worst performing seed: [Prospect Name] → 1 qualified prospect
- Discovery rate: 75% (18/24 qualified)
```

#### Session Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROFILE RECOMMENDATIONS DISCOVERY SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: [DD Mon YYYY]
Duration: [X] minutes

SEED PROSPECTS (Score 80+):
1. [Seed Prospect 1] (Score: 80/100) → 4 recommendations scanned
2. [Seed Prospect 2] (Score: 82/100) → 3 recommendations scanned
3. [Seed Prospect 3] (Score: 85/100) → 5 recommendations scanned
4. Quek Siu Rui (Score: 88/100) → 4 recommendations scanned
5. Jaslyn Lee (Score: 78/100) → 3 recommendations scanned

RECOMMENDATIONS HARVESTED: 19 total

QUALIFIED PROSPECTS: 14 saved to icp-prospects.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOP DISCOVERIES (Score 85+):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Name] (Score: 88/100)
   Role: CEO & Founder
   Company: [Company]
   Location: [Target Country]
   Industry: [Relevant Industry]
   Source: Rec from [Seed Prospect]
   Why strong: Decision-maker, target company type, relevant industry focus, pain signals

2. [Name] (Score: 87/100)
   Role: Co-Founder & COO
   Company: [Company]
   Location: [Target Country]
   Industry: [Relevant Industry]
   Source: Rec from [Seed Prospect]
   Why strong: Operations leader, scaling company, relevant tech

3. [Name] (Score: 85/100)
   Role: CFO
   Company: [Company]
   Location: [Target Country]
   Industry: [Relevant Industry]
   Source: Rec from [Seed Prospect]
   Why strong: Finance leader, growth-stage company, process optimization

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Seed prospects used: 5
Recommendations scanned: 19
Qualified prospects: 14 (74% qualification rate)
Average ICP Score: 81/100
Score distribution:
  - 85+ (Excellent): 3 prospects
  - 80-84 (Strong): 6 prospects
  - 75-79 (Good): 4 prospects
  - 70-74 (Moderate): 1 prospect

Time efficiency: 2.8 qualified prospects per seed
Next action: Begin warming 0-touch prospects via linkedin-icp-warmer
```

#### Efficiency Metrics

| Method | Time Investment | Prospects Discovered | Quality | Best For |
|--------|-----------------|---------------------|---------|----------|
| Profile Recommendations | 20 min session | 10-20 per session | HIGH (algorithmically clustered) | Pipeline expansion |
| Feed Discovery | 5 min daily | 2-3 per day | MEDIUM-HIGH (active posters) | Ongoing discovery |
| Hashtag Discovery | 5 min daily | 1-2 per day | MEDIUM (topic-specific) | Niche targeting |
| Sales Navigator "Posted" | 10 min | 5-10 per search | HIGH (active + searchable) | Immediate engagement |

**Compounding Effect:**

```
Week 1: Discover 14 prospects via recommendations
Week 2: Use those 14 as seeds → Discover 35 more prospects
Week 3: Use best 10 from Week 2 as seeds → Discover 25 more prospects
Week 4: 74 total prospects discovered, lookalike network established

Result: Self-sustaining prospect pipeline from algorithmic clustering
```

#### When to Run Profile Recommendations Discovery

**HIGH PRIORITY - Run Discovery Session:**
- 0-touch backlog < 10 prospects (pipeline needs expansion)
- After warming 5+ prospects to 2-3 touches (create new seeds)
- Weekly "Pipeline Expansion Day" (dedicated discovery time)
- When you connect with 3+ prospects (use connections as seeds)

**LOW PRIORITY - Skip Discovery:**
- 0-touch backlog > 20 prospects (focus on warming existing)
- Time-constrained (prioritize engagement over discovery)
- Seed prospects are weak ICP fit (poor recommendations expected)

#### Integration with Warming Workflow

```
DISCOVERY → WARMING → CONNECTION PIPELINE:

1. Profile Recommendations Discovery (20 min weekly)
   → Output: 10-20 new 0-touch prospects

2. ICP Warmer (daily)
   → First touch: Comment on posts
   → Move to 1-touch → 2-touch → 3-touch

3. Connect Timer (as ready)
   → 3+ touches = ready for connection
   → Send connection requests
   → Connected prospects become new seeds (repeat cycle)
```

---

### Algorithm Training Integration Summary

**How the 4 modes work together:**

```
WEEK 1-2: Discovery Phase
├─ Feed Discovery (daily) → Find 5-10 new prospects per day
├─ Hashtag Discovery (daily) → Find 3-5 topic-specific prospects per day
├─ Profile Recommendations (weekly) → Find 10-20 lookalike prospects per session
└─ Result: 75-150 new prospects in icp-prospects.md

WEEK 2-3: Training Phase
├─ Train Algorithm → Systematically train on all discovered prospects
├─ Visit profiles + Follow + Save posts
└─ Result: Algorithm starts surfacing their content

WEEK 4+: Compounding Phase
├─ Feed naturally shows trained prospect content
├─ Engage when posts appear (reinforces signal)
├─ 3-4 engagements = Network cluster effect
└─ Result: Feed dominated by prospect content, minimal discovery needed
```

**Daily + Weekly workflow integration:**

```
DAILY - Morning Block (15-20 min):
1. Feed Discovery (5 min) → Scan feed, find 2-3 new prospects, engage
2. Algorithm Training (5 min) → Train algorithm on 5 pending prospects (+ harvest recommendations automatically)
3. Hashtag Discovery (5 min) → Scan today's hashtag, find 1-2 prospects, engage
4. Standard Engagement (5 min) → Existing workflow (Peer/Leader comments)

WEEKLY - Pipeline Expansion Day (20-30 min):
→ Profile Recommendations Discovery Session (dedicated)
→ Use 5-10 best prospects (Score 80+) as seeds
→ Systematically harvest all recommendations
→ Result: 10-20 new qualified prospects added to pipeline

Compounding effect:
→ Week 1: Discovering + Training
→ Week 2: Training + Some prospects appearing in feed
→ Week 3: More prospects in feed, less discovery needed
→ Week 4+: Feed dominated by prospects, discovery on-demand only
```

**File structure changes:**

Updated icp-prospects.md columns:
```markdown
| # | Name | Date Found | Source | Role | Company | Location | Profile URL | Algorithm Trained | Last Trained | Touches | Last Touch | Connection Status | Notes |
```

New columns:
- **Source**: Feed / Hashtag: #tag / SalesNav / Inbound / etc.
- **Algorithm Trained**: ✅ YES / ⏳ PENDING / ❌ NO
- **Last Trained**: Date last visited profile (re-train every 30 days)

---

## Step 4b: LinkedIn Profile URL Discovery

**When screening prospects from external sources (web articles, events, directories), the LinkedIn Profile URL may not be immediately available. Use these strategies to find it.**

### Why This Matters

Without a LinkedIn Profile URL, you cannot:
- Visit their profile to train the algorithm
- See their recent posts to engage with
- Send connection requests
- Track them in warming pipeline

**Invest 2-3 minutes to find the LinkedIn URL for each HIGH FIT prospect.**

### Strategy 1: Google Search + LinkedIn Site Filter (PRIMARY)

**Most effective - use this FIRST for ~90% success rate:**

```
SEARCH QUERY FORMAT:
"[Full Name]" "[Company Name]" [Role] site:linkedin.com/in/

EXAMPLES:
- "[Full Name]" "[Company]" [role] site:linkedin.com/in/
  → Found: https://www.linkedin.com/in/[username]/

- "[Full Name]" "[Company]" CEO site:linkedin.com/in/
  → Found: https://linkedin.com/in/[username]

- "[Full Name]" "[Company]" founder site:linkedin.com/in/
  → Found: https://www.linkedin.com/in/[username]/
```

**Success indicators:**
- First result is usually correct (verify company name in snippet)
- Profile URL formats:
  - https://linkedin.com/in/username
  - https://sg.linkedin.com/in/username (regional)
  - https://www.linkedin.com/in/username

### Strategy 2: LinkedIn Company Page → People Search

**Use when Strategy 1 fails or returns ambiguous results (common names):**

```
WORKFLOW:
1. Google search: "[Company Name]" LinkedIn company
2. Navigate to: linkedin.com/company/[company-slug]
3. Click "People" tab
4. Use search box: Search for "[First Name] [Last Name]"
5. If not found, browse pages (employees may be listed without full profiles)
```

**When this is essential:**
- Common names (John Tan, Mary Lee, David Chen)
- Multiple people with same name
- Need to verify current employment
- Startup with <20 employees (easier to browse all)

**Example search workflow:**
```
[Prospect Name] at [Company]:
1. Searched "[Name] [Company] [Target Country]" on LinkedIn → Multiple results
2. Navigated to company page on LinkedIn
3. Clicked "People" tab to browse employees
4. Used company search approach if direct search yields too many results
```

### Strategy 3: Press Release & News Search

**For founders mentioned in articles:**

```
SEARCH QUERIES:
- "[Full Name]" "[Company]" LinkedIn profile
- "[Company]" founder "[Full Name]" LinkedIn
- "[Full Name]" "[Company]" interview LinkedIn
- "[Company]" raises funding "[Full Name]"
```

**Why this works:**
- Journalists often link to LinkedIn in articles
- Press releases include profile links
- Award announcements link to winner profiles
- Podcast/interview show notes link to guests

**Example workflow:**
```
Search: "[Full Name]" [Company] [role] [Target Country] [year]
Found: University article + industry interviews
  → Confirmed: [Role] at [Parent Company]
  → Then used name + "[Parent Company]" for LinkedIn search
```

### Strategy 4: Company Website → Team Page

**For executive-level prospects:**

```
PAGES TO CHECK:
- /team or /our-team → LinkedIn icons under photos
- /about-us → Founder/leadership bios with social links
- /leadership or /management → Executive profiles
- /contact → Sometimes has team member social links
```

**Look for:**
- LinkedIn icon links (small blue icons)
- "Connect with [Name]" links
- Social media bars under team photos

### Strategy 5: Crunchbase Cross-Reference

**For startup founders (funded companies):**

```
SEARCH: "[Full Name]" "[Company]" Crunchbase

Crunchbase profiles often include:
✓ LinkedIn profile links
✓ Twitter/X handles
✓ Personal websites (which link to LinkedIn)
✓ Confirmation of role/title
```

### Strategy 6: Try Name Variations

**If initial search fails:**

```
NAME FORMAT VARIATIONS:
Original: "Joshua Christopher Chandra"

Try:
1. Full name: "Joshua Christopher Chandra"
2. First + Last: "Joshua Chandra"
3. Initials: "J.C. Chandra"
4. Nickname: "Josh Chandra"
5. Different order: "Chandra Joshua" (Asian naming conventions)
6. Middle name variations: "Joshua C. Chandra"
```

**Real example:**
```
"Chang Wen" Ninja Van → No direct results
"Chang Wen Lai" Ninja Van → Found!
  → LinkedIn: https://sg.linkedin.com/in/chang-wen-lai
```

### Profile URL Validation Checklist

**Before saving the URL, verify it's the correct person:**

```
VERIFICATION (30-second check):
✓ Current company matches (or recent if job switch)
✓ Job title/role aligns with prospect info
✓ Location matches target geography (from `references/icp-profile.md`)
✓ Industry/sector matches
✓ Profile photo matches (if you have reference)
✓ Follower count appropriate for seniority
```

### Handling Edge Cases

| Scenario | Action | Notes Column Entry |
|----------|--------|-------------------|
| **No LinkedIn found** | Save as "TBD" | "LinkedIn: Not found 05Feb - may not have profile" |
| **Multiple same names** | Use Company Page strategy | "LinkedIn: Verified via company page 05Feb" |
| **Private/limited profile** | Still save URL | "LinkedIn: Limited profile visibility" |
| **Recently changed jobs** | Verify via news search | "LinkedIn: Updated role to [New Company]" |
| **Profile deactivated** | Mark in Notes | "LinkedIn: Profile appears deactivated" |

### Integration with Save Workflow

**When saving to icp-prospects.md (Step 5):**

```markdown
Profile URL column:
- ✅ Found: https://sg.linkedin.com/in/username
- ❌ Not found: TBD

Notes column additions:
- "LinkedIn: [method] [date]"

Examples:
- "LinkedIn: Google search 05Feb"
- "LinkedIn: Company page 05Feb"
- "LinkedIn: Press release link 05Feb"
- "LinkedIn: TBD - no profile found"
```

### Time Investment vs ROI

| Prospect Type | Avg Search Time | Success Rate | Worth It? |
|---------------|----------------|--------------|-----------|
| Startup founders (funded) | 1-2 min | 90%+ | ✅ YES |
| Target company CEOs/Co-founders | 2-3 min | 70-80% | ✅ YES |
| Executives at larger companies | 2-4 min | 60-70% | ✅ YES |
| Technical co-founders | 3-5 min | 50-60% | ⚠️ Maybe (if high-value prospect) |

**ROI calculation:**
- 3 minutes to find LinkedIn URL
- Enables: Profile visit (algorithm train) + Post engagement + Connection request
- Expected value: 3-5 future touchpoints over 30 days
- **Verdict: Always worth it for HIGH FIT prospects**

### Batch Processing Tip

**When screening 10+ prospects from same source:**

```
EFFICIENT WORKFLOW:
1. Screen all prospects first (ICP criteria)
2. Batch the LinkedIn URL searches:
   - Try Google search for all (quick wins)
   - Company page searches for remainder
   - Skip time-consuming edge cases if low priority
3. Update icp-prospects.md in one session
```

**Saves context-switching time.**

---

## Step 5: Save Prospects to File

**After screening, save HIGH FIT prospects to the master ICP prospects file.**

### File Location

```
shared/logs/icp-prospects.md
```

**Single consolidated file** - all prospects in one place, with Date Found column to track discovery.

### When to Save

Save when ALL of these are true:
- ✅ Prospect has HIGH FIT or MEDIUM FIT verdict
- ✅ Prospect is NOT already in Warming Up table (check by Profile URL)
- ✅ Prospect is NOT already in icp-prospects.md (check by Profile URL)

### File Format

```markdown
# ICP Prospects

## Prospects Table

| # | Name | Date Found | Source | Degree | Role | Company | Location | Email | Classification | Profile URL | Algorithm Trained | Last Trained | Touches | Last Touch | Connection Status | Notes |
|---|------|------------|--------|--------|------|---------|----------|-------|----------------|-------------|-------------------|--------------|---------|------------|-------------------|-------|
| 1 | [Name] | 22Jan | SalesNav | 2nd | CEO | [Company] | [Target Country] | - | PROSPECT | [URL] | ✅ YES | 28Jan | 2 | 28Jan | none | Followed + Bell ON |
| 2 | [Name] | 22Jan | Feed | 2nd | CEO | [Company] | [Target Country] | - | PROSPECT | [URL] | ⏳ PENDING | - | 1 | 23Jan | none | Engaged, not trained yet |
| 3 | [Name] | 23Jan | Hashtag: #[Tag] | 1st | COO | [Company] | [Target Country] | email@co.com | PROSPECT | [URL] | ❌ NO | - | 0 | - | none | Pain: Manual processes |

## Profile Cache (for algorithm-trained prospects)

| # | Profile URL | Last Checked | Activity Status | Followers | Last Post | Recent Post URLs | Engagement Score |
|---|-------------|--------------|-----------------|-----------|-----------|------------------|------------------|
| 1 | /in/sumei/ | 28Jan 09:14 | ACTIVE | 3K | 27Jan | https://linkedin.com/feed/update/urn:li:activity:123, https://linkedin.com/feed/update/urn:li:activity:124 | HIGH |
```

### Column Definitions

| Column | Description | Values |
|--------|-------------|--------|
| **Date Found** | Discovery date | DDMon format (e.g., 22Jan) |
| **Source** | How prospect was discovered | Feed, Hashtag: #tag, SalesNav, Inbound, Competitor, Resharer, Event, etc. |
| **Degree** | LinkedIn connection degree | `1st`, `2nd`, `3rd`, or `-` (not checked) |
| **Email** | Email if visible | email address or `-` |
| **Classification** | Contact type | PROSPECT, PEER, THOUGHT LEADER, CUSTOMER |
| **Algorithm Trained** | Has algorithm been trained to surface their content? | ✅ YES (profile visited, followed, posts saved), ⏳ PENDING (engaged but not profile-trained), ❌ NO (discovered, not trained) |
| **Last Trained** | Date of last algorithm training (re-train every 30 days) | DDMon format or `-` |
| **Touches** | Total engagement count | Number (0, 1, 2, 3+) |
| **Last Touch** | Most recent engagement | DDMon + type (e.g., "28Jan comment") |
| **Connection Status** | LinkedIn connection status | none, pending, connected |

### Connection Degree Capture

**When viewing a prospect's profile, note their connection degree:**

- **1st** = Connected (green "1st" badge) → Email likely visible, can DM directly
- **2nd** = Not connected, have mutual connections → Need to warm up
- **3rd** = Distant connection → Longer warmup needed
- **-** = Not yet checked

**How to find:**
1. Look next to the person's name on their profile
2. It shows "1st", "2nd", or "3rd+"
3. Record in the Degree column

### Email Capture Instructions

**For each prospect, check Contact Info:**

1. Go to prospect's profile
2. Click "Contact info" (below headline)
3. If email visible → Add to Email column
4. If not visible → Enter `-`

**Email Visibility by Degree:**
- 1st degree: ~90% show email
- 2nd degree: ~30% show email
- 3rd degree: ~10% show email

### Adding New Prospects

When you find new prospects:

1. **Read** `shared/logs/icp-prospects.md`
2. **Check** if prospect already exists (by Profile URL)
3. **Get next row number** (increment from last row)
4. **Add new row** with all columns filled:
   - Date Found = today (DDMon)
   - Degree = from LinkedIn profile
   - Email = from Contact Info (or `-`)
5. **Update Statistics** section at bottom
6. **Save** the file

### Where NOT to Save (Goes to Warming Up Instead)

If you've **already engaged** with the prospect (commented, liked, saved), add them directly to the **Warming Up table** in `shared/logs/linkedin-activity.md` with:
- Touch count = 1
- First Touch = today's date + engagement type

### Save Logic Flowchart

```
HIGH FIT Prospect Found
         ↓
Check: Already in Warming Up table?
         ↓
    ┌────┴────┐
   YES        NO
    ↓          ↓
  SKIP     Check: Already in ANY icp-prospects file?
                   ↓
              ┌────┴────┐
             YES        NO
              ↓          ↓
            SKIP    Check: Does today's file exist?
                              ↓
                         ┌────┴────┐
                        YES        NO
                         ↓          ↓
                    APPEND      CREATE new file
                    new         icp-prospects-[date].md
                    session     with Session 1
```

### Append vs Create Logic

```
1. Check if icp-prospects-[today's date].md exists

   IF EXISTS:
   → Read existing file
   → Count existing sessions (## Session N headers)
   → Append new section: "## Session [N+1] - [Time] - [Source]"
   → Continue numbering prospects from last # in file
   → Update "Last updated" timestamp

   IF NOT EXISTS:
   → Create new file with header: "# ICP Prospects - [Date]"
   → Add section: "## Session 1 - [Time] - [Source]"
   → Start numbering prospects from 1
   → Add "Next Steps" section at bottom
```

### Prospect Numbering Across Sessions

When appending sessions, **continue the numbering** from where the last session ended:

```
Session 1: Prospects #1-8
Session 2: Prospects #9-12  (not #1-4)
Session 3: Prospects #13-15 (not #1-3)
```

This makes it easy to reference specific prospects: "Let's warm up prospect #11"

## Updating the ICP Profile

**When to update `references/icp-profile.md`:**

1. **User provides new ICP info**: Directly update the relevant sections
2. **linkedin-profile-icp output**: Copy the targeting criteria into the profile
3. **User feedback**: "Skip finance roles" → Update Role Filter
4. **Pattern recognition**: If user consistently skips certain types, suggest adding to Skip list

**Update format**: Add entry to Update Log with date, change, and source.

## Engagement Rules

### DO ✅
- Mirror their tone (frustrated → empathetic, curious → exploratory)
- Share relevant insights from your experience
- Focus on 2nd-degree network (warmest leads)
- Limit to 5-10 high-quality engagements per day
- Reference specific things they said
- Prioritize prospects in your primary target market (from `references/icp-profile.md`)
- **Save** their last 2 posts before engaging (360Brew values Saves 5x more than Likes)
- Reply to DMs/comments within 1 hour (boosts your post reach by 35%)

### DON'T ❌
- Pitch in comments
- Use generic AI comments
- Spam or engage with every comment
- Send connection requests immediately
- Hard-sell your product/service
- Engage with ANY prospect outside your target countries (from `references/icp-profile.md`)
- Proceed with prospects whose geography is unclear or unconfirmed
- Make exceptions for "interesting" prospects who are not in your target geography
- **Engage with job postings or hiring announcements** (appears opportunistic, no pain signals)
- **Engage with posts that have comments disabled** (no engagement opportunity)
- **Send external links in first DM** (360Brew flags as "low-trust signal")
- **Exceed 15-20 connection requests/day** (triggers Automation Detection)
- **Use templated connection notes** (blank requests perform 10-15% better unless 100% bespoke)

## Value DM Strategy (PROSPECTS ONLY - Post-Connection)

**⚠️ Only DM PROSPECT connections (ICP matches). Do NOT DM Peers or Thought Leaders.**

**Value DM Framework:**

See `linkedin-daily-planner/references/dm-framework.md` for comprehensive DM patterns.

**Core Principles:**
- Build relationship through **genuine curiosity**, NOT solution-offering
- Reference something SPECIFIC from their profile/posts (not generic)
- Ask a REAL question you're genuinely curious about
- Share an observation WITHOUT offering a solution
- Keep under 50 words
- **NEVER** offer workflows, frameworks, or solutions in first DM
- **NEVER** use phrases like "happy to share", "let me know if", "I can help with"
- Goal: Start a dialogue, not pitch

**DM Guardrails:**
- Never send external links in first message (flagged as spam)
- Keep initial DM under 50 words
- Wait for response before offering more
- If they accept your connection, post a "Build-in-Public" update within 24 hours (algorithm shows new connections your content for 7 days)

## Mirror & Add Comment Patterns

**STRICT: No em-dashes (—) in comments.** Use commas or periods instead.

**Pattern 1: Empathy + Reframe**
> "I hear you on [pain]. Most [ICP type] feel like they're working FOR their software instead of it working for them. Have you identified which single process causes the most friction?"

**Pattern 2: Validation + Insight**
> "That [specific issue] hits different when you're scaling. The fix usually isn't more software. It's mapping the actual workflow first. What's your current workaround?"

**Pattern 3: Curiosity + Builder Logic**
> "Interesting you mention [specific point]. In my experience, that usually stems from [underlying cause]. Is that what you're seeing?"

**Pattern 4: Shared Struggle + Question**
> "Been there. [System/tool] promises integration but delivers headaches. Are you trying to fix the whole system or just stop the bleeding on one process first?"

## Geography-Specific Search Keywords

Run these searches with your target geography location filters (from `references/icp-profile.md`):

```
"[Target Country 1] [Company Type]" + [pain keyword]
"[Target Country 2] business" + [automation/operations keyword]
"[Target Country 3] startup" + [scaling keyword]
"[Target Country 4] enterprise" + [finance/ERP keyword]
"[Target Region]" + [ICP pain point]
```

## High-Efficiency Search Strategies (Tested 01Feb2026)

**Efficiency-tested search strings ranked by ICP match rate.**

### Tier 1: Best ROI (50%+ ICP Match Rate) ✅✅

Use these searches FIRST - highest conversion to qualified prospects.

| Search String | Match Rate | Notes |
|--------------|------------|-------|
| `Founder CEO "digital transformation" [Target Geography]` | 50% | Pain signal built into profile, decision-makers, 1K-2K followers typical |
| `("Managing Director" OR "CEO") "process automation" [Target Geography]` | ~50% | Similar pattern, automation-focused leaders |
| `Founder "[Your Niche]" [Target Geography] [Company Type]` | ~45% | Niche-forward founders in target company type |

**Why Tier 1 works:**
- Prospects **self-identify** with pain point keywords in their headline/about
- High follower counts = active LinkedIn users (more engagement opportunities)
- Decision-makers who understand the value of transformation

**LinkedIn URL format:**
```
https://www.linkedin.com/search/results/people/?keywords=Founder%20CEO%20%22digital%20transformation%22&geoUrn=%5B%22[YOUR_GEO_URN]%22%5D&origin=FACETED_SEARCH
```

### Tier 2: Role-Specific (40% ICP Match Rate) ✅

Use when targeting specific functional roles.

| Search String | Match Rate | Notes |
|--------------|------------|-------|
| `"Finance Manager" [Company Type] [Target Geography]` | 40% | Mid-level influencers, can champion internally |
| `"Operations Director" [Target Geography] startup` | ~40% | Operations pain points, scaling challenges |
| `"CFO" OR "Financial Controller" [Company Type] [Target Geography]` | ~35% | Finance decision-makers |

**Tier 2 caveats:**
- Some results are job seekers (filter by "Open to Work" banner)
- Government employees appear (filter out GovTech, ministries)
- Better for building referral network than direct selling

### Tier 3: Skip These ❌

Low efficiency - use only for comment-hunting, not prospecting.

| Search Type | Match Rate | Why It Fails |
|-------------|------------|--------------|
| Pain point post searches ("manual processes" [Target Geography]) | <10% | Low volume, attracts consultants not buyers |
| "[Company Type] Owner" generic search | <5% | Returns passive profile maintainers, not active users |
| Company page content | 0% | Wrong audience entirely |

### Search Strategy by Account Type

| Account | Recommended Tier | Daily Budget |
|---------|-----------------|--------------|
| FREE | Tier 1 only (conserve searches) | 2-3 searches/day |
| PREMIUM | Tier 1 + Tier 2 | 10+ searches/day |
| SALES_NAVIGATOR | All tiers + save as alerts | Unlimited |

### Mutual Connections Priority

When reviewing search results, **prioritize by mutual connections**:

| Mutual Connections | Priority | Reason |
|-------------------|----------|--------|
| 50+ | 🔥 HOT | Strong network overlap, warm intro possible |
| 20-50 | ✅ HIGH | Good network fit |
| 5-20 | 📍 MEDIUM | Some overlap |
| <5 | ⚪ LOW | Cold outreach territory |

**Example:** A prospect with **150+ mutual connections** would be highest priority due to strong network overlap.

## Integration

- **linkedin-profile-icp**: Run first to generate ICP criteria → copy output to `references/icp-profile.md`
- **linkedin-pro-commenter-v5**: For HIGH FIT prospects needing refined comments
- **references/target-list.md**: Goldmine accounts and search keywords (update based on ICP)

## Quality Checklist

**Before Screening (Both Modes):**
- ✅ ICP profile loaded from `references/icp-profile.md`
- ✅ Warming Up table checked (avoid re-discovering existing prospects)
- ✅ Existing icp-prospects files checked (avoid duplicates)

**During Outbound Screening:**
- ✅ Geography filter applied FIRST before any other screening
- ✅ Only prospects from target countries (per `references/icp-profile.md`) pass geography check
- ✅ Unconfirmed geography = automatic skip (not "proceed with caution")
- ✅ **Job postings and hiring announcements = automatic skip**
- ✅ **Posts with comments disabled = automatic skip**
- ✅ Screening uses loaded ICP criteria (not hardcoded)
- ✅ Non-target geography and unconfirmed prospects immediately skipped with no further evaluation

**During Inbound Screening (Lurker Mode):**
- ✅ Geography filter applied FIRST (same target geography rule)
- ✅ Signal source documented (Profile View / Follower / Reaction / Request)
- ✅ Signal date/recency noted (last 24h = hot, last week = warm)
- ✅ Engagement context captured (what triggered the signal)
- ✅ Fast-track warmth level assigned based on signal type
- ✅ Repeat viewers flagged as very high intent

**After Screening (Both Modes):**
- ✅ **HIGH FIT prospects saved to `icp-prospects-[date].md`** (if 0 touch)
- ✅ **Already engaged prospects go to Warming Up table** (if 1+ touch)
- ✅ **Inbound prospects marked with 🔥 INBOUND notation** in notes
- ✅ Profile URL captured for deduplication
- ✅ Mirror & Add comment ≤50 words (if engaging now)
- ✅ Comment references something specific they said
- ✅ No pitching in comments
- ✅ Connection request references specific conversation

## Shared Activity Log (Token Optimization)

**ALWAYS read from the shared log first before screening prospects.**

**Log location:** `shared/logs/linkedin-activity.md`

### Two Destination Files (Know the Difference)

| File | Purpose | When to Use |
|------|---------|-------------|
| `shared/logs/icp-prospects-[date].md` | **Discovery** - raw list of found prospects | 0 touches, just discovered, not engaged yet |
| `shared/logs/linkedin-activity.md` → Warming Up | **Pipeline** - actively warming prospects | 1+ touches, engagement started |

**Flow:**
```
ICP Finder discovers → icp-prospects file (0 touch)
         ↓
ICP Warmer engages → Warming Up table (1+ touches)
         ↓
Connect Timer sends request → Pending/Connected tables (3 touches)
```

### On Each Run:
1. **Read shared log first** to check:
   - Warming Up table (avoid re-discovering known prospects)
   - Today's connection requests count
   - Recent engagement with prospects (comment history)
2. **Read existing icp-prospects files** to check:
   - Prospects already discovered but not yet engaged
3. **After screening**, save appropriately:
   - NEW prospects (0 touch) → `icp-prospects-[date].md`
   - ENGAGED prospects (1+ touch) → Warming Up table in activity log
   - After connection request → Add to "Connection Requests" table

### What to Log:

**To icp-prospects file (discovery):**
```
| # | Name | Role | Company | Location | Classification | Profile URL | Notes |
```

**To Warming Up table (after first engagement):**
```
| Name | Profile URL | Recent Post URL | First Touch | Touches | Needed | Last Post Seen | Flags |
```

**Always capture Profile URL** for deduplication across files.

### Read from Log Instead of LinkedIn:
- Check "Warming Up" table for prospects already in pipeline
- Check icp-prospects files for discovered but not-yet-engaged prospects
- Check "Comments Made" for engagement history with prospects
- Check "High-Value Interactions" for warm leads
