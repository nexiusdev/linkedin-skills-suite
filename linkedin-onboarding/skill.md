---
name: linkedin-onboarding
description: |
  First-time setup for LinkedIn outreach skills. Run this BEFORE using any other LinkedIn skills to customize them for your business. Use when user says "setup linkedin", "onboard linkedin", "configure linkedin skills", "linkedin first time setup", or when a new user wants to personalize the LinkedIn skill suite for their own ICP, industry, and geography. Collects business positioning, target customer profile, geographic focus, and content pillars to generate personalized reference files.
---

# LinkedIn Onboarding Skill

First-time setup that customizes all LinkedIn outreach skills for a new user's specific business.

## What This Skill Does

1. Collects business and positioning information through guided questions
2. Optionally analyzes user's LinkedIn profile for ICP extraction
3. Generates personalized reference files:
   - `references/icp-profile.md` - Target customer criteria
   - `references/contact-classification.md` - How to classify contacts
   - `references/connect-request.md` - Connection request templates
   - `references/saved-asset.md` - Save-worthy content examples
   - `references/linkedin-strategy.md` - Personalized strategy doc
4. Updates skill files that reference user-specific content

## Onboarding Flow

### Phase 1: Business Foundation

Ask these questions (use AskUserQuestion tool for structured collection):

**Q1: Business Identity**
- "What is your company/business name?"
- "What is your LinkedIn profile URL?" (optional but recommended)

**Q2: Core Positioning**
- "In one sentence, what do you help your customers achieve?"
- "What is your primary domain/niche?" (e.g., "AI automation", "B2B SaaS", "financial consulting")

**Q3: Target Market**
- "Who is your ideal customer?" (e.g., "SME founders", "enterprise CTOs", "marketing agencies")
- "What company size do you target?" (e.g., "10-200 employees", "500+ employees", "solopreneurs")

### Phase 2: ICP Details

**Q4: ICP Example Profiles (RECOMMENDED)**
Ask: "Please provide 2-5 LinkedIn profile URLs of your ideal customers (people who match your ICP perfectly)."
- **Minimum:** 2 profile URLs
- **Maximum:** 5 profile URLs
- **Purpose:** These profiles will be analyzed to extract:
  - Common job titles/roles
  - Industries they work in
  - Company sizes
  - Pain points from their posts
  - Geographic locations
- **If user has no URLs:** Skip and proceed to manual ICP definition (Q5-Q8)
- **If user provides URLs:**
  1. Validate all URLs are LinkedIn profiles (format: linkedin.com/in/[username])
  2. Store for analysis after Q12
  3. Use extracted data to pre-fill/validate Q5-Q8 answers

**Q5: Target Roles (Decision-Makers)**
Collect 3-5 job titles of people who can buy/decide:
- Examples: CEO, Founder, CFO, Operations Director, Head of Marketing
- If Q4 provided: Cross-reference with roles from example profiles

**Q6: Target Roles (Influencers)**
Collect 2-4 job titles of people who influence the decision:
- Examples: Operations Manager, IT Manager, Business Analyst
- If Q4 provided: Look for secondary roles connected to example profiles

**Q7: Target Industries**
Collect primary (3-4) and adjacent (2-3) industries:
- Primary: Where most of your customers come from
- Adjacent: Related industries that could benefit
- If Q4 provided: Validate against industries from example profiles

**Q8: Geographic Focus**
- "What regions do you target?" (can be global, specific countries, or regions)
- If specific: List the countries/regions (e.g., "US, UK, Canada" or "APAC" or "Global")
- IMPORTANT: This becomes the geography filter in linkedin-icp-finder
- If Q4 provided: Cross-check with locations from example profiles

**Q9: Pain Keywords**
- "What problems/pain points do your customers commonly mention?"
- Collect 8-12 keywords (e.g., "manual processes", "scaling issues", "data silos")
- If Q4 provided: Supplement with pain points extracted from example profiles' posts

### Phase 3: Content & Engagement

**Q10: Content Pillars**
- "What are your 2-3 main topics you post about on LinkedIn?"
- These become profile alignment signals

**Q11: Peer Signals**
- "What keywords identify fellow builders/peers in your space?"
- Tools, technologies, communities they follow
- Examples: "React developers", "HubSpot users", "Y Combinator founders"

**Q12: Save-Worthy Assets**
- "What practical assets can you create that your audience would save?"
- Examples: templates, checklists, frameworks, code snippets, calculators
- Collect 2-3 asset types with descriptions

