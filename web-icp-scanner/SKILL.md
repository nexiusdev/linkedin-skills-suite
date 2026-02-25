---
name: web-icp-scanner
description: Discover and score new ICP prospects from non-LinkedIn web sources, then auto-approve and log qualified leads into prospect trackers. Use when users ask to scan the web for ICP prospects, run daily autonomous prospect discovery, or add scored web leads to the pipeline.
---

# Web ICP Scanner

Scan the web daily to find 10 ICP prospects outside of LinkedIn. **FULLY AUTONOMOUS** - auto-approves all prospects scoring 60+ without user interaction.

## Trigger Phrases

- "scan web for prospects"
- "find ICP prospects"
- "web icp scan"
- "daily prospect scan"
- "find 10 prospects"
- "prospect hunting"

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WEB ICP SCANNER - FULLY AUTONOMOUS DAILY PROSPECT DISCOVERY           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. LOAD → Load ICP profile + learning history                         │
│  2. SEARCH → Multi-source web search (news, directories, press)        │
│  3. FILTER → Apply ICP filters + learned patterns                      │
│  4. SCORE → Calculate ICP score for each prospect                      │
│  5. AUTO-APPROVE → All prospects scoring 60+ are AUTO-APPROVED         │
│  6. LOG → Save to web-discovered-prospects.md + icp-prospects.md       │
│  7. REPORT → Show summary of prospects added (no user input needed)    │
│                                                                         │
│  ⚠️ NO USER FEEDBACK REQUIRED - All 60+ score prospects auto-added    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## AUTONOMOUS MODE (Default)

**All prospects scoring 60+ are automatically approved and added to icp-prospects.md.**

- Do NOT ask for user feedback
- Do NOT wait for approval
- Auto-add all qualifying prospects immediately
- Show summary when complete

## Phase 1: Load ICP Profile & Learning History

**Before any search, ALWAYS read these files:**

```
REQUIRED FILES:
├── linkedin-core/references/icp-profile.md              # Current ICP criteria
├── web-icp-scanner/icp-learning-log.md    # Feedback history + learned patterns
└── linkedin-core/shared/logs/icp-prospects.md           # Master prospect list (dedup check)
```

**Extract from ICP Profile:**
- Target roles (primary + secondary)
- Target industries (primary + adjacent)
- Company size range
- Geography ({{CLIENT_TARGET_GEO}} focus)
- Pain keywords
- Search keywords

**Extract from Learning Log:**
- Positive signals (from approved prospects)
- Negative signals (from rejected prospects)
- Refined search queries (what works)
- Industries/roles to boost or demote

## Phase 2: Multi-Source Web Search

**Search Categories (rotate daily for coverage):**

### Category A: Company News & Press Releases

Search queries (combine ICP keywords + signals):

```
Day 1: "[industry] company funding Singapore Malaysia 2026"
Day 2: "[industry] SME expansion ASEAN announcement"
Day 3: "[pain keyword] solution provider Singapore"
Day 4: "CEO founder [industry] interview Singapore Malaysia"
Day 5: "[industry] digital transformation case study ASEAN"
Day 6: "[industry] startup raises series A Singapore"
Day 7: "SME [industry] awards Singapore Malaysia 2026"
```

### Category B: Industry Directories & Lists

Search queries:

```
- "top SME [industry] companies Singapore 2026"
- "[industry] companies list Malaysia"
- "fastest growing [industry] SME ASEAN"
- "[industry] association members Singapore"
- "Enterprise Singapore [industry] companies"
```

### Category C: Event Speakers & Panelists

Search queries:

```
- "[industry] conference speaker Singapore 2026"
- "SME summit panelist ASEAN"
- "[industry] webinar presenter Malaysia"
- "digital transformation event speaker Singapore"
```

### Category D: Awards & Recognition

Search queries:

```
- "SME awards [industry] Singapore 2026"
- "enterprise [industry] award winner Malaysia"
- "business excellence award [industry] ASEAN"
- "fastest growing company award Singapore"
```

### Category E: Job Postings (Company Signal)

Search queries:

```
- "[industry] company hiring Singapore"
- "SME hiring [role] Malaysia"
- "startup hiring operations manager ASEAN"
```

### Category F: Startup Founder Lists & Rankings

Search queries:

```
- "top startup founders Singapore 2026"
- "startup founders to watch ASEAN 2026"
- "Forbes 30 under 30 Singapore Malaysia"
- "emerging entrepreneurs Southeast Asia 2026"
- "Tech in Asia startup founders Singapore"
```

### Category G: Entrepreneur of the Year & Business Awards

Search queries:

```
- "EY Entrepreneur of the Year Singapore Malaysia nominees"
- "SME100 Awards Malaysia winners"
- "Singapore SME 500 Award winners Best Digital Adopter"
- "Emerging Enterprise Awards Singapore winners"
- "Platinum Business Awards Malaysia winners"
- "SOBA Star Outstanding Business Awards Malaysia"
```

