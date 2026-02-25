---
name: linkedin-profile-icp
description: Analyze a LinkedIn profile to determine ideal customer profile (ICP) targeting. Use when user says "find my ICP" or provides their LinkedIn profile for ICP analysis. Extracts positioning signals from headline, about section, and experience to output job roles, titles, industries, and company types to target. Designed to feed targeting criteria into linkedin-icp-finder skill.
---

# LinkedIn Profile ICP Analyzer

Extract ICP targeting criteria from a LinkedIn profile to guide lead generation efforts.

## 360Brew Profile Optimization (2026)

LinkedIn's 360Brew algorithm "reads" your profile to verify your "Right to Speak" on topics. Profile optimization is critical:

**Headline as "Entity Signal":**
- Avoid clever titles like "Revolutionizing SMEs with AI"
- Use specific, indexable keywords: "Building Agentic ERP & CRM Systems for Singapore SMEs | Founder at Nexius Labs | Agentic AI Expert"
- 360Brew uses headline keywords as "Semantic Weights" for content distribution

**About Section as "System Prompt":**
- First 2 paragraphs must name 2-3 core pillars (e.g., Agentic AI, SQL/Schema Automation, SME Workflow)
- Write in clear, structured language the algorithm can parse
- 360Brew cross-references your DMs and posts against About section to verify authority

**Skill Tags as Semantic Weights:**
- Ensure core skills (e.g., "Agentic AI", "SQL Schema Design") are in top skills
- These directly influence content distribution to relevant audiences

**Profile-to-Content Alignment Rule:**
- If your profile says "Agentic AI" but you post motivational quotes, 360Brew flags as "Low Authority"
- 80% of content must align with entities/keywords in your profile

## Trigger

**Initial Analysis:**
- "find my ICP"
- "analyze my profile"
- Provides LinkedIn profile content for ICP analysis

**Refresh Mode:**
- "refresh my ICP"
- "update ICP profile"
- "has my ICP changed"

## Input

User provides their LinkedIn profile via:
- Copy-pasted profile sections (headline, about, experience)
- Screenshot of profile
- LinkedIn profile URL (requires browser MCP (Chrome DevTools or Playwright))

## Workflow

### Step 1: Extract Positioning Signals

Parse the profile for:

| Signal Type | Where to Find | What to Extract |
|-------------|---------------|-----------------|
| Value Proposition | Headline, About | Who they help + what outcome |
| Service/Product | About, Experience | What they build/deliver |
| Industry Focus | About, Experience | Sectors mentioned explicitly |
| Company Size Signals | About, Experience | "SME," "enterprise," "startup," employee counts |
| Pain Points Addressed | About | Problems they solve |
| Social Proof | Experience, About | Client types, case studies, numbers |

### Step 2: Map to ICP Criteria

From extracted signals, determine:

**Job Roles & Titles**
- Primary decision-makers who would buy this service
- Secondary influencers who might champion internally
- Map value proposition → who cares about this outcome

**Industries**
- Explicitly mentioned sectors
- Adjacent sectors with similar pain points
- Industries where the solved problems are acute

**Company Characteristics**
- Size range (employee count, revenue tier)
- Growth stage (startup, scaling, established)
- Geographic focus
- Tech maturity level

### Step 3: Define Anti-ICP (Who NOT to Target)

**Critical for efficiency** - Define who to skip immediately.

| Anti-ICP Category | Why Skip | Examples |
|-------------------|----------|----------|
| **Wrong Geography** | Outside service area | Non-ASEAN for ASEAN-focused business |
| **Wrong Company Size** | Can't afford / too complex | Enterprise for SME-focused, <5 employees |
| **Wrong Role Level** | No budget/authority | Individual contributors, interns |
| **Wrong Industry** | No fit for solution | Incompatible sectors |
| **Competitor Employees** | Conflict of interest | People working at competing vendors |
| **Job Seekers** | Not buying, seeking employment | "Open to Work" badge, recruiters |
| **Serial Networkers** | Connect with everyone, buy nothing | 10K+ connections, no engagement |

### Step 4: Create ICP Scoring Matrix

Weight criteria to prioritize prospects:

| Criteria | Weight | Score Range | How to Assess |
|----------|--------|-------------|---------------|
| **Geography** | 25% | 0 or 100 | ASEAN-5 = 100, Other = 0 (binary) |
| **Role Match** | 25% | 0-100 | Primary = 100, Secondary = 70, Adjacent = 40 |
| **Company Size** | 20% | 0-100 | Exact match = 100, Close = 70, Far = 30 |
| **Pain Signal** | 20% | 0-100 | Explicit pain = 100, Implied = 60, None = 20 |
| **Engagement Signal** | 10% | 0-100 | Inbound = 100, Active poster = 70, Lurker = 40 |

