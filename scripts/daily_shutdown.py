#!/usr/bin/env python3
"""
Daily Shutdown & Wrap-Up Routine for Obsidian PKM Vault
Audits today's task completion, extracts Anki cards, previews tomorrow,
logs reflections, and creates an atomic git commit and push to remote.
"""

import sys
import re
import subprocess
import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# Ensure stdout handles UTF-8 safely on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from anki_exporter import scan_and_export_anki

TASK_REGEX = re.compile(r'^\s*-\s*\[([ xX])\]\s*(.*)$', re.MULTILINE)

def audit_daily_note(vault_root: Path, target_date: date) -> Dict:
    """Reads today's daily note and calculates task completion stats."""
    date_str = target_date.isoformat()
    daily_file = vault_root / "01-Daily" / f"{date_str}.md"
    
    result = {
        "exists": False,
        "path": daily_file,
        "completed_tasks": [],
        "pending_tasks": [],
        "total_tasks": 0,
        "completion_rate": 0.0,
    }
    
    if not daily_file.exists():
        return result

    result["exists"] = True
    content = daily_file.read_text(encoding="utf-8")
    
    matches = TASK_REGEX.findall(content)
    for status, text in matches:
        text_clean = text.strip()
        if status.lower() == 'x':
            result["completed_tasks"].append(text_clean)
        else:
            result["pending_tasks"].append(text_clean)
            
    total = len(result["completed_tasks"]) + len(result["pending_tasks"])
    result["total_tasks"] = total
    if total > 0:
        result["completion_rate"] = (len(result["completed_tasks"]) / total) * 100.0
        
    return result

def scaffold_tomorrow_daily(vault_root: Path, tomorrow_date: date, carryover_tasks: List[str] = None) -> Path:
    """Ensures tomorrow's daily note exists and optionally migrates pending tasks."""
    tomorrow_str = tomorrow_date.isoformat()
    daily_dir = vault_root / "01-Daily"
    templates_dir = vault_root / "06-Templates"
    daily_dir.mkdir(parents=True, exist_ok=True)
    
    dest_file = daily_dir / f"{tomorrow_str}.md"
    if dest_file.exists():
        return dest_file
        
    template_file = templates_dir / "Template-Daily-Note.md"
    if template_file.exists():
        content = template_file.read_text(encoding="utf-8")
    else:
        content = f"""---
title: "{tomorrow_str}"
type: daily
date: {tomorrow_str}
tags: [daily, study-log, iowa-state]
courses_today: []
---

# 📅 {tomorrow_str} — Daily Plan & Study Log

> [!INFO] Day Overview
> **Focus for Today**: 

---

## 🎯 Top Priorities
- [ ] 

---

## 🏛️ Google Calendar Schedule & Locations
| Time | Course / Event | Location | Note Link | Status |
| :--- | :--- | :--- | :--- | :--- |

---

## 🔄 Daily Reflection & Shutdown
- **What went well:** 
- **What got delayed:** 
- **Tomorrow's main priority:** 
"""

    populated = content.replace("{{date}}", tomorrow_str).replace("{{title}}", tomorrow_str)
    # Remove unpopulated sample template rows if present
    populated = re.sub(r'\|\s*\{\{start_time\}\}[^\n]*\n', '', populated)
    
    if carryover_tasks:
        carryover_str = "\n".join([f"- [ ] {t} (Carried over from {tomorrow_date - timedelta(days=1)})" for t in carryover_tasks])
        populated = populated.replace("## 🎯 Top Priorities\n- [ ]", f"## 🎯 Top Priorities\n{carryover_str}")

    dest_file.write_text(populated, encoding="utf-8")
    return dest_file

def append_reflection(vault_root: Path, target_date: date, went_well: str = "", got_delayed: str = "", tomorrow_priority: str = ""):
    """Updates the reflection block of today's daily note."""
    date_str = target_date.isoformat()
    daily_file = vault_root / "01-Daily" / f"{date_str}.md"
    if not daily_file.exists():
        return
        
    content = daily_file.read_text(encoding="utf-8")
    
    # Update reflection fields if present
    if went_well:
        content = re.sub(r'(- \*\*What went well:\*\*).*$', f'\\1 {went_well}', content, flags=re.MULTILINE)
    if got_delayed:
        content = re.sub(r'(- \*\*What got delayed:\*\*).*$', f'\\1 {got_delayed}', content, flags=re.MULTILINE)
    if tomorrow_priority:
        content = re.sub(r'(- \*\*Tomorrow\'s main priority:\*\*).*$', f'\\1 {tomorrow_priority}', content, flags=re.MULTILINE)
        
    daily_file.write_text(content, encoding="utf-8")

