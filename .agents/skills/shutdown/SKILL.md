---
name: shutdown
description: Runs the session shutdown and daily wrap-up routine when prompted with "finished for the day", "wrap up", "/shutdown", "done for today", "shutdown", or "end session". Audits completed tasks, logs daily reflections, extracts new Anki flashcards, checks tomorrow's Google Calendar schedule, and scaffolds tomorrow's daily note.
---

# Daily Shutdown & Session Wrap-Up Skill

This skill is designed to run at the end of the day or study session when the user prompts with **`finished for the day`**, **`done for today`**, **`wrap up`**, **`shutdown`**, **`/shutdown`**, **`end session`**, or **`call it a night`**. It audits task velocity, logs daily reflections, exports newly generated active recall flashcards, checks tomorrow's schedule, and sets up a frictionless start for the next morning.

## Triggering Prompts
- `finished for the day`
- `done for the day`
- `done for today`
- `wrap up for today`
- `shutdown`
- `/shutdown`
- `end session`
- `eod` / `end of day`
- `call it a day`
- `call it a night`

---

## Execution Sequence

```
[1. Daily Task Audit] ➔ [2. Anki Flashcard Sync] ➔ [3. Tomorrow's Calendar & Scaffolding] ➔ [4. Reflection & Log Update] ➔ [5. Git Remote Backup (Commit & Push)] ➔ [6. Executive Wrap-Up Summary]
```

---

### Step 1: Daily Task & Study Audit
1. Determine the current local date `YYYY-MM-DD`.
2. Inspect `01-Daily/<YYYY-MM-DD>.md`:
   - Identify all completed tasks (`- [x]`) vs pending tasks (`- [ ]`).
   - Calculate task completion percentage.
   - List any incomplete priority items.

---

### Step 2: Anki Flashcard Extraction & Sync
1. Run `python scripts/vault_cli.py anki` (or `python scripts/daily_shutdown.py`) to automatically extract all active recall questions (`### Q:` / `> [!TIP]-`) across recently edited notes.
2. Confirm the export into `exports/anki_cards.tsv`.

---

### Step 3: Tomorrow's Outlook & Google Calendar Sync
1. Calculate tomorrow's date ($D+1$).
2. Query `google-calendar:list-events` for tomorrow (`timeMin` set to tomorrow `00:00:00`, `timeMax` set to tomorrow `23:59:59`):
   - Identify tomorrow's first lecture/event, start time, and campus location (e.g., `0171 Durham`, `1227 Hoover`).
   - Identify any deadlines due tomorrow ($D-0$ / $D-1$).
3. Scaffold tomorrow's daily note `01-Daily/<Tomorrow-Date>.md` with tomorrow's schedule table and carry over any top incomplete tasks from today.

---

### Step 4: Daily Reflection & Log Update
1. Ask the user (or record based on session accomplishments):
   - **What went well today?** (Major concepts mastered, assignments completed).
   - **What got delayed or needs focus tomorrow?**
2. Update the `## 🔄 Daily Reflection & Shutdown` section in `01-Daily/<YYYY-MM-DD>.md`.

---

### Step 5: Git Remote Backup (Commit & Push)
1. Automatically stage all newly created notes, daily logs, and exports (`git add -A`).
2. Create an atomic daily wrap-up commit:
   `git commit -m "docs(daily): daily wrap-up and reflection for <YYYY-MM-DD>"`
3. Push all committed changes to GitHub:
   `git push origin main`
4. Confirm successful remote backup and clean working tree.

---

### Step 6: Executive Wrap-Up & Sign-Off
Present a structured, motivating evening briefing:

```markdown
# 🌙 Daily Shutdown & Wrap-Up (`YYYY-MM-DD`)

> [!SUCCESS] Great work today! Here is your daily wrap-up summary:

---

## 📊 Daily Scorecard & Velocity
- ✅ **Completed Tasks (X/Y)**: `X% completion rate`
  - Completed: ...
- ⏳ **Carried Over to Tomorrow**:
  - `[ ] Task 1`
- 🎴 **Anki Flashcards**: `N total cards synchronized to exports/anki_cards.tsv`
- 🚀 **GitHub Backup**: `Committed & Pushed to origin/main` (Clean)

---

## 🌅 Tomorrow's Outlook (`YYYY-MM-DD`)
- ⏰ **First Event**: `Course / Event Name` at `Time` in `Location`
- 📅 **Tomorrow's Daily Note**: `[[01-Daily/YYYY-MM-DD|Tomorrow's Note]]` (Scaffolded & Ready)
- ⚠️ **Upcoming Deadlines**: (If any due in next 48 hours)

---

## 🧠 Concepts & Notes Created/Updated Today
- [[Concept-1]]
- [[Concept-2]]

---

💤 **Rest well and see you tomorrow! Run `startup` or `/startup` when you're ready to begin.**
```
