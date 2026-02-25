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

### Phase 5: Integrations & API Keys

Present all integration groups upfront so the client can decide what to set up now vs later.

Ask: "Which integrations do you want to set up now?" using AskUserQuestion (multiSelect: true):

| Integration | What It Enables | Free Tier |
|------------|-----------------|-----------|
| Google Sheets CRM | Lightweight contact tracking via spreadsheet | Free (Google account) |
| HubSpot CRM | Full pipeline tracking, contact sync, deal stages | Free CRM |
| Email Enrichment | Find emails for unresponsive prospects (5 providers) | 275 lookups/month |

Then collect keys ONLY for selected groups, in the order below.

**CRM choice:** Google Sheets and HubSpot are alternatives — client picks one (or both). Google Sheets is simpler (no account setup beyond Google), HubSpot is more powerful (deal stages, activity timeline, pipeline reporting).

---

#### 5A: Google Sheets CRM Setup (Lightweight Option)

**Q13a: Google Sheets CRM**

Ask: "Do you want to use Google Sheets as a lightweight CRM for contact tracking? (Just needs a Google account — no extra signups.)"

If yes, guide the client through Google Cloud Service Account setup:

**Step 1: Create a Google Cloud Service Account**

| Step | Action |
|------|--------|
| 1 | Go to console.cloud.google.com > Create or select a project |
| 2 | IAM & Admin > Service Accounts > Create Service Account |
| 3 | Name: `mcp-gsheets`, click Create |
| 4 | Skip optional permissions, click Done |
| 5 | Click the new service account > Keys > Add Key > Create new key > JSON |
| 6 | Save the downloaded JSON file somewhere safe (e.g., `~/.config/mcp-gdrive/gsheets-service-account.json`) |

**Step 2: Enable Google Sheets API**

| Step | Action |
|------|--------|
| 1 | In Cloud Console > APIs & Services > Library |
| 2 | Search "Google Sheets API" > Enable it |

**Step 3: Register MCP server**

Run in terminal:
```bash
claude mcp add google-sheets -s user -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/gsheets-service-account.json -e GOOGLE_PROJECT_ID=your-project-id -- npx -y mcp-gsheets@latest
```

Replace `/path/to/gsheets-service-account.json` with the actual path to the downloaded JSON key, and `your-project-id` with the Google Cloud project ID.

**Step 4: Share spreadsheets with the service account**

The service account email (e.g., `mcp-gsheets@your-project.iam.gserviceaccount.com`) needs **Editor** access on any spreadsheet it reads/writes. Share the prospect tracking spreadsheet with this email.

**Verification:** After setup, test by creating a spreadsheet via the MCP tool. If it succeeds, Google Sheets CRM is ready.

If skipped: Prospect tracking still works via `icp-prospects.md` (local markdown file).

---

#### 5A-alt: HubSpot CRM Setup (Full-Featured Option)

**Q13b: HubSpot CRM**

Ask: "Do you have a HubSpot account? The free CRM tier is enough."

If yes, collect:

| Key | Where to Get It |
|-----|-----------------|
| `HUBSPOT_API_KEY` | HubSpot > Settings > Integrations > Private Apps > Create app > Copy access token |
| `HUBSPOT_PORTAL_ID` | HubSpot > Settings > Account > Hub ID (top-right corner) |

**Required HubSpot Private App scopes:**
- `crm.objects.contacts.read` + `.write`
- `crm.objects.companies.read` + `.write`
- `crm.objects.deals.read` + `.write`
- `crm.schemas.contacts.read` + `.write`

Write to `.mcp.json` under `hubspot-crm.env`:
```json
"HUBSPOT_API_KEY": "pat-na1-xxxxx",
"HUBSPOT_PORTAL_ID": "12345678"
```

After writing, run `crm_setup_properties` to create custom HubSpot properties (idempotent, safe to re-run).

If skipped: CRM sync and email-to-HubSpot features will be unavailable. Prospect tracking still works via `icp-prospects.md`.

---

#### 5B: Email Enrichment Setup (Optional)

**Q14: Email Enrichment**

Ask: "Do you want to set up email enrichment for prospects who don't accept connection requests? (Free tier covers 275 lookups/month across 5 providers)"

If yes, present provider options using AskUserQuestion (multiSelect: true):

| Provider | Free Credits | What to Sign Up |
|----------|-------------|-----------------|
| Apollo.io | 50/month | apollo.io > Settings > API Keys |
| Hunter.io | 25/month | hunter.io > API tab |
| Snov.io | 50/month | snov.io > Account Settings (Client ID + Secret) |
| GetProspect | 50/month | getprospect.com > API |
| Prospeo | 100/month | prospeo.io > Dashboard > API |

For each selected provider, collect the API key(s) using AskUserQuestion.

**Snov.io requires TWO values:** Client ID and Client Secret (both from Account Settings).

Write to `.mcp.json` under `hubspot-crm.env`:
```json
"APOLLO_API_KEY": "...",
"HUNTER_API_KEY": "...",
"SNOV_CLIENT_ID": "...",
"SNOV_CLIENT_SECRET": "...",
"GETPROSPECT_API_KEY": "...",
"PROSPEO_API_KEY": "..."
```

**Validation step:** After writing keys, run the validation script to confirm each key works:

```bash
python "C:\Users\wdqia\linkedin-skills-suite\email-finder\validate-keys.py"
```

This tests each configured provider with a known lookup and reports pass/fail. Display the results:

```
Email Enrichment Setup Results:
- Apollo: PASS (50 credits/month)
- Hunter: PASS (25 credits/month)
- Snov.io: PASS (50 credits/month)
- GetProspect: FAIL — Invalid API key
- Prospeo: PASS (100 credits/month)

Total monthly capacity: 225 lookups/month (4 providers active)

Tip: Fix GetProspect key later via .mcp.json, or skip it — the waterfall
handles missing providers gracefully.
```

If skipped: Add a note to the post-onboarding checklist suggesting they set it up later with "find emails" when needed.

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

Integrations:

  Google Sheets CRM: [if configured]
  - Service account connected
  - Share prospect spreadsheets with: [service account email]
  [if skipped]
  - Not configured. Set up later with a Google Cloud Service Account.

  HubSpot CRM: [if configured]
  - Connected (Portal ID: [id])
  - Custom properties created via crm_setup_properties
  [if skipped]
  - Not configured. Run "setup hubspot" later.

  Email enrichment: [if configured]
  - [X] providers active ([total] lookups/month)
  - Run "find emails" to enrich pending prospects with no response after 7 days
  [if skipped]
  - Not configured. Run "find emails" later to set up when needed.

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
