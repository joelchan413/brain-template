# Brain - College Second Brain & PKM Vault

Welcome to the `brain-template` workspace. This repository is an Obsidian-compatible Personal Knowledge Management (PKM) vault specifically engineered for college studies, academic learning, and long-term knowledge retention.

## Vault Topology & Workflow Conventions

- **`00-Inbox/`**: Fast capture landing zone for raw ideas, unorganized snippets, and web clippings.
- **`01-Daily/`**: Daily notes (`YYYY-MM-DD.md`) containing study plans, lecture logs, time-blocking, and daily reflections.
- **`02-Courses/`**: Active academic courses structured by semester or course code (e.g., `SAMPLE1010/`).
  - Subfolders: `Lectures/`, `Assignments/`, `Readings/`, `Exams/`.
- **`03-Concepts/`**: Atomic, evergreen concept notes representing reusable ideas, definitions, algorithms, and theories. Always interlinked with `[[Concept Name]]`.
- **`04-Sources/`**: Literature and source notes (textbooks, research papers, articles, YouTube videos, slide decks, syllabi).
- **`05-MOCs/`**: Maps of Content. High-level indexes, hubs, and curriculum overviews linking concepts and courses (`[[Academic-Hub]]`).
- **`06-Templates/`**: Standard templates for Obsidian (Daily, Lecture, Concept, Source, Exam Prep, Flashcards).
- **`07-Archive/`**: Inactive courses, completed projects, and past semesters.

## Available Workspace Skills

When working in this vault, use these specialized skills located in `.agents/skills/`:
- **`startup`**: Morning briefing and session bootstrapper that checks Google Calendar schedules, verifies today's daily note, audits 14-day upcoming deadlines, and sets the session focus. (Triggered via `startup`, `/startup`, `start session`).
- **`shutdown`**: Evening wrap-up and session shutdown that audits completed tasks, records daily reflections, extracts new Anki flashcards, checks tomorrow's Google Calendar schedule, and scaffolds tomorrow's daily note. (Triggered via `finished for the day`, `done for today`, `wrap up`, `shutdown`, `/shutdown`, `end session`).
- **`teach`**: Interactive personal tutor that builds stateful, multi-session learning courses with interactive HTML lessons, self-grading quizzes, learning records (ZPD tracking), and cheat sheets. (Automatically triggered whenever asking to learn/be taught a topic).
- **`vault-capture`**: Ingest URLs, papers, notes, or quick thoughts into the correct folder with standardized YAML frontmatter.
- **`study-assistant`**: Generate active recall quizzes, spaced repetition flashcards, practice exam questions, and intuitive explanations for complex concepts.
- **`flashcard-synthesizer`**: Extract high-yield active recall flashcards from lecture notes and export directly to Anki (`exports/anki_cards.tsv`) and Obsidian Spaced Repetition format.
- **`course-manager`**: Scaffold new courses, track syllabus milestones, and organize weekly lecture modules.
- **`assignment-tracker`**: Deconstruct complex homework assignments, programming labs, and rubrics into milestone checklists and prerequisite concept links.
- **`canvas-course-sync`**: Ingest raw syllabus schedules, LMS announcements, and slide decks to auto-populate course overviews and lecture indices.
- **`daily-planner`**: Automatically generate daily notes synced with Google Calendar schedules, classroom locations, and time-blocked study sessions.
- **`weekly-review`**: Conduct structured end-of-week retrospectives analyzing task velocity, concept growth, and 14-day upcoming deadlines.
- **`exam-planner`**: Compute spaced-repetition study milestones ($D-14, D-7, D-3, D-1$) for upcoming exams, create Exam Prep MOCs, and schedule study blocks on Google Calendar.
- **`unslop`**: Mandatory writing filter that cuts AI tells, bans decorative emojis, bans em dashes, removes AI vocabulary, enforces sentence case headings, and injects direct human voice and concrete mechanics.
- **`vault-health`**: Run diagnostic checks on dead links, orphaned notes, missing frontmatter, and auto-link related concepts.

## Core Rules for Agent Actions

1. **Format Standards**: All notes must use standard GitHub Flavored Markdown and valid YAML frontmatter.
2. **Atomic Linking**: Always use `[[WikiLink]]` syntax to connect notes to existing or related concepts.
3. **No Proprietary Syntax**: Avoid tool-specific locks so the vault remains 100% portable and readable in Obsidian, VS Code, or plain text.
4. **No Auto-Generated / Speculative Lecture Notes**: NEVER create, pre-populate, or synthesize lecture notes for any class unless the user explicitly provides raw notes, recordings, slides, or explicitly requests the capture/review of that specific lecture. Course overviews, daily notes, and schedules must only list upcoming lecture topics as plain text or table entries without creating speculative lecture files.
5. **Unslop Writing Standards (Mandatory for ALL Responses & Vault Notes)**:
   - **No decorative emojis**: Never use emojis in headings, titles, tables, or list items (`# 📝`, `## 🎯`, etc.).
   - **No em dashes**: Never use em dashes (`, ` or `--`). Use periods or commas.
   - **Sentence case headings**: Headings must use standard sentence case, not title case.
   - **No AI vocabulary**: Ban words like *crucial*, *delve*, *foster*, *leverage*, *paramount*, *pivotal*, *profound*, *showcase*, *tapestry*, *testament*, *underscore*, *utilize*, *vital*, and *nuanced*. Use plain, concrete words.
   - **No inline-header restatements**: Do not use bold labels that just restate the sentence (`**Feature:** This feature...`). Write direct prose.
   - **No chatbot filler or sycophancy**: Cut conversational filler, praise, and generic closing check-ins (*"Let me know if you need anything else"*, *"I hope this helps"*). Answer directly and state facts.
   - **Natural rhythm and active voice**: Mix short and long sentences. State what happened, who did it, and the exact mechanics or numbers.
