#!/usr/bin/env python3
"""
CLI wrapper for HubSpot CRM sync operations.

Fallback for when MCP tools aren't loaded in Codex Code session.
Reuses the same logic as hubspot_mcp.py but callable via command line.

Usage:
    # Sync specific prospects by name (reads from icp-prospects.md)
    python crm-integration/cli_sync.py sync "Hsien Naidu" "Bhavana Ravindran" "Daniel Yew"

    # Sync all changed prospects (reads names from stdin, one per line)
    echo "Hsien Naidu" | python crm-integration/cli_sync.py sync -

    # Get pipeline summary
    python crm-integration/cli_sync.py pipeline

    # Look up a contact
    python crm-integration/cli_sync.py lookup "Hsien Naidu"
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Load env from .env file if present (for API keys)
ENV_FILE = Path(__file__).parent.parent / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

# Also load from .mcp.json env block as fallback
MCP_JSON = Path(__file__).parent.parent / ".mcp.json"
if MCP_JSON.exists():
    import json
    try:
        config = json.loads(MCP_JSON.read_text())
        env_vars = config.get("mcpServers", {}).get("hubspot-crm", {}).get("env", {})
        for key, value in env_vars.items():
            os.environ.setdefault(key, value)
    except (json.JSONDecodeError, KeyError):
        pass

# Now import the MCP server module (env vars must be set first)
sys.path.insert(0, str(Path(__file__).parent))
from hubspot_mcp import (
    _parse_prospects_table,
    _prospect_to_hubspot_properties,
    _create_or_update_contact,
    _ensure_company_association,
    _ensure_deal,
    _determine_pipeline_stage,
    _search_contact_by_linkedin_url,
    _make_api_request,
    _handle_api_error,
    _split_name,
    ICP_PROSPECTS_PATH,
    PIPELINE_STAGES,
)


def _read_prospects_file():
    """Read and parse icp-prospects.md."""
    if not ICP_PROSPECTS_PATH.exists():
        print(f"ERROR: Prospects file not found: {ICP_PROSPECTS_PATH}", file=sys.stderr)
        sys.exit(1)
    content = ICP_PROSPECTS_PATH.read_text(encoding="utf-8")
    return _parse_prospects_table(content)


def _find_prospect_by_name(prospects, name):
    """Find a prospect by name (case-insensitive partial match)."""
    name_lower = name.lower().strip()
    # Exact match first
    for p in prospects:
        if p.get("Name", "").lower().strip() == name_lower:
            return p
    # Partial match
    for p in prospects:
        if name_lower in p.get("Name", "").lower():
            return p
    return None


async def sync_prospects(names):
    """Sync specific prospects by name."""
    prospects = _read_prospects_file()
    results = []

    for name in names:
        prospect = _find_prospect_by_name(prospects, name)
        if not prospect:
            results.append(f"NOT FOUND: '{name}' — not in icp-prospects.md")
            continue

        linkedin_url = prospect.get("Profile URL", "")
        if not linkedin_url or linkedin_url == "TBD":
            results.append(f"SKIPPED: {prospect['Name']} — no LinkedIn URL")
            continue

        try:
            properties = _prospect_to_hubspot_properties(prospect)
            result = await _create_or_update_contact(properties)
            action = result.get("_action", "synced")
            contact_id = result["id"]

            # Associate company
            company_name = prospect.get("Company", "")
            company_id = await _ensure_company_association(contact_id, company_name)

            # Determine pipeline stage
            touches_str = prospect.get("Touches", "0").strip()
            try:
                touches = int(touches_str.replace("+", ""))
            except ValueError:
                touches = 0
            conn_status = prospect.get("Connection Status", "none")
            touch_history = prospect.get("Touch History", "-")
            stage = _determine_pipeline_stage(touches, conn_status, touch_history)

            # Create/update deal
            deal_id = await _ensure_deal(contact_id, stage, prospect["Name"])

            line = f"OK: {prospect['Name']} — {action} | Stage: {stage} | Touches: {touches} | Connection: {conn_status}"
            if company_id:
                line += f" | Company: {company_name}"
            results.append(line)

        except Exception as e:
            results.append(f"ERROR: {prospect['Name']} — {e}")

    return results


async def get_pipeline():
    """Get pipeline summary from HubSpot."""
    try:
        # Search all contacts with linkedin_profile set
        all_contacts = []
        has_more = True
        after = None

        while has_more:
            body = {
                "filterGroups": [{
                    "filters": [{
                        "propertyName": "linkedin_profile",
                        "operator": "HAS_PROPERTY",
                    }]
                }],
                "properties": ["firstname", "lastname", "lead_classification",
                               "touch_count", "linkedin_connection_status"],
                "limit": 100,
            }
            if after:
                body["after"] = after

            data = await _make_api_request("/crm/v3/objects/contacts/search", method="POST", json_data=body)
            all_contacts.extend(data.get("results", []))
            paging = data.get("paging", {}).get("next", {})
            after = paging.get("after")
            has_more = bool(after)

        # Count by classification
        counts = {"PROSPECT": 0, "PEER": 0, "THOUGHT LEADER": 0, "OTHER": 0}
        for c in all_contacts:
            cls = c.get("properties", {}).get("lead_classification", "OTHER")
            counts[cls] = counts.get(cls, 0) + 1

        print(f"\nHubSpot Pipeline Summary ({len(all_contacts)} total contacts)")
        print("=" * 50)
        for cls, count in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  {cls}: {count}")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)


async def lookup_contact(name):
    """Look up a contact in HubSpot by name."""
    prospects = _read_prospects_file()
    prospect = _find_prospect_by_name(prospects, name)

    if prospect:
        linkedin_url = prospect.get("Profile URL", "")
        if linkedin_url and linkedin_url != "TBD":
            contact = await _search_contact_by_linkedin_url(linkedin_url)
            if contact:
                props = contact.get("properties", {})
                print(f"\nHubSpot Contact: {props.get('firstname', '')} {props.get('lastname', '')}")
                print("=" * 50)
                for key, val in sorted(props.items()):
                    if val and key not in ("hs_object_id", "createdate", "lastmodifieddate"):
                        print(f"  {key}: {val}")
                return
    print(f"Contact '{name}' not found in HubSpot")


def main():
    parser = argparse.ArgumentParser(description="HubSpot CRM CLI sync")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # sync command
    sync_parser = subparsers.add_parser("sync", help="Sync prospects by name")
    sync_parser.add_argument("names", nargs="+", help="Prospect names to sync (use '-' for stdin)")

    # pipeline command
    subparsers.add_parser("pipeline", help="Show pipeline summary")

    # lookup command
    lookup_parser = subparsers.add_parser("lookup", help="Look up a contact")
    lookup_parser.add_argument("name", help="Contact name to look up")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check API key
    if not os.environ.get("HUBSPOT_API_KEY"):
        print("ERROR: HUBSPOT_API_KEY not set. Check .mcp.json or .env file.", file=sys.stderr)
        sys.exit(1)

    if args.command == "sync":
        names = args.names
        if names == ["-"]:
            names = [line.strip() for line in sys.stdin if line.strip()]

        results = asyncio.run(sync_prospects(names))
        print(f"\nCRM Sync Results ({len(results)} records)")
        print("=" * 50)
        for r in results:
            print(f"  {r}")
        print()

    elif args.command == "pipeline":
        asyncio.run(get_pipeline())

    elif args.command == "lookup":
        asyncio.run(lookup_contact(args.name))


if __name__ == "__main__":
    main()
