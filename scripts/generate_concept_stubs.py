#!/usr/bin/env python3
"""
Concept & Course Stub Generator for Obsidian Vault
Scans the vault for unresolved wikilinks and scaffolds atomic concept notes
or course artifact notes with standardized YAML frontmatter, backlinks, and structure.
"""

import os
import re
import sys
import argparse
from datetime import date
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Ensure stdout handles UTF-8 safely on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WIKILINK_PATTERN = re.compile(r'\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]')
EXCLUDE_DIRS = {'.git', '.agents', '.system_generated', 'node_modules', 'scripts', '.obsidian', 'docs', 'exports'}

# Course prefixes in this vault
KNOWN_COURSES = ("COMS3110", "CPRE2320", "CPRE3080", "CPRE4370", "CPRE4910", "CPRE4940")

def classify_target(target: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Classifies a link target into:
      category: 'concept', 'lecture', 'assignment', 'quiz', or 'ignore'
      course_code: associated course code if detected, else None
      subfolder: recommended subfolder relative to vault root
    """
    clean = Path(target).name
    stem = Path(clean).stem

    # Ignore meta/overview/MOC links
    if stem.endswith('-Overview') or stem.endswith('-MOC') or stem in ('Academic-Hub', 'Formula-Sheet-Master', 'README', 'AGENTS'):
        return 'ignore', None, None

    # Ignore lecture note format (lectures must only be created with actual student notes)
    lecture_match = re.match(r'^\d{4}-\d{2}-\d{2}-([A-Z0-9]+)-L\d+', stem)
    if lecture_match:
        return 'ignore', None, None

    # Check for course assignment / lab / deliverable / meeting
    for course in KNOWN_COURSES:
        if stem.startswith(course):
            rest = stem[len(course):].lstrip('-')
            if any(rest.startswith(p) for p in ('HW', 'Lab', 'Assignment', 'Problem-Set', 'Case-Study', 'Discussion')):
                return 'assignment', course, f"02-Courses/{course}/Assignments"
            if any(rest.startswith(p) for p in ('Sprint', 'Advisor', 'Client', 'Deliverable', 'Portfolio', 'Resume', 'Presentation', 'Team', 'Project')):
                return 'assignment', course, f"02-Courses/{course}/Deliverables"
            if any(rest.startswith(p) for p in ('Quiz', 'Exam', 'Midterm', 'Final')):
                return 'quiz', course, f"02-Courses/{course}/Exams"

    # Check for Quiz notes (e.g. Quiz-Algorithm-Basics or Quiz-COMS3110-...)
    if stem.startswith('Quiz-'):
        for course in KNOWN_COURSES:
            if course in stem:
                return 'quiz', course, f"02-Courses/{course}/Exams"
        return 'quiz', "COMS3110", "02-Courses/COMS3110/Exams"

    # By default, anything else is an evergreen concept
    return 'concept', None, "03-Concepts"

def is_concept_target(target: str) -> bool:
    """Convenience helper returning True if target classifies as an evergreen concept."""
    cat, _, _ = classify_target(target)
    return cat == 'concept'

def titleize_target(target: str) -> str:
    """Converts Hyphen-Separated-Name or CamelCase to human-readable title."""
    clean = Path(target).name
    spaced = clean.replace('-', ' ').replace('_', ' ')
    return spaced.strip()

def collect_unresolved_links(vault_root: Path) -> Tuple[Dict[str, Set[str]], Dict[str, Path]]:
    """
    Returns:
      missing_targets: dict of target_name -> set of relative file paths referencing it
      all_existing_notes: dict of note_stem (lowercase) -> Path
    """
    all_existing_notes: Dict[str, Path] = {}
    note_files: List[Path] = []

    for dirpath, dirnames, filenames in os.walk(vault_root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if f.endswith('.md'):
                p = Path(dirpath) / f
                note_files.append(p)
                all_existing_notes[p.stem.lower()] = p

    missing_targets: Dict[str, Set[str]] = {}

    for p in note_files:
        rel_str = str(p.relative_to(vault_root))
        if "06-Templates" in rel_str or rel_str.startswith("AGENTS") or rel_str.startswith("README"):
            continue

        try:
            content = p.read_text(encoding='utf-8')
        except Exception:
            continue

        links = WIKILINK_PATTERN.findall(content)
        for link in links:
            clean_link = link.strip().split('/')[-1]
            stem_lower = Path(clean_link).stem.lower()

            if stem_lower not in all_existing_notes:
                if clean_link not in missing_targets:
                    missing_targets[clean_link] = set()
                missing_targets[clean_link].add(rel_str)

    return missing_targets, all_existing_notes

def generate_concept_note_content(target_name: str, referencing_files: Set[str]) -> str:
    """Generates the Markdown body for a new concept stub."""
    title = titleize_target(target_name)
    today_str = date.today().isoformat()
    
    tags = ["concept", "evergreen"]
    lower_target = target_name.lower()
    if any(k in lower_target for k in ("algorithm", "sort", "tree", "graph", "search", "complexity", "theorem", "dp", "dynamic", "np")):
        tags.extend(["algorithms", "cs"])
    if any(k in lower_target for k in ("process", "memory", "paging", "thread", "kernel", "os", "deadlock", "tlb", "file-system", "sync")):
        tags.extend(["operating-systems", "cpre"])
    if any(k in lower_target for k in ("isa", "pipeline", "cache", "verilog", "fpga", "register", "vhdl", "cpu", "hardware")):
        tags.extend(["computer-architecture", "hardware"])
    if any(k in lower_target for k in ("wireless", "security", "ble", "wpa", "eap", "sniffing", "imsi", "iot")):
        tags.extend(["cybersecurity", "networking"])
    if any(k in lower_target for k in ("ethics", "dei", "whistleblowing", "responsibility", "standards")):
        tags.extend(["ethics", "professionalism"])

    tag_list_str = ", ".join(dict.fromkeys(tags))
    backlinks_list = "\n".join(f"- [[{Path(rf).stem}]] (`{rf}`)" for rf in sorted(referencing_files))

    return f"""---
title: "{title}"
type: concept
tags: [{tag_list_str}]
created: {today_str}
updated: {today_str}
status: stub
---

# 💡 {title}

> [!NOTE] Definition & High-Level Summary
> **{title}** is a core concept in computer science and engineering. 
> *(Summary to be expanded during lecture review or deep study session)*.

---

## ⚙️ Key Invariants & Principles
- **Core Mechanism**: 
- **Time / Space Complexity or Bounds**: 
- **Assumptions & Preconditions**: 

---

## 📊 Formal Representation & Code / Equation Drill
```text
[Insert relevant algorithm pseudocode, diagram, or mathematical formulation here]
```

---

## 🔗 Related Concepts & Backlinks
{backlinks_list}
"""

def generate_assignment_stub_content(target_name: str, course_code: str, referencing_files: Set[str]) -> str:
    """Generates Markdown body for an assignment or lab stub."""
    title = titleize_target(target_name)
    today_str = date.today().isoformat()
    course_tag = course_code.lower() if course_code else "coursework"
    backlinks_list = "\n".join(f"- [[{Path(rf).stem}]] (`{rf}`)" for rf in sorted(referencing_files))

    return f"""---
title: "{title}"
type: assignment
course: "[[{course_code}-Overview]]"
tags: [assignment, {course_tag}, coursework]
created: {today_str}
due_date: 
status: not-started
priority: medium
---

# 📝 {title}

> [!INFO] Assignment Overview
> **Course**: [[{course_code}-Overview]]
> **Due Date**: TBD
> **Submission Platform**: Canvas / Git Repository

---

## 🎯 Objectives & Deliverables
- [ ] Task 1: 
- [ ] Task 2: 
- [ ] Final Submission & Verification

---

## 🧪 Test Cases & Notes
- 

---

## 🔗 Referenced From
{backlinks_list}
"""

def generate_lecture_stub_content(target_name: str, course_code: str, referencing_files: Set[str]) -> str:
    """Generates Markdown body for a lecture note stub."""
    title = titleize_target(target_name)
    today_str = date.today().isoformat()
    course_tag = course_code.lower() if course_code else "lecture"
    backlinks_list = "\n".join(f"- [[{Path(rf).stem}]] (`{rf}`)" for rf in sorted(referencing_files))

    return f"""---
title: "{title}"
type: lecture
course: "[[{course_code}-Overview]]"
tags: [lecture, {course_tag}]
date: {today_str}
status: unreviewed
---

# 🎓 {title}

> [!INFO] Lecture Metadata
> **Course**: [[{course_code}-Overview]]
> **Date**: {today_str}

---

## 📌 Core Topics & Key Takeaways
- 

---

## 📝 Detailed Lecture Notes
- 

---

## 🔗 References
{backlinks_list}
"""

def create_stubs(
    vault_root: Path,
    dest_dir: str = "03-Concepts",
    dry_run: bool = False,
    only_target: Optional[str] = None,
    route_all: bool = False
) -> int:
    """Scaffolds stubs in the destination directory or routed directories."""
    vault_root = vault_root.resolve()
    missing_targets, existing_notes = collect_unresolved_links(vault_root)

    targets_to_create: List[Tuple[str, str, str, Optional[str], Set[str]]] = []
    # Items: (target_name, category, dest_rel_folder, course_code, referencing_files)

    for target, refs in missing_targets.items():
        if only_target and target.lower() != only_target.lower():
            continue

        cat, course, subfolder = classify_target(target)
        if cat == 'ignore':
            continue

        if not route_all and cat != 'concept':
            # In standard mode, only process concept targets
            continue

        target_folder = subfolder if route_all else dest_dir
        targets_to_create.append((target, cat, target_folder, course, refs))

    print("=" * 60)
    print("🧠 OBSIDIAN STUB GENERATOR")
    print("=" * 60)
    print(f"📁 Default Folder: {dest_dir}/")
    print(f"🔀 Route Course Notes: {'YES (Routing lectures/assignments to course folders)' if route_all else 'NO (Concepts only)'}")
    print(f"🔍 Stubs to Generate: {len(targets_to_create)}")
    print(f"⚙️ Mode: {'DRY RUN (No files created)' if dry_run else 'WRITE (Creating stubs)'}")
    print("-" * 60)

    if not targets_to_create:
        print("✅ No unresolved links match the requested criteria.")
        print("=" * 60)
        return 0

    count = 0
    for target, cat, rel_folder, course, refs in sorted(targets_to_create, key=lambda x: (x[1], x[0])):
        dest_dir_path = vault_root / rel_folder
        filename = f"{target}.md" if not target.endswith('.md') else target
        dest_path = dest_dir_path / filename

        cat_badge = f"[{cat.upper()}]"
        print(f"  • {cat_badge:<14} [[{target}]] -> `{rel_folder}/{filename}` ({len(refs)} ref{'s' if len(refs) > 1 else ''})")

        if not dry_run:
            dest_dir_path.mkdir(parents=True, exist_ok=True)
            if dest_path.exists():
                print(f"    ⚠️ Note already exists at {dest_path.name}, skipping.")
                continue

            if cat == 'concept':
                content = generate_concept_note_content(target, refs)
            elif cat in ('assignment', 'quiz'):
                content = generate_assignment_stub_content(target, course or "COMS3110", refs)
            elif cat == 'lecture':
                content = generate_lecture_stub_content(target, course or "COMS3110", refs)
            else:
                content = generate_concept_note_content(target, refs)

            dest_path.write_text(content, encoding='utf-8')
            count += 1

    print("-" * 60)
    if dry_run:
        print(f"💡 Dry run completed. {len(targets_to_create)} notes would be generated.")
    else:
        print(f"✅ Successfully created {count} new stubs across the vault!")
    print("=" * 60)
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate concept and course note stubs from unresolved wikilinks.")
    parser.add_argument("--vault", default=".", help="Path to the Obsidian vault root directory.")
    parser.add_argument("--dest", default="03-Concepts", help="Subdirectory for concept notes (default: 03-Concepts).")
    parser.add_argument("--dry-run", action="store_true", help="Preview stubs without writing files.")
    parser.add_argument("--route-all", action="store_true", help="Automatically route course assignments and lectures to their respective 02-Courses subfolders.")
    parser.add_argument("--target", default=None, help="Generate a stub for a single specific target link.")

    args = parser.parse_args()
    create_stubs(
        vault_root=Path(args.vault),
        dest_dir=args.dest,
        dry_run=args.dry_run,
        only_target=args.target,
        route_all=args.route_all
    )