**ICP Score Calculation:**
```
ICP Score = (Geo × 0.25) + (Role × 0.25) + (Size × 0.20) + (Pain × 0.20) + (Engagement × 0.10)
```

**Priority Tiers:**
- 🔥 **HOT** (80-100): Pursue immediately
- 🟡 **WARM** (60-79): Worth engaging
- ⚪ **COOL** (40-59): Lower priority
- ❌ **SKIP** (<40 or Geography = 0): Don't pursue

### Step 5: Map Pain Points to Content Angles

For each pain point the profile addresses, create content mapping:

| Pain Point | Content Angle | Post Type | Hook Example |
|------------|---------------|-----------|--------------|
| [Pain 1] | [Angle] | [Educational/Story/Demo] | "[Hook]" |
| [Pain 2] | [Angle] | [Educational/Story/Demo] | "[Hook]" |
| [Pain 3] | [Angle] | [Educational/Story/Demo] | "[Hook]" |

**Content Types That Attract ICPs:**
- **Educational**: How-to, frameworks, tutorials (builds authority)
- **Story**: Case studies, failures, lessons learned (builds trust)
- **Demo**: Screenshots, videos, proof of work (builds credibility)
- **Contrarian**: Challenge conventional wisdom (builds thought leadership)
- **Curation**: Industry news + your take (builds relevance)

### Step 6: Generate Messaging Angles per Role

Create specific hooks for each target role:

**Template per Role:**
```
ROLE: [Title]
├─ Primary Pain: [What keeps them up at night]
├─ Desired Outcome: [What success looks like to them]
├─ Buying Trigger: [What makes them act NOW]
├─ Objection: [Why they might hesitate]
├─ Objection Handler: [How to address it]
└─ Hook Angle: "[Specific message that resonates]"
```

### Step 7: Generate Content Pillars

Based on profile and ICP, generate 3-5 content pillars:

**Content Pillar Framework:**
```
PILLAR 1: [Topic]
├─ Why It Matters to ICP: [Connection to their pain]
├─ Your Authority: [Why you can speak on this]
├─ Content Ideas:
│   ├─ [Idea 1]
│   ├─ [Idea 2]
│   └─ [Idea 3]
└─ Keywords: [For 360Brew algorithm]

PILLAR 2: [Topic]
...
```

**Pillar Balance:**
- 40% - Core expertise (what you do)
- 30% - Adjacent topics (industry trends, tools)
- 20% - Personal/human (stories, lessons, behind-the-scenes)
- 10% - Engagement (questions, polls, discussions)

### Step 8: Deep Dive Competitor Analysis

Identify competitors to monitor for ICP prospecting:

**Competitor Types:**
| Type | Who | Why Monitor |
|------|-----|-------------|
| **Direct Competitors** | Same solution space | Their frustrated customers = your prospects |
| **Legacy Vendors** | Old-school solutions | Users seeking alternatives |
| **Adjacent Tools** | Complementary products | Shared audience, different angle |
| **Industry Consultants** | Advisory in your space | Their audience trusts them |
| **Thought Leaders** | High-profile voices | Visibility + credibility boost |

**Per Competitor, Track:**
```
COMPETITOR: [Name/Company]
├─ LinkedIn URL: [URL]
├─ Follower Count: [X]
├─ Post Frequency: [X/week]
├─ Content Themes: [Topics they cover]
├─ Comment Quality: [Are commenters ICP-like?]
├─ Pain Signals in Comments: [Common complaints/questions]
└─ Monitor Strategy: [What to watch for]
```

### Step 9: Output ICP Targeting Brief

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICP TARGETING BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: [Date]
Profile: [Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 360BREW PROFILE AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Headline:
- Current: [Current headline]
- Entity Keywords Found: [List indexable terms]
- Recommendation: [Optimized headline if needed]

About Section:
- Core Pillars Identified: [List 2-3 pillars or "Missing"]
- Algorithm Readability: [Clear/Unclear]
- First 2 Paragraphs Signal: [What topics it signals authority for]

Skill Tags:
- Top Skills: [List visible skills]
- Missing Critical Skills: [Recommend additions]

Profile-Content Alignment Score: [High/Medium/Low]
- [Assessment of whether profile supports content topics]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. PROFILE POSITIONING SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1-2 sentence distillation of what the profile communicates]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. TARGET ICP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TARGET JOB ROLES:

Primary (Decision-Makers):
• [Role 1] — [Why they care]
• [Role 2] — [Why they care]

