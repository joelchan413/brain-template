---
name: weekly-review
description: Runs automated end-of-week academic retrospectives, analyzes study velocity and task completion rates, checks 14-day upcoming syllabus milestones, and prepares the next week's focus areas.
---

# Weekly Review & Academic Retrospective Skill

This skill conducts a structured end-of-week review session, synthesizing daily study notes, task completion velocity, concept graph growth, and upcoming exam/assignment deadlines.

## Triggering Prompts
- *"Run my weekly review"*
- *"Synthesize my week's study progress"*
- *"Prepare for next week and review open tasks"*
- *"Generate weekly review for Week WW / YYYY-MM-DD"*

## Weekly Review Workflow

1. **Execute Progress Synthesis**:
   - Run `python scripts/weekly_review.py --date <YYYY-MM-DD> --write` to parse all daily logs from `01-Daily/` for the target week.
   - Extract:
     - Task execution velocity (% of tasks checked off vs carried over).
     - New concept notes created in `03-Concepts/`.
     - In-class quick captures and reflections (`What went well`, `What got delayed`).

2. **Audit Upcoming 14-Day Academic Milestones**:
   - Scan `02-Courses/*/*-Overview.md` for upcoming:
     - Homework assignments and lab deadlines.
     - Spaced repetition exam milestones ($D-14, D-7, D-3, D-1$).
     - Team project deliverables.

3. **Query Next Week's Google Calendar Schedule**:
   - Check `google-calendar:list-events` for the upcoming week to identify exam slots, lab sessions, and open study windows.

4. **Facilitate Interactive Retrospective**:
   - Present a concise executive summary to the user:
     - 🎯 **Weekly Scorecard**: Completed tasks, attendance, study hours.
     - 💡 **Knowledge Growth**: Concepts added to the evergreen web.
     - ⚠️ **Upcoming Deadlines**: Pressing dates for the next 1–2 weeks.
   - Ask the user for their top 3 academic priorities for next week and insert them into the generated `01-Daily/Weekly-Review-YYYY-Wxx.md` note.
