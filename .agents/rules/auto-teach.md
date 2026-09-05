---
description: Automatically triggers the teach skill workflow whenever the user asks to learn a topic, concept, subject, or skill.
always_on: true
---

# Automatic Learning & Teaching Workflow

Whenever the user prompts to **learn**, **understand**, or **be taught** a topic, concept, subject, framework, theory, or skill (e.g., *"teach me X"*, *"I want to learn X"*, *"explain how X works from scratch"*, *"help me study/learn X"*, *"walk me through learning X"*):

1. **Auto-Route to `teach` Skill**:
   - Automatically adopt the pedagogical workflow defined in `.agents/skills/teach/SKILL.md`.
   - Do not just output a flat markdown summary; run the interactive teaching loop.

2. **Scope the Workspace**:
   - For an active academic course: Scope files inside `02-Courses/<CourseCode>/Teaching/` (e.g. `02-Courses/COMS3110/Teaching/`).
   - For standalone or general topics: Scope inside `00-Inbox/Learning/<Topic>/`.
   - Never write lesson directories or `MISSION.md` directly at the root of `brain/`.

3. **Teaching Workflow & Artifacts**:
   - **Grounding (`MISSION.md`)**: Ensure the learning objective and real-world goal are clarified and recorded.
   - **Sources (`RESOURCES.md`)**: Ground the lesson in high-trust primary sources rather than guessing.
   - **Interactive Lesson (`./lessons/*.html`)**: Produce a self-contained, beautifully styled HTML lesson equipped with interactive self-grading quizzes, visual diagrams, or simulators.
   - **Instant Browser Launch**: Automatically launch the HTML lesson in the user's browser using `Start-Process "<path_to_lesson.html>"`.
   - **Retention & Progression (`./learning-records/*.md`)**: Log key non-obvious lessons and calculate the user's Zone of Proximal Development (ZPD) for subsequent sessions.
   - **Quick Reference (`./reference/*.html`)**: Maintain high-density glossaries, syntax cheat sheets, and algorithm summaries.

4. **Vault Cohesion & Distillation**:
   - **Atomic Concepts**: Extract core definitions and theories into `03-Concepts/[[Concept-Name.md]]` with proper YAML frontmatter and `[[WikiLinks]]`.
   - **Spaced Repetition**: Convert retrieval quiz questions into Obsidian flashcards tagged with `#flashcards` or `#active-recall`.