### Category H: Venture Capital & Funding Announcements

Search queries:

```
- "Series A funding Singapore startup 2026 founder"
- "seed round raised Singapore SME 2026"
- "venture capital investment Malaysia startup founder"
- "Tech in Asia funding round ASEAN SME"
- "Deal Street Asia startup funding Singapore Malaysia"
```

### Category I: Government Programs & Accelerator Graduates

Search queries:

```
- "Enterprise Singapore startup SG founder grant recipients"
- "MDEC Malaysia digital economy corporation SME"
- "startup accelerator graduates Singapore 2025 2026"
- "Antler Singapore cohort founders"
- "SWITCH Singapore startup pitch competition winners"
- "MaGIC Malaysia accelerator program graduates"
```

### Category J: Industry-Specific Thought Leadership

Search queries:

```
- "SME CEO interview [industry] Singapore podcast"
- "[industry] founder story Malaysia ASEAN"
- "digital transformation success story SME Singapore"
- "automation case study SME operations ASEAN"
- "Business Times Singapore SME profile [industry]"
```

### Category K: Podcast Guest Appearances ⭐ HIGH PRIORITY

Search queries:

```
- "SME founder interview podcast Singapore 2026"
- "BFM podcast entrepreneur Malaysia CEO"
- "Money FM 89.3 business leader interview Singapore"
- "e27 podcast startup founder ASEAN"
- "Asia Tech Podcast founder CEO Singapore Malaysia"
- "[industry] founder podcast interview Southeast Asia"
```

### Category L: Business Media Founder Profiles ⭐ HIGH PRIORITY

Search queries:

```
- "The Peak Singapore entrepreneur profile founder"
- "Tatler Asia founder CEO Singapore Malaysia"
- "Singapore Business Review CEO interview SME"
- "The Edge Singapore entrepreneur profile"
- "Business Times Singapore CEO of the week SME"
- "Digital News Asia founder profile Malaysia"
```

### Category M: Franchise & Multi-Unit Operators ⭐ HIGH PRIORITY

Search queries:

```
- "franchise owner Singapore multiple outlets founder"
- "multi-unit operator Malaysia F&B retail chain"
- "franchise expansion Singapore Malaysia ASEAN 2026"
- "restaurant chain founder Singapore 10 outlets"
- "retail chain operator Malaysia expansion scaling"
- "franchise owner CEO interview Singapore operations"
```

---

### LOW PRIORITY CATEGORIES

*Use these when primary categories (A-M) are exhausted or for targeted scans.*

### Category N: University Alumni Entrepreneur Networks (LOW PRIORITY)

Search queries:

```
- "NUS Enterprise alumni startup founders"
- "SMU Institute of Innovation alumni entrepreneurs"
- "NTU alumni startup Singapore founder"
- "INSEAD Singapore alumni entrepreneur CEO"
- "University of Malaya alumni startup founder"
```

### Category O: Co-working / Incubator Member Directories (LOW PRIORITY)

Search queries:

```
- "JTC LaunchPad Singapore startup members"
- "Block71 Singapore portfolio companies founders"
- "Found8 Singapore startup members"
- "WORQ Malaysia coworking startup founders"
- "1337 Ventures accelerator Malaysia portfolio"
```

### Category P: M&A and Exit Announcements (LOW PRIORITY)

Search queries:

```
- "startup acquisition Singapore founder 2025 2026"
- "SME exit Malaysia acquired founder"
- "merger acquisition announcement Singapore SME"
- "second-time founder Singapore startup serial entrepreneur"
```

### Category Q: Government Tender Winners (LOW PRIORITY)

Search queries:

```
- "GeBIZ Singapore tender awarded SME company"
- "government procurement winner SME Singapore"
- "MyProcurement Malaysia awarded company SME"
- "government contract winner [industry] Singapore"
```

### Category R: Industry Association Directories (LOW PRIORITY)

Search queries:

```
- "Singapore Fintech Association members directory"
- "Singapore Manufacturing Federation member companies"
- "Malaysia SME Association council members"
- "Singapore Retailers Association member list"
- "ASEAN Business Advisory Council members"
```

### Category S: Trade Show & Exhibition Exhibitors (LOW PRIORITY)

Search queries:

```
- "SME exhibitor list Singapore Expo 2025 2026"
- "Food & Hotel Asia exhibitor Singapore SME"
- "Manufacturing Solutions Expo exhibitor Singapore"
- "SEMICON Southeast Asia exhibitor Malaysia"
- "RetailAsia Expo Singapore exhibitor list company"
```

### Category T: Business Networking Groups (LOW PRIORITY)

Search queries:

```
- "BNI Singapore chapter members business owner"
- "Entrepreneurs' Organization EO Singapore members"
- "Young Presidents Organization YPO Singapore Malaysia"
- "TiE Singapore charter member entrepreneur"
- "Rotary Club Singapore business owner founder"
```

