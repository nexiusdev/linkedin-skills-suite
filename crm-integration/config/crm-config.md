# CRM Integration Configuration

Client-editable settings for HubSpot CRM sync. Modify values below to customize behavior.

## Connection Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **CRM Provider** | HubSpot | Currently supported: HubSpot |
| **API Key Env Var** | `HUBSPOT_API_KEY` | Set in MCP server config |
| **Portal ID Env Var** | `HUBSPOT_PORTAL_ID` | Set in MCP server config |
| **Pipeline ID** | `default` | HubSpot pipeline for deals (set `HUBSPOT_PIPELINE_ID` to override) |

## Sync Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **Auto-sync after Afternoon Block** | Yes | Syncs prospects after outreach session |
| **Auto-sync after Evening Block** | Yes | Syncs prospects after inbound audit |
| **Skip TBD URLs** | Yes | Prospects without LinkedIn URLs are skipped |
| **Create companies** | Yes | Auto-create company records and associate |
| **Create deals** | Yes | Auto-create deals for pipeline tracking |

## Source File

| Setting | Value |
|---------|-------|
| **Prospects file** | `shared/logs/icp-prospects.md` |
| **Override path** | Set `ICP_PROSPECTS_PATH` env var to use a different file |

## Pipeline Stage Mapping

Customize which conditions map to which HubSpot deal stage.

| Condition | Stage | Stage ID |
|-----------|-------|----------|
| 0 touches, not connected | Lead | `lead` |
| 1 touch | Prospect | `prospect` |
| 2 touches | Qualified | `qualified` |
| 3+ touches | Engaged | `engaged` |
| Connected on LinkedIn | Connected | `connected` |
| DM sent | In Conversation | `in_conversation` |
| INACTIVE or rejected | Nurture | `nurture` |

> **Note:** Stage IDs must match your HubSpot pipeline configuration. If using custom stage IDs, update the `PIPELINE_STAGES` dict in `hubspot_mcp.py`.

## Field Mapping Overrides

Default mapping from `icp-prospects.md` columns to HubSpot properties. To change, edit `_prospect_to_hubspot_properties()` in `hubspot_mcp.py`.

| Source Column | HubSpot Property | Custom? |
|--------------|------------------|---------|
| Name | firstname + lastname | No |
| Role | jobtitle | No |
| Company | Company association | No |
| Location | city | No |
| Profile URL | linkedin_profile | Yes |
| Classification | lead_classification | Yes |
| Touches | touch_count | Yes |
| Last Touch | last_touch_date | Yes |
| Touch History | touch_history | Yes |
| Connection Status | linkedin_connection_status | Yes |

## Rate Limits

| Setting | Value |
|---------|-------|
| Max requests per window | 100 |
| Window size | 10 seconds |
| Request timeout | 30 seconds |

HubSpot free plan allows 100 requests per 10 seconds. Paid plans have higher limits. The built-in rate limiter handles throttling automatically.
