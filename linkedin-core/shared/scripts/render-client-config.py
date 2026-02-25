#!/usr/bin/env python3
"""
Render tokenized skill files from a client profile.

Usage:
  python linkedin-core/shared/scripts/render-client-config.py --profile linkedin-core/references/client-profile.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".ps1",
    ".py",
    ".sh",
    ".bat",
    ".csv",
    ".json",
    ".yaml",
    ".yml",
}


REQUIRED_KEYS = [
    "CLIENT_BRAND_PRIMARY",
    "CLIENT_BRAND_PRIMARY_SLUG",
    "CLIENT_BRAND_SECONDARY",
    "CLIENT_BRAND_SECONDARY_SLUG",
    "CLIENT_COMMUNITY_NAME",
    "CLIENT_COMMUNITY_SLUG",
    "CLIENT_FOUNDER_NAME",
    "CLIENT_GSHEETS_CREDENTIALS_FILE",
    "CLIENT_GSHEETS_PROJECT_ID",
    "CLIENT_GSHEETS_SERVICE_ACCOUNT_EMAIL",
    "CLIENT_LINKEDIN_HANDLE",
    "CLIENT_TIMEZONE",
    "CLIENT_TARGET_GEO",
    "CLIENT_TARGET_GEO_LIST",
    "CLIENT_WORKSPACE_ROOT",
    "CLIENT_LOCAL_USER",
]


SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "node_modules",
}


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def load_profile(profile_path: Path) -> dict[str, str]:
    raw = json.loads(profile_path.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED_KEYS if k not in raw]
    if missing:
        raise ValueError(f"Missing required profile keys: {', '.join(missing)}")
    return {f"{{{{{k}}}}}": str(v) for k, v in raw.items()}


def render(root: Path, mapping: dict[str, str], dry_run: bool) -> tuple[int, int]:
    files_scanned = 0
    files_updated = 0
    for path in iter_text_files(root):
        files_scanned += 1
        original = path.read_text(encoding="utf-8", errors="replace")
        updated = original
        for token, value in mapping.items():
            updated = updated.replace(token, value)
        if updated != original:
            files_updated += 1
            if not dry_run:
                path.write_text(updated, encoding="utf-8")
    return files_scanned, files_updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        default="references/client-profile.json",
        help="Path to client profile JSON file",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to render",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute changes but do not write files",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    profile_path = Path(args.profile).resolve()

    if not profile_path.exists():
        raise FileNotFoundError(f"Profile file not found: {profile_path}")

    mapping = load_profile(profile_path)
    files_scanned, files_updated = render(root, mapping, args.dry_run)

    mode = "DRY RUN" if args.dry_run else "APPLIED"
    print(f"[{mode}] scanned={files_scanned} updated={files_updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
