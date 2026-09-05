---
name: study-assistant
description: Generates active recall quizzes, spaced repetition flashcards, practice exams, and intuitive Feynman-technique explanations from vault notes.
---

# Study Assistant & Active Recall Skill

Use this skill when the user asks to study, prepare for an exam, generate quizzes/flashcards, or break down difficult course topics.

## Study Capabilities

### 1. Active Recall Quiz Generation
When asked to create a quiz for a topic or course:
- Scan `02-Courses/<CourseCode>/` and relevant `03-Concepts/` notes.
- Create or update a quiz note in `02-Courses/<CourseCode>/Exams/Quiz-<Topic>.md` following `06-Templates/Template-Active-Recall-Quiz.md`.
- Formulate 3 tiers of questions:
  1. **Tier 1 (Factual / Definitional)**: "What is X?", "Define invariant Y".
  2. **Tier 2 (Mechanics & Edge Cases)**: "Why does algorithm A fail when condition B occurs?", "Compare X and Y".
  3. **Tier 3 (Synthesis / Applied Problem)**: Code snippets, math derivations, or scenario analysis.
- Wrap answers in `<details><summary><b>Reveal Solution</b></summary>...</details>` so the user can test themselves without accidental spoilers.

### 2. Feynman Technique Explanation (ELI5)
When the user expresses confusion on a concept:
- Break the idea down into:
  1. Real-world analogy.
  2. Concrete step-by-step invariant.
  3. Where students typically make mistakes.
- Offer to save the distilled explanation into `03-Concepts/<Concept-Name>.md`.

### 3. Practice Exam Formulation
- Build full practice exams with timed recommendations, rubric scoring, and solution keys based on course lecture series.
