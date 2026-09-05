---
name: exam-planner
description: Schedules optimal spaced-repetition study blocks leading up to exams directly on Google Calendar, and generates comprehensive Exam Prep MOCs in the vault.
---

# Reverse Exam & Spaced-Repetition Planner Skill

This skill calculates cognitive-science-backed spaced repetition intervals leading up to midterms, finals, and major project deadlines, creates an **Exam Prep Kit Note** in the vault, and schedules study blocks directly onto Google Calendar.

## Triggering Prompts
- *"Plan study schedule for [Course] [Exam] on [Date]"*
- *"Schedule spaced repetition blocks on Google Calendar for my COMS 3110 Midterm on October 15"*
- *"Create an exam prep kit for CPRE 3080"*

## Spaced Repetition Formula

Given an exam on date **$D$**:

| Phase | Timing | Duration | Activity | GCal Color / Tag |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Scope & Concept Map** | **$D - 14$** | 60 min | Syllabus audit, collect all lecture notes, identify weak topics | Blue / Study |
| **Phase 2: Deep Dive & Flashcards** | **$D - 7$** | 90 min | Fill concept gaps, create active recall quiz notes | Purple / Study |
| **Phase 3: Active Recall Sprint** | **$D - 3$** | 120 min | Timed practice exam, solve past problem sets without notes | Orange / Quiz |
| **Phase 4: High-Yield Polish** | **$D - 1$** | 60 min | Formula sheet review, mistake journal review, mental rehearsal | Green / Polish |
| **Exam Event** | **$D$** | Exam Time | The actual exam session | Red / Exam |

## Execution Workflow

1. **Calculate Interval Dates**:
   - Compute $D-14$, $D-7$, $D-3$, and $D-1$.
2. **Check Calendar Free-Busy**:
   - Query `google-calendar:list-events` or `get-freebusy` on those target dates to find available daytime or evening study slots that don't conflict with existing Iowa State classes.
3. **Schedule Events on Google Calendar**:
   - Call `google-calendar:create-event` for each study block with descriptive summaries (e.g., `[Study] COMS 3110: Active Recall Practice Exam`).
4. **Generate Exam Prep MOC**:
   - Create `02-Courses/<CourseCode>/Exams/Exam-Prep-<ExamName>.md` using `06-Templates/Template-Exam-Prep.md`.
   - Link all tested concept notes, active recall quizzes, and formula sheets.
