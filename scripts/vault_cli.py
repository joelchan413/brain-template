#!/usr/bin/env python3
"""
Vault CLI - Master Command-Line Interface for Obsidian PKM Vault
Provides unified access to health audits, concept stubs generation,
Anki flashcard exports, daily note creation, and weekly retrospectives.
"""

import sys
import argparse
from datetime import date, datetime
from pathlib import Path

# Ensure stdout handles UTF-8 safely on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Import sibling modules
from vault_health import scan_vault
from generate_concept_stubs import create_stubs
from anki_exporter import scan_and_export_anki
from weekly_review import generate_weekly_review
from daily_shutdown import run_shutdown
from unslop import run_unslop_audit

def handle_daily_note_creation(vault_root: Path, target_date_str: str) -> None:
    """Scaffolds a daily note from Template-Daily-Note.md if it doesn't exist."""
    daily_dir = vault_root / "01-Daily"
    templates_dir = vault_root / "06-Templates"
    daily_dir.mkdir(parents=True, exist_ok=True)

    dest_file = daily_dir / f"{target_date_str}.md"
    if dest_file.exists():
        print(f"⚠️ Daily note for `{target_date_str}` already exists at: `{dest_file.relative_to(vault_root)}`")
        return

    template_file = templates_dir / "Template-Daily-Note.md"
    if template_file.exists():
        template_content = template_file.read_text(encoding='utf-8')
    else:
        template_content = f"""---
title: "{target_date_str}"
type: daily
date: {target_date_str}
tags: [daily, study-log]
---

# 📅 {target_date_str} — Daily Plan & Study Log

## 🎯 Top Priorities
- [ ] 

## 🏛️ Schedule & Tasks
| Time | Category | Event / Course | Location / Link | Status |
| :--- | :--- | :--- | :--- | :--- |

## 🔄 Daily Reflection
- **What went well:** 
- **What got delayed:** 
"""

    # Populate date variables
    parsed_dt = datetime.strptime(target_date_str, "%Y-%m-%d")
    day_name = parsed_dt.strftime("%A, %B %d, %Y")
    populated = template_content.replace("{{date}}", target_date_str).replace("{{title}}", target_date_str)
    
    dest_file.write_text(populated, encoding='utf-8')
    print(f"✅ Created new daily note: `{dest_file.relative_to(vault_root)}` ({day_name})")

def handle_vault_stats(vault_root: Path) -> None:
    """Displays key statistics about notes and vault composition."""
    all_notes = list(vault_root.rglob("*.md"))
    daily_notes = list((vault_root / "01-Daily").glob("*.md")) if (vault_root / "01-Daily").exists() else []
    courses = [d.name for d in (vault_root / "02-Courses").iterdir() if d.is_dir()] if (vault_root / "02-Courses").exists() else []
    concepts = list((vault_root / "03-Concepts").glob("*.md")) if (vault_root / "03-Concepts").exists() else []
    mocs = list((vault_root / "05-MOCs").glob("*.md")) if (vault_root / "05-MOCs").exists() else []
    templates = list((vault_root / "06-Templates").glob("*.md")) if (vault_root / "06-Templates").exists() else []

    print("=" * 60)
    print("📊 VAULT STATISTICS & METRICS")
    print("=" * 60)
    print(f"📁 Vault Root           : {vault_root}")
    print(f"📄 Total Markdown Notes : {len(all_notes)}")
    print(f"📅 Daily Notes Logged   : {len(daily_notes)}")
    print(f"🎓 Active Courses       : {len(courses)} ({', '.join(courses)})")
    print(f"💡 Concept Notes        : {len(concepts)}")
    print(f"🗺️ Maps of Content (MOCs): {len(mocs)}")
    print(f"📐 Templates Available  : {len(templates)}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(
        prog="vault",
        description="Master CLI utility suite for Obsidian PKM Vault."
    )
    parser.add_argument("--vault", default=".", help="Path to the vault root directory (default: .)")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 1. Health
    subparsers.add_parser("health", help="Run link integrity, orphan notes, and metadata audit.")

    # 2. Stats
    subparsers.add_parser("stats", help="Display overall vault metrics and note counts.")

    # 3. Stubs
    stubs_parser = subparsers.add_parser("stubs", help="Scaffold notes for unresolved wikilinks.")
    stubs_parser.add_argument("--dest", default="03-Concepts", help="Subdirectory for concepts.")
    stubs_parser.add_argument("--dry-run", action="store_true", help="Preview stubs without writing.")
    stubs_parser.add_argument("--route-all", action="store_true", help="Route course notes to course folders.")
    stubs_parser.add_argument("--target", default=None, help="Generate stub for a single target link.")

    # 4. Anki
    anki_parser = subparsers.add_parser("anki", help="Export active recall quiz cards to Anki TSV.")
    anki_parser.add_argument("--out", default="exports/anki_cards.tsv", help="Output file path.")
    anki_parser.add_argument("--deck-prefix", default="Brain", help="Prefix for deck hierarchy.")

    # 5. Weekly
    weekly_parser = subparsers.add_parser("weekly", help="Generate weekly progress review.")
    weekly_parser.add_argument("--date", default=None, help="Date YYYY-MM-DD within the target week.")
    weekly_parser.add_argument("--write", action="store_true", help="Save review note to 01-Daily/.")

    # 6. Daily
    daily_parser = subparsers.add_parser("daily", help="Scaffold a daily note from template.")
    daily_parser.add_argument("--date", default=date.today().isoformat(), help="Target date YYYY-MM-DD.")

    # 7. Shutdown
    shutdown_parser = subparsers.add_parser("shutdown", help="Run end-of-day shutdown routine.")
    shutdown_parser.add_argument("--date", default=None, help="Target date YYYY-MM-DD (defaults to today).")
    shutdown_parser.add_argument("--push", action="store_true", help="Automatically commit and push changes to GitHub.")

    # 8. Unslop
    unslop_parser = subparsers.add_parser("unslop", help="Audit or clean markdown notes for AI slop, em dashes, and emojis.")
    unslop_parser.add_argument("--inplace", action="store_true", help="Automatically clean em dashes and heading emojis.")

    args = parser.parse_args()
    vault_root = Path(args.vault).resolve()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "unslop":
        run_unslop_audit(vault_root, inplace=args.inplace)
    elif args.command == "health":
        scan_vault(str(vault_root))
    elif args.command == "stats":
        handle_vault_stats(vault_root)
    elif args.command == "stubs":
        create_stubs(
            vault_root=vault_root,
            dest_dir=args.dest,
            dry_run=args.dry_run,
            only_target=args.target,
            route_all=args.route_all
        )
    elif args.command == "anki":
        scan_and_export_anki(
            vault_root=vault_root,
            output_tsv=args.out,
            deck_prefix=args.deck_prefix
        )
    elif args.command == "weekly":
        target_dt = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
        generate_weekly_review(vault_root, target_date=target_dt, write_file=args.write)
    elif args.command == "daily":
        handle_daily_note_creation(vault_root, args.date)
    elif args.command == "shutdown":
        target_dt = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
        res = run_shutdown(vault_root, target_date=target_dt, push_git=args.push)
        print(f"✅ Daily shutdown complete for {res['date']}.")
        print(f"📊 Completed: {res['completed_count']} | Pending: {res['pending_count']} | Velocity: {res['completion_rate']:.1f}%")
        print(f"🎴 Anki Cards: {res['anki_count']} | Tomorrow Note: {res['tomorrow_file']}")
        if res.get("git_status"):
            print(f"🚀 Remote Sync: {res['git_status']}")

if __name__ == "__main__":
    main()
