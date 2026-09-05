#!/usr/bin/env python3
"""
Anki Flashcard & Active Recall Exporter for Obsidian Vault
Scans markdown notes, active recall quizzes, and flashcard blocks in the vault
and exports them into clean Anki-compatible TSV and Spaced Repetition formats.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Ensure stdout handles UTF-8 safely on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXCLUDE_DIRS = {'.git', '.agents', '.system_generated', 'node_modules', 'scripts', '.obsidian', 'docs', 'exports'}

FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
TAG_LINE_PATTERN = re.compile(r'tags:\s*\[(.*?)\]|tags:\s*\n((?:\s*-\s*.*\n)+)')
COURSE_PATTERN = re.compile(r'course:\s*["\']?(?:\[\[)?([^\]"\']+)\]?["\']?')

# Match ### Q1: [Question text] or ### Question 1: [Question text] followed within 4 lines by <details>
HEADING_QUIZ_PATTERN = re.compile(
    r'###\s*(?:Q\d+[:.]?\s*|Question\s*\d*[:.]?\s*)([^\n]+)\n(?:\s*-\s*\*\*[A-Za-z\s]+\*\*:[^\n]*\n|\s*\n){0,4}\s*<details>\s*<summary>.*?<\/summary>\s*(.*?)\s*<\/details>',
    re.DOTALL | re.IGNORECASE
)

# Match bullet list question: - **Q**: [Question text] \n <details>...
BULLET_QUIZ_PATTERN = re.compile(
    r'(?:^|\n)\s*-\s*\*\*(?:Q|Question)\*\*:\s*([^\n]+)\s*\n\s*<details>\s*<summary>.*?<\/summary>\s*(.*?)\s*<\/details>',
    re.DOTALL | re.IGNORECASE
)

# Pattern: Inline double-colon cards (Question::Answer)
INLINE_CARD_PATTERN = re.compile(r'^(?!#)(.+?)::(.+?)$', re.MULTILINE)

# Pattern: Obsidian Callout question / answer
CALLOUT_CARD_PATTERN = re.compile(
    r'>\s*\[!question\]\s*(.*?)\n(?:>\s*.*?\n)*?>\s*\[!answer\]\s*(.*?)(?=\n\n|\n[^\>]|$)',
    re.DOTALL | re.IGNORECASE
)

# Pattern: Obsidian Spaced Repetition Multiline format (Question \n? \nAnswer)
MULTILINE_CARD_PATTERN = re.compile(
    r'(?:^|\n)(?!\s*#|\s*`)(.+?)\n\s*\?\s*\n((?:[^\n]+\n?)+?)(?=\n\s*<!--ID:|\n\n|\n\s*#|$)',
    re.DOTALL
)

def parse_frontmatter_metadata(content: str) -> Tuple[List[str], Optional[str]]:
    """Extracts tags and course code from YAML frontmatter."""
    fm_match = FRONTMATTER_PATTERN.match(content)
    if not fm_match:
        return [], None
    
    fm_text = fm_match.group(1)
    tags = []
    
    # Extract tags
    tag_match = TAG_LINE_PATTERN.search(fm_text)
    if tag_match:
        if tag_match.group(1):
            tags = [t.strip() for t in tag_match.group(1).split(',') if t.strip()]
        elif tag_match.group(2):
            tags = [re.sub(r'^\s*-\s*', '', line).strip() for line in tag_match.group(2).strip().split('\n') if line.strip()]

    # Extract course
    course = None
    course_match = COURSE_PATTERN.search(fm_text)
    if course_match:
        course = course_match.group(1).replace('-Overview', '').replace('[[', '').replace(']]', '').strip()

    return tags, course

class Flashcard:
    def __init__(self, front: str, back: str, deck: str, tags: List[str], source_file: str):
        self.front = front.strip()
        self.back = back.strip()
        self.deck = deck.strip()
        self.tags = tags
        self.source_file = source_file

    def to_tsv_row(self) -> str:
        clean_front = self.front.replace('\t', ' ').replace('\n', '<br>')
        clean_back = self.back.replace('\t', ' ').replace('\n', '<br>')
        tag_str = " ".join(self.tags)
        return f"{clean_front}\t{clean_back}\t{self.deck}\t{tag_str}\t{self.source_file}"

def extract_cards_from_file(file_path: Path, vault_root: Path, deck_prefix: str = "Brain") -> List[Flashcard]:
    cards: List[Flashcard] = []
    rel_path = str(file_path.relative_to(vault_root))
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return []

    tags, course = parse_frontmatter_metadata(content)
    
    # Infer deck name
    deck = deck_prefix
    if course:
        deck = f"{deck_prefix}::{course}"
    elif "02-Courses" in rel_path:
        parts = rel_path.split(os.sep)
        if len(parts) > 1:
            deck = f"{deck_prefix}::{parts[1]}"
    elif "03-Concepts" in rel_path:
        deck = f"{deck_prefix}::Concepts"

    indexed_cards: List[Tuple[int, Flashcard]] = []
    seen_fronts: Set[str] = set()

    # 1. Check for Heading ### Q1: ... <details> blocks
    for match in HEADING_QUIZ_PATTERN.finditer(content):
        q_raw = match.group(1).strip()
        a_raw = match.group(2).strip()
        a_cleaned = re.sub(r'^\s*\*\*Answer\*\*:\s*', '', a_raw, flags=re.IGNORECASE)
        if q_raw not in seen_fronts:
            seen_fronts.add(q_raw)
            card_tags = list(set(tags + ["active-recall"]))
            indexed_cards.append((match.start(), Flashcard(q_raw, a_cleaned, deck, card_tags, rel_path)))

    # 2. Check for bullet list Q: ... <details> blocks
    for match in BULLET_QUIZ_PATTERN.finditer(content):
        q_raw = match.group(1).strip()
        a_raw = match.group(2).strip()
        a_cleaned = re.sub(r'^\s*\*\*Answer\*\*:\s*', '', a_raw, flags=re.IGNORECASE)
        if q_raw not in seen_fronts:
            seen_fronts.add(q_raw)
            card_tags = list(set(tags + ["active-recall"]))
            indexed_cards.append((match.start(), Flashcard(q_raw, a_cleaned, deck, card_tags, rel_path)))

    # 3. Check for inline :: cards
    for match in INLINE_CARD_PATTERN.finditer(content):
        q_raw = match.group(1).strip()
        a_raw = match.group(2).strip()
        if not q_raw.startswith('http') and not q_raw.startswith('//') and q_raw not in seen_fronts:
            seen_fronts.add(q_raw)
            card_tags = list(set(tags + ["flashcard"]))
            indexed_cards.append((match.start(), Flashcard(q_raw, a_raw, deck, card_tags, rel_path)))

    # 4. Check for Callout cards
    for match in CALLOUT_CARD_PATTERN.finditer(content):
        q_raw = match.group(1).strip()
        a_raw = match.group(2).strip()
        a_raw = re.sub(r'^>\s?', '', a_raw, flags=re.MULTILINE)
        if q_raw not in seen_fronts:
            seen_fronts.add(q_raw)
            card_tags = list(set(tags + ["callout-card"]))
            indexed_cards.append((match.start(), Flashcard(q_raw, a_raw, deck, card_tags, rel_path)))

    # 5. Check for Obsidian Spaced Repetition Multiline (? format)
    for match in MULTILINE_CARD_PATTERN.finditer(content):
        q_raw = match.group(1).strip().strip('`')
        a_raw = match.group(2).strip()
        if q_raw and q_raw not in seen_fronts and len(q_raw) > 5:
            seen_fronts.add(q_raw)
            card_tags = list(set(tags + ["spaced-repetition"]))
            indexed_cards.append((match.start(), Flashcard(q_raw, a_raw, deck, card_tags, rel_path)))

    # Sort by appearance in source file
    indexed_cards.sort(key=lambda x: x[0])
    return [c for _, c in indexed_cards]

def scan_and_export_anki(
    vault_root: Path,
    output_tsv: Optional[str] = None,
    deck_prefix: str = "Brain"
) -> List[Flashcard]:
    vault_root = vault_root.resolve()
    all_cards: List[Flashcard] = []

    for dirpath, dirnames, filenames in os.walk(vault_root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if f.endswith('.md') and not f.startswith('Template-'):
                file_path = Path(dirpath) / f
                extracted = extract_cards_from_file(file_path, vault_root, deck_prefix)
                all_cards.extend(extracted)

    print("=" * 60)
    print("📇 OBSIDIAN TO ANKI FLASHCARD EXPORTER")
    print("=" * 60)
    print(f"📁 Vault Root: {vault_root}")
    print(f"🃏 Total Cards Extracted: {len(all_cards)}")
    print("-" * 60)

    # Deck summary breakdown
    deck_counts: Dict[str, int] = {}
    for card in all_cards:
        deck_counts[card.deck] = deck_counts.get(card.deck, 0) + 1

    for deck_name, count in sorted(deck_counts.items()):
        print(f"  📦 {deck_name:<35} : {count} cards")

    print("-" * 60)

    if output_tsv:
        out_path = vault_root / output_tsv
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        header = "#separator:tab\n#html:true\n#tags column:4\n#deck column:3\n#columns:Front\tBack\tDeck\tTags\tSource\n"
        rows = [card.to_tsv_row() for card in all_cards]
        out_path.write_text(header + "\n".join(rows) + "\n", encoding='utf-8')
        print(f"✅ Exported {len(all_cards)} cards to `{out_path.relative_to(vault_root)}`")
    else:
        print("💡 No output file specified. Run with `--out exports/anki_cards.tsv` to save.")

    print("=" * 60)
    return all_cards

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export active recall quiz items to Anki TSV format.")
    parser.add_argument("--vault", default=".", help="Path to the Obsidian vault root directory.")
    parser.add_argument("--out", default="exports/anki_cards.tsv", help="Path to output TSV file.")
    parser.add_argument("--deck-prefix", default="Brain", help="Prefix for Anki subdecks (e.g., Brain).")

    args = parser.parse_args()
    scan_and_export_anki(
        vault_root=Path(args.vault),
        output_tsv=args.out,
        deck_prefix=args.deck_prefix
    )
