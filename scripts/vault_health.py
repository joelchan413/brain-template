#!/usr/bin/env python3
"""
Vault Health & Link Integrity Scanner
Audits an Obsidian Markdown vault for link integrity, orphan notes, and metadata health.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, Set, List, Tuple

# Ensure stdout handles UTF-8 safely on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WIKILINK_PATTERN = re.compile(r'\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]')
FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

EXCLUDE_DIRS = {'.git', '.agents', '.system_generated', 'node_modules', 'scripts', '.obsidian', 'docs'}

def scan_vault(root_dir: str):
    root_path = Path(root_dir).resolve()
    all_notes: Dict[str, Path] = {} # note_stem (lowercase) -> Path
    note_files: List[Path] = []
    
    # 1. Collect all markdown files
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if f.endswith('.md'):
                p = Path(dirpath) / f
                note_files.append(p)
                all_notes[p.stem.lower()] = p

    outgoing_links: Dict[str, Set[str]] = {p.stem.lower(): set() for p in note_files}
    incoming_links: Dict[str, Set[str]] = {p.stem.lower(): set() for p in note_files}
    broken_links: List[Tuple[str, str]] = [] # (source_note, target_stem)
    missing_frontmatter: List[str] = []

    # 2. Parse links and frontmatter
    for p in note_files:
        stem_lower = p.stem.lower()
        rel_str = str(p.relative_to(root_path))
        is_meta_file = "06-Templates" in rel_str or rel_str.startswith("AGENTS") or rel_str.startswith("README")
        
        try:
            content = p.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {p}: {e}")
            continue

        # Frontmatter check
        if not FRONTMATTER_PATTERN.match(content) and not is_meta_file:
            missing_frontmatter.append(rel_str)

        # Find wikilinks (skip templates for dead-link checking)
        if not is_meta_file:
            links = WIKILINK_PATTERN.findall(content)
            for link_target in links:
                target_cleaned = link_target.strip().split('/')[-1] # handle path prefixes if any
                target_stem_lower = Path(target_cleaned).stem.lower()
                
                # Record outgoing
                outgoing_links[stem_lower].add(target_stem_lower)
                
                # Check existence
                if target_stem_lower in all_notes:
                    incoming_links[target_stem_lower].add(stem_lower)
                else:
                    broken_links.append((rel_str, link_target.strip()))

    # 3. Find orphan notes (excluding templates, inbox, mocs, readme)
    orphans = []
    for p in note_files:
        stem_lower = p.stem.lower()
        rel_str = str(p.relative_to(root_path))
        if "06-Templates" in rel_str or "00-Inbox" in rel_str or "05-MOCs" in rel_str or "README" in rel_str or "AGENTS" in rel_str:
            continue
        if len(incoming_links[stem_lower]) == 0 and len(outgoing_links[stem_lower]) == 0:
            orphans.append(rel_str)

    # 4. Print Report
    print("=" * 60)
    print("🧠 OBSIDIAN VAULT HEALTH REPORT")
    print("=" * 60)
    print(f"📁 Total Markdown Notes:  {len(note_files)}")
    print(f"🔗 Total Wikilinks Found: {sum(len(v) for v in outgoing_links.values())}")
    print("-" * 60)

    if broken_links:
        print(f"❌ Dead / Unresolved Wikilinks ({len(broken_links)}):")
        for src, target in broken_links[:15]:
            print(f"   • [{src}] -> [[{target}]] (Target note does not exist)")
        if len(broken_links) > 15:
            print(f"   ... and {len(broken_links) - 15} more")
    else:
        print("✅ No dead wikilinks found! All links resolve properly.")

    print("-" * 60)
    if orphans:
        print(f"⚠️  Orphan Notes ({len(orphans)} - zero incoming/outgoing links):")
        for o in orphans[:10]:
            print(f"   • {o}")
        if len(orphans) > 10:
            print(f"   ... and {len(orphans) - 10} more")
    else:
        print("✅ No orphan notes detected.")

    print("-" * 60)
    if missing_frontmatter:
        print(f"ℹ️  Notes Missing YAML Frontmatter ({len(missing_frontmatter)}):")
        for mf in missing_frontmatter[:10]:
            print(f"   • {mf}")
    else:
        print("✅ All standard notes have YAML frontmatter.")

    print("=" * 60)

if __name__ == "__main__":
    vault_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_vault(vault_dir)
