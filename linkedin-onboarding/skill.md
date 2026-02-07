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

**Q4: Target Roles (Decision-Makers)**
Collect 3-5 job titles of people who can buy/decide:
- Examples: CEO, Founder, CFO, Operations Director, Head of Marketing

**Q5: Target Roles (Influencers)**
Collect 2-4 job titles of people who influence the decision:
- Examples: Operations Manager, IT Manager, Business Analyst

**Q6: Target Industries**
Collect primary (3-4) and adjacent (2-3) industries:
- Primary: Where most of your customers come from
- Adjacent: Related industries that could benefit

**Q7: Geographic Focus**
- "What regions do you target?" (can be global, specific countries, or regions)
- If specific: List the countries/regions (e.g., "US, UK, Canada" or "APAC" or "Global")
- IMPORTANT: This becomes the geography filter in linkedin-icp-finder

**Q8: Pain Keywords**
- "What problems/pain points do your customers commonly mention?"
- Collect 8-12 keywords (e.g., "manual processes", "scaling issues", "data silos")

### Phase 3: Content & Engagement

**Q9: Content Pillars**
- "What are your 2-3 main topics you post about on LinkedIn?"
- These become profile alignment signals

**Q10: Peer Signals**
- "What keywords identify fellow builders/peers in your space?"
- Tools, technologies, communities they follow
- Examples: "React developers", "HubSpot users", "Y Combinator founders"

**Q11: Save-Worthy Assets**
- "What practical assets can you create that your audience would save?"
- Examples: templates, checklists, frameworks, code snippets, calculators
- Collect 2-3 asset types with descriptions

### Phase 4: Timezone & Preferences

**Q12: Primary Timezone**
- "What timezone are you in?" (for optimal posting times)
- This adjusts the daily planner time blocks

## Output Generation

After collecting all information, generate these files:

### 1. references/icp-profile.md

```markdown
# ICP Profile - [Company Name]

## Profile Positioning Summary
[One sentence positioning from Q2]

## Target Job Roles

### Primary (Decision-Makers)
[From Q4 - formatted as table with "Why They Care" column]

### Secondary (Influencers)
[From Q5 - formatted as table with "Why They Champion" column]

## Target Industries

### Primary
[From Q6 primary list]

### Adjacent
[From Q6 adjacent list]

## Target Company Profile
- **Size:** [From Q3]
- **Stage:** [Infer from size/market]
- **Geography:** [From Q7]
- **Tech Maturity:** [Infer or ask]

## ICP Screening Filters

### Role Filter
[Comma-separated list of all target roles]

### Industry Filter
[Comma-separated list of all industries]

### Company Size
[From Q3]

### Pain Keywords
[From Q8]

## Posts to Engage
Look for posts discussing:
[Generate 5-6 bullet points based on pain keywords and domain]

## Search Keywords
[Generate 6-8 search terms based on domain and pain keywords]
```

### 2. references/contact-classification.md

Use the template from `references/templates/contact-classification-template.md`, replacing:
- PEER signals with Q10 answers
- PROSPECT criteria with Q4, Q5, Q6, Q7 answers
- Geographic focus from Q7

### 3. references/connect-request.md

Generate connection request templates using:
- Company name from Q1
- Domain/niche from Q2
- Asset types from Q11

### 4. references/saved-asset.md

Generate save-worthy asset guidance using:
- Asset types from Q11
- Domain context from Q2
- Pain points from Q8

### 5. Update linkedin-icp-finder geography filter

Replace the ASEAN-5 filter with the user's Q7 geography:
- If "Global": Remove geography filter entirely
- If specific countries: Update the country list
- If region: Update to region check

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
- linkedin-icp-finder/references/icp-profile.md (symlinked)

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
