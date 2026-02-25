---
name: linkedin-icp-finder
description: Contact classification and ICP discovery for LinkedIn engagement in ASEAN markets. Classifies contacts as PEER (1K-10K followers, same niche), THOUGHT LEADER (10K+ followers), or PROSPECT (ICP criteria match). Use when user says "start icp", "classify contacts", "find prospects", or wants to screen LinkedIn profiles. Designed to work with browser MCP (Chrome DevTools or Playwright). References contact-classification.md for classification criteria and icp-profile.md for ICP screening. Outputs classification verdicts, engagement recommendations, and comment strategies per contact type.
---

# LinkedIn Contact Classifier & ICP Finder

Classify LinkedIn contacts and find prospects using the Digital Breadcrumb Strategy. Supports three contact types with tailored engagement approaches.

**Reference:** `references/contact-classification.md` for full classification criteria.

**🚨 STRICT GEOGRAPHY FILTER: Singapore, Malaysia, Thailand, Indonesia, Philippines ONLY**

**HARD RULE: If a prospect's location is not clearly one of these 5 ASEAN countries, SKIP IMMEDIATELY. Do not proceed with any further screening. No exceptions.**

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

## Contact Classification (Apply FIRST)

Before ICP screening, classify each contact into one of three categories.

**Reference:** See `references/contact-classification.md` for full criteria and flowchart.

### Classification Criteria

| Category | Follower Range | Key Signals |
|----------|---------------|-------------|
| **PEER** | 1K - 10K | Same niche (AI/automation), content creator, builder |
| **THOUGHT LEADER** | 10K+ | Established authority, high engagement, Top Voice |
| **PROSPECT** | Any | Decision-maker at SME, ICP role match, pain signals |

### Quick Classification Logic

```
1. Check if PROSPECT first (role-based, not follower-based):
   → Is this person a potential CUSTOMER?
   → Decision-maker at SME? Pain points you solve?
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

## Step 0: Cache-First Approach (Minimize LinkedIn Searches)

**CRITICAL: Free LinkedIn accounts have limited searches. Always check local files before searching LinkedIn.**

### Pre-Search Checklist

```
BEFORE ANY LINKEDIN SEARCH:
1. Read `shared/logs/icp-prospects.md`
   → Check if prospect already exists (by Name or Profile URL)
   → Check Profile Cache for recent data (< 7 days old)

2. Read `shared/logs/linkedin-activity.md`
   → Check Warming Up table (already engaged)
   → Check Connected table (already connected)

3. ONLY search LinkedIn if:
   → Prospect NOT in any file
   → OR cache data > 7 days old
   → OR specific new data needed (email, recent posts)
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
   - "CEO Singapore SME" instead of "CEO"
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
   Example: (CEO OR Founder OR "Managing Director") AND Singapore AND (SME OR "small business")

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

1. BUILD SAVED SEARCHES WITH ALERTS:
   Create these searches and enable daily/weekly alerts:

   Search 1: "ASEAN SME Decision Makers"
   ├─ Company size: 11-50, 51-200
   ├─ Seniority: Director, VP, CXO, Owner
   ├─ Geography: Singapore, Malaysia, Thailand, Indonesia, Philippines
   └─ Posted on LinkedIn: Yes (last 30 days)

   Search 2: "Operations Leaders Singapore"
   ├─ Function: Operations
   ├─ Seniority: Manager, Director, VP
   ├─ Geography: Singapore
   └─ Company size: 11-500

   Search 3: "Recent Job Changers (ICP Roles)"
   ├─ Changed jobs: Last 90 days
   ├─ Seniority: Director, VP, CXO
   ├─ Geography: ASEAN-5
   └─ Function: Operations, Finance, General Management

2. USE ADVANCED FILTERS (replaces manual screening):
   → Company Size filter = auto-screen SME
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

**ONLY PASS if prospect is CLEARLY from one of these 5 countries:**
- 🇸🇬 Singapore
- 🇲🇾 Malaysia
- 🇹🇭 Thailand
- 🇮🇩 Indonesia
- 🇵🇭 Philippines

**IMMEDIATELY SKIP if:**
- Prospect is from ANY other country (USA, UK, India, Australia, etc.)
- Location field shows any non-ASEAN country
- Company is headquartered outside these 5 countries (even if prospect claims ASEAN location)
- Geography is unclear, ambiguous, or not specified

**Geography verification (check in order):**
1. Profile location field (must explicitly show one of the 5 countries)
2. "Based in [ASEAN location]" in headline/about
3. Current company location

**If geography cannot be confirmed as one of the 5 ASEAN countries, SKIP. Do not guess. Do not proceed with caution. Just skip.**

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

