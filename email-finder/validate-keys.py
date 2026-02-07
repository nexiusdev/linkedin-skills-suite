#!/usr/bin/env python3
"""
Validate email enrichment API keys by making a lightweight test call to each provider.
Uses a known test lookup (Tim Cook at Apple) to confirm authentication works.
Exit code 0 if at least one provider passes, 1 if all fail or none configured.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import httpx

# Test data — public figure, high match rate
TEST_FIRST = "Tim"
TEST_LAST = "Cook"
TEST_COMPANY = "Apple"
TEST_DOMAIN = "apple.com"
TEST_LINKEDIN = "https://www.linkedin.com/in/timcook/"

PROVIDERS = {
    "Apollo": {"credits": 50, "env": ["APOLLO_API_KEY"]},
    "Hunter": {"credits": 25, "env": ["HUNTER_API_KEY"]},
    "Snov.io": {"credits": 50, "env": ["SNOV_CLIENT_ID", "SNOV_CLIENT_SECRET"]},
    "GetProspect": {"credits": 50, "env": ["GETPROSPECT_API_KEY"]},
    "Prospeo": {"credits": 100, "env": ["PROSPEO_API_KEY"]},
}


async def validate_apollo(api_key: str) -> tuple[bool, str]:
    """Test Apollo People Match API."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.apollo.io/api/v1/people/match",
            headers={"Content-Type": "application/json", "X-Api-Key": api_key},
            json={"first_name": TEST_FIRST, "last_name": TEST_LAST,
                  "organization_name": TEST_COMPANY},
            timeout=15.0,
        )
    if resp.status_code == 200:
        return True, "authenticated"
    if resp.status_code == 401:
        return False, "invalid API key"
    return False, f"HTTP {resp.status_code}"


async def validate_hunter(api_key: str) -> tuple[bool, str]:
    """Test Hunter Email Finder API."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.hunter.io/v2/account",
            params={"api_key": api_key},
            timeout=15.0,
        )
    if resp.status_code == 200:
        return True, "authenticated"
    if resp.status_code == 401:
        return False, "invalid API key"
    return False, f"HTTP {resp.status_code}"


async def validate_snov(client_id: str, client_secret: str) -> tuple[bool, str]:
    """Test Snov.io OAuth token generation."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.snov.io/v1/oauth/access_token",
            json={"grant_type": "client_credentials",
                  "client_id": client_id, "client_secret": client_secret},
            timeout=15.0,
        )
    if resp.status_code == 200:
        data = resp.json()
        if data.get("access_token"):
            return True, "authenticated"
        return False, "no token returned"
    return False, f"HTTP {resp.status_code}"


async def validate_getprospect(api_key: str) -> tuple[bool, str]:
    """Test GetProspect Email Find API."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.getprospect.com/public/v1/email/find",
            headers={"apiKey": api_key},
            params={"name": f"{TEST_FIRST} {TEST_LAST}", "company": TEST_DOMAIN},
            timeout=15.0,
        )
    if resp.status_code == 200:
        return True, "authenticated"
    if resp.status_code == 401:
        return False, "invalid API key"
    return False, f"HTTP {resp.status_code}"


async def validate_prospeo(api_key: str) -> tuple[bool, str]:
    """Test Prospeo Enrich Person API."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.prospeo.io/enrich-person",
            headers={"Content-Type": "application/json", "X-KEY": api_key},
            json={"data": {"linkedin_url": TEST_LINKEDIN}, "only_verified_email": True},
            timeout=15.0,
        )
    if resp.status_code == 200:
        return True, "authenticated"
    if resp.status_code in (401, 403):
        return False, "invalid API key"
    return False, f"HTTP {resp.status_code}"


async def main():
    # Try loading keys from .mcp.json first, fall back to env vars
    mcp_json_path = Path(__file__).resolve().parent.parent / ".mcp.json"
    mcp_env = {}
    if mcp_json_path.exists():
        try:
            config = json.loads(mcp_json_path.read_text(encoding="utf-8"))
            mcp_env = config.get("mcpServers", {}).get("hubspot-crm", {}).get("env", {})
        except (json.JSONDecodeError, KeyError):
            pass

    def get_key(name: str) -> str:
        return mcp_env.get(name, "") or os.environ.get(name, "")

    print("=" * 55)
    print("  Email Enrichment API Key Validation")
    print("=" * 55)
    print()

    results = {}
    total_credits = 0
    active_count = 0

    # Apollo
    key = get_key("APOLLO_API_KEY")
    if key:
        ok, msg = await validate_apollo(key)
        results["Apollo"] = (ok, msg)
        if ok:
            total_credits += 50
            active_count += 1
    else:
        results["Apollo"] = (None, "not configured")

    # Hunter
    key = get_key("HUNTER_API_KEY")
    if key:
        ok, msg = await validate_hunter(key)
        results["Hunter"] = (ok, msg)
        if ok:
            total_credits += 25
            active_count += 1
    else:
        results["Hunter"] = (None, "not configured")

    # Snov.io
    cid = get_key("SNOV_CLIENT_ID")
    csec = get_key("SNOV_CLIENT_SECRET")
    if cid and csec:
        ok, msg = await validate_snov(cid, csec)
        results["Snov.io"] = (ok, msg)
        if ok:
            total_credits += 50
            active_count += 1
    else:
        results["Snov.io"] = (None, "not configured")

    # GetProspect
    key = get_key("GETPROSPECT_API_KEY")
    if key:
        ok, msg = await validate_getprospect(key)
        results["GetProspect"] = (ok, msg)
        if ok:
            total_credits += 50
            active_count += 1
    else:
        results["GetProspect"] = (None, "not configured")

    # Prospeo
    key = get_key("PROSPEO_API_KEY")
    if key:
        ok, msg = await validate_prospeo(key)
        results["Prospeo"] = (ok, msg)
        if ok:
            total_credits += 100
            active_count += 1
    else:
        results["Prospeo"] = (None, "not configured")

    # Display results
    for provider, (ok, msg) in results.items():
        credits = PROVIDERS[provider]["credits"]
        if ok is True:
            print(f"  PASS  {provider} ({credits} credits/month) — {msg}")
        elif ok is False:
            print(f"  FAIL  {provider} — {msg}")
        else:
            print(f"  SKIP  {provider} — {msg}")

    print()
    print("-" * 55)

    if active_count > 0:
        print(f"  {active_count} provider(s) active | {total_credits} lookups/month")
        print()
        print("  Waterfall order: Apollo > Hunter > Snov.io > GetProspect > Prospeo")
        print("  Each miss falls through to the next active provider.")
    else:
        print("  No providers configured or validated.")
        print()
        print("  Add API keys to .mcp.json under hubspot-crm.env")
        print("  See email-finder/skill.md for signup links.")

    print()

    # Return appropriate exit code
    sys.exit(0 if active_count > 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
