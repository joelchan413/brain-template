---
name: startup
description: Runs the session startup briefing routine when prompted with "startup" or "/startup", pulling latest changes from GitHub, initializing daily notes, checking Google Calendar schedules, scanning upcoming academic deadlines, and executing the Sunday Weekly Review if prompted after 3:00 PM on Sundays.
---

# Session Startup & Daily Briefing Skill

This skill is designed to be run at the start of every session when the user prompts with **`startup`**, **`/startup`**, **`start session`**, **`morning briefing`**, or **`boot up`**. It synchronizes the repository with GitHub, initializes the workspace, audits today's schedule, surfaces urgent deadlines, and prepares the user for high-velocity learning.

## Triggering Prompts
- `startup`
- `/startup`
- `start session`
- `morning briefing`
- `boot up`
- `let's begin today's session`

## Execution Sequence

```
[0. Git Remote Sync (git pull)] ➔ [1. Date & Daily Note Check] ➔ [2. Google Calendar Schedule] ➔ [3. Sunday Weekly Review Check] ➔ [4. Deadlines Radar] ➔ [5. Spaced Repetition Warmup] ➔ [6. Session Focus Prompt]
```

---

### Step 0: Remote Repository Synchronization (Git Pull)
1. Run `git pull --rebase origin main` (or `git pull`) to ensure the local vault is synchronized with remote updates (e.g., changes made on Obsidian Mobile, web, or other devices).
2. Report any newly pulled commits or sync status.

---

### Step 1: Date & Daily Note Check
1. Determine the current local time, date `YYYY-MM-DD`, and day of week.
2. Check if `01-Daily/<YYYY-MM-DD>.md` exists:
   - **If it exists**: Read top priorities and planned study windows.
   - **If not**: Run `python scripts/vault_cli.py daily --date <YYYY-MM-DD>` to scaffold today's note from `06-Templates/Template-Daily-Note.md`.

---

### Step 2: Google Calendar Health Check, Schedule & Locations
1. **Verify Google Calendar Access**:
   - Check authenticated accounts using `google-calendar:manage-accounts` (`action: 'list'`).
   - If any account status shows an error (such as `invalid_grant` or token expired):
     - Trigger `google-calendar:manage-accounts` (`action: 'add'`, `account_id: 'isu'`) to generate a new browser authorization link.
     - Add an alert in the startup briefing informing the user that Google Calendar access is disconnected, providing the clickable re-auth link.
2. **Query Schedule & Canvas Feed**:
   - If authenticated, query `google-calendar:list-events` across primary and Canvas calendar (`timeMin` set to `00:00:00`, `timeMax` set to `23:59:59` for today):
     - Extract class meetings, room locations (e.g. `1227 Hoover`, `0117 MacKay`), and work shifts.
     - Extract any Canvas assignment due dates synced to the calendar.
     - Identify the **Next Immediate Event** and time remaining.
     - Highlight open study and prep blocks between classes.

---

### Step 3: Special Sunday Weekly Review Routine (After 3:00 PM)
If **today is Sunday** AND **the current local time is $\ge$ 3:00 PM (15:00)**:
1. Check if `01-Daily/Weekly-Review-<YYYY>-W<xx>.md` exists for the current ISO week.
2. **If it does NOT exist yet**:
   - Run `python scripts/vault_cli.py weekly --write` to synthesize the past 7 days of study logs, task velocity, and new concepts.
   - Incorporate the **Weekly Retrospective Scorecard** directly into the Sunday Startup Briefing.
   - Prompt the user to set their Top 3 Academic Priorities for the upcoming week and record them.

---

### Step 4: Urgent Deadlines & Exam Milestones ($D-14$ to $D-0$)
1. Scan `02-Courses/*/*-Overview.md` for upcoming deliverables and exam dates:
   - 🔴 **CRITICAL**: Due today or tomorrow ($D-0, D-1$).
   - 🟡 **UPCOMING**: Due within 3–7 days ($D-3, D-7$).
   - 🔵 **ON RADAR**: Spaced repetition study milestones within 14 days ($D-14$).

---

### Step 5: Spaced Repetition & Study Readiness
1. Check available active recall decks and card counts in `exports/anki_cards.tsv` (or run `python scripts/anki_exporter.py`).
2. Highlight 1 suggested flashcard drill or quick quiz from an active course.

---

### Step 6: Executive Briefing & Focus Selector
Present a concise, structured markdown briefing:

```markdown
# 🌅 Session Startup Briefing (`YYYY-MM-DD`)

> [!INFO] Day Overview: **DayOfWeek, Month DD, YYYY**
> 📅 **Daily Note**: `[[01-Daily/YYYY-MM-DD|Today's Daily Note]]` (Active)
> ⏰ **Next Event**: `Event Name` at `Time` in `Location`

---

## 🏛️ Today's Schedule & Campus Locations
| Time | Category | Course / Event | Location | Dedicated Note |
| :--- | :--- | :--- | :--- | :--- |
| ... | ... | ... | ... | ... |

---

## ⚠️ High-Priority Deadlines & Exam Milestones
- 🔴 **Due in X Days**: `[[Course-Overview]]` — Assignment Name (`Date`)
- 🟡 **Upcoming Exam**: `[[Course-Overview]]` — Exam Name (`Date`)

---

## 🎯 What would you like to focus on for this session?
1. 📖 **Lecture Review / Capture**: Ingest or synthesize today's lecture notes.
2. 💻 **Assignment Sprint**: Break down or work on an upcoming problem set/lab.
3. 🧠 **Deep Learning (`/teach`)**: Interactive multi-session lesson on a concept.
4. ⚡ **Active Recall Drill**: 5-minute flashcard / practice quiz session.
5. 🗺️ **Vault Organization & Health**: Triage inbox, link concepts, or review schedule.
```
