#!/usr/bin/env python3
"""Safely update skills installed in $CODEX_HOME/skills from a GitHub repo.

Workflow:
1) Resolve target skill directories
2) Backup local state paths
3) Remove old skill directories
4) Reinstall latest versions via system skill-installer
5) Restore local state paths
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


DEFAULT_REF = "main"
DEFAULT_STATE_PATHS = [
    "linkedin-core/references",
    "linkedin-core/shared/logs",
    "linkedin-core/shared/linkedin-account-config.md",
    "references",
    "shared/logs",
]


class UpdateError(Exception):
    """Raised for controlled update failures."""


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).resolve()


def skills_root() -> Path:
    return codex_home() / "skills"


def github_json(url: str, token: str | None) -> object:
    req = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "codex-skills-maintainer",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def detect_repo_skill_dirs(repo: str, ref: str, token: str | None) -> list[str]:
    root_url = f"https://api.github.com/repos/{repo}/contents?ref={quote(ref)}"
    try:
        root_entries = github_json(root_url, token)
    except HTTPError as exc:
        raise UpdateError(f"Failed to read repo root via GitHub API ({exc.code}).") from exc
    except URLError as exc:
        raise UpdateError(f"Failed to reach GitHub API: {exc.reason}") from exc

    if not isinstance(root_entries, list):
        raise UpdateError("Unexpected GitHub API response for repo root.")

    candidate_dirs = [e["name"] for e in root_entries if isinstance(e, dict) and e.get("type") == "dir"]
    skill_dirs: list[str] = []

    for d in candidate_dirs:
        if d.startswith("."):
            continue
        skill_url = f"https://api.github.com/repos/{repo}/contents/{quote(d)}/SKILL.md?ref={quote(ref)}"
        try:
            github_json(skill_url, token)
            skill_dirs.append(d)
        except HTTPError as exc:
            if exc.code == 404:
                continue
            raise UpdateError(f"Failed probing {d}/SKILL.md via GitHub API ({exc.code}).") from exc
        except URLError as exc:
            raise UpdateError(f"Failed probing {d}/SKILL.md: {exc.reason}") from exc

    return sorted(skill_dirs)


def installed_skill_dirs(root: Path) -> list[str]:
    if not root.exists():
        return []
    items: list[str] = []
    for d in root.iterdir():
        if not d.is_dir() or d.name.startswith("."):
            continue
        if (d / "SKILL.md").exists():
            items.append(d.name)
    return sorted(items)


def detect_current_skill_name(script_path: Path, root: Path) -> str | None:
    parts = script_path.resolve().parts
    root_parts = root.resolve().parts
    if len(parts) <= len(root_parts):
        return None
    if parts[: len(root_parts)] != root_parts:
        return None
    return parts[len(root_parts)]


def ensure_relative_path(path_value: str) -> str:
    p = Path(path_value)
    if p.is_absolute() or str(p).startswith(".."):
        raise UpdateError(f"State path must be relative to skills root: {path_value}")
    return str(p).replace("\\", "/")


def copy_path(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def backup_state(root: Path, state_paths: Iterable[str], backup_root: Path) -> list[str]:
    copied: list[str] = []
    for rel in state_paths:
        src = root / rel
        if not src.exists():
            continue
        dst = backup_root / rel
        copy_path(src, dst)
        copied.append(rel)
    return copied


def restore_state(root: Path, backup_root: Path, copied_paths: Iterable[str]) -> list[str]:
    restored: list[str] = []
    for rel in copied_paths:
        src = backup_root / rel
        if not src.exists():
            continue
        dst = root / rel
        copy_path(src, dst)
        restored.append(rel)
    return restored


def run_installer(installer: Path, repo: str, ref: str, skill: str, dest_root: Path) -> None:
    cmd = [
        sys.executable,
        str(installer),
        "--repo",
        repo,
        "--path",
        skill,
        "--ref",
        ref,
        "--dest",
        str(dest_root),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        stdout = proc.stdout.strip()
        detail = stderr or stdout or "Unknown installer failure"
        raise UpdateError(f"Install failed for '{skill}': {detail}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update skills installed in $CODEX_HOME/skills.")
    parser.add_argument("--repo", required=True, help="GitHub repo in owner/repo format")
    parser.add_argument("--ref", default=DEFAULT_REF, help=f"Git ref/branch/tag (default: {DEFAULT_REF})")
    parser.add_argument("--skills", nargs="+", help="Specific skill directory names to update")
    parser.add_argument("--dest", help="Override destination skills root (default: $CODEX_HOME/skills)")
    parser.add_argument("--state-path", action="append", default=[], help="Additional relative state path to backup/restore")
    parser.add_argument("--no-default-state", action="store_true", help="Disable default state backup paths")
    parser.add_argument("--backup-dir", help="Backup directory (default: $CODEX_HOME/backups/skills-update-<timestamp>)")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without changing anything")
    parser.add_argument("--include-self", action="store_true", help="Also update the running maintainer skill if targeted")
    parser.add_argument("--json", action="store_true", help="Output final summary as JSON")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

    if "/" not in args.repo or len([p for p in args.repo.split("/") if p]) != 2:
        raise UpdateError("--repo must be in owner/repo format (e.g. org/repo).")

    root = Path(args.dest).resolve() if args.dest else skills_root()
    installer = (root / ".system" / "skill-installer" / "scripts" / "install-skill-from-github.py").resolve()

    if not root.exists():
        raise UpdateError(f"Skills root not found: {root}")
    if not installer.exists():
        raise UpdateError(f"System installer script not found: {installer}")

    repo_skill_dirs = detect_repo_skill_dirs(args.repo, args.ref, token)
    installed = installed_skill_dirs(root)

    if args.skills:
        requested = sorted(set(args.skills))
        missing = [s for s in requested if s not in repo_skill_dirs]
        if missing:
            raise UpdateError(f"Requested skills not found in repo/ref: {', '.join(missing)}")
        targets = requested
    else:
        targets = [s for s in installed if s in repo_skill_dirs]

    current_skill = detect_current_skill_name(Path(__file__), root)
    skipped_self = False
    if not args.include_self and current_skill and current_skill in targets:
        targets = [t for t in targets if t != current_skill]
        skipped_self = True

    if not targets:
        raise UpdateError("No target skills to update. Provide --skills or ensure matching skills are installed.")

    state_paths = [] if args.no_default_state else list(DEFAULT_STATE_PATHS)
    state_paths.extend(args.state_path)
    state_paths = [ensure_relative_path(p) for p in state_paths]

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = Path(args.backup_dir).resolve() if args.backup_dir else codex_home() / "backups" / f"skills-update-{timestamp}"

    summary = {
        "skills_root": str(root),
        "repo": args.repo,
        "ref": args.ref,
        "targets": targets,
        "skipped_self": skipped_self,
        "current_skill": current_skill,
        "backup_dir": str(backup_root),
        "state_paths": state_paths,
        "dry_run": args.dry_run,
    }

    if args.dry_run:
        print(json.dumps(summary, indent=2))
        return 0

    backup_root.mkdir(parents=True, exist_ok=True)
    copied = backup_state(root, state_paths, backup_root)

    updated: list[str] = []
    try:
        for skill in targets:
            skill_dir = root / skill
            if skill_dir.exists():
                shutil.rmtree(skill_dir)
            run_installer(installer, args.repo, args.ref, skill, root)
            updated.append(skill)
    finally:
        restored = restore_state(root, backup_root, copied)

    summary["copied_state_paths"] = copied
    summary["restored_state_paths"] = restored
    summary["updated_skills"] = updated

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print("")
        print("Codex skills update complete.")
        print(f"Repo/ref: {args.repo}@{args.ref}")
        print(f"Updated skills ({len(updated)}): {', '.join(updated)}")
        if skipped_self and current_skill:
            print(f"Skipped self-update for running skill: {current_skill} (use --include-self to include)")
        print(f"Backup directory: {backup_root}")
        if copied:
            print(f"State paths backed up/restored: {', '.join(copied)}")
        else:
            print("No matching state paths found to backup.")
        print("Restart Codex to load updated skills.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except UpdateError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