### Category U: Crowdfunding & Community-Funded Projects (LOW PRIORITY)

Search queries:

```
- "Kickstarter Singapore founder project funded"
- "Indiegogo Singapore Malaysia startup campaign"
- "equity crowdfunding Singapore FundedHere Fundnel"
- "crowdfunding success story ASEAN founder SME"
```

### Category V: Patent & IP Filings (LOW PRIORITY)

Search queries:

```
- "patent filed Singapore startup founder IPOS"
- "intellectual property Malaysia SME innovation"
- "Singapore patent grant company founder [industry]"
- "MyIPO Malaysia patent registered SME"
```

### Category W: E-commerce Marketplace Top Sellers (LOW PRIORITY)

Search queries:

```
- "top Shopee seller Singapore founder brand owner"
- "Lazada top seller Malaysia SME business owner"
- "Amazon Singapore seller SME founder story"
- "e-commerce brand owner Singapore success story"
- "D2C brand founder Singapore Malaysia ASEAN"
```

### Category X: Business Book Authors & Course Creators (LOW PRIORITY)

Search queries:

```
- "Singapore entrepreneur author business book founder"
- "Malaysia CEO author book SME business"
- "Udemy Skillshare course creator Singapore founder"
- "ASEAN business author entrepreneur speaker"
```

### Category Y: Angel Investor Portfolios (LOW PRIORITY)

Search queries:

```
- "angel investor Singapore portfolio companies founders"
- "Angel Central Singapore invested startups"
- "BANSEA Business Angel Network Southeast Asia members"
- "angel syndicate Malaysia startup founder invested"
- "Singapore angel network portfolio company CEO"
```

### Category Z: Office Expansion & Lease Announcements (LOW PRIORITY)

Search queries:

```
- "company new office Singapore expansion SME"
- "startup office move Singapore larger space hiring"
- "Malaysia SME new headquarters expansion announcement"
- "JTC industrial space lease Singapore company"
- "company expansion announcement ASEAN new market"
```

---

**Execute 5-7 searches per scan** using WebSearch tool. Rotate across categories to ensure broad coverage - use 2-3 categories per scan. Prioritize ⭐ HIGH PRIORITY categories (K, L, M) alongside proven categories (F, G, H). Use LOW PRIORITY categories (N-Z) when primary categories are exhausted or for targeted industry-specific scans.

## Phase 3: ICP Filtering & Scoring

For each potential prospect found, apply this scoring matrix:

### ICP Score Matrix (100 points total)

| Criteria | Weight | Scoring |
|----------|--------|---------|
| **Geography** | 25 pts | Singapore (25), Malaysia (20), Thailand/Indonesia/Philippines (15), Other ASEAN (10), Outside ASEAN (0) |
| **Role Match** | 25 pts | Primary role (25), Secondary role (15), Adjacent role (10), Unclear (5), Non-target (0) |
| **Company Size** | 20 pts | 10-200 employees (20), 200-500 (15), <10 (10), >500 (5), Unknown (10) |
| **Industry Match** | 20 pts | Primary industry (20), Adjacent industry (15), Other (10), Mismatch (0) |
| **Pain Signal** | 10 pts | Strong pain indicator (10), Moderate (5), None (0) |

**Minimum Score to Include: 60 points**

### Learned Pattern Adjustments

Apply modifiers from learning log:

```
POSITIVE SIGNALS (add points):
- [From approved prospects - dynamically populated]
- Example: "+5 for Series A companies" (learned pattern)

NEGATIVE SIGNALS (subtract points):
- [From rejected prospects - dynamically populated]
- Example: "-10 for consulting firms" (learned pattern)
```

## Phase 4: Present Prospects

**Output format for each prospect (show 10 per scan):**

```markdown
## Prospect [#]: [Name]

**Role:** [Title] at [Company]
**Location:** [City, Country]
**Industry:** [Industry]
**Company Size:** [Estimated size]
**Source:** [Where found - article title, directory, etc.]
**Source URL:** [Link]

### ICP Score: [XX]/100

| Criteria | Score | Reasoning |
|----------|-------|-----------|
| Geography | X/25 | [Singapore = 25] |
| Role | X/25 | [CEO = Primary = 25] |
| Company Size | X/20 | [~50 employees = 20] |
| Industry | X/20 | [E-commerce = Primary = 20] |
| Pain Signal | X/10 | [Mentioned "scaling challenges" = 10] |

### Key Signals

- [Signal 1 from source]
- [Signal 2 from source]
- [Relevant quote if available]

### Contact Discovery

- **LinkedIn:** [Search query to find them]
- **Company Website:** [URL if found]
- **Email:** [Actual email if found, or pattern-based guess]

---

**Your verdict?** [APPROVE] [REJECT] [MAYBE]
**If REJECT, why?** (This trains the learning system)
```

## Phase 4b: Dedicated Email Search (Per Prospect)

**For EVERY auto-approved prospect, run a dedicated email search BEFORE moving to Phase 5.**

