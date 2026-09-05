---
description: Standards and schemas for creating and maintaining markdown notes in the Obsidian PKM vault.
always_on: true
---

# Vault Standards & Schemas

## 1. File Naming Rules
- Use PascalCase or hyphen-separated names for concept notes (e.g., `Binary-Search-Trees.md` or `Bayes-Theorem.md`).
- Daily notes must follow format: `YYYY-MM-DD.md` in `01-Daily/`.
- Lecture notes must follow: `Lecture-01-Topic-Name.md` or `YYYY-MM-DD-Lecture-Topic.md` inside `02-Courses/<CourseCode>/Lectures/`.
- Avoid special characters in filenames (`:`, `/`, `\`, `?`, `*`, `"`).

## 2. Standard YAML Frontmatter Schemas

Every note in the vault must have clean YAML frontmatter at the very top.

### Concept Note Frontmatter:
```yaml
---
title: Concept Name
type: concept
tags: [concept, computer-science, algorithms]
aliases: [BST, Binary Search Tree]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: seedling # seedling | growing | evergreen
related: ["[[Related-Concept]]", "[[Course-Code]]"]
---
```

### Lecture Note Frontmatter:
```yaml
---
title: "Lecture 03: Big-O and Algorithm Analysis"
type: lecture
course: "[[COMS3110-Overview]]"
tags: [lecture, coms3110, algorithms]
date: YYYY-MM-DD
professor: "Dr. Smith"
topics: ["Time Complexity", "Space Complexity", "Asymptotic Notation"]
---
```

### Source / Reading Note Frontmatter:
```yaml
---
title: "Introduction to Algorithms (CLRS) - Chapter 3"
type: source
source_type: textbook # textbook | paper | video | article | lecture_slides
tags: [source, textbook, algorithms]
author: "Cormen et al."
year: 2022
url: ""
related_courses: ["[[COMS3110-Overview]]"]
---
```

### Active Recall / Quiz Note Frontmatter:
```yaml
---
title: "Quiz: Data Structures Midterm Review"
type: quiz
course: "[[COMS3110-Overview]]"
tags: [quiz, flashcards, active-recall, coms3110]
topics: ["Arrays", "Trees", "Graphs"]
created: YYYY-MM-DD
mastery_level: low # low | medium | high | mastered
---
```

## 3. Linking & Structure Guidelines
- **Interlinking**: When mentioning an established concept, always link with `[[Concept-Name]]` or `[[Concept-Name|Display Text]]`.
- **Headings**: Use hierarchical Markdown headings (`#`, `##`, `###`).
- **Callouts**: Use Obsidian callouts (`> [!NOTE]`, `> [!TIP]`, `> [!QUESTION]`, `> [!IMPORTANT]`, `> [!SUMMARY]`) for highlighting key insights, formulas, and questions.
- **Code & Math**: Use fenced code blocks with language tags (` ```python `) and LaTeX syntax for mathematics (`$E = mc^2$` inline or `$$ \sum_{i=1}^n i = \frac{n(n+1)}{2} $$` display).
