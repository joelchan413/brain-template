---
name: daily-planner
description: Generates automated daily study notes synced with Google Calendar schedules, campus locations, pre-linked lecture notes, and time-blocked study sessions.
---

# Daily Planner & Calendar Sync Skill

This skill automates the creation of comprehensive Daily Notes in `01-Daily/YYYY-MM-DD.md` by querying Google Calendar for the day's class schedule, lab blocks, and milestones.

## Triggering Prompts
- *"Generate my daily note for today"*
- *"Create daily plan for YYYY-MM-DD"*
- *"What is my schedule for tomorrow and build my daily study note"*

## Daily Note Generation Workflow

1. **Query Google Calendar**:
   - Call `google-calendar:list-events` with `timeMin` and `timeMax` set to `YYYY-MM-DD 00:00:00` and `23:59:59`.
   - Extract event start/end times, course titles/codes (e.g. `CPR E 3080`), and classroom locations (e.g. `1227 Hoover`).

2. **Calculate Free Study Windows**:
   - Identify gaps between classes (e.g. between 9:40 AM and 11:00 AM) and suggest focused study blocks (e.g., active recall, assignment prep).

3. **Scaffold Associated Lecture Notes**:
   - In `02-Courses/<CourseCode>/Lectures/`, generate or link corresponding lecture notes for the day (e.g. `[[2026-08-25-COMS3110-L01]]`).

4. **Format and Save `01-Daily/YYYY-MM-DD.md`**:
   - Include standard YAML frontmatter (`type: daily`, `date: YYYY-MM-DD`, `tags: [daily, study-log]`).
   - Fill in:
     - Top Priorities checklist
     - Google Calendar class schedule table with locations
     - Dedicated lecture notes links
     - Time-blocked study sessions
     - Quick Capture & End of Day Reflection