This is a **4-tier waterfall approach** with escalating cost:

1. **Tier 1:** Web Search (FREE) — Primary method
2. **Tier 2:** Opportunistic Extraction (FREE) — From sources already visited
3. **Tier 3:** API Waterfall (PAID CREDITS) — Only for 70+ score prospects
4. **Tier 4:** Pattern Detection (FREE) — Last resort guessing

**Credit conservation strategy:** API enrichment (Tier 3) runs ONLY for high-priority prospects scoring 70+ to preserve the 275 lookups/month quota for top-tier ICP matches.

### Tier 1: Targeted Web Search Queries (PRIMARY — run for every prospect)

Run these searches using WebSearch for each approved prospect:

```
QUERY 1: "[Full Name]" "[Company]" email
QUERY 2: "[Full Name]" "[Company]" contact site:rocketreach.co OR site:contactout.com OR site:signalhire.com OR site:zoominfo.com
QUERY 3: "[Company]" website domain email
```

**Accept criteria:**
- Email domain must match the company (e.g., `@acme.sg` for Acme Pte Ltd)
- Personal business emails preferred over generic (info@, hello@, contact@)
- Only accept fully visible emails — reject masked emails (j***@company.com)

**Batch optimization:** When processing 10 prospects, launch parallel sub-agents (batches of 5) to search emails concurrently. Each sub-agent runs all 3 queries per prospect.

### Tier 2: Opportunistic Extraction (SECONDARY — from sources already visited)

#### From Article/Press Release Content

When reading news articles or press releases about a prospect:
- Look for direct quotes with contact info: "For more information, contact [name] at [email]"
- Check article author bylines for email addresses
- Look for "About the Author" sections with contact details

#### From Company Website Deep Dive

When you find a prospect's company website, check these pages:

```
PRIORITY ORDER:
1. /contact or /contact-us → Often has direct emails
2. /about or /about-us → Team page with individual emails
3. /team or /our-team → Leadership bios with emails
4. /leadership or /management → Executive contact info
5. Footer → Often contains info@ or hello@ emails
6. /press or /media → Press contact emails
```

#### From Conference/Event Speaker Pages

Event websites often list speaker contact info:
- Speaker bio pages
- Event contact directories
- Speaker submission forms (sometimes show email)

#### From Industry Directory Listings

Business directories often include:
- Company profile pages with contact details
- Member directories with email listings
- Association member pages

### Tier 3: API Waterfall (ONLY if Tier 1 & 2 fail) 💳

**For high-priority prospects where web search and opportunistic extraction found nothing.**

Run this ONLY for prospects scoring **70+ points** to conserve API credits:

```
EXECUTION:
1. Load MCP tool: crm_find_email (via ToolSearch first)
2. Call with prospect data:
   - name: [Full Name]
   - company: [Company Name]
   - linkedin_url: [LinkedIn URL from Phase 4c]
   - domain: [Company domain if found]
3. Waterfall tries providers in sequence:
   → Apollo (50/month) — name + company + LinkedIn URL
   → Hunter (25/month) — name + domain
   → Snov.io (50/month) — name + domain
   → GetProspect (50/month) — name + company/domain
   → Prospeo (100/month) — LinkedIn URL or name + company
4. Stops at first verified email found
```

**Credit Management:**
- Total capacity: 275 lookups/month across all providers
- Use ONLY for prospects scoring 70+ (top-tier ICP matches)
- Track usage per scan to avoid exhausting monthly quota
- Log which provider found the email for cost analysis

**When to skip API enrichment:**
- Prospect scores < 70 (medium priority)
- Monthly credits exhausted
- No company name or LinkedIn URL available (insufficient data)

**Result handling:**
- ✅ Email found → Update Email column with source "(Apollo)", "(Hunter)", etc.
- ❌ Not found → Fall through to Tier 4 (Pattern Detection)

### Tier 4: Email Pattern Detection (Last Resort)

If no direct email found from Tier 1, 2, or 3, infer from company domain:

```
COMMON PATTERNS (use with Company URL domain):
- firstname@company.com (most common)
- firstname.lastname@company.com
- f.lastname@company.com
- first.last@company.com
- firstnamelastname@company.com

EXAMPLE:
Prospect: John Tan
Company URL: https://acme.sg
Pattern guess: john@acme.sg or john.tan@acme.sg
```

### Email Validation & Confidence Levels

Mark email confidence level and source:

**Tier 1 - Web Search:**
- **Confirmed** — Found directly on website, article, or contact database (rocketreach, contactout, etc.)
- Mark source: "Web Search"

**Tier 2 - Opportunistic:**
- **Confirmed** — Found on company website, event page, or directory
- Mark source: "Company Website", "Event Page", "Directory"

**Tier 3 - API Waterfall:**
- **Verified** — Found via API provider with verified/valid status
- Mark source: "(Apollo)", "(Hunter)", "(GetProspect)", etc.