🌏 GEOGRAPHY: [✅ CONFIRMED ASEAN / ❌ NON-ASEAN / ❌ UNCONFIRMED - SKIP]
Location: [Country/City - must be SG/MY/TH/ID/PH]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT / ❌ SKIP - NOT ASEAN-5 / ❌ SKIP - JOB POST / ❌ SKIP - COMMENTS DISABLED]

Role: [Title] → [Match assessment vs ICP roles]
Company: [Company, size if visible] → [Match assessment vs ICP company profile]
Pain Signal: [Quote/paraphrase] → [Match vs ICP pain keywords]

Fit Score: [X/4 criteria met] (Geography + Role + Company + Pain)
```

**If ❌ NON-ASEAN or ❌ UNCONFIRMED**: Stop screening immediately. Do not evaluate role, company, or pain signals. Output only geography verdict and move to next prospect. No exceptions.

## Step 4: Breadcrumb Engagement Plan

**PREREQUISITE: Only proceed to this step if prospect has ✅ CONFIRMED ASEAN geography (SG/MY/TH/ID/PH).**

For ✅ HIGH FIT or ⚠️ MEDIUM FIT prospects with confirmed ASEAN-5 location:

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
         ├─ Geography: ASEAN-5 only (SG/MY/TH/ID/PH)
         ├─ Role: Decision-maker, Manager+
         ├─ Company: SME size
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
├─ ✅ PASS: SG, MY, TH, ID, PH only
└─ ❌ SKIP: All others, unclear = immediate skip

👤 ROLE CHECK
├─ ✅ Decision-maker, Manager, Director, Head of, C-suite
└─ ❌ Skip: Junior, Individual Contributor, Student

🏢 COMPANY CHECK
├─ ✅ SME (10-500 employees)
└─ ❌ Skip: Enterprise, MNC, Startup <10

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

🌏 GEOGRAPHY: [✅ CONFIRMED ASEAN / ❌ SKIP]
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
- [X] Non-ASEAN
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
| 9 | Jane Tan | COO | ScaleSG | Singapore | PROSPECT | [URL] | 🔥 INBOUND: Viewed after automation post, 2x viewer |
| 10 | Mike Lee | Director Ops | GrowthMY | Malaysia | PROSPECT | [URL] | 🔥 INBOUND: New follower, liked 3 posts |
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

🌏 GEOGRAPHY: [✅ CONFIRMED ASEAN / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

WARMTH LEVEL: 2 touches (reshare = strong endorsement)
ACTION: Thank them + 1 comment on their content → Connect
```

**File Notation:**
```
| 11 | [Name] | [Role] | [Company] | Singapore | PROSPECT | [URL] | 🔄 RESHARER: Shared my [topic] post with commentary |
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

🌏 GEOGRAPHY: [✅ CONFIRMED ASEAN / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

PAIN CATEGORY: [Which ICP pain this maps to]
ACTION: Find their posts → Comment with relevant insight → Build touches
```

**File Notation:**
```
| 12 | [Name] | [Role] | [Company] | Singapore | PROSPECT | [URL] | 🎯 COMPETITOR: Commented on [Vendor] about [pain] |
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

🌏 GEOGRAPHY: [✅ CONFIRMED ASEAN / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

WARM INTRO PATH: [Yes - can ask mutual / No - engage directly]
ACTION: [Ask for intro / Mention mutual in request / Engage content first]
```

**File Notation:**
```
| 13 | [Name] | [Role] | [Company] | Singapore | PROSPECT | [URL] | 🤝 SHARED: Via [Mutual Name], can request intro |
```

---

### Strategy 4: Group Members (Low Priority)

**Why Lower:** Groups can be noisy, but members self-selected into relevant topics.

**How to Find:**
```
1. Join groups relevant to your ICP:
   - Singapore SME groups
   - ASEAN business groups
   - Industry-specific groups (F&B, Manufacturing, etc.)
   - Operations/Finance professional groups
2. Go to Group → Members
3. Filter/search by role keywords
4. Screen for ICP fit
```

**Best Groups for ASEAN SME ICPs:**
- Singapore Business Federation
- SME Centre Singapore
- ASEAN Entrepreneurs Network
- Industry-specific: F&B Singapore, Manufacturing Leaders, etc.

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