### Phase 4: Timezone & Preferences

**Q13: Primary Timezone**
- "What timezone are you in?" (for optimal posting times)
- This adjusts the daily planner time blocks

### Phase 5: Account & Pages Configuration

**Q14: LinkedIn Username**
- "What is your LinkedIn username/profile path?" (e.g., "johndoe" from linkedin.com/in/johndoe)
- This is used by linkedin-connect-timer for URL generation
- REQUIRED for full skill suite functionality
- If user provides full URL, extract just the username portion

**Q15: Company Pages (Optional)**
- "Do you manage any LinkedIn company pages? If yes, provide details for each."
- For each page, collect:
  - Page name (e.g., "Acme Corp")
  - LinkedIn numeric ID (found in page admin URL)
  - URL slug (e.g., "acme-corp" from linkedin.com/company/acme-corp/)
  - Focus area (e.g., "Product updates and thought leadership")
  - Content pillars (2-3 topics, e.g., "Industry insights, product demos, customer stories")
- Maximum 5 pages
- If user doesn't manage pages: Skip and note in config

**Q16: Account Type**
- "What LinkedIn account type do you have?"
- Options: FREE, PREMIUM_CAREER, PREMIUM_BUSINESS, SALES_NAVIGATOR
- This determines daily limits and available features
- If unsure: Default to FREE (most conservative limits)

## Output Generation

After collecting all information (Q1-Q16), follow these steps:

### Step 0: Analyze ICP Example Profiles (if Q4 provided)

If user provided LinkedIn profile URLs in Q4:

1. **Visit each profile** (2-5 profiles)
2. **Extract and analyze:**
   - Job title/role
   - Company name and size (from company page)
   - Industry
   - Location/geography
   - Recent posts (scan for pain points, challenges, topics discussed)
   - Headline keywords
3. **Aggregate findings:**
   - Most common roles across profiles
   - Most common industries
   - Geographic distribution
   - Recurring pain keywords from their posts
   - Company size patterns
4. **Use extracted data to:**
   - Validate user's answers to Q5-Q9
   - Fill gaps if user was unsure on any questions
   - Enrich ICP profile with real-world examples
   - Add these profiles as seed prospects to `shared/logs/icp-prospects.md`

**Output from analysis:**
```
ICP Example Profiles Analysis:

Profiles analyzed:
1. [Name] - [Role] at [Company] ([Size], [Industry], [Location])
2. [Name] - [Role] at [Company] ([Size], [Industry], [Location])
...

Common patterns:
- Roles: [Most common job titles]
- Industries: [Most common industries]
- Company sizes: [Range observed]
- Locations: [Geographic distribution]
- Pain keywords: [Extracted from posts - 5-8 keywords]

Validation:
✓ User's Q5 answer matches [X]% of example profiles
✓ User's Q7 answer covers [X]% of example geographies
⚠ Consider adding: [Suggestions based on profiles]
```

---

After profile analysis (or if Q4 skipped), generate these files:

### 1. references/icp-profile.md

```markdown
# ICP Profile - [Company Name]

## Profile Positioning Summary
[One sentence positioning from Q2]

## ICP Example Profiles
[If Q4 provided - list the 2-5 example profile URLs with names and roles]

## Target Job Roles

### Primary (Decision-Makers)
[From Q5 - formatted as table with "Why They Care" column]
[If Q4 provided - note which roles were validated by example profiles]

### Secondary (Influencers)
[From Q6 - formatted as table with "Why They Champion" column]

## Target Industries

### Primary
[From Q7 primary list]
[If Q4 provided - note which industries appeared in example profiles]

### Adjacent
[From Q7 adjacent list]

## Target Company Profile
- **Size:** [From Q3]
- **Stage:** [Infer from size/market]
- **Geography:** [From Q8]
- **Tech Maturity:** [Infer or ask]

## ICP Screening Filters

### Role Filter
[Comma-separated list of all target roles from Q5 + Q6]

### Industry Filter
[Comma-separated list of all industries from Q7]

### Company Size
[From Q3]

### Pain Keywords
[From Q9 + keywords extracted from Q4 example profiles if provided]

## Posts to Engage
Look for posts discussing:
[Generate 5-6 bullet points based on pain keywords and domain]

## Search Keywords
[Generate 6-8 search terms based on domain and pain keywords]
```