**Tier 4 - Pattern:**
- **Pattern-based** — Inferred from company email pattern
- Mark with `(pattern)` suffix

**Not found:**
- No email discovered across all tiers
- Leave as `-` or `Not found`

**Do NOT store:**
- Masked/partial emails (j***@company.com)
- Generic company emails (info@, hello@, contact@) unless the prospect IS the sole owner
- Unverified guesses without domain confirmation
- Low-confidence API results (< 80% confidence)

### Update Master Prospect List

When adding APPROVED prospects to `icp-prospects.md`:

```markdown
Email column values:
- Web Search found → john.tan@acme.sg
- API found → john.tan@acme.sg
- Pattern-based → john.tan@acme.sg (pattern)
- Unknown → Not found

Notes column tracking:
- "Email: Web Search 07Feb" (Tier 1)
- "Email: Company Website 07Feb" (Tier 2)
- "Email: Apollo API 07Feb" (Tier 3)
- "Email: Hunter API 07Feb" (Tier 3)
- "Email: Pattern-based 07Feb" (Tier 4)
- "Email: Not found (tried all tiers) 07Feb"
```

---

## Phase 4c: LinkedIn Profile URL Discovery

**ALWAYS attempt to find LinkedIn profile URL for each prospect. This is CRITICAL for future engagement.**

### Strategy 1: Google Search with LinkedIn Site Filter (PRIMARY METHOD)

**Most effective approach - use this FIRST:**

```
SEARCH QUERY FORMAT:
"[Full Name]" "[Company Name]" [Role/Title] site:linkedin.com/in/

EXAMPLES:
- "Brian Ng" "Kskin" co-founder site:linkedin.com/in/
- "Jennifer Zhang" "WIZ.AI" CEO site:linkedin.com/in/
- "Alan Lai" "ProfilePrint" founder site:linkedin.com/in/
```

**Success indicators:**
- First result is usually the correct profile
- Look for job title match in search snippet
- Verify company name in snippet
- Profile URL format: https://linkedin.com/in/[username] or https://sg.linkedin.com/in/[username]

### Strategy 2: LinkedIn Company Page → People Tab

**Use when Strategy 1 fails or returns ambiguous results:**

```
WORKFLOW:
1. Search Google for: "[Company Name]" LinkedIn company page
2. Navigate to company LinkedIn page: linkedin.com/company/[company-slug]
3. Click "People" tab on company page
4. Use search box to search for prospect's name
5. If not found in search, browse employee list (may need multiple pages)
```

**Why this works:**
- Directly shows all employees with LinkedIn profiles at that company
- No ambiguity about which "[Common Name]" is the right person
- Can verify role/title matches

**When to use:**
- Common names (e.g., "John Tan", "Mary Lee")
- Google search returns too many results
- Need to verify prospect still works at company

### Strategy 3: Company Website → Team/About Page

**Use for executive-level prospects or when LinkedIn search fails:**

```
WEBSITE PAGES TO CHECK:
1. /team or /our-team → Often links to LinkedIn profiles
2. /about-us or /about → Team bios with social links
3. /leadership or /management → Executive profiles
4. /founders or /our-story → Founder bios
5. Footer → Sometimes has team member social links
```

**Look for:**
- LinkedIn icon links next to team member photos
- "Connect with [Name] on LinkedIn" links
- Social media icon bars under bio sections

### Strategy 4: Press Release & News Article Search

**For high-profile founders and executives:**

```
SEARCH QUERIES:
- "[Full Name]" "[Company]" LinkedIn interview
- "[Full Name]" "[Company]" founder profile
- "[Company]" raises funding "[Full Name]" LinkedIn
- "[Full Name]" "[Company]" startup awards LinkedIn
```

**Why this works:**
- Journalists often link to LinkedIn profiles in articles
- Press releases sometimes include profile links
- Award announcements link to winner profiles

### Strategy 5: Crunchbase Cross-Reference

**For startup founders and funded companies:**

```
SEARCH: "[Full Name]" "[Company]" Crunchbase

Crunchbase profiles often link to:
- LinkedIn profile URLs
- Personal websites (which may link to LinkedIn)
- Other social profiles
```

### Strategy 6: Alternative Name Formats

**If initial search fails, try variations:**

```
NAME VARIATIONS TO TRY:
- Full name: "Joshua Christopher Chandra"
- First + Last: "Joshua Chandra"
- Initials: "J.C. Chandra"
- Nickname: "Josh Chandra"
- Different surname order (for Asian names): "Chandra Joshua"
```

### LinkedIn Profile URL Validation

**Before saving, verify it's the correct person:**

```
VERIFICATION CHECKLIST:
✓ Current company matches (or recent if they switched jobs)
✓ Job title/role aligns with prospect info
✓ Location matches (Singapore, Malaysia, etc.)
✓ Industry matches
✓ Follower count seems appropriate for role
```

### Handling Edge Cases