🌏 GEOGRAPHY: [✅ CONFIRMED ASEAN / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

ACTION: Engage in group discussions first → Then connect
```

**File Notation:**
```
| 14 | [Name] | [Role] | [Company] | Singapore | PROSPECT | [URL] | 👥 GROUP: [Group Name] member, active poster |
```

---

### Strategy 5: Event Attendees (Low Priority)

**Why Lower:** Events are periodic, but attendees have concentrated interest in topic.

**How to Find:**
```
1. Search LinkedIn Events for relevant topics:
   - "AI Singapore"
   - "SME Digital Transformation"
   - "Operations Excellence ASEAN"
2. Click event → View attendees
3. Screen attendees for ICP fit
```

**Event Types to Monitor:**
- Webinars on topics you solve
- Industry conferences (virtual or in-person)
- Networking events for SME leaders
- Tech/AI events in ASEAN

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

🌏 GEOGRAPHY: [✅ CONFIRMED ASEAN / ❌ SKIP]

VERDICT: [✅ HIGH FIT / ⚠️ MEDIUM FIT / ❌ NO FIT]

Role: [Title] → [Match assessment]
Company: [Company] → [Match assessment]

ACTION: Connect with event context → Follow up with value-add
```

**File Notation:**
```
| 15 | [Name] | [Role] | [Company] | Singapore | PROSPECT | [URL] | 📅 EVENT: Attending [Event Name] on [Date] |
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

| # | Name | Date Found | Degree | Role | Company | Location | Email | Classification | Profile URL | Notes |
|---|------|------------|--------|------|---------|----------|-------|----------------|-------------|-------|
| 1 | Su Mei Toh | 22Jan | 2nd | CEO | SME Republic | Singapore | - | PROSPECT | [URL] | SME-focused |
| 2 | David Cheang | 22Jan | 2nd | CEO | DC13 Group | Singapore | - | PROSPECT | [URL] | Board Director |
| 3 | New Prospect | 23Jan | 1st | COO | NewCo | Malaysia | john@newco.com | PROSPECT | [URL] | Pain signal |
```

### Column Definitions

| Column | Description | Values |
|--------|-------------|--------|
| **Date Found** | Discovery date | DDMon format (e.g., 22Jan) |
| **Degree** | LinkedIn connection degree | `1st`, `2nd`, `3rd`, or `-` (not checked) |
| **Email** | Email if visible | email address or `-` |
| **Classification** | Contact type | PROSPECT, PEER, THOUGHT LEADER |

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
- Prioritize Singapore prospects (home market)
- **Save** their last 2 posts before engaging (360Brew values Saves 5x more than Likes)
- Reply to DMs/comments within 1 hour (boosts your post reach by 35%)

### DON'T ❌
- Pitch in comments
- Use generic AI comments
- Spam or engage with every comment
- Send connection requests immediately
- Hard-sell your product/service
- Engage with ANY prospect outside Singapore, Malaysia, Thailand, Indonesia, or Philippines
- Proceed with prospects whose geography is unclear or unconfirmed
- Make exceptions for "interesting" prospects who aren't in the ASEAN-5
- **Engage with job postings or hiring announcements** (appears opportunistic, no pain signals)
- **Engage with posts that have comments disabled** (no engagement opportunity)
- **Send external links in first DM** (360Brew flags as "low-trust signal")
- **Exceed 15-20 connection requests/day** (triggers Automation Detection)
- **Use templated connection notes** (blank requests perform 10-15% better unless 100% bespoke)

## Value-First DM Strategy (PROSPECTS ONLY - Post-Connection)

**⚠️ Only DM PROSPECT connections (ICP matches). Do NOT DM Peers or Thought Leaders.**

**360Brew "Anti-Pitch" Approach:**
Once connected with a PROSPECT, don't pitch. Offer a "Native Asset" instead:

```
VALUE-FIRST DM TEMPLATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hey [Name], enjoyed your post on [Topic].

I just finished a workflow for [Specific Pain Point]. Happy to share the logic diagram if useful for your team—no strings attached.
```

**Native Assets to Offer:**
- Loom video walkthrough
- Schema/logic diagram
- PRD template
- SQL seed data structure

**DM Guardrails:**
- Never send external links in first message (flagged as spam)
- Keep initial DM under 3 sentences
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

## ASEAN-Specific Search Keywords

Run these searches with ASEAN location filters:

```
"Singapore SME" + [pain keyword]
"Malaysia business" + [automation/operations keyword]
"Thailand startup" + [scaling keyword]
"Indonesia enterprise" + [finance/ERP keyword]
"Philippines company" + [operations keyword]
"Southeast Asia" + [ICP pain point]
```

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
- ✅ Only prospects from SG/MY/TH/ID/PH pass geography check
- ✅ Unconfirmed geography = automatic skip (not "proceed with caution")
- ✅ **Job postings and hiring announcements = automatic skip**
- ✅ **Posts with comments disabled = automatic skip**
- ✅ Screening uses loaded ICP criteria (not hardcoded)
- ✅ Non-ASEAN and unconfirmed prospects immediately skipped with no further evaluation

**During Inbound Screening (Lurker Mode):**
- ✅ Geography filter applied FIRST (same ASEAN-5 rule)
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
