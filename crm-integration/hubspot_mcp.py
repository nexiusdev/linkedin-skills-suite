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
APOLLO_API_BASE = "https://api.apollo.io/api/v1"
HUNTER_API_BASE = "https://api.hunter.io/v2"
SNOV_API_BASE = "https://api.snov.io"
GETPROSPECT_API_BASE = "https://api.getprospect.com/public/v1"
PROSPEO_API_BASE = "https://api.prospeo.io"
CHARACTER_LIMIT = 25000
RATE_LIMIT_MAX = 100
RATE_LIMIT_WINDOW = 10  # seconds
APOLLO_MONTHLY_LIMIT = 50
HUNTER_MONTHLY_LIMIT = 25
SNOV_MONTHLY_LIMIT = 50
GETPROSPECT_MONTHLY_LIMIT = 50
PROSPEO_MONTHLY_LIMIT = 100
ICP_PROSPECTS_PATH = Path(os.environ.get(
    "ICP_PROSPECTS_PATH",
    str(Path.home() / ".codex" / "skills" / "shared" / "logs" / "icp-prospects.md")
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
    Handles escaped pipes (\\|) in ANY column by replacing them with a placeholder
    before splitting, then restoring after. This prevents column misalignment when
    Touch History or Notes contain escaped pipes.
    """
    PIPE_PLACEHOLDER = "\x00PIPE\x00"
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

        # Replace escaped pipes with placeholder BEFORE splitting
        safe_line = stripped.replace("\\|", PIPE_PLACEHOLDER)
        cells = [c.strip().replace(PIPE_PLACEHOLDER, "|") for c in safe_line.split("|")]
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
            # Handle any remaining overflow (extra unescaped pipes)
            if len(cells) > len(headers):
                overflow = cells[len(headers) - 1:]
                cells = cells[:len(headers) - 1] + [" | ".join(overflow)]
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
        "email": prospect.get("Email", ""),
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


async def _search_contact_by_email(email: str) -> Optional[Dict]:
    """Search HubSpot for a contact by email address. Returns contact or None."""
    if not email or email == "-":
        return None
    data = await _make_api_request(
        "/crm/v3/objects/contacts/search",
        method="POST",
        json_data={
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": email,
                }]
            }],
            "properties": ["firstname", "lastname", "email", "linkedin_profile"],
        },
    )
    results = data.get("results", [])
    return results[0] if results else None


async def _create_or_update_contact(properties: Dict[str, str]) -> Dict[str, Any]:
    """Create or update a HubSpot contact. Deduplicates by linkedin_profile, then email."""
    linkedin_url = properties.get("linkedin_profile", "")
    existing = await _search_contact_by_linkedin_url(linkedin_url)

    # Fallback: search by email if LinkedIn URL match not found
    if not existing:
        email = properties.get("email", "")
        existing = await _search_contact_by_email(email)

    if existing:
        contact_id = existing["id"]
        result = await _make_api_request(
            f"/crm/v3/objects/contacts/{contact_id}",
            method="PATCH",
            json_data={"properties": properties},
        )
        return {**result, "_action": "updated"}
    else:
        try:
            result = await _make_api_request(
                "/crm/v3/objects/contacts",
                method="POST",
                json_data={"properties": properties},
            )
            return {**result, "_action": "created"}
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                # Conflict — contact exists, try to find and update
                email = properties.get("email", "")
                existing = await _search_contact_by_email(email)
                if existing:
                    contact_id = existing["id"]
                    result = await _make_api_request(
                        f"/crm/v3/objects/contacts/{contact_id}",
                        method="PATCH",
                        json_data={"properties": properties},
                    )
                    return {**result, "_action": "updated"}
            raise


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


# ─── Email Enrichment Helpers ────────────────────────────────────────────────

def _parse_touch_date_to_datetime(date_str: str) -> Optional[datetime]:
    """Parse DDMon date string (e.g., '23Jan', '01Feb') into a datetime object."""
    if not date_str or date_str.strip() == "-":
        return None
    date_str = date_str.strip()
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
        return dt
    except ValueError:
        return None


def _filter_email_eligible_prospects(
    prospects: List[Dict[str, str]], min_days: int = 7
) -> List[Dict[str, str]]:
    """Filter prospects: pending connection > min_days ago, no email yet."""
    eligible = []
    now = datetime.now(timezone.utc)
    for p in prospects:
        conn_status = p.get("Connection Status", "").strip().lower()
        email = p.get("Email", "-").strip()
        touch_history = p.get("Touch History", "").strip()
        last_touch_str = p.get("Last Touch", "-").strip()

        if conn_status != "pending":
            continue
        if email and email != "-":
            continue
        if "connect_sent" not in touch_history:
            continue

        last_touch_dt = _parse_touch_date_to_datetime(last_touch_str)
        if not last_touch_dt:
            continue
        days_since = (now - last_touch_dt).days
        if days_since < min_days:
            continue

        p["_days_since_connect"] = str(days_since)
        eligible.append(p)

    return eligible


def _extract_company_domain(prospect: Dict[str, str]) -> Optional[str]:
    """Try to extract a company domain from prospect data."""
    company = prospect.get("Company", "").strip()
    notes = prospect.get("Notes", "").strip()

    # Check notes for URLs that might contain domain
    url_match = re.search(r"https?://(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", notes)
    if url_match:
        return url_match.group(1)

    # Derive domain from company name (basic heuristic)
    if company and company != "-":
        # Clean up company name for domain guess
        clean = re.sub(r'\s*(Pte\.?\s*Ltd\.?|Ltd\.?|Inc\.?|Corp\.?|Group|Holdings?|Sdn\.?\s*Bhd\.?)\s*$', '', company, flags=re.IGNORECASE)
        clean = re.sub(r'[^a-zA-Z0-9]', '', clean).lower()
        if clean:
            return f"{clean}.com"

    return None


async def _apollo_email_lookup(
    first_name: str, last_name: str, organization: str,
    linkedin_url: str, api_key: str
) -> Optional[Dict[str, str]]:
    """Look up email via Apollo People Match API."""
    payload: Dict[str, Any] = {
        "first_name": first_name,
        "last_name": last_name,
    }
    if organization and organization != "-":
        payload["organization_name"] = organization
    if linkedin_url and linkedin_url != "TBD":
        payload["linkedin_url"] = linkedin_url

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{APOLLO_API_BASE}/people/match",
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": api_key,
            },
            json=payload,
            timeout=30.0,
        )
        if response.status_code != 200:
            return None
        data = response.json()

    person = data.get("person")
    if not person:
        return None

    email = person.get("email")
    email_status = person.get("email_status", "")

    if email and email_status == "verified":
        return {"email": email, "status": "verified", "source": "Apollo"}

    return None


async def _hunter_email_lookup(
    first_name: str, last_name: str, domain: str, api_key: str
) -> Optional[Dict[str, str]]:
    """Look up email via Hunter Email Finder API."""
    if not domain:
        return None

    params = {
        "domain": domain,
        "first_name": first_name,
        "last_name": last_name,
        "api_key": api_key,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{HUNTER_API_BASE}/email-finder",
            params=params,
            timeout=30.0,
        )
        if response.status_code != 200:
            return None
        data = response.json()

    result = data.get("data", {})
    email = result.get("email")
    confidence = result.get("confidence", 0)

    if email and confidence >= 80:
        return {
            "email": email,
            "status": f"confidence: {confidence}%",
            "source": "Hunter",
        }

    return None


# Snov.io token cache (expires after 1 hour)
_snov_token_cache: Dict[str, Any] = {"token": "", "expires_at": 0.0}


async def _snov_get_token(client_id: str, client_secret: str) -> str:
    """Get or refresh Snov.io OAuth access token."""
    now = time.monotonic()
    if _snov_token_cache["token"] and _snov_token_cache["expires_at"] > now:
        return _snov_token_cache["token"]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SNOV_API_BASE}/v1/oauth/access_token",
            json={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=30.0,
        )
        if response.status_code != 200:
            raise ValueError(f"Snov.io auth failed: {response.status_code}")
        data = response.json()

    token = data.get("access_token", "")
    expires_in = data.get("expires_in", 3600)
    _snov_token_cache["token"] = token
    _snov_token_cache["expires_at"] = now + expires_in - 60  # refresh 1 min early
    return token


async def _snov_email_lookup(
    first_name: str, last_name: str, domain: str,
    client_id: str, client_secret: str
) -> Optional[Dict[str, str]]:
    """Look up email via Snov.io Email Finder API (async two-step)."""
    if not domain:
        return None

    token = await _snov_get_token(client_id, client_secret)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Step 1: Start the search
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SNOV_API_BASE}/v2/emails-by-domain-by-name/start",
            headers=headers,
            json={
                "rows": [{"first_name": first_name, "last_name": last_name, "domain": domain}],
            },
            timeout=30.0,
        )
        if response.status_code != 200:
            return None
        data = response.json()

    task_hash = data.get("data", {}).get("task_hash")
    if not task_hash:
        return None

    # Step 2: Poll for results (up to 3 attempts, 2s apart)
    for _ in range(3):
        await asyncio.sleep(2)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SNOV_API_BASE}/v2/emails-by-domain-by-name/result",
                headers=headers,
                params={"task_hash": task_hash},
                timeout=30.0,
            )
            if response.status_code != 200:
                continue
            data = response.json()

        if data.get("status") == "completed":
            for row in data.get("data", []):
                for result in row.get("result", []):
                    email = result.get("email")
                    smtp_status = result.get("smtp_status", "")
                    if email and smtp_status == "valid":
                        return {"email": email, "status": "valid", "source": "Snov.io"}
            return None

    return None


async def _getprospect_email_lookup(
    full_name: str, company_or_domain: str, api_key: str
) -> Optional[Dict[str, str]]:
    """Look up email via GetProspect Email Finder API."""
    if not company_or_domain:
        return None

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GETPROSPECT_API_BASE}/email/find",
            headers={"apiKey": api_key},
            params={"name": full_name, "company": company_or_domain},
            timeout=30.0,
        )
        if response.status_code != 200:
            return None
        data = response.json()

    email = data.get("email")
    status = data.get("status", "")

    if email and status and status.lower() not in ("invalid", "unknown", ""):
        return {"email": email, "status": status, "source": "GetProspect"}

    return None


async def _prospeo_email_lookup(
    first_name: str, last_name: str, company: str,
    domain: Optional[str], linkedin_url: str, api_key: str
) -> Optional[Dict[str, str]]:
    """Look up email via Prospeo Enrich Person API."""
    payload: Dict[str, Any] = {"only_verified_email": True}
    data_obj: Dict[str, str] = {}

    # Prefer LinkedIn URL (highest match rate)
    if linkedin_url and linkedin_url != "TBD":
        data_obj["linkedin_url"] = linkedin_url
    else:
        data_obj["first_name"] = first_name
        data_obj["last_name"] = last_name
        if company and company != "-":
            data_obj["company_name"] = company
        if domain:
            data_obj["company_website"] = domain

    payload["data"] = data_obj

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PROSPEO_API_BASE}/enrich-person",
            headers={
                "Content-Type": "application/json",
                "X-KEY": api_key,
            },
            json=payload,
            timeout=30.0,
        )
        if response.status_code != 200:
            return None
        data = response.json()

    if data.get("error"):
        return None

    person = data.get("person", {})
    email_obj = person.get("email", {})
    email = email_obj.get("email")
    status = email_obj.get("status", "")

    if email and status == "VERIFIED":
        return {"email": email, "status": "verified", "source": "Prospeo"}

    return None


class FindEmailAdhocInput(BaseModel):
    """Input for ad-hoc single email lookup."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., description="Full name of the person (e.g., 'John Smith')", min_length=1)
    company: str = Field(default="", description="Company name (e.g., 'Acme Corp')")
    linkedin_url: str = Field(default="", description="LinkedIn profile URL (improves match rate)")
    domain: str = Field(default="", description="Company domain (e.g., 'acme.com'). Auto-derived from company if empty.")
    add_to_prospects: bool = Field(
        default=False,
        description="If true and email found, add/update the prospect in icp-prospects.md",
    )


class FindEmailsInput(BaseModel):
    """Input for email enrichment tool."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    min_days_pending: int = Field(
        default=7,
        description="Minimum days since connect_sent to be eligible (default: 7)",
        ge=1,
    )
    dry_run: bool = Field(
        default=False,
        description="If true, only show eligible prospects without calling APIs",
    )


@mcp.tool(
    name="crm_find_email",
    annotations={
        "title": "Find Email for a Single Person",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_find_email(params: FindEmailAdhocInput) -> str:
    """Ad-hoc email lookup for a single person by name + company/domain/LinkedIn URL.

    Runs the same 5-provider waterfall (Apollo -> Hunter -> Snov.io -> GetProspect -> Prospeo)
    but for one person on demand. Does NOT require the person to be in icp-prospects.md.

    Args:
        params (FindEmailAdhocInput): Lookup data containing:
            - name (str): Full name (required)
            - company (str): Company name (optional but improves results)
            - linkedin_url (str): LinkedIn URL (optional, best match rate)
            - domain (str): Company domain (optional, auto-derived from company if empty)
            - add_to_prospects (bool): If true, update icp-prospects.md Email column

    Returns:
        str: Email found with source/status, or 'not found' with providers tried.
    """
    try:
        apollo_key = os.environ.get("APOLLO_API_KEY", "")
        hunter_key = os.environ.get("HUNTER_API_KEY", "")
        snov_id = os.environ.get("SNOV_CLIENT_ID", "")
        snov_secret = os.environ.get("SNOV_CLIENT_SECRET", "")
        getprospect_key = os.environ.get("GETPROSPECT_API_KEY", "")
        prospeo_key = os.environ.get("PROSPEO_API_KEY", "")

        has_any_key = any([apollo_key, hunter_key, snov_id and snov_secret, getprospect_key, prospeo_key])
        if not has_any_key:
            return (
                "Error: No email enrichment API keys are set.\n\n"
                "**Setup:** Add to .mcp.json under hubspot-crm env (any combination):\n"
                '```json\n'
                '"APOLLO_API_KEY": "...",        // 50 free/month\n'
                '"HUNTER_API_KEY": "...",        // 25 free/month\n'
                '"SNOV_CLIENT_ID": "...",        // 50 free/month\n'
                '"SNOV_CLIENT_SECRET": "...",    // (pair with client_id)\n'
                '"GETPROSPECT_API_KEY": "...",   // 50 free/month\n'
                '"PROSPEO_API_KEY": "..."        // 100 free/month\n'
                '```'
            )

        first, last = _split_name(params.name)
        full_name = f"{first} {last}".strip()
        company = params.company
        linkedin_url = params.linkedin_url
        domain = params.domain

        # Auto-derive domain from company if not provided
        if not domain and company:
            fake_prospect = {"Company": company, "Notes": ""}
            domain = _extract_company_domain(fake_prospect) or ""

        email_result = None
        providers_tried = []

        # 1. Apollo
        if not email_result and apollo_key:
            try:
                email_result = await _apollo_email_lookup(
                    first, last, company, linkedin_url, apollo_key
                )
                providers_tried.append("Apollo")
            except Exception:
                providers_tried.append("Apollo (error)")

        # 2. Hunter
        if not email_result and hunter_key and domain:
            try:
                email_result = await _hunter_email_lookup(
                    first, last, domain, hunter_key
                )
                providers_tried.append("Hunter")
            except Exception:
                providers_tried.append("Hunter (error)")

        # 3. Snov.io
        if not email_result and snov_id and snov_secret and domain:
            try:
                email_result = await _snov_email_lookup(
                    first, last, domain, snov_id, snov_secret
                )
                providers_tried.append("Snov.io")
            except Exception:
                providers_tried.append("Snov.io (error)")

        # 4. GetProspect
        if not email_result and getprospect_key:
            try:
                email_result = await _getprospect_email_lookup(
                    full_name, domain or company, getprospect_key
                )
                providers_tried.append("GetProspect")
            except Exception:
                providers_tried.append("GetProspect (error)")

        # 5. Prospeo
        if not email_result and prospeo_key:
            try:
                email_result = await _prospeo_email_lookup(
                    first, last, company, domain or None, linkedin_url, prospeo_key
                )
                providers_tried.append("Prospeo")
            except Exception:
                providers_tried.append("Prospeo (error)")

        if email_result:
            lines = [
                f"## Email Found for {full_name}",
                "",
                f"| Field | Value |",
                f"|-------|-------|",
                f"| **Email** | {email_result['email']} |",
                f"| **Source** | {email_result['source']} |",
                f"| **Status** | {email_result['status']} |",
                f"| **Providers tried** | {', '.join(providers_tried)} |",
            ]

            # Update HubSpot if contact exists
            if linkedin_url:
                try:
                    existing = await _search_contact_by_linkedin_url(linkedin_url)
                    if existing:
                        await _make_api_request(
                            f"/crm/v3/objects/contacts/{existing['id']}",
                            method="PATCH",
                            json_data={"properties": {"email": email_result["email"]}},
                        )
                        lines.append(f"| **HubSpot** | Updated (ID: {existing['id']}) |")
                except Exception:
                    pass

            if params.add_to_prospects:
                lines.extend([
                    "",
                    f"Update `icp-prospects.md` Email column for **{full_name}** → `{email_result['email']}` (source: {email_result['source']})",
                ])

            return "\n".join(lines)
        else:
            return (
                f"## No Email Found for {full_name}\n\n"
                f"- **Company:** {company or '(not provided)'}\n"
                f"- **Domain:** {domain or '(not provided)'}\n"
                f"- **LinkedIn:** {linkedin_url or '(not provided)'}\n"
                f"- **Providers tried:** {', '.join(providers_tried)}\n\n"
                "**Tips:** Provide a LinkedIn URL or company domain for better match rates."
            )

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="crm_find_emails",
    annotations={
        "title": "Find Emails for Pending Prospects",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_find_emails(params: FindEmailsInput) -> str:
    """Find business emails for prospects with pending connections > 7 days.

    Reads icp-prospects.md, filters for prospects where:
    - Connection Status = "pending"
    - Touch History contains "connect_sent"
    - Last Touch > min_days_pending days ago
    - Email = "-" (not yet populated)

    Then enriches via waterfall: Apollo -> Hunter -> Snov.io -> GetProspect -> Prospeo.
    Only accepts verified/high-confidence emails. Updates HubSpot contact email property.

    Args:
        params (FindEmailsInput): Configuration:
            - min_days_pending (int): Days since connect_sent (default: 7)
            - dry_run (bool): If true, list eligible prospects without API calls

    Returns:
        str: Markdown report with emails found, credits used, and missed prospects.
    """
    try:
        apollo_key = os.environ.get("APOLLO_API_KEY", "")
        hunter_key = os.environ.get("HUNTER_API_KEY", "")
        snov_id = os.environ.get("SNOV_CLIENT_ID", "")
        snov_secret = os.environ.get("SNOV_CLIENT_SECRET", "")
        getprospect_key = os.environ.get("GETPROSPECT_API_KEY", "")
        prospeo_key = os.environ.get("PROSPEO_API_KEY", "")

        has_any_key = any([apollo_key, hunter_key, snov_id and snov_secret, getprospect_key, prospeo_key])
        if not has_any_key:
            return (
                "Error: No email enrichment API keys are set.\n\n"
                "**Setup:** Add to .mcp.json under hubspot-crm env (any combination):\n"
                '```json\n'
                '"APOLLO_API_KEY": "...",        // 50 free/month\n'
                '"HUNTER_API_KEY": "...",        // 25 free/month\n'
                '"SNOV_CLIENT_ID": "...",        // 50 free/month\n'
                '"SNOV_CLIENT_SECRET": "...",    // (pair with client_id)\n'
                '"GETPROSPECT_API_KEY": "...",   // 50 free/month\n'
                '"PROSPEO_API_KEY": "..."        // 100 free/month\n'
                '```'
            )

        if not ICP_PROSPECTS_PATH.exists():
            return f"Error: icp-prospects.md not found at {ICP_PROSPECTS_PATH}"

        content = ICP_PROSPECTS_PATH.read_text(encoding="utf-8")
        prospects = _parse_prospects_table(content)
        if not prospects:
            return "Error: No prospects found in icp-prospects.md table"

        eligible = _filter_email_eligible_prospects(prospects, params.min_days_pending)

        if not eligible:
            return (
                f"No eligible prospects found.\n\n"
                f"Criteria: Connection Status = pending, connect_sent > {params.min_days_pending} days ago, Email = -\n"
                f"Total prospects scanned: {len(prospects)}"
            )

        # Dry run — just list eligible prospects
        if params.dry_run:
            lines = [
                "## Email Enrichment — Dry Run",
                "",
                f"**Eligible prospects:** {len(eligible)}",
                "",
                "| # | Name | Company | Days Pending | Profile URL |",
                "|---|------|---------|-------------|-------------|",
            ]
            for p in eligible:
                lines.append(
                    f"| {p.get('#', '-')} | {p.get('Name', '-')} | "
                    f"{p.get('Company', '-')} | {p.get('_days_since_connect', '?')} | "
                    f"{p.get('Profile URL', 'TBD')} |"
                )
            keys_status = " | ".join([
                f"Apollo: {'Yes' if apollo_key else 'No'}",
                f"Hunter: {'Yes' if hunter_key else 'No'}",
                f"Snov.io: {'Yes' if snov_id and snov_secret else 'No'}",
                f"GetProspect: {'Yes' if getprospect_key else 'No'}",
                f"Prospeo: {'Yes' if prospeo_key else 'No'}",
            ])
            lines.extend([
                "",
                f"**API keys available:** {keys_status}",
                "",
                "Run again with `dry_run: false` to execute email lookups.",
            ])
            return "\n".join(lines)

        # Execute enrichment
        credits = {
            "Apollo": 0, "Hunter": 0, "Snov.io": 0,
            "GetProspect": 0, "Prospeo": 0,
        }
        limits = {
            "Apollo": APOLLO_MONTHLY_LIMIT, "Hunter": HUNTER_MONTHLY_LIMIT,
            "Snov.io": SNOV_MONTHLY_LIMIT, "GetProspect": GETPROSPECT_MONTHLY_LIMIT,
            "Prospeo": PROSPEO_MONTHLY_LIMIT,
        }
        found = []
        missed = []
        errors = []

        for p in eligible:
            name = p.get("Name", "Unknown")
            first, last = _split_name(name)
            company = p.get("Company", "")
            linkedin_url = p.get("Profile URL", "TBD")
            domain = _extract_company_domain(p)
            full_name = f"{first} {last}".strip()
            email_result = None

            # Waterfall: Apollo -> Hunter -> Snov.io -> GetProspect -> Prospeo

            # 1. Apollo
            if not email_result and apollo_key and credits["Apollo"] < limits["Apollo"]:
                try:
                    email_result = await _apollo_email_lookup(
                        first, last, company, linkedin_url, apollo_key
                    )
                    credits["Apollo"] += 1
                except Exception as e:
                    errors.append(f"Apollo error for {name}: {e}")

            # 2. Hunter
            if not email_result and hunter_key and credits["Hunter"] < limits["Hunter"]:
                try:
                    email_result = await _hunter_email_lookup(
                        first, last, domain or "", hunter_key
                    )
                    credits["Hunter"] += 1
                except Exception as e:
                    errors.append(f"Hunter error for {name}: {e}")

            # 3. Snov.io
            if not email_result and snov_id and snov_secret and credits["Snov.io"] < limits["Snov.io"]:
                try:
                    email_result = await _snov_email_lookup(
                        first, last, domain or "", snov_id, snov_secret
                    )
                    credits["Snov.io"] += 1
                except Exception as e:
                    errors.append(f"Snov.io error for {name}: {e}")

            # 4. GetProspect
            if not email_result and getprospect_key and credits["GetProspect"] < limits["GetProspect"]:
                try:
                    email_result = await _getprospect_email_lookup(
                        full_name, domain or company, getprospect_key
                    )
                    credits["GetProspect"] += 1
                except Exception as e:
                    errors.append(f"GetProspect error for {name}: {e}")

            # 5. Prospeo
            if not email_result and prospeo_key and credits["Prospeo"] < limits["Prospeo"]:
                try:
                    email_result = await _prospeo_email_lookup(
                        first, last, company, domain, linkedin_url, prospeo_key
                    )
                    credits["Prospeo"] += 1
                except Exception as e:
                    errors.append(f"Prospeo error for {name}: {e}")

            if email_result:
                found.append({
                    "number": p.get("#", "-"),
                    "name": name,
                    "email": email_result["email"],
                    "source": email_result["source"],
                    "status": email_result["status"],
                    "linkedin_url": linkedin_url,
                })
                # Update HubSpot contact email
                try:
                    existing = await _search_contact_by_linkedin_url(linkedin_url)
                    if existing:
                        await _make_api_request(
                            f"/crm/v3/objects/contacts/{existing['id']}",
                            method="PATCH",
                            json_data={"properties": {"email": email_result["email"]}},
                        )
                except Exception as e:
                    errors.append(f"HubSpot update error for {name}: {e}")
            else:
                missed.append({
                    "number": p.get("#", "-"),
                    "name": name,
                    "company": company,
                })

            # Stop if all credit pools exhausted
            all_exhausted = True
            if apollo_key and credits["Apollo"] < limits["Apollo"]:
                all_exhausted = False
            if hunter_key and credits["Hunter"] < limits["Hunter"]:
                all_exhausted = False
            if snov_id and snov_secret and credits["Snov.io"] < limits["Snov.io"]:
                all_exhausted = False
            if getprospect_key and credits["GetProspect"] < limits["GetProspect"]:
                all_exhausted = False
            if prospeo_key and credits["Prospeo"] < limits["Prospeo"]:
                all_exhausted = False
            if all_exhausted:
                errors.append("All credit limits reached — stopping enrichment")
                break

        # Build report
        lines = [
            "## Email Enrichment Results",
            "",
        ]

        if found:
            lines.extend([
                "### Emails Found",
                "",
                "| # | Name | Email | Source | Status |",
                "|---|------|-------|--------|--------|",
            ])
            for f in found:
                lines.append(
                    f"| {f['number']} | {f['name']} | {f['email']} | "
                    f"{f['source']} | {f['status']} |"
                )
            lines.append("")

        if missed:
            lines.extend([
                "### Not Found",
                "",
                "| # | Name | Company |",
                "|---|------|---------|",
            ])
            for m in missed:
                lines.append(f"| {m['number']} | {m['name']} | {m['company']} |")
            lines.append("")

        credit_lines = []
        for provider, used in credits.items():
            if used > 0 or (provider == "Apollo" and apollo_key) or \
               (provider == "Hunter" and hunter_key) or \
               (provider == "Snov.io" and snov_id) or \
               (provider == "GetProspect" and getprospect_key) or \
               (provider == "Prospeo" and prospeo_key):
                credit_lines.append(f"- **{provider} credits used:** {used}/{limits[provider]}")

        lines.extend([
            "### Summary",
            "",
            f"- **Found:** {len(found)} emails",
            f"- **Missed:** {len(missed)} prospects",
            *credit_lines,
        ])

        if errors:
            lines.extend(["", "### Errors", ""])
            for err in errors:
                lines.append(f"- {err}")

        if found:
            lines.extend([
                "",
                "### Next Steps",
                "",
                "Update `icp-prospects.md` Email column for found emails.",
                "HubSpot contacts have been updated automatically.",
            ])

        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


@mcp.tool(
    name="crm_pull_emails",
    annotations={
        "title": "Pull Emails from HubSpot to Prospects File",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def crm_pull_emails() -> str:
    """Reverse sync: pull emails from HubSpot contacts back to icp-prospects.md.

    Searches HubSpot for contacts that have both a linkedin_profile and email set.
    Cross-references against icp-prospects.md by Profile URL.
    Reports which prospects have emails in HubSpot but not in the local file.

    Use this to catch emails added manually in HubSpot or via other integrations.

    Returns:
        str: Markdown report listing prospects whose Email column should be updated.
    """
    try:
        if not ICP_PROSPECTS_PATH.exists():
            return f"Error: icp-prospects.md not found at {ICP_PROSPECTS_PATH}"

        content = ICP_PROSPECTS_PATH.read_text(encoding="utf-8")
        prospects = _parse_prospects_table(content)
        if not prospects:
            return "Error: No prospects found in icp-prospects.md table"

        # Build lookup: linkedin_url -> prospect row
        prospects_missing_email = {}
        for p in prospects:
            email = p.get("Email", "-").strip()
            url = p.get("Profile URL", "").strip()
            if url and url != "TBD" and (not email or email == "-"):
                prospects_missing_email[url] = p

        if not prospects_missing_email:
            return "All prospects with LinkedIn URLs already have emails populated."

        # Query HubSpot for contacts with email set
        updates = []
        all_contacts = []
        after = None

        for _ in range(10):
            data = await _make_api_request(
                "/crm/v3/objects/contacts/search",
                method="POST",
                json_data={
                    "filterGroups": [{
                        "filters": [
                            {
                                "propertyName": "linkedin_profile",
                                "operator": "HAS_PROPERTY",
                            },
                            {
                                "propertyName": "email",
                                "operator": "HAS_PROPERTY",
                            },
                        ]
                    }],
                    "properties": ["firstname", "lastname", "email", "linkedin_profile"],
                    "limit": 100,
                    "after": after or 0,
                },
            )
            results = data.get("results", [])
            all_contacts.extend(results)

            paging = data.get("paging", {})
            after = paging.get("next", {}).get("after")
            if not after:
                break

        # Cross-reference
        for contact in all_contacts:
            props = contact.get("properties", {})
            linkedin_url = props.get("linkedin_profile", "")
            email = props.get("email", "")

            if linkedin_url in prospects_missing_email and email:
                p = prospects_missing_email[linkedin_url]
                updates.append({
                    "number": p.get("#", "-"),
                    "name": p.get("Name", "Unknown"),
                    "email": email,
                    "linkedin_url": linkedin_url,
                })

        if not updates:
            return (
                f"No new emails found in HubSpot.\n\n"
                f"Checked {len(all_contacts)} HubSpot contacts against "
                f"{len(prospects_missing_email)} prospects missing emails."
            )

        lines = [
            "## Emails Found in HubSpot (Reverse Sync)",
            "",
            "These prospects have emails in HubSpot but not in `icp-prospects.md`:",
            "",
            "| # | Name | Email | LinkedIn URL |",
            "|---|------|-------|-------------|",
        ]
        for u in updates:
            lines.append(
                f"| {u['number']} | {u['name']} | {u['email']} | {u['linkedin_url']} |"
            )
        lines.extend([
            "",
            f"**Total:** {len(updates)} emails to sync back to icp-prospects.md",
            "",
            "Update the Email column in `icp-prospects.md` for these prospects.",
        ])

        return "\n".join(lines)

    except Exception as e:
        return _handle_api_error(e)


if __name__ == "__main__":
    mcp.run()
