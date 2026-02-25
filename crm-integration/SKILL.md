---
name: crm-integration
description: Sync LinkedIn prospect pipeline data with HubSpot CRM, including contact/company/deal upserts, pipeline retrieval, activity logging, and optional email enrichment or reverse email pull. Use when users ask to set up HubSpot CRM integration, run CRM sync, check pipeline status, log outreach activity, or enrich prospect emails.
---

# HubSpot CRM Integration

Sync LinkedIn prospect pipeline data to HubSpot CRM. One-way auto-sync from `icp-prospects.md` to HubSpot contacts, companies, and deals.

## Trigger Phrases

- "sync to crm" / "crm sync" — runs `crm_sync_all`
- "setup hubspot" / "setup crm" — runs `crm_setup_properties`
- "crm pipeline" / "pipeline summary" — runs `crm_get_pipeline`
- "log activity to crm" — runs `crm_log_activity`
- "lookup in crm" / "crm contact" — runs `crm_get_contact`
- "find emails" / "enrich emails" / "email lookup" — runs `crm_find_emails`
- "pull emails" / "reverse sync emails" — runs `crm_pull_emails`

## Setup Instructions

### 1. Create HubSpot Private App

1. Go to **HubSpot > Settings > Integrations > Private Apps**
2. Click **Create a private app**
3. Name: `LinkedIn Pipeline Sync`
4. Under **Scopes**, enable:
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`
   - `crm.objects.companies.read`
   - `crm.objects.companies.write`
   - `crm.objects.deals.read`
   - `crm.objects.deals.write`
   - `crm.schemas.contacts.read`
   - `crm.schemas.contacts.write`
5. Click **Create app** and copy the access token

### 2. Set Environment Variables

Add to your MCP server config in `.mcp.json`:

```json
"hubspot-crm": {
  "command": "python",
  "args": ["C:\\Users\\melve\\.claude\\skills\\crm-integration\\hubspot_mcp.py"],
  "env": {
    "HUBSPOT_API_KEY": "pat-na1-xxxxx",
    "HUBSPOT_PORTAL_ID": "12345678",
    "APOLLO_API_KEY": "your-apollo-api-key",
    "HUNTER_API_KEY": "your-hunter-api-key",
    "SNOV_CLIENT_ID": "your-snov-client-id",
    "SNOV_CLIENT_SECRET": "your-snov-client-secret",
    "GETPROSPECT_API_KEY": "your-getprospect-api-key",
    "PROSPEO_API_KEY": "your-prospeo-api-key"
  }
}
```

### 2b. Get Email Enrichment API Keys

All are optional — the waterfall uses whichever keys are configured:

| Provider | Free Tier | Env Vars | Sign Up |
|----------|-----------|----------|---------|
| Apollo.io | 50/month | `APOLLO_API_KEY` | [apollo.io](https://app.apollo.io) > Settings > API Keys |
| Hunter.io | 25/month | `HUNTER_API_KEY` | [hunter.io](https://hunter.io) > API tab |
| Snov.io | 50/month | `SNOV_CLIENT_ID` + `SNOV_CLIENT_SECRET` | [snov.io](https://snov.io) > Account Settings |
| GetProspect | 50/month | `GETPROSPECT_API_KEY` | [getprospect.com](https://getprospect.com) > API |
| Prospeo | 100/month | `PROSPEO_API_KEY` | [prospeo.io](https://prospeo.io) > Dashboard > API |

**Waterfall order:** Apollo -> Hunter -> Snov.io -> GetProspect -> Prospeo
**Max combined free credits:** 275/month

### 3. Install Dependencies

```bash
pip install mcp httpx pydantic
```

### 4. Run Setup

Call `crm_setup_properties` once to create custom HubSpot properties. Safe to re-run (idempotent).

## Auto-Sync Behavior (Autonomous Mode)

When running with `linkedin-daily-planner`:

| Trigger | When | What |
|---------|------|------|
| After Afternoon Block | ~3-4 PM | CLI sync × N — syncs ONLY prospects modified during this session |
| After Evening Block | ~8-9 PM | CLI sync × N — syncs ONLY prospects modified during this session |

**PRIMARY METHOD: CLI Sync (always works, no MCP dependency):**
```bash
python crm-integration/cli_sync.py sync "Name1" "Name2" "Name3"
```

**FALLBACK METHOD: MCP tools (only if loaded in session):**
Call `crm_sync_prospect` via MCP tool for each changed record.

**Why CLI is preferred:** Claude Code defers MCP tool loading when many servers are connected (8+). The hubspot-crm tools may not be loaded in every session. The CLI script reads API keys from `.mcp.json` automatically and uses the exact same sync logic.

**INCREMENTAL SYNC RULE:** Do NOT call `crm_sync_all` during routine blocks. Instead, track which prospects changed during the session (new discoveries, touch updates, connection status changes, email enrichments) and sync individually. This reduces API calls from 200+ to typically 5-15 per sync.

**When to use `crm_sync_all`:** Only for initial setup, data migration, or periodic full reconciliation (e.g., weekly audit on Fridays).

## CLI Reference

```bash
# Sync specific prospects (reads from icp-prospects.md, matches by name)
python crm-integration/cli_sync.py sync "Hsien Naidu" "Bhavana Ravindran"

