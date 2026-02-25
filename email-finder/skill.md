---
name: email-finder
description: Find business emails for ICP prospects using a free-first workflow (web search and LinkedIn Contact Info) before paid enrichment providers. Use when users request batch email enrichment for stale pending connections or ad-hoc lookup of a specific prospect's work email.
---

# Email Finder

Find business emails for ICP prospects where connection requests have been pending 7+ days. Uses a **web search first** approach (free) before falling back to paid API providers (Apollo, Hunter, Snov.io, GetProspect, Prospeo — 275 credits/month total). LinkedIn Contact Info is used for connected contacts.

## Trigger Phrases

- "find emails" / "enrich emails" / "email lookup" (batch mode)
- "email enrichment" / "get prospect emails" (batch mode)
- "find email for [name]" / "email for [name] at [company]" (ad-hoc mode)
- "look up email [name]" / "get email [name]" (ad-hoc mode)

## When to Use

**Batch mode** — run when:
- Connection requests have been pending for 7+ days with no acceptance
- You need an alternative outreach channel (email) for unresponsive prospects
- After Evening Block to batch-enrich any newly eligible prospects

**Ad-hoc mode** — run when:
- User asks for a specific person's email by name
- Quick one-off lookup needed (person does NOT need to be in icp-prospects.md)
- Pre-meeting research — need contact email before a call

## Filter Logic

Only enrich prospects matching ALL of these:
1. **Connection Status = `pending`**
2. **Touch History contains `connect_sent`**
3. **Last Touch date is 7+ days ago** (parse DDMon format, e.g., "23Jan")
4. **Email = `-`** (not already populated)

### How to Calculate Days Since Connect Sent

1. Parse the `Last Touch` column (DDMon format: "23Jan", "01Feb")
2. Calculate days between Last Touch date and today
3. If > 7 days, prospect is eligible

## Ad-Hoc Workflow

When the user asks for a specific person's email (e.g., "find email for John Smith at Acme Corp"):

1. Extract **name** (required), **company**, **LinkedIn URL**, and **domain** from the request
2. **Web Search First (FREE)** — search the internet before using API credits:
   - Search `"[Full Name]" "[Company]" email`
   - Search `"[Full Name]" "[Company]" contact` with site filters (rocketreach.co, contactout.com, signalhire.com, zoominfo.com)
   - Search `"[Company]" website domain email` to find the company domain
   - If a likely email is found, verify the domain matches the company before accepting
   - **If found:** Display result, update records, SKIP the API waterfall entirely
3. **API Waterfall (ONLY if web search found nothing)** — call `crm_find_email` with name, company, linkedin_url, domain
4. Display the result — email found or "not found" with tips
5. If `add_to_prospects: true`, update `icp-prospects.md` Email column

**Examples:**
- `"find email for Sarah Chen at Grab"` → name: "Sarah Chen", company: "Grab"
- `"email lookup David Tan https://linkedin.com/in/davidtan"` → name: "David Tan", linkedin_url provided
- `"get email for john@acme — his domain is acme.io"` → name: "John", domain: "acme.io"

## Batch Workflow

### Step 0: Filter Eligible Prospects

Read `shared/logs/icp-prospects.md` and filter using the criteria above. Display the filtered list for confirmation before proceeding.

### Step 1: Check Connection Status (Free)

For each eligible prospect:
- Visit their LinkedIn profile using browser automation
- Check the action button: "Message" = connected, "Connect"/"Follow" = none, "Pending" = pending
- **If now connected:** Use LinkedIn Contact Info section to get email (free, no API credits needed)
- Update Connection Status in `icp-prospects.md`

### Step 2: Web Search (FREE — run before API calls)

For each remaining prospect still pending with no email, search the internet first:

1. **Run parallel web searches per prospect:**
   - `"[Full Name]" "[Company]" email`
   - `"[Full Name]" "[Company]" contact site:rocketreach.co OR site:contactout.com OR site:signalhire.com OR site:zoominfo.com`
   - `"[Company]" website domain` (to find the company email domain)
