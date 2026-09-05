---
name: canvas-course-sync
description: Ingests syllabus text, course schedules, Canvas/Blackboard modules, or lecture slide decks to automatically populate course overviews, lecture indexes, exam dates, and assignment deadlines in the vault.
---

# Canvas Course Sync & Syllabus Ingester Skill

This skill ingests raw course syllabi, lecture schedules, LMS announcements, and assignment descriptions into structured Course MOCs and lecture indices.

## Triggering Prompts
- *"Import syllabus for CPR E 4370"*
- *"Here is my syllabus text for COMS 3110, sync it to the course overview"*
- *"Populate lecture schedule from this course calendar"*
- *"Ingest Canvas assignment list"*

## Syllabus Ingestion Workflow

1. **Extract Structured Course Metadata**:
   - Course code, course title, instructor, office hours, classroom location.
   - Weekly lecture topics and dates.
   - Homework, lab, project, and exam dates and weightings.

2. **Update Course Overview MOC**:
   - Location: `02-Courses/<CourseCode>/<CourseCode>-Overview.md`
   - Populate `## 🎯 Key Milestones & Exam Dates` with parsed due dates.
   - Populate `## 📚 Lecture Index` with lecture numbers, dates, titles, and concept wikilinks.
   - Populate `## 🧠 Core Concept Graph` with key subjects covered in the syllabus.

3. **Scaffold Missing Items**:
   - Run `python scripts/generate_concept_stubs.py --target <Concept>` or `--route-all` to scaffold placeholders for referenced concept notes and assignments.

4. **Sync Calendar & Study Milestones**:
   - Offer to schedule exam study blocks ($D-14, D-7, D-3, D-1$) via `exam-planner` and recurring lecture reminders on Google Calendar.
