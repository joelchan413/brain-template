---
name: assignment-tracker
description: Scaffolds and breaks down complex academic homework assignments, problem sets, coding labs, and project rubrics into actionable tasks, concept wikilinks, and milestone checkpoints.
---

# Assignment Tracker & Lab Breakdown Skill

This skill helps students break down large coursework assignments, programming labs, and problem sets into bite-sized actionable steps with prerequisite concept links.

## Triggering Prompts
- *"Break down COMS 3110 Homework 1"*
- *"Scaffold CPR E 3080 Lab 1"*
- *"Track new assignment for Course X"*
- *"Create assignment workspace for [[Assignment-Name]]"*

## Assignment Scaffolding Workflow

1. **Create the Assignment Workspace**:
   - Location: `02-Courses/<CourseCode>/Assignments/<CourseCode>-<AssignmentType>-<Number>.md`
   - Include standard YAML frontmatter:
     ```yaml
     ---
     title: "<CourseCode> <AssignmentType> <Number>: <Topic>"
     type: assignment
     course: "[[<CourseCode>-Overview]]"
     tags: [assignment, <course_tag>, coursework]
     created: YYYY-MM-DD
     due_date: YYYY-MM-DD
     status: not-started # not-started, in-progress, completed, submitted
     priority: high # low, medium, high
     ---
     ```

2. **Structure the Assignment Note**:
   - **Overview & Rubric Criteria**: Due date, points, submission format (Canvas, Git repo).
   - **Prerequisite Concepts & Readings**: Explicit `[[Concept-Name]]` links needed to solve the problem.
   - **Step-by-Step Task Breakdown**: Ordered checklist tasks (`- [ ] Step 1: ...`).
   - **Testing & Verification Suite**: Edge cases, unit tests, sanity checks.
   - **Submission Checklist**: Git tag, PDF export, Canvas upload verification.

3. **Link to Course MOC & Calendar**:
   - Add the assignment to `## 📝 Assignments & Problem Sets` in `02-Courses/<CourseCode>/<CourseCode>-Overview.md`.
   - If due date is specified, offer to create calendar study blocks or reminder alerts.