### 2. references/contact-classification.md

Use the template from `references/templates/contact-classification-template.md`, replacing:
- PEER signals with Q11 answers
- PROSPECT criteria with Q5, Q6, Q7, Q8 answers
- Geographic focus from Q8
- If Q4 provided: Add note about example profile characteristics

### 3. references/connect-request.md

Generate connection request templates using:
- Company name from Q1
- Domain/niche from Q2
- Asset types from Q12
- If Q4 provided: Reference example profiles as validation

### 4. references/saved-asset.md

Generate save-worthy asset guidance using:
- Asset types from Q12
- Domain context from Q2
- Pain points from Q9 (+ Q4 extracted keywords if provided)

### 5. Update linkedin-icp-finder geography filter

Replace the geography filter with the user's Q8 geography:
- If "Global": Remove geography filter entirely
- If specific countries: Update the country list
- If region: Update to region check
- Update `linkedin-icp-finder/references/icp-profile.md` with the same data

### 6. shared/linkedin-account-config.md

Update the account configuration file:

```markdown
# LinkedIn Account Configuration

## Account Status

| Setting | Value | Last Updated |
|---------|-------|--------------|
| **LinkedIn Username** | [From Q14] | [Today's date] |
| **Account Type** | [From Q16] | [Today's date] |
| **Has Sales Navigator** | [Yes if Q16 = SALES_NAVIGATOR, No otherwise] | [Today's date] |
| **InMail Credits** | [Based on Q16: FREE=0, PREMIUM_CAREER=5, PREMIUM_BUSINESS=15, SALES_NAVIGATOR=50] | [Today's date] |
```

Also update the local copy at `linkedin-daily-planner/shared/linkedin-account-config.md`.

### 7. references/company-pages-config.md (if Q15 provided)

If the user manages company pages, generate:

```markdown
# Company Pages Configuration

| Page | LinkedIn ID | URL Slug | Focus | Content Pillars |
|------|-------------|----------|-------|-----------------|
| **[Page 1 Name]** | [ID] | [slug] | [Focus] | [Pillars] |
| **[Page 2 Name]** | [ID] | [slug] | [Focus] | [Pillars] |
...

## Admin URLs
- [Page 1]: linkedin.com/company/[ID]/admin/
- [Page 2]: linkedin.com/company/[ID]/admin/
...
```

If user does not manage pages, create the file with:
```markdown
# Company Pages Configuration

> No company pages configured. Update this file if you start managing LinkedIn company pages.
```

### 8. references/linkedin-strategy.md

Generate the full LinkedIn strategy document incorporating:
- Company name from Q1
- Domain/niche from Q2
- Target market from Q3
- Content pillars from Q10
- Timezone from Q13
- Account type features from Q16
- Include the full 360Brew compliance strategy, algorithm training guide, engagement loop, and pipeline management sections

## Post-Onboarding Checklist

After generating files, display:

```
Onboarding complete! Your LinkedIn skills are now customized for [Company Name].

Files created/updated:
- references/icp-profile.md
- references/contact-classification.md
- references/connect-request.md
- references/saved-asset.md
- references/linkedin-strategy.md
- references/company-pages-config.md [if Q15 provided]
- shared/linkedin-account-config.md
- linkedin-icp-finder/references/icp-profile.md (local copy)
- linkedin-daily-planner/shared/linkedin-account-config.md (local copy)

Account configured:
- LinkedIn Username: [From Q14]
- Account Type: [From Q16]
- Company Pages: [Count from Q15, or "None configured"]
- Timezone: [From Q13]

Next steps:
1. Review the generated files and adjust any details
2. Run "start linkedin" to begin your first session
3. Use "linkedin-profile-icp" to further refine your ICP if needed

Optional profile optimization:
- Update your LinkedIn headline to include: [suggested headline keywords]
- Add these skills to your profile: [suggested skills from domain]
```

## Handling Existing Users

If reference files already exist:
1. Ask: "I found existing LinkedIn configuration. Do you want to (A) Start fresh, (B) Update specific sections, or (C) Cancel?"
2. If Update: Show which sections they can modify
3. Preserve any manual customizations when possible

## Error Handling

- If user skips optional questions: Use sensible defaults or mark as "TO BE CONFIGURED"
- If LinkedIn profile URL provided: Offer to run linkedin-profile-icp for auto-extraction
- If user seems unsure: Provide examples from common industries