2. **Accept criteria:** Email domain must match the company (e.g., `@lexasure.com` for Lexasure Financial Group)
3. **If found:** Record the email with source "Web Search", remove prospect from the API batch
4. **If not found:** Prospect stays in the batch for Step 3

This step costs zero API credits and often finds emails for well-known companies.

### Step 3: API Enrichment Waterfall (via `crm_find_emails`) — ONLY for remaining prospects

For prospects where web search found nothing, the tool runs a 5-provider waterfall — each miss falls through to the next:

| Order | Provider | Free Credits | Match By | Accept If |
|-------|----------|-------------|----------|-----------|
| 1 | Apollo | 50/month | name + company + LinkedIn URL | `email_status: "verified"` |
| 2 | Hunter | 25/month | name + domain | `confidence >= 80%` |
| 3 | Snov.io | 50/month | name + domain (async) | `smtp_status: "valid"` |
| 4 | GetProspect | 50/month | full name + company/domain | status not invalid/unknown |
| 5 | Prospeo | 100/month | LinkedIn URL or name + company | `status: "VERIFIED"` |

**Total free capacity:** 275 lookups/month

### Step 4: Update Records (for emails found in Steps 1-3)

For each email found:
- Update `icp-prospects.md` Email column
- Sync to HubSpot via `crm_sync_prospect` or direct email property update
- Log the source (LinkedIn/Apollo/Hunter) in Notes column

### Step 5: Summary Report

Output a summary:
```
## Email Enrichment Results

| Prospect | Source | Email | Status |
|----------|--------|-------|--------|
| Name     | Apollo | email@example.com | verified |
| Name     | Hunter | email@example.com | confidence: 85% |
| Name     | -      | -     | not found |

**Credits Used:** Apollo: X/50 | Hunter: Y/25
**Found:** N emails | **Missed:** M prospects
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `crm_find_email` | **Ad-hoc** single-person email lookup by name + company/domain/LinkedIn URL |
| `crm_find_emails` | **Batch** email lookup for pending prospects (7+ days, no email) |
| `crm_pull_emails` | Reverse sync: pull emails from HubSpot back to icp-prospects.md |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| `APOLLO_API_KEY` not set | Skip Apollo, use Hunter only |
| `HUNTER_API_KEY` not set | Skip Hunter, use Apollo only |
| Both keys missing | Error with setup instructions |
| No LinkedIn URL ("TBD") | Try by name + company only |
| Unverified email (Apollo) | Skip — don't store unverified data |
| Low confidence email (Hunter < 80) | Skip — don't store low-confidence data |
| Email already populated | Skip prospect entirely |
| Credits exhausted mid-batch | Stop, report progress so far |
| Connection accepted since last check | Use LinkedIn Contact Info (free) |
| Company domain unknown | Try extracting from LinkedIn company page URL or Notes |

## Setup

### API Keys

Add to `.mcp.json` under `hubspot-crm` env (all optional, use any combination):

```json
"APOLLO_API_KEY": "...",
"HUNTER_API_KEY": "...",
"SNOV_CLIENT_ID": "...",
"SNOV_CLIENT_SECRET": "...",
"GETPROSPECT_API_KEY": "...",
"PROSPEO_API_KEY": "..."
```

### Getting API Keys

| Provider | Free Credits | Where to Get Key |
|----------|-------------|------------------|
| Apollo.io | 50/month | apollo.io > Settings > API Keys |
| Hunter.io | 25/month | hunter.io > API tab |
| Snov.io | 50/month | snov.io > Account Settings (Client ID + Secret) |
| GetProspect | 50/month | getprospect.com > API |
| Prospeo | 100/month | prospeo.io > Dashboard > API |

## Dependencies

- `crm-integration/hubspot_mcp.py` — MCP server with `crm_find_emails` + `crm_pull_emails` tools
- `shared/logs/icp-prospects.md` — Source of truth for prospect data
- Browser automation (Chrome) — For Step 1 LinkedIn connection status checks
