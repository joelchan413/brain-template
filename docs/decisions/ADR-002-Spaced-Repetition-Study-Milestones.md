# ADR-002: Cognitive Spaced-Repetition Study Protocol ($D-14, D-7, D-3, D-1$)

## Status
Accepted

## Date
2026-08-15

## Context
Preparing for engineering and computer science exams (e.g., Operating Systems, Algorithms, Ethics, Senior Design) requires systematic active recall across spaced intervals rather than last-minute cramming.

Requirements:
- Predictable, mathematically grounded review intervals leading up to exam date $D$.
- Automatic generation of self-contained Exam Prep MOCs containing concept checklists, practice problem indexes, and mistake logs.
- Automatic insertion of study blocks into Google Calendar around existing class schedules.

## Decision
Adopt a 4-tier spaced repetition ramp protocol:

1. **Phase 1 ($D-14$, 2 weeks out - 60 min)**: Scope & Concept Map Audit.
2. **Phase 2 ($D-7$, 1 week out - 90 min)**: Deep Dive & Flashcard / Quiz Note Generation.
3. **Phase 3 ($D-3$, 3 days out - 120 min)**: Timed Active Recall & Past Exam Problem Sets.
4. **Phase 4 ($D-1$, Day before - 60 min)**: High-Yield Formula Sheet & Mistake Log Polish.

## Alternatives Considered

### 1. Flashcard-Only (Anki / SM-2 algorithm)
- **Pros**: Optimal for atomic fact memorization.
- **Cons**: Does not structure high-level exam prep (e.g. proof writing, coding labs, large-scale problem sets, or calendar time-blocking).
- **Decision**: Anki/SM-2 flashcards complement Phase 2 & 3, but the 4-phase milestone protocol governs overall study planning.

### 2. Manual Calendar Booking
- **Pros**: Full manual control.
- **Cons**: High cognitive overhead and friction often leads to delayed studying or missed review intervals.

## Consequences
- Every exam has a dedicated kit note in `02-Courses/<CourseCode>/Exams/Exam-Prep-<ExamName>.md`.
- Calendar blocks are created deterministically with color coding and clear learning objectives.
- The `exam-planner` skill standardizes this workflow across all courses.
