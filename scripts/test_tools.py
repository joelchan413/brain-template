#!/usr/bin/env python3
"""
Unit and Integration Test Suite for Vault Python Automation Tools
Tests health scanner, stub generator, Anki exporter, and weekly review synthesizer.
"""

import sys
import unittest
import tempfile
import shutil
from datetime import date, datetime
from pathlib import Path

# Add scripts directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from vault_health import scan_vault, WIKILINK_PATTERN, FRONTMATTER_PATTERN
from generate_concept_stubs import classify_target, generate_concept_note_content, is_concept_target
from anki_exporter import extract_cards_from_file, Flashcard
from weekly_review import get_week_bounds, parse_daily_note, extract_reflection_line

class TestVaultTools(unittest.TestCase):

    def setUp(self):
        # Create a temporary vault environment
        self.temp_dir = Path(tempfile.mkdtemp())
        (self.temp_dir / "01-Daily").mkdir()
        (self.temp_dir / "02-Courses" / "COMS3110" / "Lectures").mkdir(parents=True)
        (self.temp_dir / "02-Courses" / "COMS3110" / "Exams").mkdir(parents=True)
        (self.temp_dir / "03-Concepts").mkdir()
        (self.temp_dir / "05-MOCs").mkdir()
        (self.temp_dir / "06-Templates").mkdir()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_link_regex_patterns(self):
        sample_text = "Here is a link to [[Binary-Search]] and another [[Divide-and-Conquer|Divide & Conquer]]."
        matches = WIKILINK_PATTERN.findall(sample_text)
        self.assertEqual(matches, ["Binary-Search", "Divide-and-Conquer"])

    def test_frontmatter_regex(self):
        valid_doc = "---\ntitle: Sample\ntype: concept\n---\n# Content"
        invalid_doc = "# No frontmatter"
        self.assertTrue(bool(FRONTMATTER_PATTERN.match(valid_doc)))
        self.assertFalse(bool(FRONTMATTER_PATTERN.match(invalid_doc)))

    def test_classify_target(self):
        cat, course, folder = classify_target("Dynamic-Programming")
        self.assertEqual(cat, "concept")
        self.assertEqual(folder, "03-Concepts")

        cat, course, folder = classify_target("COMS3110-HW-01")
        self.assertEqual(cat, "assignment")
        self.assertEqual(course, "COMS3110")
        self.assertEqual(folder, "02-Courses/COMS3110/Assignments")

        cat, course, folder = classify_target("2026-08-24-CPRE3080-L01")
        self.assertEqual(cat, "ignore")

        cat, course, folder = classify_target("Quiz-Algorithm-Basics")
        self.assertEqual(cat, "quiz")

    def test_concept_stub_generation(self):
        refs = {"02-Courses/COMS3110/COMS3110-Overview.md"}
        content = generate_concept_note_content("Master-Theorem", refs)
        self.assertIn('title: "Master Theorem"', content)
        self.assertIn('type: concept', content)
        self.assertIn('[[COMS3110-Overview]]', content)
        self.assertIn('tags: [concept, evergreen, algorithms, cs]', content)

    def test_anki_flashcard_extraction(self):
        quiz_file = self.temp_dir / "02-Courses" / "COMS3110" / "Exams" / "Quiz-Test.md"
        quiz_content = """---
title: "Quiz: Testing"
type: quiz
course: "[[COMS3110-Overview]]"
tags: [quiz, coms3110]
---

### Q1: What is 2 + 2?
<details>
<summary><b>Reveal Answer</b></summary>
**Answer**: 4
</details>

- **Q**: What is the capital of France?
<details><summary>Reveal</summary>Paris</details>

What is the CPU speed::3.5 GHz
"""
        quiz_file.write_text(quiz_content, encoding='utf-8')

        cards = extract_cards_from_file(quiz_file, self.temp_dir, deck_prefix="TestBrain")
        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0].front, "What is 2 + 2?")
        self.assertEqual(cards[0].back, "4")
        self.assertEqual(cards[0].deck, "TestBrain::COMS3110")
        self.assertEqual(cards[1].front, "What is the capital of France?")
        self.assertEqual(cards[1].back, "Paris")
        self.assertEqual(cards[2].front, "What is the CPU speed")
        self.assertEqual(cards[2].back, "3.5 GHz")

    def test_weekly_review_bounds_and_parsing(self):
        sample_date = date(2026, 8, 25) # Tuesday
        start, end, year, week = get_week_bounds(sample_date)
        self.assertEqual(start, date(2026, 8, 24)) # Monday
        self.assertEqual(end, date(2026, 8, 30))   # Sunday
        self.assertEqual(week, 35)

        daily_file = self.temp_dir / "01-Daily" / "2026-08-25.md"
        daily_content = """---
title: "2026-08-25"
type: daily
---
- [x] Task 1 completed
- [ ] Task 2 pending

- **What went well:** Finished algorithm assignment early
- **What got delayed:** Linux kernel compile
"""
        daily_file.write_text(daily_content, encoding='utf-8')

        parsed = parse_daily_note(daily_file)
        self.assertEqual(parsed["completed_tasks"], ["Task 1 completed"])
        self.assertEqual(parsed["pending_tasks"], ["Task 2 pending"])
        self.assertEqual(parsed["went_well"], "Finished algorithm assignment early")
        self.assertEqual(parsed["delayed"], "Linux kernel compile")

if __name__ == "__main__":
    unittest.main()