| Scenario | Action |
|----------|--------|
| **No LinkedIn profile found** | Mark Profile URL as "TBD" - may not have LinkedIn |
| **Multiple profiles with same name** | Use Company Page strategy to disambiguate |
| **Profile is private/limited** | Still save URL - can at least send connection request |
| **Wrong company in profile** | Check if they recently changed jobs; verify via news search |
| **Profile deactivated** | Mark as "INACTIVE" in Notes field |

### Update Master Prospect List

When adding APPROVED prospects to `icp-prospects.md`:

```markdown
Profile URL column values:
- Found via Google: https://sg.linkedin.com/in/username
- Found via company page: https://www.linkedin.com/in/username
- Not found: TBD

Add to Notes: "LinkedIn: [discovery method] [date]"
Examples:
- "LinkedIn: Google search 05Feb"
- "LinkedIn: Company page 05Feb"
- "LinkedIn: TBD - no profile found 05Feb"
```

### Success Rate Benchmarks

Based on 20-prospect batch testing:

| Prospect Type | Success Rate | Primary Method |
|---------------|--------------|----------------|
| Startup founders (funded) | 90%+ | Google + site:linkedin.com/in/ |
| SME CEOs/Co-founders | 70-80% | Company page search |
| Executives at larger SMEs | 60-70% | Company page + Google |
| Technical co-founders | 50-60% | May use different name formats |

**Time investment:** 2-3 minutes per prospect (worthwhile for engagement ROI)

---

## Phase 5: Auto-Approve All Qualifying Prospects

**⚠️ AUTONOMOUS MODE - No user feedback required**

All prospects scoring **60 points or higher** are automatically:
1. Marked as APPROVED
2. Added to `linkedin-core/shared/logs/icp-prospects.md`
3. Logged to `web-discovered-prospects.md`

**Do NOT:**
- Ask user for feedback
- Wait for approval
- Present options to choose from

**Just execute and report results.**

---

## Phase 5b: Post-Scan Rejection (User-Triggered Learning)

**Learning happens when the user REJECTS a prospect with reasoning.**

### Rejection Trigger Phrases

```
- "reject #129 - too large"
- "remove prospect [Name] - not SME"
- "reject [Name] because [reason]"
- "bad ICP: [Name] - [reason]"
```

### Rejection Workflow

When user rejects a previously auto-approved prospect:

1. **Parse rejection:**
   - Extract prospect name/number
   - Extract rejection reason

2. **Update icp-prospects.md:**
   - Find the prospect row
   - Add to Notes: "REJECTED [date]: [reason]"
   - Change Classification: PROSPECT → REJECTED

3. **Update icp-learning-log.md:**
   - Add to "Learned Negative Signals" table
   - Increment frequency if pattern already exists
   - Add rejection reason to User Feedback Patterns

4. **Apply future scoring adjustment:**
   - If same rejection reason appears 3+ times → Auto-create score penalty
   - Example: 3x "too large" for >500 employees → Add "-15 for >500 employees" to scoring

5. **Confirm to user:**
   ```
   ✓ Rejected: [Name] - [Reason]
   ✓ Learning updated: [Pattern added/incremented]
   ✓ Future scans will penalize: [Specific adjustment]
   ```

### Rejection Reason Categories

Standard rejection reasons (for consistent learning):

| Short Code | Full Meaning | Score Penalty (after 3x) |
|------------|--------------|--------------------------|
| `too large` | Company >200 employees | -15 to Company Size |
| `too small` | Company <10 employees | -10 to Company Size |
| `not ASEAN` | Outside {{CLIENT_TARGET_GEO}} geography | -20 to Geography |
| `not decision-maker` | Not C-suite/Director level | -15 to Role Match |
| `seller not buyer` | Service provider/consultant | -20 to Industry Match |
| `enterprise` | Enterprise/MNC, not SME | -15 to Company Size |
| `stale` | News/source >6 months old | -10 to Pain Signal |
| `duplicate` | Already in pipeline | Skip (no penalty) |

### Example Rejection

```
User: "reject #135 - too large, SBF is an association not SME"

Codex:
✓ Rejected: Kok Ping Soon (Singapore Business Federation)
✓ Reason logged: "too large, association not SME"
✓ Learning updated:
  - Added "association" to negative signals (1/3 to become pattern)
  - Added "federation" to negative signals (1/3 to become pattern)
  - "too large" incremented to 2/3 frequency
✓ icp-prospects.md updated: Row #135 marked REJECTED
```

---

## Phase 6: Learning Engine (Rejection-Based)

**Learning is driven ONLY by user rejection feedback.**

Since all 60+ prospects are auto-approved, the system learns exclusively from:
- User rejections with reasoning (Phase 5b)
- Pattern detection across multiple rejections

### Pattern Detection Algorithm

