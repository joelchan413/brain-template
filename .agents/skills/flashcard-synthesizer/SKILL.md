---
name: flashcard-synthesizer
description: Synthesizes high-yield active recall flashcards from lecture notes, textbooks, and concept notes, and exports them directly into Anki TSV and Obsidian Spaced Repetition formats.
---

# Flashcard Synthesizer & Anki Deck Manager Skill

This skill extracts and structures high-retention flashcards from course materials and exports them into Anki and Obsidian Spaced Repetition formats.

## Triggering Prompts
- *"Create flashcards for Lecture X"*
- *"Turn [[Note-Name]] into Anki flashcards"*
- *"Extract active recall deck for COMS 3110"*
- *"Export all vault cards to Anki"*

## Flashcard Construction Principles

Follow cognitive science and the **Minimum Information Principle**:
1. **One Idea Per Card**: Never combine multiple unrelated facts into a single question.
2. **Cloze Deletion for Invariants**: Use `{{c1::key term}}` for precise equations, algorithm invariants, or terminology.
3. **Conceptual Contrast**: Frame questions that highlight differences (e.g. *"Why choose Dijkstra over Bellman-Ford?"* rather than just *"What is Dijkstra?"*).
4. **Mathematical Precision**: Keep math expressions formatted in standard LaTeX `$...$` and `$$...$$`.

## Workflow

1. **Extract Card Candidates**:
   - Read the target lecture note or concept note.
   - Formulate 3–10 high-yield questions covering:
     - Core definitions & invariants.
     - Failure modes & edge cases.
     - Code/algorithmic mechanics.

2. **Insert into Note or Dedicated Quiz**:
   - For in-note review, append:
     ```markdown
     ### Q1: [Precise Question Prompt]
     <details>
     <summary><b>🔍 Reveal Answer</b></summary>
     **Answer**: [Concise, high-yield explanation]
     </details>
     ```
   - Or inline flashcards: `Question prompt::Concise answer`.

3. **Export to Anki TSV**:
   - Run `python scripts/anki_exporter.py --vault . --out exports/anki_cards.tsv --deck-prefix Brain`
   - Report the updated deck counts and card summary to the user.
