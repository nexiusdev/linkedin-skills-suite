# HubSpot CRM Integration

Sync LinkedIn prospect pipeline data to HubSpot CRM. One-way auto-sync from `icp-prospects.md` to HubSpot contacts, companies, and deals.

## Trigger Phrases

- "sync to crm" / "crm sync" — runs `crm_sync_all`
- "setup hubspot" / "setup crm" — runs `crm_setup_properties`
- "crm pipeline" / "pipeline summary" — runs `crm_get_pipeline`
- "log activity to crm" — runs `crm_log_activity`
- "lookup in crm" / "crm contact" — runs `crm_get_contact`

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

Add to your MCP server config in `.claude/settings.local.json`:

```json
"hubspot-crm": {
  "command": "python",
  "args": ["C:\\Users\\melve\\.claude\\skills\\crm-integration\\hubspot_mcp.py"],
  "env": {
    "HUBSPOT_API_KEY": "pat-na1-xxxxx",
    "HUBSPOT_PORTAL_ID": "12345678"
  }
}
```

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
| After Afternoon Block | ~3-4 PM | `crm_sync_all` — captures new prospects, connection updates, touch history |
| After Evening Block | ~8-9 PM | `crm_sync_all` — captures inbound audit results, new ICP matches |

Auto-sync reads `shared/logs/icp-prospects.md` and pushes all changes to HubSpot. Deduplication by LinkedIn URL means repeated syncs are safe.

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
Batch sync all prospects from `icp-prospects.md`. Reads the markdown table, syncs each to HubSpot. Skips entries with "TBD" URLs.

### crm_log_activity
Log a LinkedIn engagement (comment, DM, connection request, like) as a HubSpot Note on the contact's timeline.

### crm_get_contact
Look up a contact by LinkedIn URL (exact match) or name (fuzzy search). Returns all pipeline fields.

### crm_get_pipeline
Pipeline funnel summary — count of contacts in each stage.

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