```
FOR each rejected prospect (user-triggered via Phase 5b):
  - Extract: role, industry, company size, source type, specific signals
  - Count frequency of rejection reasons
  - IF rejection_reason appears 3+ times → Add to Learned Negative Signals WITH score penalty

FOR search effectiveness:
  - Track which search queries yielded rejected prospects
  - If query yields 3+ rejections → DEMOTE query (reduce usage)
  - If query yields 0 rejections over 3 scans → BOOST query (prioritize)
```

**Note:** Positive signals are NOT learned since everything is auto-approved. The system improves by learning what to AVOID.

### ICP Profile Updates

When negative patterns emerge (3+ similar rejections), update `linkedin-core/references/icp-profile.md`:

**Auto-updates (from rejections):**
- Add keywords from rejected companies to exclusion list
- Adjust company size ceiling based on "too large" rejections
- Reduce industry priority based on consistent rejection

**Suggested updates (require user approval):**
- Removing industries with consistent rejection
- Changing company size range
- Adding new exclusion rules

## Phase 7: Logging

### Save to web-discovered-prospects.md

```markdown
## [Date] Scan Results

**Scan Parameters:**
- Search queries used: [list]
- Sources checked: [list]
- Total found: [X]
- Passed ICP filter: [Y]

**Prospects:**

| # | Name | Role | Company | Location | Score | Verdict | Notes |
|---|------|------|---------|----------|-------|---------|-------|
| 1 | ... | ... | ... | ... | 85 | APPROVED | Added to master list |
| 2 | ... | ... | ... | ... | 72 | REJECTED | Too large (500+ employees) |
...

**Learning Updates:**
- [Any patterns detected]
- [Any ICP updates made]
```

### Update Master Prospect List

For APPROVED prospects, add to `linkedin-core/shared/logs/icp-prospects.md`:

```markdown
| # | Name | Date Found | Role | Company | Company URL | Location | Classification | Touches | Last Touch | Touch History | Connection Status | Profile URL | Email | Notes |
|---|------|------------|------|---------|-------------|----------|----------------|---------|------------|---------------|-------------------|-------------|-------|-------|
| [next#] | [Name] | [Today] | [Role] | [Company] | [URL] | [Location] | PROSPECT | 0 | - | - | none | TBD | [email or TBD] | Source: Web ICP Scan [Date] \| [Key signal] |
```

---

## ICP Learning Log Structure

**Location:** `web-icp-scanner/icp-learning-log.md`

**Learning is REJECTION-BASED only.** All 60+ prospects are auto-approved; learning happens when user rejects with reasoning.

```markdown
# ICP Learning Log

Last updated: [Date]
Total scans: [X]
Total prospects auto-approved: [Y]
Total rejections (user feedback): [Z]

## Learned Negative Signals (From User Rejections)

Signals from REJECTED prospects that trigger score penalties:

| Signal | Frequency | First Seen | Score Modifier | Rejection Reason |
|--------|-----------|------------|----------------|------------------|
| "Enterprise" in company name | 3/3 rejected | 15Jan | -15 | Too large |
| "Consulting firm" | 3/4 rejected | 18Jan | -20 | Service provider, not buyer |
| "Government agency" | 3/3 rejected | 20Jan | -20 | Not SME |
| "Association" | 1/3 | 02Feb | (pending) | Not SME target |

**Minimum frequency to become active pattern:** 3 occurrences

## Search Query Performance

| Query Template | Times Used | Auto-Approved | Rejected | Status |
|----------------|------------|---------------|----------|--------|
| "SME funding Singapore [industry]" | 10 | 7 | 3 | ACTIVE |
| "[industry] startup ASEAN" | 8 | 5 | 0 | BOOST |
| "top [industry] companies Singapore" | 6 | 2 | 4 | DEMOTE |

**Status Key:**
- `BOOST` - 0-1 rejections, prioritize in future scans
- `ACTIVE` - 2 rejections, keep using
- `DEMOTE` - 3+ rejections, reduce usage
- `RETIRE` - >50% rejection rate, stop using

## ICP Refinement History

| Date | Change Type | Before | After | Trigger (Rejection Pattern) |
|------|-------------|--------|-------|------------------------------|
| 28Jan | Removed industry | "Heavy manufacturing" | - | 3x "too large" rejections |
| 30Jan | Added exclusion | - | "Association/Federation" | 3x "not SME" rejections |

## User Rejection Patterns (Ranked by Frequency)

1. **Too large** - Company >200 employees → -15 Company Size
2. **Not ASEAN** - Outside {{CLIENT_TARGET_GEO}} geography → -20 Geography
3. **Seller not buyer** - Consulting/agency → -20 Industry Match
4. **Not decision-maker** - Manager level → -15 Role Match
5. **Enterprise** - MNC/corporate → -15 Company Size
```

---

## Execution Modes

### Mode 1: Full Scan (Default - AUTONOMOUS)

```
Trigger: "scan web for prospects"

1. Load ICP + Learning history
2. Execute 5 web searches
3. Filter to top 10 prospects (score 60+)
4. AUTO-APPROVE ALL qualifying prospects
5. Add ALL to icp-prospects.md (no user input)
6. Update learning log
7. Show summary report

⚠️ NO USER INTERACTION - Fully autonomous execution
```

