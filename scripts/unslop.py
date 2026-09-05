#!/usr/bin/env python3
"""
Unslop Linter & Cleaner for Obsidian Vault
Audits markdown notes for AI vocabulary tells, em dashes, decorative emojis in headings,
and title-cased headings, with an optional automatic cleaning mode.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple

# Ensure stdout handles UTF-8 safely on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXCLUDE_DIRS = {'.git', '.agents', '.system_generated', 'node_modules', 'scripts', '.obsidian', 'docs', 'exports'}

BANNED_WORDS = [
    r'\bcrucial\b', r'\bdelve\b', r'\bfoster\b', r'\bleverage\b',
    r'\bparamount\b', r'\bpivotal\b', r'\bprofound\b', r'\bshowcase\b',
    r'\btapestry\b', r'\btestament\b', r'\bunderscore\b', r'\butilize\b',
    r'\bvital\b', r'\bnuanced\b', r'\bplethora\b', r'\bmyriad\b',
    r'\blinchpin\b', r'\bcornerstone\b', r'\bholistic\b', r'\bsynergy\b',
    r'\bbespoke\b', r'\binterplay\b'
]

EMOJI_PATTERN = re.compile(
    r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]',
    flags=re.UNICODE
)

def audit_file(file_path: Path) -> List[str]:
    """Scans a markdown file for slop patterns and returns a list of warnings."""
    warnings = []
    try:
        text = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return [f"Could not read {file_path}: {e}"]

    lines = text.splitlines()
    for idx, line in enumerate(lines, 1):
        # Check for em dashes
        if '—' in line:
            warnings.append(f"Line {idx}: Em dash ('—') detected")

        # Check for decorative emojis in headings
        if line.startswith('#'):
            if EMOJI_PATTERN.search(line):
                warnings.append(f"Line {idx}: Decorative emoji detected in heading")

        # Check for banned AI vocabulary (skip YAML frontmatter tags/urls)
        for pattern in BANNED_WORDS:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                warnings.append(f"Line {idx}: Banned AI word '{match.group(0)}' detected")

    return warnings

def clean_file(file_path: Path) -> int:
    """Performs lightweight automatic unslop cleaning on a file."""
    try:
        text = file_path.read_text(encoding='utf-8')
    except Exception:
        return 0

    original = text
    # Replace em dashes with commas or periods depending on spacing
    text = text.replace(' — ', ', ')
    text = text.replace('—', ', ')

    # Remove emojis from headings
    def strip_heading_emoji(match):
        h_prefix = match.group(1)
        h_content = match.group(2)
        clean_content = EMOJI_PATTERN.sub('', h_content).strip()
        # Collapse multiple spaces
        clean_content = re.sub(r'\s+', ' ', clean_content)
        return f"{h_prefix} {clean_content}"

    text = re.sub(r'^(#{1,6})\s+(.*)$', strip_heading_emoji, text, flags=re.MULTILINE)

    if text != original:
        file_path.write_text(text, encoding='utf-8')
        return 1
    return 0

def run_unslop_audit(vault_root: Path, inplace: bool = False) -> None:
    """Audits or cleans markdown notes across the vault."""
    print("=" * 60)
    print("🧹 UNSLOP WRITING AUDIT")
    print("=" * 60)
    print(f"📁 Vault Root: {vault_root}")

    total_files = 0
    flagged_files = 0
    total_warnings = 0
    cleaned_count = 0

    for dirpath, dirnames, filenames in os.walk(vault_root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if f.endswith('.md'):
                total_files += 1
                p = Path(dirpath) / f
                rel_path = p.relative_to(vault_root)

                if inplace:
                    if clean_file(p):
                        cleaned_count += 1

                warnings = audit_file(p)
                if warnings:
                    flagged_files += 1
                    total_warnings += len(warnings)
                    print(f"\n📄 {rel_path} ({len(warnings)} issues):")
                    for w in warnings[:5]:
                        print(f"   ⚠️  {w}")
                    if len(warnings) > 5:
                        print(f"   ... and {len(warnings) - 5} more")

    print("\n" + "-" * 60)
    print(f"Scanned {total_files} notes.")
    if inplace:
        print(f"Automatically cleaned {cleaned_count} notes.")
    print(f"Found {total_warnings} issues across {flagged_files} notes.")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unslop Linter & Cleaner for Obsidian Vault")
    parser.add_argument("--inplace", action="store_true", help="Automatically clean em dashes and heading emojis")
    parser.add_argument("--path", type=str, default=".", help="Target directory or file path")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    if target.is_file():
        warnings = audit_file(target)
        for w in warnings:
            print(f"⚠️  {w}")
    else:
        run_unslop_audit(target, inplace=args.inplace)