def git_commit_and_push(vault_root: Path, target_date: date) -> Tuple[bool, str]:
    """Stages all changes, creates a daily wrap-up commit, and pushes to remote."""
    date_str = target_date.isoformat()
    try:
        # Check status
        status_proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(vault_root),
            capture_output=True,
            text=True,
            check=True
        )
        has_uncommitted = bool(status_proc.stdout.strip())
        
        if has_uncommitted:
            # Stage changes
            subprocess.run(["git", "add", "-A"], cwd=str(vault_root), check=True)
            commit_msg = f"docs(daily): daily wrap-up and reflection for {date_str}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(vault_root), check=True)
            
        # Push to remote
        push_proc = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=str(vault_root),
            capture_output=True,
            text=True,
            check=True
        )
        return True, f"Successfully committed and pushed daily updates for {date_str} to origin/main."
    except subprocess.CalledProcessError as e:
        return False, f"Git push operation encountered an error: {e}"

def run_shutdown(vault_root: Path, target_date: date = None, export_anki: bool = True, prepare_tomorrow: bool = True, push_git: bool = False) -> Dict:
    """Master shutdown execution function."""
    if target_date is None:
        target_date = date.today()
        
    tomorrow = target_date + timedelta(days=1)
    
    # 1. Audit Daily Note
    audit = audit_daily_note(vault_root, target_date)
    
    # 2. Export Anki Cards
    anki_count = 0
    if export_anki:
        anki_tsv = vault_root / "exports" / "anki_cards.tsv"
        scan_and_export_anki(vault_root, str(anki_tsv))
        if anki_tsv.exists():
            anki_count = len(anki_tsv.read_text(encoding="utf-8").strip().splitlines()) - 1
            
    # 3. Scaffold Tomorrow
    tomorrow_file = None
    if prepare_tomorrow:
        tomorrow_file = scaffold_tomorrow_daily(vault_root, tomorrow, carryover_tasks=audit["pending_tasks"][:3])
        
    # 4. Optional Git Commit & Push
    git_status_msg = None
    if push_git:
        success, git_status_msg = git_commit_and_push(vault_root, target_date)
        
    return {
        "date": target_date.isoformat(),
        "tomorrow": tomorrow.isoformat(),
        "completed_count": len(audit["completed_tasks"]),
        "pending_count": len(audit["pending_tasks"]),
        "completion_rate": audit["completion_rate"],
        "pending_tasks": audit["pending_tasks"],
        "completed_tasks": audit["completed_tasks"],
        "tomorrow_file": str(tomorrow_file.relative_to(vault_root)) if tomorrow_file else None,
        "anki_count": max(0, anki_count),
        "git_status": git_status_msg
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daily Shutdown & Wrap-Up Routine")
    parser.add_argument("--date", help="Target date YYYY-MM-DD (defaults to today)")
    parser.add_argument("--push", action="store_true", help="Automatically commit and push changes to GitHub")
    args = parser.parse_args()

    v_root = Path(".").resolve()
    target_dt = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
    res = run_shutdown(v_root, target_date=target_dt, push_git=args.push)
    print("=" * 60)
    print(f"🌙 DAILY SHUTDOWN REPORT — {res['date']}")
    print("=" * 60)
    print(f"✅ Tasks Completed : {res['completed_count']}")
    print(f"⏳ Pending Tasks   : {res['pending_count']}")
    print(f"📈 Velocity Rate   : {res['completion_rate']:.1f}%")
    print(f"🎴 Total Anki Cards: {res['anki_count']}")
    if res['tomorrow_file']:
        print(f"📅 Tomorrow Ready  : {res['tomorrow_file']}")
    if res['git_status']:
        print(f"🚀 Remote Sync     : {res['git_status']}")
    print("=" * 60)
