#!/usr/bin/env python3
"""
MCP Server for HubSpot CRM Integration.

One-way sync from LinkedIn prospect pipeline (icp-prospects.md) to HubSpot CRM.
Provides tools for contact management, activity logging, and pipeline reporting.
"""

import asyncio
import json
import os
import re
import time
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Initialize the MCP server
mcp = FastMCP("hubspot_mcp")

# Constants
HUBSPOT_API_BASE = "https://api.hubapi.com"
CHARACTER_LIMIT = 25000
RATE_LIMIT_MAX = 100
RATE_LIMIT_WINDOW = 10  # seconds
ICP_PROSPECTS_PATH = Path(os.environ.get(
    "ICP_PROSPECTS_PATH",
    str(Path.home() / ".claude" / "skills" / "shared" / "logs" / "icp-prospects.md")
))

# Custom HubSpot properties to create
CUSTOM_PROPERTIES = [
    {
        "name": "linkedin_profile",
        "label": "LinkedIn Profile URL",
        "type": "string",
        "fieldType": "text",
        "groupName": "contactinformation",
        "description": "Full LinkedIn profile URL - used as unique key for deduplication"
    },
    {
        "name": "lead_classification",
        "label": "Lead Classification",
        "type": "enumeration",
        "fieldType": "select",
        "groupName": "contactinformation",
        "description": "ICP classification from LinkedIn pipeline",
        "options": [
            {"label": "Prospect", "value": "PROSPECT"},
            {"label": "Thought Leader", "value": "THOUGHT LEADER"},
            {"label": "Peer", "value": "PEER"},
        ]
    },
    {
        "name": "touch_count",
        "label": "Touch Count",
        "type": "number",
        "fieldType": "number",
        "groupName": "contactinformation",
        "description": "Number of LinkedIn engagement touches"
    },
    {
        "name": "last_touch_date",
        "label": "Last Touch Date",
        "type": "date",
        "fieldType": "date",
        "groupName": "contactinformation",
        "description": "Date of most recent LinkedIn engagement"
    },
    {
        "name": "touch_history",
        "label": "Touch History",
        "type": "string",
        "fieldType": "text",
        "groupName": "contactinformation",
        "description": "Comma-separated LinkedIn engagement actions"
    },
    {
        "name": "linkedin_connection_status",
        "label": "LinkedIn Connection Status",
        "type": "enumeration",
        "fieldType": "select",
        "groupName": "contactinformation",
        "description": "Current LinkedIn connection state",
        "options": [
            {"label": "None", "value": "none"},
            {"label": "Pending", "value": "pending"},
            {"label": "Connected", "value": "connected"},
            {"label": "Rejected", "value": "rejected"},
        ]
    },
    {
        "name": "activity_status",
        "label": "Activity Status",
        "type": "enumeration",
        "fieldType": "select",
        "groupName": "contactinformation",
        "description": "LinkedIn posting activity level",
        "options": [
            {"label": "Active", "value": "ACTIVE"},
            {"label": "Moderate", "value": "MODERATE"},
            {"label": "Inactive", "value": "INACTIVE"},
            {"label": "Unknown", "value": "UNKNOWN"},
        ]
    },
    {
        "name": "engagement_score",
        "label": "Engagement Score",
        "type": "enumeration",
        "fieldType": "select",
        "groupName": "contactinformation",
        "description": "LinkedIn engagement frequency score",
        "options": [
            {"label": "High", "value": "HIGH"},
            {"label": "Medium", "value": "MED"},
            {"label": "Low", "value": "LOW"},
            {"label": "Unknown", "value": "UNKNOWN"},
        ]
    },
]

# Pipeline stage definitions
# Mapped to HubSpot default pipeline stages (free plan = 1 pipeline only)
# Lead → appointmentscheduled, Prospect → qualifiedtobuy, Qualified → presentationscheduled,
# Engaged → decisionmakerboughtin, Connected → contractsent,
# In Conversation → closedwon, Nurture → closedlost
PIPELINE_STAGES = {
    "Lead": "appointmentscheduled",
    "Prospect": "qualifiedtobuy",
    "Qualified": "presentationscheduled",
    "Engaged": "decisionmakerboughtin",
    "Connected": "contractsent",
    "In Conversation": "closedwon",
    "Nurture": "closedlost",
}