# Pipeline summary
python crm-integration/cli_sync.py pipeline

# Look up a contact in HubSpot
python crm-integration/cli_sync.py lookup "Hsien Naidu"
```

API keys are loaded automatically from `.mcp.json` (hubspot-crm env block). No extra config needed.

## Tools Reference

### crm_setup_properties (one-time)
Creates 8 custom HubSpot contact properties for LinkedIn pipeline data. Idempotent — skips existing properties.

### crm_sync_prospect
Sync a single prospect. Creates or updates contact, associates company, creates deal with pipeline stage.

**Pipeline stage mapping:**

| Condition | Stage |
|-----------|-------|
| 0 touches, not connected | Lead |
| 1 touch | Prospect |
| 2 touches | Qualified |
| 3+ touches | Engaged |
| Connected | Connected |
| dm_sent in history | In Conversation |
| INACTIVE or rejected | Nurture |

### crm_sync_all
Batch sync ALL prospects from `icp-prospects.md`. Reads the markdown table, syncs each to HubSpot. Skips entries with "TBD" URLs.

**WARNING:** This syncs all 200+ records. Only use for initial setup, data migration, or weekly full reconciliation (Friday audit). For routine daily blocks, use `crm_sync_prospect` for each changed record instead.

### crm_log_activity
Log a LinkedIn engagement (comment, DM, connection request, like) as a HubSpot Note on the contact's timeline.

### crm_get_contact
Look up a contact by LinkedIn URL (exact match) or name (fuzzy search). Returns all pipeline fields.

### crm_get_pipeline
Pipeline funnel summary — count of contacts in each stage.

### crm_find_emails
Find business emails for prospects with pending connections > 7 days. Uses Apollo (primary, 50/month) then Hunter (fallback, 25/month). Only stores verified emails (Apollo) or confidence >= 80% (Hunter). Updates HubSpot email property automatically.

**Parameters:**
- `min_days_pending` (int, default 7): Days since connect_sent to qualify
- `dry_run` (bool, default false): Preview eligible prospects without calling APIs

**Credit tracking:** Stops when monthly limits hit (Apollo: 50, Hunter: 25).

### crm_pull_emails
Reverse sync: checks HubSpot contacts for emails that aren't in `icp-prospects.md`. Reports which prospects need their Email column updated. Useful for catching manually-added emails in HubSpot.

## Field Mapping

| icp-prospects.md | HubSpot Property | Type |
|-----------------|-----------------|------|
| Name | firstname, lastname | Standard (split) |
| Role | jobtitle | Standard |
| Company | Company association | Association |
| Location | city | Standard |
| Profile URL | `linkedin_profile` | Custom |
| Classification | `lead_classification` | Custom dropdown |
| Touches | `touch_count` | Custom number |
| Last Touch | `last_touch_date` | Custom date |
| Touch History | `touch_history` | Custom text |
| Connection Status | `linkedin_connection_status` | Custom dropdown |
| Activity Status | `activity_status` | Custom dropdown |
| Engagement Score | `engagement_score` | Custom dropdown |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `HUBSPOT_API_KEY not set` | Check env vars in settings.local.json mcpServers config |
| `401 Invalid API key` | Regenerate private app token in HubSpot |
| `403 Insufficient permissions` | Check API scopes match the 8 listed above |
| `429 Rate limit exceeded` | Built-in rate limiter (100 req/10s) should handle this; wait and retry |
| `No prospects found` | Check icp-prospects.md exists and has the expected table format |
| `Skipped (no URL)` | Prospect has "TBD" as Profile URL; update in icp-prospects.md first |
| Duplicate contacts | Check `linkedin_profile` property — dedup uses exact URL match |
| Deal not updating | Verify `HUBSPOT_PIPELINE_ID` env var matches your pipeline (defaults to "default") |
