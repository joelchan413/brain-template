---
description: Automatically triggers the startup session briefing workflow whenever the user prompts with startup, /startup, start session, morning briefing, or boot up, including running the weekly review when prompted on Sunday after 3:00 PM.
always_on: true
---

# Session Startup Workflow Rule

Whenever the user starts a session with **`startup`**, **`/startup`**, **`start session`**, **`morning briefing`**, or **`boot up`**:

1. **Adopt `startup` Skill**:
   - Immediately execute the sequence defined in `.agents/skills/startup/SKILL.md`.
   - Steps:
     1. Verify/create today's daily note in `01-Daily/YYYY-MM-DD.md`.
     2. Query Google Calendar for today's classes and locations.
     3. **Sunday $\ge$ 3:00 PM Check**: If it is Sunday afternoon/evening ($\ge$ 15:00) and this week's `Weekly-Review-YYYY-Wxx.md` has not yet been generated, automatically run the **Weekly Review** synthesis and include the weekly retrospective in the briefing.
     4. Scan `02-Courses/` for upcoming deadlines ($D-14$ to $D-0$).
     5. Check active recall flashcard decks.
     6. Present the Session Briefing dashboard and prompt for the session focus.

2. **Tone & Experience**:
   - Clean, high-density, actionable formatting using standard GitHub markdown tables, alerts, and `[[WikiLinks]]`.