# ─── Rate Limiter ───────────────────────────────────────────────────────────

class RateLimiter:
    """Simple sliding-window rate limiter for HubSpot API (100 req/10s)."""

    def __init__(self, max_requests: int = RATE_LIMIT_MAX, window: int = RATE_LIMIT_WINDOW):
        self.max_requests = max_requests
        self.window = window
        self.timestamps: list[float] = []

    async def acquire(self):
        now = time.monotonic()
        self.timestamps = [t for t in self.timestamps if now - t < self.window]
        if len(self.timestamps) >= self.max_requests:
            wait = self.window - (now - self.timestamps[0])
            if wait > 0:
                await asyncio.sleep(wait)
        self.timestamps.append(time.monotonic())


rate_limiter = RateLimiter()


# ─── API Helpers ─────────────────────────────────────────────────────────────

def _get_api_key() -> str:
    key = os.environ.get("HUBSPOT_API_KEY", "")
    if not key:
        raise ValueError("HUBSPOT_API_KEY environment variable is not set")
    return key


def _auth_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_api_key()}",
        "Content-Type": "application/json",
    }


async def _make_api_request(
    endpoint: str,
    method: str = "GET",
    json_data: Optional[Dict] = None,
    params: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Reusable function for all HubSpot API calls with rate limiting."""
    await rate_limiter.acquire()
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{HUBSPOT_API_BASE}{endpoint}",
            headers=_auth_headers(),
            json=json_data,
            params=params,
            timeout=30.0,
        )
        response.raise_for_status()
        if response.status_code == 204:
            return {}
        return response.json()


def _handle_api_error(e: Exception) -> str:
    """Consistent error formatting across all tools."""
    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        try:
            body = e.response.json()
            message = body.get("message", "")
        except Exception:
            message = e.response.text[:200]
        if status == 400:
            return f"Error: Bad request — {message}"
        elif status == 401:
            return "Error: Invalid API key. Check HUBSPOT_API_KEY env var."
        elif status == 403:
            return "Error: Insufficient permissions. Check API key scopes."
        elif status == 404:
            return f"Error: Resource not found — {message}"
        elif status == 429:
            return "Error: Rate limit exceeded. Wait 10 seconds and retry."
        return f"Error: HubSpot API returned {status} — {message}"
    elif isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. Please try again."
    elif isinstance(e, ValueError):
        return f"Error: {e}"
    return f"Error: {type(e).__name__}: {e}"


# ─── Utility Functions ───────────────────────────────────────────────────────

def _split_name(full_name: str) -> tuple[str, str]:
    """Split full name into (firstname, lastname). Handles multi-part names."""
    parts = full_name.strip().split()
    if len(parts) == 0:
        return ("", "")
    if len(parts) == 1:
        return (parts[0], "")
    return (parts[0], " ".join(parts[1:]))


def _parse_touch_date(date_str: str) -> Optional[str]:
    """Parse date like '07Feb' or '22Jan' into ISO date string for HubSpot.

    HubSpot date properties expect midnight UTC timestamps in milliseconds.
    We assume current year if the date is in the past, otherwise last year.
    """
    if not date_str or date_str.strip() == "-":
        return None
    date_str = date_str.strip()
    # Match patterns like "07Feb", "22Jan", "23Jan 17:45"
    match = re.match(r"(\d{1,2})([A-Za-z]{3})", date_str)
    if not match:
        return None
    day = int(match.group(1))
    month_str = match.group(2)
    try:
        month = datetime.strptime(month_str, "%b").month
    except ValueError:
        return None
    year = datetime.now().year
    try:
        dt = datetime(year, month, day, tzinfo=timezone.utc)
        if dt > datetime.now(timezone.utc):
            dt = dt.replace(year=year - 1)
        # HubSpot date properties need midnight UTC in ms
        return str(int(dt.timestamp() * 1000))
    except ValueError:
        return None


def _determine_pipeline_stage(
    touches: int, connection_status: str, touch_history: str
) -> str:
    """Map prospect data to a pipeline stage name."""
    history_lower = touch_history.lower() if touch_history else ""

    # Check special statuses first
    if "inactive" in history_lower or connection_status == "rejected":
        return "Nurture"
    if "dm_sent" in history_lower:
        return "In Conversation"
    if connection_status == "connected":
        return "Connected"
    if touches >= 3:
        return "Engaged"
    if touches == 2:
        return "Qualified"
    if touches == 1:
        return "Prospect"
    return "Lead"


def _parse_prospects_table(content: str) -> List[Dict[str, str]]:
    """Parse the markdown prospects table from icp-prospects.md.

    Returns list of dicts with keys matching column headers.
    """
    prospects = []
    lines = content.split("\n")
    headers = []
    in_prospects_table = False

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_prospects_table and headers:
                break  # End of table
            continue

        cells = [c.strip() for c in stripped.split("|")]
        # Remove empty first/last from leading/trailing pipes
        cells = cells[1:-1] if len(cells) > 2 else cells

        if not headers:
            if "#" in cells and "Name" in cells:
                headers = cells
                in_prospects_table = True
                continue
        elif in_prospects_table:
            # Skip separator row
            if all(c.replace("-", "").replace(":", "").strip() == "" for c in cells):
                continue
            if len(cells) == len(headers):
                row = dict(zip(headers, cells))
                prospects.append(row)

    return prospects


def _prospect_to_hubspot_properties(prospect: Dict[str, str]) -> Dict[str, str]:
    """Convert a parsed prospect row into HubSpot contact properties."""
    firstname, lastname = _split_name(prospect.get("Name", ""))
    touch_date = _parse_touch_date(prospect.get("Last Touch", ""))

    props: Dict[str, str] = {
        "firstname": firstname,
        "lastname": lastname,
        "jobtitle": prospect.get("Role", ""),
        "city": prospect.get("Location", ""),
        "linkedin_profile": prospect.get("Profile URL", ""),
        "lead_classification": prospect.get("Classification", ""),
        "linkedin_connection_status": prospect.get("Connection Status", "none"),
        "touch_history": prospect.get("Touch History", ""),
    }

    # Parse touch count
    touches_str = prospect.get("Touches", "0").strip()
    try:
        props["touch_count"] = str(int(touches_str.replace("+", "")))
    except ValueError:
        props["touch_count"] = "0"

    if touch_date:
        props["last_touch_date"] = touch_date

    # Remove empty values
    return {k: v for k, v in props.items() if v and v != "-"}


async def _search_contact_by_linkedin_url(linkedin_url: str) -> Optional[Dict]:
    """Search HubSpot for a contact by LinkedIn profile URL. Returns contact or None."""
    if not linkedin_url or linkedin_url == "TBD":
        return None
    data = await _make_api_request(
        "/crm/v3/objects/contacts/search",
        method="POST",
        json_data={
            "filterGroups": [{
                "filters": [{
                    "propertyName": "linkedin_profile",
                    "operator": "EQ",
                    "value": linkedin_url,
                }]
            }],
            "properties": [
                "firstname", "lastname", "jobtitle", "city",
                "linkedin_profile", "lead_classification", "touch_count",
                "last_touch_date", "touch_history", "linkedin_connection_status",
                "activity_status", "engagement_score",
            ],
        },
    )
    results = data.get("results", [])
    return results[0] if results else None


async def _create_or_update_contact(properties: Dict[str, str]) -> Dict[str, Any]:
    """Create or update a HubSpot contact. Deduplicates by linkedin_profile."""
    linkedin_url = properties.get("linkedin_profile", "")
    existing = await _search_contact_by_linkedin_url(linkedin_url)

    if existing:
        contact_id = existing["id"]
        result = await _make_api_request(
            f"/crm/v3/objects/contacts/{contact_id}",
            method="PATCH",
            json_data={"properties": properties},
        )
        return {**result, "_action": "updated"}
    else:
        result = await _make_api_request(
            "/crm/v3/objects/contacts",
            method="POST",
            json_data={"properties": properties},
        )
        return {**result, "_action": "created"}


async def _ensure_company_association(contact_id: str, company_name: str):
    """Search for company by name and associate with contact. Creates company if not found."""
    if not company_name or company_name.strip() == "-":
        return None

    # Search for existing company
    data = await _make_api_request(
        "/crm/v3/objects/companies/search",
        method="POST",
        json_data={
            "filterGroups": [{
                "filters": [{
                    "propertyName": "name",
                    "operator": "EQ",
                    "value": company_name,
                }]
            }],
            "properties": ["name"],
        },
    )
    results = data.get("results", [])

    if results:
        company_id = results[0]["id"]
    else:
        # Create company
        company = await _make_api_request(
            "/crm/v3/objects/companies",
            method="POST",
            json_data={"properties": {"name": company_name}},
        )
        company_id = company["id"]

    # Associate contact with company
    try:
        await _make_api_request(
            f"/crm/v3/objects/contacts/{contact_id}/associations/companies/{company_id}/contact_to_company",
            method="PUT",
        )
    except httpx.HTTPStatusError:
        pass  # Association may already exist

    return company_id


async def _ensure_deal(
    contact_id: str, stage_name: str, prospect_name: str
) -> Optional[str]:
    """Create or update deal for pipeline tracking. One deal per contact."""
    pipeline_id = os.environ.get("HUBSPOT_PIPELINE_ID", "default")
    stage_id = PIPELINE_STAGES.get(stage_name, "lead")

    # Search for existing deal associated with this contact
    data = await _make_api_request(
        f"/crm/v3/objects/contacts/{contact_id}/associations/deals",
        method="GET",
    )
    existing_deals = data.get("results", [])

    if existing_deals:
        deal_id = existing_deals[0]["id"]
        await _make_api_request(
            f"/crm/v3/objects/deals/{deal_id}",
            method="PATCH",
            json_data={
                "properties": {
                    "dealstage": stage_id,
                    "dealname": f"LinkedIn Pipeline - {prospect_name}",
                }
            },
        )
        return deal_id
    else:
        deal = await _make_api_request(
            "/crm/v3/objects/deals",
            method="POST",
            json_data={
                "properties": {
                    "dealname": f"LinkedIn Pipeline - {prospect_name}",
                    "dealstage": stage_id,
                    "pipeline": pipeline_id,
                },
            },
        )
        deal_id = deal["id"]
        # Associate deal with contact
        try:
            await _make_api_request(
                f"/crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/deal_to_contact",
                method="PUT",
            )
        except httpx.HTTPStatusError:
            pass
        return deal_id


# ─── Pydantic Input Models ──────────────────────────────────────────────────

class SyncProspectInput(BaseModel):
    """Input for syncing a single prospect to HubSpot."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., description="Full name of the prospect (e.g., 'David Cheang')", min_length=1)
    role: str = Field(default="", description="Job title (e.g., 'CEO & Founder')")
    company: str = Field(default="", description="Company name (e.g., 'DC13 Group')")
    location: str = Field(default="", description="Location (e.g., 'Singapore')")
    linkedin_url: str = Field(..., description="Full LinkedIn profile URL", min_length=5)
    classification: str = Field(default="PROSPECT", description="PROSPECT, THOUGHT LEADER, or PEER")
    touches: int = Field(default=0, description="Number of engagement touches", ge=0)
    last_touch: str = Field(default="-", description="Date of last touch (e.g., '07Feb' or '-')")
    touch_history: str = Field(default="-", description="Comma-separated actions (e.g., 'connect_sent, dm_sent')")
    connection_status: str = Field(default="none", description="none, pending, connected, or rejected")
    notes: str = Field(default="", description="Additional notes about the prospect")


class LogActivityInput(BaseModel):
    """Input for logging a LinkedIn activity as a HubSpot note."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    linkedin_url: str = Field(..., description="LinkedIn profile URL of the contact", min_length=5)
    activity_type: str = Field(..., description="Type: comment, dm_sent, connect_sent, like, follow, reply")
    description: str = Field(..., description="Activity description (e.g., 'Commented on AI automation post')", min_length=1)
    date: str = Field(default="", description="Date of activity (e.g., '07Feb'). Defaults to today.")


class GetContactInput(BaseModel):
    """Input for looking up a HubSpot contact."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    linkedin_url: str = Field(default="", description="LinkedIn profile URL to search by")
    name: str = Field(default="", description="Name to search by (used if linkedin_url not provided)")

    @field_validator("linkedin_url", "name")
    @classmethod
    def at_least_one(cls, v: str, info) -> str:
        return v  # Cross-field validation handled in tool


# ─── Tool Definitions ────────────────────────────────────────────────────────

@mcp.tool(
    name="crm_setup_properties",
    annotations={
        "title": "Setup HubSpot Custom Properties",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_setup_properties() -> str:
    """Create custom HubSpot properties for LinkedIn pipeline tracking.

    One-time setup that creates custom contact properties in HubSpot for:
    linkedin_profile, lead_classification, touch_count, last_touch_date,
    touch_history, linkedin_connection_status, activity_status, engagement_score.

    Safe to call multiple times — skips properties that already exist.

    Returns:
        str: Summary of properties created and skipped.
    """
    try:
        created = []
        skipped = []

        for prop_def in CUSTOM_PROPERTIES:
            try:
                body: Dict[str, Any] = {
                    "name": prop_def["name"],
                    "label": prop_def["label"],
                    "type": prop_def["type"],
                    "fieldType": prop_def["fieldType"],
                    "groupName": prop_def["groupName"],
                    "description": prop_def.get("description", ""),
                }
                if "options" in prop_def:
                    body["options"] = [
                        {"label": o["label"], "value": o["value"], "displayOrder": i}
                        for i, o in enumerate(prop_def["options"])
                    ]
                await _make_api_request(
                    "/crm/v3/properties/contacts",
                    method="POST",
                    json_data=body,
                )
                created.append(prop_def["name"])
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 409:
                    skipped.append(prop_def["name"])
                else:
                    return _handle_api_error(e)

        lines = ["## CRM Setup Properties — Complete", ""]
        if created:
            lines.append(f"**Created:** {', '.join(created)}")
        if skipped:
            lines.append(f"**Already existed (skipped):** {', '.join(skipped)}")
        lines.append(f"\n**Total:** {len(created)} created, {len(skipped)} skipped")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="crm_sync_prospect",
    annotations={
        "title": "Sync Prospect to HubSpot",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_sync_prospect(params: SyncProspectInput) -> str:
    """Sync a single prospect to HubSpot CRM. Creates or updates the contact.

    Uses LinkedIn profile URL as unique key for deduplication. Also:
    - Creates/associates Company record
    - Creates/updates Deal with pipeline stage based on touches + status
    - Adds notes from prospect data

    Args:
        params (SyncProspectInput): Prospect data containing:
            - name (str): Full name
            - role (str): Job title
            - company (str): Company name
            - location (str): City/country
            - linkedin_url (str): Full LinkedIn URL (unique key)
            - classification (str): PROSPECT/THOUGHT LEADER/PEER
            - touches (int): Engagement count
            - last_touch (str): Date of last engagement
            - touch_history (str): Comma-separated actions
            - connection_status (str): none/pending/connected/rejected
            - notes (str): Additional notes

    Returns:
        str: Markdown summary of sync result (created/updated, deal stage).
    """
    try:
        if params.linkedin_url == "TBD":
            return f"Skipped {params.name} — LinkedIn URL is TBD"

        firstname, lastname = _split_name(params.name)
        touch_date = _parse_touch_date(params.last_touch)

        properties: Dict[str, str] = {
            "firstname": firstname,
            "lastname": lastname,
            "jobtitle": params.role,
            "city": params.location,
            "linkedin_profile": params.linkedin_url,
            "lead_classification": params.classification,
            "touch_count": str(params.touches),
            "touch_history": params.touch_history if params.touch_history != "-" else "",
            "linkedin_connection_status": params.connection_status,
        }
        if touch_date:
            properties["last_touch_date"] = touch_date

        # Remove empty values
        properties = {k: v for k, v in properties.items() if v}

        result = await _create_or_update_contact(properties)
        action = result.get("_action", "synced")
        contact_id = result["id"]

        # Associate company
        company_id = await _ensure_company_association(contact_id, params.company)

        # Create/update deal
        stage = _determine_pipeline_stage(
            params.touches, params.connection_status, params.touch_history
        )
        deal_id = await _ensure_deal(contact_id, stage, params.name)

        lines = [
            f"**{params.name}** — {action}",
            f"- Contact ID: {contact_id}",
            f"- Stage: {stage}",
            f"- Touches: {params.touches} | Connection: {params.connection_status}",
        ]
        if company_id:
            lines.append(f"- Company: {params.company} (ID: {company_id})")
        if deal_id:
            lines.append(f"- Deal ID: {deal_id}")
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="crm_sync_all",
    annotations={
        "title": "Sync All Prospects to HubSpot",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_sync_all() -> str:
    """Batch sync all prospects from icp-prospects.md to HubSpot CRM.

    Reads the prospects table from icp-prospects.md, then creates or updates
    each contact in HubSpot. Skips prospects with TBD profile URLs.
    Uses linkedin_profile as dedup key — safe to run repeatedly.

    Triggered automatically after Afternoon Block and Evening Block.

    Returns:
        str: Markdown summary with counts (created, updated, skipped, errors).
    """
    try:
        if not ICP_PROSPECTS_PATH.exists():
            return f"Error: icp-prospects.md not found at {ICP_PROSPECTS_PATH}"

        content = ICP_PROSPECTS_PATH.read_text(encoding="utf-8")
        prospects = _parse_prospects_table(content)

        if not prospects:
            return "Error: No prospects found in icp-prospects.md table"

        created = 0
        updated = 0
        skipped = 0
        errors = []
        results_detail = []

        for prospect in prospects:
            name = prospect.get("Name", "Unknown")
            url = prospect.get("Profile URL", "TBD")

            if not url or url == "TBD":
                skipped += 1
                results_detail.append(f"- {name}: skipped (no URL)")
                continue

            try:
                properties = _prospect_to_hubspot_properties(prospect)
                result = await _create_or_update_contact(properties)
                action = result.get("_action", "synced")
                contact_id = result["id"]

                if action == "created":
                    created += 1
                else:
                    updated += 1

                # Company association
                await _ensure_company_association(
                    contact_id, prospect.get("Company", "")
                )

                # Deal/pipeline
                touches = int(prospect.get("Touches", "0").replace("+", "") or "0")
                stage = _determine_pipeline_stage(
                    touches,
                    prospect.get("Connection Status", "none"),
                    prospect.get("Touch History", ""),
                )
                await _ensure_deal(contact_id, stage, name)

                results_detail.append(f"- {name}: {action} (stage: {stage})")

            except Exception as e:
                errors.append(f"- {name}: {_handle_api_error(e)}")

        # Build summary
        total = len(prospects)
        lines = [
            "## CRM Sync Complete",
            "",
            f"**Total:** {total} prospects processed",
            f"- Created: {created}",
            f"- Updated: {updated}",
            f"- Skipped: {skipped} (no LinkedIn URL)",
            f"- Errors: {len(errors)}",
        ]

        if results_detail:
            lines.extend(["", "### Details", *results_detail[:30]])
            if len(results_detail) > 30:
                lines.append(f"... and {len(results_detail) - 30} more")

        if errors:
            lines.extend(["", "### Errors", *errors])

        result_text = "\n".join(lines)
        if len(result_text) > CHARACTER_LIMIT:
            result_text = result_text[:CHARACTER_LIMIT] + "\n\n... truncated"
        return result_text

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="crm_log_activity",
    annotations={
        "title": "Log LinkedIn Activity to HubSpot",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def crm_log_activity(params: LogActivityInput) -> str:
    """Log a LinkedIn engagement action as a Note on a HubSpot contact.

    Creates a timestamped note on the contact's timeline. Use this to track
    comments, DMs, connection requests, likes, and other engagement actions.

    Args:
        params (LogActivityInput): Activity data containing:
            - linkedin_url (str): LinkedIn URL to find the contact
            - activity_type (str): comment, dm_sent, connect_sent, like, follow, reply
            - description (str): What happened (e.g., 'Commented on AI automation post')
            - date (str): Activity date (e.g., '07Feb'). Defaults to today.

    Returns:
        str: Confirmation with note ID, or error if contact not found.
    """
    try:
        contact = await _search_contact_by_linkedin_url(params.linkedin_url)
        if not contact:
            return f"Error: No HubSpot contact found for {params.linkedin_url}"

        contact_id = contact["id"]
        contact_name = f"{contact['properties'].get('firstname', '')} {contact['properties'].get('lastname', '')}".strip()

        date_str = params.date if params.date else datetime.now().strftime("%d%b")
        note_body = (
            f"**LinkedIn Activity: {params.activity_type.upper()}**\n\n"
            f"Date: {date_str}\n"
            f"Type: {params.activity_type}\n"
            f"Details: {params.description}\n\n"
            f"_Logged via CRM auto-sync_"
        )

        note = await _make_api_request(
            "/crm/v3/objects/notes",
            method="POST",
            json_data={
                "properties": {
                    "hs_note_body": note_body,
                    "hs_timestamp": str(int(datetime.now(timezone.utc).timestamp() * 1000)),
                },
            },
        )
        note_id = note["id"]

        # Associate note with contact
        await _make_api_request(
            f"/crm/v3/objects/notes/{note_id}/associations/contacts/{contact_id}/note_to_contact",
            method="PUT",
        )

        return f"Activity logged for **{contact_name}** — Note ID: {note_id}\nType: {params.activity_type} | {params.description}"

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="crm_get_contact",
    annotations={
        "title": "Look Up HubSpot Contact",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_get_contact(params: GetContactInput) -> str:
    """Look up a contact in HubSpot by LinkedIn URL or name.

    Returns all LinkedIn pipeline fields including classification, touches,
    connection status, and pipeline stage.

    Args:
        params (GetContactInput): Search criteria containing:
            - linkedin_url (str): LinkedIn profile URL (preferred, exact match)
            - name (str): Name to search by (fuzzy, used if no URL provided)

    Returns:
        str: Markdown-formatted contact details, or error if not found.
    """
    try:
        if not params.linkedin_url and not params.name:
            return "Error: Provide either linkedin_url or name to search."

        contact = None

        # Try LinkedIn URL first (exact match)
        if params.linkedin_url:
            contact = await _search_contact_by_linkedin_url(params.linkedin_url)

        # Fall back to name search
        if not contact and params.name:
            data = await _make_api_request(
                "/crm/v3/objects/contacts/search",
                method="POST",
                json_data={
                    "filterGroups": [{
                        "filters": [{
                            "propertyName": "firstname",
                            "operator": "CONTAINS_TOKEN",
                            "value": params.name.split()[0],
                        }]
                    }],
                    "properties": [
                        "firstname", "lastname", "jobtitle", "city", "company",
                        "linkedin_profile", "lead_classification", "touch_count",
                        "last_touch_date", "touch_history", "linkedin_connection_status",
                        "activity_status", "engagement_score",
                    ],
                },
            )
            results = data.get("results", [])
            # Filter by full name match
            name_lower = params.name.lower()
            for r in results:
                p = r.get("properties", {})
                full = f"{p.get('firstname', '')} {p.get('lastname', '')}".strip().lower()
                if name_lower in full or full in name_lower:
                    contact = r
                    break
            if not contact and results:
                contact = results[0]  # Best effort

        if not contact:
            search_term = params.linkedin_url or params.name
            return f"No contact found for: {search_term}"

        p = contact.get("properties", {})
        touches = int(p.get("touch_count", "0") or "0")
        conn_status = p.get("linkedin_connection_status", "none") or "none"
        touch_hist = p.get("touch_history", "") or ""
        stage = _determine_pipeline_stage(touches, conn_status, touch_hist)

        lines = [
            f"## {p.get('firstname', '')} {p.get('lastname', '')}",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| **Role** | {p.get('jobtitle', '-')} |",
            f"| **Location** | {p.get('city', '-')} |",
            f"| **LinkedIn** | {p.get('linkedin_profile', '-')} |",
            f"| **Classification** | {p.get('lead_classification', '-')} |",
            f"| **Touches** | {touches} |",
            f"| **Touch History** | {touch_hist or '-'} |",
            f"| **Connection** | {conn_status} |",
            f"| **Activity** | {p.get('activity_status', '-')} |",
            f"| **Engagement** | {p.get('engagement_score', '-')} |",
            f"| **Pipeline Stage** | {stage} |",
            f"| **HubSpot ID** | {contact['id']} |",
        ]
        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="crm_get_pipeline",
    annotations={
        "title": "Get Pipeline Summary",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_get_pipeline() -> str:
    """Get a pipeline summary showing contact counts per stage.

    Reads all contacts with a linkedin_profile property and groups them
    by their calculated pipeline stage. Provides a quick overview of the
    LinkedIn prospect funnel.

    Returns:
        str: Markdown table with stage names and counts, plus total.
    """
    try:
        # Get all contacts with linkedin_profile set
        all_contacts = []
        after = None
        max_pages = 10  # Safety limit

        for _ in range(max_pages):
            params: Dict[str, Any] = {"limit": 100}
            if after:
                params["after"] = after

            data = await _make_api_request(
                "/crm/v3/objects/contacts/search",
                method="POST",
                json_data={
                    "filterGroups": [{
                        "filters": [{
                            "propertyName": "linkedin_profile",
                            "operator": "HAS_PROPERTY",
                        }]
                    }],
                    "properties": [
                        "firstname", "lastname", "touch_count",
                        "linkedin_connection_status", "touch_history",
                        "lead_classification",
                    ],
                    "limit": 100,
                    "after": after or 0,
                },
            )
            results = data.get("results", [])
            all_contacts.extend(results)

            paging = data.get("paging", {})
            next_page = paging.get("next", {})
            after = next_page.get("after")
            if not after:
                break

        # Count by stage
        stage_counts: Dict[str, int] = {stage: 0 for stage in PIPELINE_STAGES}
        for contact in all_contacts:
            p = contact.get("properties", {})
            touches = int(p.get("touch_count", "0") or "0")
            conn = p.get("linkedin_connection_status", "none") or "none"
            hist = p.get("touch_history", "") or ""
            stage = _determine_pipeline_stage(touches, conn, hist)
            stage_counts[stage] = stage_counts.get(stage, 0) + 1

        # Build table
        lines = [
            "## LinkedIn Pipeline Summary",
            "",
            "| Stage | Count |",
            "|-------|-------|",
        ]
        total = 0
        for stage_name in PIPELINE_STAGES:
            count = stage_counts.get(stage_name, 0)
            total += count
            bar = "#" * min(count, 20)
            lines.append(f"| {stage_name} | {count} {bar} |")
        lines.extend([
            f"| **Total** | **{total}** |",
            "",
            f"_Last updated: {datetime.now().strftime('%d %b %Y %H:%M')}_",
        ])

        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


class SyncPhotosInput(BaseModel):
    """Input for syncing LinkedIn profile photos to HubSpot."""

    filter_by: Optional[str] = Field(
        default=None,
        description="Optional filter: 'high_priority' (3+ touches or connected), 'all', or None for high priority"
    )
    limit: Optional[int] = Field(
        default=20,
        description="Maximum number of photos to sync in one run (default: 20)"
    )


@mcp.tool(
    name="crm_sync_photos",
    annotations={
        "title": "Sync LinkedIn Profile Photos to HubSpot",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_sync_photos(params: SyncPhotosInput) -> str:
    """Sync LinkedIn profile photos to HubSpot contact avatars.

    Fetches LinkedIn profile photos using browser automation (Chrome DevTools MCP)
    and uploads them to HubSpot as contact avatars.

    IMPORTANT: This tool requires the Chrome DevTools MCP to be available and
    a Chrome browser to be running with DevTools enabled.

    Args:
        params (SyncPhotosInput): Sync parameters:
            - filter_by: 'high_priority' (3+ touches or connected), 'all', or None
            - limit: Max photos to sync (default: 20)

    Returns:
        str: Summary with counts of photos synced, skipped, and errors.
    """
    try:
        # Check if Chrome DevTools MCP is available
        # This is a placeholder - the actual implementation would need to:
        # 1. Use Chrome DevTools MCP to navigate to LinkedIn profiles
        # 2. Extract profile photo URLs
        # 3. Download the images
        # 4. Upload to HubSpot Files API
        # 5. Set hs_avatar_filemanager_key property on contacts

        return (
            "## Photo Sync Not Yet Implemented\n\n"
            "This tool requires:\n"
            "1. Chrome DevTools MCP integration\n"
            "2. LinkedIn authentication (browser must be logged in)\n"
            "3. HubSpot Files API upload implementation\n\n"
            "**Next Steps:**\n"
            "- Install and configure Chrome DevTools MCP server\n"
            "- Implement photo extraction from LinkedIn profiles\n"
            "- Add HubSpot Files API upload functionality\n\n"
            "This is a placeholder tool that will be implemented in a future update."
        )

    except Exception as e:
        return _handle_api_error(e)


if __name__ == "__main__":
    mcp.run()