### Mode 2: Quick Scan (AUTONOMOUS)

```
Trigger: "quick prospect scan"

1. Load ICP (skip learning history)
2. Execute 2 web searches (highest performing queries)
3. Filter to top 5 prospects (score 60+)
4. AUTO-APPROVE ALL qualifying prospects
5. Add ALL to icp-prospects.md
6. Show summary report

⚠️ NO USER INTERACTION - Fully autonomous execution
```

### Mode 3: Industry Focus (AUTONOMOUS)

```
Trigger: "scan for [industry] prospects"

1. Load ICP
2. Execute searches focused on specific industry
3. Filter to top 10 from that industry (score 60+)
4. AUTO-APPROVE ALL qualifying prospects
5. Add ALL to icp-prospects.md
6. Show summary report

⚠️ NO USER INTERACTION - Fully autonomous execution
```

### Mode 4: Learning Review

```
Trigger: "review icp learning"

1. Display current learned patterns
2. Show approval rate trends
3. Show search query performance
4. Suggest ICP profile updates
5. Get user approval for changes (only mode requiring input)
```

---

## Search Source Configuration

**Priority news sources (for press/funding news):**

```
- Tech in Asia (techinasia.com)
- e27 (e27.co)
- The Business Times (businesstimes.com.sg)
- The Edge Singapore (theedgesingapore.com)
- Digital News Asia (digitalnewsasia.com)
- Deal Street Asia (dealstreetasia.com)
- KrASIA (kr-asia.com)
```

**Priority directory sources:**

```
- Enterprise Singapore company directory
- Singapore Business Federation
- SME Centre Singapore
- Malaysia SME Corp
- ASEAN Business Advisory Council
```

**Priority event sources:**

```
- Singapore Week of Innovation and Technology (SWITCH)
- Singapore FinTech Festival
- TechInAsia Conference
- Echelon Asia Summit
- Wild Digital
```

---

## Deduplication Rules

**Before adding to output, check:**

1. **Name match** - Already in icp-prospects.md?
2. **Company match** - Different person, same company already tracked?
3. **Recent scan** - Found in last 7 days of web scans?

**If duplicate found:**
- Skip silently (don't count toward 10)
- Log in scan results: "Skipped [Name] - duplicate"

---

## Example Execution

```
User: "scan web for prospects"

Codex: Reading ICP profile and learning history...

**ICP Loaded:**
- Target: SME Founders/CEOs, Operations Directors, Finance Directors
- Industries: Accounting, E-commerce, Manufacturing, Professional Services
- Geography: Singapore, Malaysia (ASEAN)
- Size: 10-200 employees

**Learned Patterns Applied:**
- Boosting: Series A companies (+5), "digital transformation" mentions (+3)
- Demoting: Consulting firms (-10), Government agencies (-15)

**Executing web searches...**

1. "SME funding Singapore accounting fintech 2026"
2. "e-commerce company expansion Malaysia ASEAN 2026"
3. "digital transformation award winner Singapore SME"
4. "startup founder CEO interview Singapore operations"
5. "enterprise singapore sme awards 2026"

**Found 47 potential prospects. Filtering...**

**Top 10 ICP Matches:**

[Presents 10 prospects with full details and scoring]

---

After user feedback:

**Feedback Summary:**
- APPROVED: 6 prospects
- REJECTED: 3 prospects (2 too large, 1 wrong geography)
- MAYBE: 1 prospect

**Learning Updates:**
- Detected pattern: 2 rejections for ">200 employees" → Strengthening company size filter
- New positive signal: "recently hired COO" appeared in 3/6 approved

**Added 6 prospects to master list.**

Next scan recommendations:
- Try: "SME COO hire Singapore 2026" (new positive signal)
- Avoid: "[source] top enterprises" queries (yielded oversized companies)
```

---

## Integration Points

### Connects to:
- `linkedin-icp-finder` - Handoff approved prospects for LinkedIn search & warming
- `linkedin-icp-warmer` - Feed approved prospects into engagement pipeline
- `linkedin-connect-timer` - Track web-discovered prospects in connection timing

### Outputs to:
- `linkedin-core/shared/logs/icp-prospects.md` - Master prospect list
- `web-icp-scanner/web-discovered-prospects.md` - Daily scan logs
- `web-icp-scanner/icp-learning-log.md` - Learning patterns
- `linkedin-core/references/icp-profile.md` - ICP criteria updates (with approval)

---

## Maintenance

### Weekly Tasks
- Review learning log for pattern accuracy
- Prune outdated search queries
- Check approval rate trends

### Monthly Tasks
- Full ICP profile review based on learning
- Refresh news source effectiveness
- Archive old scan logs (>30 days)

---

*Skill created: 02 February 2026*
*Version: 1.0*