Secondary (Influencers):
• [Role 1] — [Why they'd champion]

TARGET INDUSTRIES:

Primary:
• [Industry 1] — [Fit reason]
• [Industry 2] — [Fit reason]

Adjacent:
• [Industry] — [Why similar pain points]

TARGET COMPANY PROFILE:

Size: [Range, e.g., 10-200 employees]
Stage: [Growth phase]
Geography: [Region focus - ASEAN-5]
Tech Maturity: [Low/Medium/High]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. ANTI-ICP (Who NOT to Target)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SKIP IMMEDIATELY:
❌ Geography: [Countries/regions to skip]
❌ Company Size: [Sizes to skip - too small/too large]
❌ Roles: [Roles with no authority/budget]
❌ Industries: [Non-fit industries]
❌ Red Flags: [Job seekers, competitors, serial networkers]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. ICP SCORING MATRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Criteria | Weight | Score 100 | Score 70 | Score 40 | Score 0 |
|----------|--------|-----------|----------|----------|---------|
| Geography | 25% | [Exact match] | - | - | [Non-ASEAN] |
| Role | 25% | [Primary roles] | [Secondary] | [Adjacent] | [No fit] |
| Company | 20% | [Exact size] | [Close] | [Far] | [Wrong] |
| Pain Signal | 20% | [Explicit] | [Implied] | [Weak] | [None] |
| Engagement | 10% | [Inbound] | [Active] | [Lurker] | [None] |

PRIORITY TIERS:
🔥 HOT (80-100): Pursue immediately
🟡 WARM (60-79): Worth engaging
⚪ COOL (40-59): Lower priority
❌ SKIP (<40): Don't pursue

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. MESSAGING ANGLES PER ROLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROLE: [Primary Role 1]
├─ Primary Pain: [What keeps them up at night]
├─ Desired Outcome: [What success looks like]
├─ Buying Trigger: [What makes them act NOW]
├─ Objection: [Why they might hesitate]
├─ Objection Handler: [How to address it]
└─ Hook: "[Specific message that resonates]"

ROLE: [Primary Role 2]
├─ Primary Pain: [Pain]
├─ Desired Outcome: [Outcome]
├─ Buying Trigger: [Trigger]
├─ Objection: [Objection]
├─ Objection Handler: [Handler]
└─ Hook: "[Hook]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. PAIN POINTS → CONTENT MAPPING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Pain Point | Content Angle | Post Type | Hook Example |
|------------|---------------|-----------|--------------|
| [Pain 1] | [Angle] | [Type] | "[Hook]" |
| [Pain 2] | [Angle] | [Type] | "[Hook]" |
| [Pain 3] | [Angle] | [Type] | "[Hook]" |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. CONTENT PILLARS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PILLAR 1: [Topic] (40% - Core Expertise)
├─ Why ICP Cares: [Connection to pain]
├─ Your Authority: [Why you can speak]
├─ Content Ideas: [Idea 1], [Idea 2], [Idea 3]
└─ Keywords: [For 360Brew]

PILLAR 2: [Topic] (30% - Adjacent)
├─ Why ICP Cares: [Connection]
├─ Your Authority: [Authority]
├─ Content Ideas: [Ideas]
└─ Keywords: [Keywords]

PILLAR 3: [Topic] (20% - Personal/Human)
├─ Why ICP Cares: [Builds trust]
├─ Content Ideas: [Stories, lessons, BTS]
└─ Keywords: [Keywords]

PILLAR 4: [Topic] (10% - Engagement)
├─ Purpose: [Drive discussion]
├─ Content Ideas: [Questions, polls]
└─ Keywords: [Keywords]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. COMPETITOR MONITORING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPETITOR 1: [Name]
├─ Type: [Direct/Legacy/Adjacent/Consultant/Thought Leader]
├─ LinkedIn: [URL]
├─ Why Monitor: [Their audience = your prospects]
├─ Content Themes: [What they post about]
└─ Watch For: [Pain signals in comments]

COMPETITOR 2: [Name]
├─ Type: [Type]
├─ LinkedIn: [URL]
├─ Why Monitor: [Reason]
├─ Content Themes: [Themes]
└─ Watch For: [Signals]

COMPETITOR 3: [Name]
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. SEARCH KEYWORDS & POSTS TO ENGAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LinkedIn Search Keywords:
• "[keyword 1]"
• "[keyword 2]"
• "[keyword 3]"
• "[keyword 4]"

Look for posts from:
• [Role] discussing [topic/pain point]
• [Role] asking about [topic]
• [Industry] thought leaders on [theme]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. READY FOR ICP-FINDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copy these filters to linkedin-icp-finder:

Role Filter: [Comma-separated titles]
Industry Filter: [Comma-separated industries]
Company Size: [Range]
Geography: [ASEAN-5 countries]
Pain Keywords: [Comma-separated terms]
Anti-ICP: [What to skip]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 10: Auto-Save to Reference File

**After generating the targeting brief, automatically save to reference file.**

**File location:** `references/icp-profile.md`

```markdown
# ICP Profile - [Name]

*Last updated: [Date]*
*Source: linkedin-profile-icp analysis*

## Quick Reference

| Criteria | Value |
|----------|-------|
| Target Roles | [Primary roles] |
| Target Industries | [Industries] |
| Company Size | [Range] |
| Geography | [ASEAN-5] |
| Pain Keywords | [Keywords] |

## Anti-ICP (Skip Immediately)

- ❌ [Anti-ICP item 1]
- ❌ [Anti-ICP item 2]
- ❌ [Anti-ICP item 3]

## ICP Scoring Matrix

[Copy scoring matrix from output]

## Messaging Angles

[Copy messaging angles from output]

## Content Pillars

[Copy content pillars from output]

## Competitors to Monitor

[Copy competitor list from output]

## Search Keywords

[Copy search keywords from output]

---

## Update Log

| Date | Change | Source |
|------|--------|--------|
| [Date] | Initial ICP profile created | linkedin-profile-icp |
```

**Auto-save behavior:**
- If `references/icp-profile.md` exists → Ask to overwrite or append
- If doesn't exist → Create new file
- Always add entry to Update Log

---

## Refresh Mode

**Trigger:** "refresh my ICP" / "update ICP profile" / "has my ICP changed"

**When to Refresh:**
- Profile has changed significantly (new role, new company)
- ICP hypothesis isn't generating quality leads
- Pivoting to new market/offering
- Quarterly review (recommended)

**Refresh Workflow:**

```
1. Read existing references/icp-profile.md
2. Re-analyze LinkedIn profile (same Steps 1-9)
3. Compare new analysis vs existing:
   - What changed?
   - What stayed the same?
   - Any new insights?
4. Output COMPARISON report
5. Ask: "Update the ICP profile with these changes?"
6. If yes → Update references/icp-profile.md with new data
```

**Refresh Output Format:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICP REFRESH COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Previous analysis: [Date]
Current analysis: [Date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHANGES DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 CHANGED:
• [Criteria]: [Old value] → [New value]
• [Criteria]: [Old value] → [New value]

➕ ADDED:
• [New criteria or insight]

➖ REMOVED:
• [Criteria no longer relevant]

✅ UNCHANGED:
• [Criteria that stayed the same]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Assessment of whether changes are significant enough to update]

Update ICP profile? (yes/no)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Integration with Other Skills

| Skill | How It Uses ICP Profile |
|-------|-------------------------|
| **linkedin-icp-finder** | Reads `references/icp-profile.md` for screening criteria |
| **linkedin-icp-warmer** | Uses ICP criteria to prioritize warming |
| **linkedin-elite-post** | Uses content pillars for post creation |
| **linkedin-pro-commenter** | Uses messaging angles for comment tone |
| **linkedin-daily-planner** | References competitors for monitoring tasks |

**Integration Flow:**
```
linkedin-profile-icp
         ↓
   references/icp-profile.md
         ↓
   ┌─────┴─────┬─────────────┬──────────────┐
   ↓           ↓             ↓              ↓
icp-finder  icp-warmer  elite-post  pro-commenter
```

---

## Quality Checklist

**Profile Analysis:**
- ✅ 360Brew Profile Audit completed (headline, about, skills)
- ✅ Profile-Content Alignment assessed
- ✅ Headline optimization suggested if needed

**ICP Definition:**
- ✅ Roles are specific titles, not vague categories
- ✅ Industries are concrete, not "various sectors"
- ✅ Company profile has specific size range
- ✅ Anti-ICP clearly defined (who to skip)

**Scoring & Messaging:**
- ✅ ICP Scoring Matrix has specific criteria per tier
- ✅ Messaging angles defined for each primary role
- ✅ Objections and handlers included

**Content Strategy:**
- ✅ Pain points mapped to content angles
- ✅ Content pillars follow 40/30/20/10 balance
- ✅ Keywords align with 360Brew requirements

**Competitor & Search:**
- ✅ Competitor accounts are real, monitorable pages
- ✅ Search keywords are terms prospects actually use

**File Management:**
- ✅ Output saved to `references/icp-profile.md`
- ✅ Update Log entry added with date