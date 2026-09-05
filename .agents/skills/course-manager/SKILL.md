---
name: course-manager
description: Scaffolds new academic courses, organizes lecture series, tracks syllabus deadlines, and maintains course Maps of Content (MOCs).
---

# Course Manager Skill

Use this skill to set up new academic courses, organize semester schedules, and link course materials.

## Workflow

### 1. New Course Scaffolding
When the user says "Set up course CS201 Data Structures":
1. Create directory structure:
   - `02-Courses/<CourseCode>/`
   - `02-Courses/<CourseCode>/Lectures/`
   - `02-Courses/<CourseCode>/Assignments/`
   - `02-Courses/<CourseCode>/Readings/`
   - `02-Courses/<CourseCode>/Exams/`
2. Create the Course MOC at `02-Courses/<CourseCode>/<CourseCode>-Overview.md` using `06-Templates/Template-Course-MOC.md`.
3. Add a wikilink in `05-MOCs/Semester-Overview.md` and `05-MOCs/Academic-Hub.md`.

### 2. Syllabus / Deadline Sync
- Ingest syllabus files or dates and populate the milestone table in the course overview note.
- Create placeholder notes for upcoming assignments.
