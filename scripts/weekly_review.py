#!/usr/bin/env python3
"""
Weekly Review & Academic Progress Synthesizer for Obsidian Vault
Aggregates daily notes, completed tasks, course milestones, and concept graph growth
into a comprehensive weekly retrospective and study planning note.
"""

import os
import re
import sys
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Ensure stdout handles UTF-8 safely on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXCLUDE_DIRS = {'.git', '.agents', '.system_generated', 'node_modules', 'scripts', '.obsidian', 'docs', 'exports'}

TASK_PATTERN = re.compile(r'^\s*-\s*\[([ xX])\]\s*(.+)$', re.MULTILINE)
FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
COURSE_MILESTONE_PATTERN = re.compile(r'^\s*-\s*\[([ xX])\]\s*\*\*(.*?)\*\*:\s*(?:Due\s*)?`?([^`\n]+)`?', re.MULTILINE)

def get_week_bounds(target_date: date) -> Tuple[date, date, int, int]:
    """
    Returns (monday_date, sunday_date, iso_year, iso_week)
    """
    start_monday = target_date - timedelta(days=target_date.weekday())
    end_sunday = start_monday + timedelta(days=6)
    iso_year, iso_week, _ = target_date.isocalendar()
    return start_monday, end_sunday, iso_year, iso_week

def extract_reflection_line(content: str, header_label: str) -> Optional[str]:
    """Safely extracts the single-line value following a reflection header."""
    pattern = re.compile(rf'-\s*\*\*{re.escape(header_label)}:\*\*[ \t]*([^\r\n]*)')
    match = pattern.search(content)
    if match:
        val = match.group(1).strip()
        if val and not val.startswith('- **'):
            return val
    return None

