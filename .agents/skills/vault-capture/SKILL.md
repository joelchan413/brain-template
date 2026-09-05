---
name: vault-capture
description: Ingests text, URLs, bookmarks, lecture slides, papers, or quick thoughts into the Obsidian vault with clean YAML frontmatter and folder routing.
---

# Vault Capture Skill

Use this skill whenever the user asks to capture, save, ingest, or log information into the Obsidian second brain.

## Ingestion Workflow

1. **Classify Content Type**:
   - **Fleeting / Raw Thought**: Route to `00-Inbox/<timestamp-or-slug>.md` or append to today's `01-Daily/YYYY-MM-DD.md`.
   - **Lecture Material / Transcript**: Route to `02-Courses/<CourseCode>/Lectures/Lecture-XX-<Topic>.md` using the lecture template.
   - **Academic Paper / Book / Article**: Route to `04-Sources/<Author-Year-Title>.md` using the source template.
   - **Atomic Concept / Formula / Theory**: Route to `03-Concepts/<Concept-Name>.md`.

2. **Standardize Frontmatter**:
   - Always populate `title`, `type`, `tags`, `created`, and relevant `course` or `related` wikilinks.

3. **Atomic Extraction**:
   - When ingesting long sources, extract any key definitions or algorithms into separate notes in `03-Concepts/` and link back to the source note with `[[Source-Title]]`.

4. **Verify Clean Markdown**:
   - Ensure tables are properly formatted, callouts use `> [!NOTE]` style, and code/math blocks are cleanly delimited.