def parse_daily_note(file_path: Path) -> Dict:
    """Parses a daily note for tasks, reflections, and logged items."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return {}

    completed_tasks = []
    pending_tasks = []
    
    for match in TASK_PATTERN.finditer(content):
        status, task_text = match.group(1), match.group(2).strip()
        if status in ('x', 'X'):
            completed_tasks.append(task_text)
        else:
            pending_tasks.append(task_text)

    went_well = extract_reflection_line(content, "What went well")
    delayed = extract_reflection_line(content, "What got delayed")

    return {
        "path": file_path,
        "filename": file_path.name,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "went_well": went_well,
        "delayed": delayed,
        "content": content
    }

def find_upcoming_course_milestones(vault_root: Path, current_date: date, lookahead_days: int = 14) -> List[Dict]:
    """Scans 02-Courses/ for upcoming deadlines and milestones."""
    milestones = []
    courses_dir = vault_root / "02-Courses"
    if not courses_dir.exists():
        return []

    for p in courses_dir.rglob("*-Overview.md"):
        try:
            content = p.read_text(encoding='utf-8')
        except Exception:
            continue

        course_code = p.stem.replace('-Overview', '')
        for match in COURSE_MILESTONE_PATTERN.finditer(content):
            status = match.group(1)
            name = match.group(2).strip()
            due_raw = match.group(3).strip()

            try:
                due_dt = datetime.strptime(due_raw, "%Y-%m-%d").date()
                days_until = (due_dt - current_date).days
                if 0 <= days_until <= lookahead_days:
                    milestones.append({
                        "course": course_code,
                        "name": name,
                        "due_date": due_raw,
                        "days_until": days_until,
                        "completed": status in ('x', 'X')
                    })
            except ValueError:
                if status not in ('x', 'X') and "YYYY" not in due_raw:
                    milestones.append({
                        "course": course_code,
                        "name": name,
                        "due_date": due_raw,
                        "days_until": 999,
                        "completed": False
                    })

    milestones.sort(key=lambda x: x["days_until"])
    return milestones

def find_new_concepts_in_range(vault_root: Path, start_date: date, end_date: date) -> List[str]:
    """Scans 03-Concepts/ for notes created in the date range."""
    concepts_dir = vault_root / "03-Concepts"
    if not concepts_dir.exists():
        return []

    concepts = []
    for p in concepts_dir.glob("*.md"):
        try:
            content = p.read_text(encoding='utf-8')
            created_match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', content)
            if created_match:
                c_date = datetime.strptime(created_match.group(1), "%Y-%m-%d").date()
                if start_date <= c_date <= end_date:
                    concepts.append(p.stem)
        except Exception:
            continue

    return sorted(concepts)

def generate_weekly_review(
    vault_root: Path,
    target_date: Optional[date] = None,
    write_file: bool = False
) -> str:
    vault_root = vault_root.resolve()
    if target_date is None:
        target_date = date.today()

    start_monday, end_sunday, iso_year, iso_week = get_week_bounds(target_date)
    week_str = f"{iso_year}-W{iso_week:02d}"

    daily_dir = vault_root / "01-Daily"
    daily_notes: List[Dict] = []

    curr = start_monday
    while curr <= end_sunday:
        note_file = daily_dir / f"{curr.isoformat()}.md"
        if note_file.exists():
            daily_notes.append(parse_daily_note(note_file))
        curr += timedelta(days=1)

    all_completed = []
    all_pending = []
    all_went_well = []
    all_delayed = []

    for dn in daily_notes:
        all_completed.extend(dn["completed_tasks"])
        all_pending.extend(dn["pending_tasks"])
        if dn["went_well"]:
            all_went_well.append(f"**{dn['filename'].replace('.md', '')}**: {dn['went_well']}")
        if dn["delayed"]:
            all_delayed.append(f"**{dn['filename'].replace('.md', '')}**: {dn['delayed']}")

    total_tasks = len(all_completed) + len(all_pending)
    completion_rate = (len(all_completed) / total_tasks * 100) if total_tasks > 0 else 0

    new_concepts = find_new_concepts_in_range(vault_root, start_monday, end_sunday)
    upcoming_milestones = find_upcoming_course_milestones(vault_root, target_date, lookahead_days=14)

    lines = [
        "---",
        f"title: \"Weekly Review: {week_str}\"",
        "type: weekly_review",
        f"week: {week_str}",
        f"date_start: {start_monday.isoformat()}",
        f"date_end: {end_sunday.isoformat()}",
        "tags: [weekly-review, retrospective, study-analytics]",
        f"created: {date.today().isoformat()}",
        f"task_completion_rate: {completion_rate:.1f}%",
        "---",
        "",
        f"# 📊 Weekly Retrospective: Week {iso_week:02d} ({iso_year})",
        "",
        f"> [!INFO] Summary Period: **{start_monday.strftime('%b %d, %Y')}** to **{end_sunday.strftime('%b %d, %Y')}**",
        f"> **Daily Notes Logged**: {len(daily_notes)}/7 days  |  **Task Velocity**: {len(all_completed)}/{total_tasks} completed ({completion_rate:.1f}%)",
        "",
        "---",
        "",
        "## 🎯 Task Execution & Productivity",
        f"- **Completed Tasks ({len(all_completed)})**:"
    ]

    if all_completed:
        for t in all_completed:
            lines.append(f"  - [x] {t}")
    else:
        lines.append("  - *(No completed tasks logged this week)*")

    lines.append(f"\n- **Carried Over / Pending Tasks ({len(all_pending)})**:")
    if all_pending:
        for t in all_pending:
            lines.append(f"  - [ ] {t}")
    else:
        lines.append("  - *(All tasks cleared!)*")

    lines.extend([
        "",
        "---",
        "",
        "## 🧠 Knowledge Vault Growth",
        f"- **New Concept Notes Created ({len(new_concepts)})**:"
    ])

    if new_concepts:
        for c in new_concepts:
            lines.append(f"  - [[{c}]]")
    else:
        lines.append("  - *(No new concept notes created this week)*")

    lines.extend([
        "",
        "---",
        "",
        "## 🔄 Reflections & Patterns",
        "### 🟢 Wins & Breakthroughs"
    ])
    if all_went_well:
        for w in all_went_well:
            lines.append(f"- {w}")
    else:
        lines.append("- *(No specific reflection logged)*")

    lines.append("\n### 🟡 Bottlenecks & Delays")
    if all_delayed:
        for d in all_delayed:
            lines.append(f"- {d}")
    else:
        lines.append("- *(None reported)*")

    lines.extend([
        "",
        "---",
        "",
        "## 🚀 Upcoming Deadlines & Exam Milestones (Next 14 Days)"
    ])

    if upcoming_milestones:
        for m in upcoming_milestones:
            badge = "✅" if m["completed"] else "⏳"
            days_str = f"in {m['days_until']} days" if m['days_until'] > 0 else "TODAY"
            lines.append(f"- {badge} **[[{m['course']}-Overview]]**: {m['name']} (Due `{m['due_date']}` — {days_str})")
    else:
        lines.append("- *(No pressing milestones in the next 14 days)*")

    lines.extend([
        "",
        "---",
        "",
        "## 📝 Next Week's Primary Goals",
        "- [ ] Goal 1: ",
        "- [ ] Goal 2: ",
        "- [ ] Goal 3: ",
        ""
    ])

    report = "\n".join(lines)

    if write_file:
        out_file = daily_dir / f"Weekly-Review-{week_str}.md"
        out_file.write_text(report, encoding='utf-8')
        print(f"✅ Generated weekly review note: `{out_file.relative_to(vault_root)}`")

    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate weekly retrospective and study progress review.")
    parser.add_argument("--vault", default=".", help="Path to the Obsidian vault root directory.")
    parser.add_argument("--date", default=None, help="Target date YYYY-MM-DD (defaults to today).")
    parser.add_argument("--write", action="store_true", help="Write Weekly-Review-YYYY-Wxx.md to 01-Daily/")

    args = parser.parse_args()
    target_dt = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
    
    report_text = generate_weekly_review(
        vault_root=Path(args.vault),
        target_date=target_dt,
        write_file=args.write
    )

    if not args.write:
        print(report_text)
