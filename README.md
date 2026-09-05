# Brain Template: College Second Brain & PKM System

A production-grade, Obsidian-compatible Personal Knowledge Management (PKM) vault integrated with agentic skills for college academics, active recall, spaced repetition, lecture synthesis, and automated schedule synchronization.

---

## Vault topology

```text
brain-template/
├── .agents/                      # AI Agent configuration
│   ├── rules/
│   │   ├── auto-teach.md         # Auto-routes learning requests to interactive course mode
│   │   ├── session-startup.md    # Automatic morning startup sequence
│   │   └── vault-standards.md    # Note schemas, YAML frontmatter, and linking rules
│   └── skills/                   # 13 specialized agent skills
│       ├── startup/              # Morning schedule briefing, calendar sync, deadline radar
│       ├── shutdown/             # Evening reflection, Anki export, tomorrow note scaffolding
│       ├── teach/                # Stateful personal tutor with interactive HTML lessons
│       ├── vault-capture/        # Fast-capture transcripts, slides, and papers into notes
│       ├── study-assistant/      # Active recall quizzes and Feynman explanations
│       ├── flashcard-synthesizer/# Extracts high-yield flashcards to Anki TSV format
│       ├── course-manager/       # Scaffolds new courses, lecture indexes, and course MOCs
│       ├── assignment-tracker/   # Deconstructs homework and coding rubrics into checklists
│       ├── canvas-course-sync/   # Ingests syllabi schedules into lecture indices
│       ├── daily-planner/        # Generates time-blocked daily study notes
│       ├── weekly-review/        # Sunday academic retrospective and task velocity audit
│       ├── exam-planner/         # Spaced-repetition study milestones (D-14, D-7, D-3, D-1)
│       ├── unslop/               # Writing filter cutting AI filler, clichés, and emojis
│       └── vault-health/         # Link diagnostics and orphan note detection
├── 00-Inbox/                     # Fast-capture landing zone for raw ideas and web snippets
├── 01-Daily/                     # Daily notes (YYYY-MM-DD.md) and weekly reviews
├── 02-Courses/                   # Active academic courses (structured by course code)
│   └── SAMPLE1010/               # Starter example course demonstrating vault patterns
│       ├── Assignments/          # Problem sets, coding labs, and rubrics
│       ├── Exams/                # Exam prep MOCs and active recall quizzes
│       ├── Lectures/             # Markdown lecture notes with Cornell-style takeaways
│       ├── Readings/             # Paper annotations and textbook chapter notes
│       └── SAMPLE1010-Overview.md# Central Course Map of Content (MOC)
├── 03-Concepts/                  # Atomic evergreen notes interlinked with [[WikiLinks]]
├── 04-Sources/                   # Syllabi, literature notes, and textbook references
├── 05-MOCs/                      # Maps of Content (Academic-Hub.md dashboard)
├── 06-Templates/                 # Obsidian templates (Daily, Lecture, Concept, Quiz, MOC)
├── 07-Archive/                   # Inactive courses and past semesters
├── docs/
│   ├── Google-Calendar-MCP-Setup-Guide.md # Step-by-step MCP configuration guide
│   └── decisions/                # Architecture Decision Records (ADRs)
├── exports/                      # Target directory for exported anki_cards.tsv
├── scripts/                      # Local Python automation tools
│   ├── vault_cli.py              # Master CLI dispatcher (health, stubs, anki, daily, weekly)
│   ├── vault_health.py           # Integrity checker for broken links and missing frontmatter
│   ├── generate_concept_stubs.py # Scaffolds atomic notes for broken concept links
│   ├── anki_exporter.py          # Extracts active recall questions to Anki TSV format
│   ├── weekly_review.py          # Aggregates completed tasks and study metrics
│   ├── daily_shutdown.py         # Evening shutdown routines and card extraction
│   └── test_tools.py             # Unit and integration test suite
├── AGENTS.md                     # Agent system prompt and writing rules
├── README.md                     # This setup and workflow guide
└── requirements.txt              # Python dependencies
```

---

## Step-by-step setup guide

### Step 1: Clone the template repository
Clone this repository to your local drive where you want your personal vault to live:

```bash
git clone https://github.com/joelchan413/brain-template.git my-brain
cd my-brain
```

### Step 2: Open the vault in Obsidian
1. Download and install [Obsidian](https://obsidian.md/) (macOS, Windows, or Linux).
2. Launch Obsidian and select **Open folder as vault**.
3. Navigate to your cloned `my-brain` directory and click **Select Folder**.
4. When prompted about "Trust author and enable plugins", click **Trust and enable plugins**.

### Step 3: Verify community plugins
The `.obsidian/` folder includes configurations for community plugins:
- **Dataview**: Renders dynamic query tables for course overviews, assignments, and daily notes.
- **Spaced Repetition**: Enables native flashcard reviews within Obsidian using `#flashcards` tags.
- **Calendar**: Adds a calendar widget in the sidebar that links directly to `01-Daily/YYYY-MM-DD.md`.
- **Omnisearch**: Provides instant fuzzy search across notes, PDFs, and OCR text.
- **Tasks**: Tracks checklist items across daily notes and assignments.
- **Linter**: Automatically formats markdown and frontmatter on save.

To verify they are active:
1. In Obsidian, open **Settings** (gear icon) -> **Community plugins**.
2. Confirm **Dataview**, **Spaced Repetition**, **Calendar**, and **Omnisearch** are toggled on.

### Step 4: Configure the Python automation environment
The scripts automate note scaffolding, weekly reviews, health checks, and flashcard exports using standard library Python 3.10+:

```bash
# Verify Python version (requires Python 3.10 or newer)
python --version

# Optional: Install extra document processing libraries
pip install -r requirements.txt
```

Verify your setup by running the vault statistics command:
```bash
python scripts/vault_cli.py stats
```

### Step 5: Configure AI agents (Antigravity CLI / Cursor / Claude Code)
This vault includes customized `.agents/skills` and `AGENTS.md` rules.

#### Using Antigravity CLI:
1. Install the `antigravity` CLI.
2. Launch Antigravity inside your vault root:
   ```bash
   agy
   ```
3. The CLI detects `.agents/skills/` and `AGENTS.md` automatically.

#### Using Cursor or Claude Code:
Point your tool to the workspace root. Both tools read `AGENTS.md` and can invoke scripts under `scripts/`.

### Step 6: Connect Google Calendar (optional but recommended)
To enable automated schedule lookups during morning briefings and daily note scaffolding:
1. Follow the step-by-step instructions in [Google-Calendar-MCP-Setup-Guide.md](file:///C:/Users/User/Documents/Github/brain-template/docs/Google-Calendar-MCP-Setup-Guide.md).
2. Configure the Google Calendar MCP server in your agent configuration.
3. Authenticate with your primary university or personal Google account.

---

## The academic operating system: Daily workflow

### 1. Morning startup briefing
At the start of your day, prompt your agent:
> *"startup"* or *"/startup"*

What happens:
- Runs `git pull` to fetch any mobile or web updates.
- Verifies or generates today's daily note: `01-Daily/YYYY-MM-DD.md`.
- Queries Google Calendar for your class schedule, classroom locations, and work shifts.
- Scans `02-Courses/` for deliverables due in the next 14 days ($D-14$ to $D-0$).
- Suggests an active recall flashcard drill from `exports/anki_cards.tsv`.
- Prompts you to select your primary focus for the study session.

### 2. Lecture notes capture
During or after class, drop slides, raw transcripts, or rough notes:
> *"Here are the slides for SAMPLE 1010 Lecture 2. Create the lecture note and extract any new concepts."*

What happens:
- The agent builds a structured note in `02-Courses/<Course>/Lectures/` with learning objectives, ASCII architecture diagrams, takeaways, and active recall flashcards.
- Links atomic definitions to `03-Concepts/[[Concept-Name]]`.
- Updates the course lecture index table in `<Course>-Overview.md`.

### 3. Homework & coding lab deconstruction
When receiving a complex assignment:
> *"Break down SAMPLE 1010 Homework 1 into milestone tasks and concept links."*

What happens:
- Creates an assignment file under `02-Courses/<Course>/Assignments/`.
- Deconstructs the assignment rubric into phased milestones (Decomposition, Implementation, Verification).
- Links prerequisite concept notes so you know what to review before writing code.

### 4. Interactive deep learning (`/teach`)
Whenever you want to learn a difficult topic from scratch:
> *"Teach me Dynamic Programming from scratch."*

What happens:
- Activates the `teach` skill.
- Builds an interactive, styled HTML lesson with self-grading quizzes and visual simulators.
- Launches the lesson directly in your browser.
- Tracks your retention and Zone of Proximal Development (ZPD) across learning records.

### 5. Evening wrap-up & shutdown
When finished studying for the day:
> *"shutdown"* or *"/shutdown"*

What happens:
- Audits completed checklist items in today's daily note.
- Prompts for brief reflection bullets: *What went well*, *What got delayed*, *Tomorrow's main priority*.
- Extracts all new `#flashcards` or quiz blocks across recently edited notes into `exports/anki_cards.tsv`.
- Checks tomorrow's schedule on Google Calendar and scaffolds tomorrow's daily note.

### 6. Sunday weekly review
Every Sunday afternoon:
> *"Run my weekly review."*

What happens:
- Aggregates task completion rates, study logs, and new concept growth over the past 7 days.
- Audits syllabus milestones across all active courses for the upcoming 14 days.
- Writes a permanent retrospective note: `01-Daily/Weekly-Review-YYYY-Wxx.md`.

---

## Python CLI command reference

All vault automation is accessible directly through `scripts/vault_cli.py`:

```bash
# View overall vault statistics (note count, active courses, concept count)
python scripts/vault_cli.py stats

# Audit vault health (broken links, orphaned notes, missing frontmatter)
python scripts/vault_cli.py health

# Preview concept stubs that would be created from unresolved wikilinks
python scripts/vault_cli.py stubs --dry-run

# Automatically scaffold missing concept notes for unresolved wikilinks
python scripts/vault_cli.py stubs --route-all

# Export all active recall questions and flashcard blocks to Anki TSV format
python scripts/vault_cli.py anki --out exports/anki_cards.tsv

# Scaffold a daily note from template
python scripts/vault_cli.py daily --date YYYY-MM-DD

# Generate end-of-week academic retrospective and task velocity scorecard
python scripts/vault_cli.py weekly --write

# Run the test suite to verify script integrity
python scripts/test_tools.py
```

---

## Customizing the template for your semester

### 1. Add your active courses
1. Run the `course-manager` skill or copy `02-Courses/SAMPLE1010/` to a new course directory (e.g. `02-Courses/MATH2400/`).
2. Rename `SAMPLE1010-Overview.md` to `MATH2400-Overview.md`.
3. Update the YAML frontmatter (`course_code`, `institution`, `schedule`, `instructors`).
4. Update the Dataview query paths inside the overview file to point to your new course folder.

### 2. Import your syllabi
1. Place syllabus files or text in `04-Sources/Syllabus-<CourseCode>-Fall-2026.md`.
2. Ask your agent: *"Sync syllabus dates from 04-Sources/Syllabus-MATH2400 into MATH2400-Overview.md"*.

### 3. Remove or archive sample content
Once comfortable with the structure:
- Move `SAMPLE1010` into `07-Archive/` or delete it.
- Update `05-MOCs/Academic-Hub.md` to reflect your semester courses.

---

## Core rules & unslop writing standards

Every note in this vault follows strict technical standards:
- **Sentence case headings**: Use standard sentence case (`## In-depth lecture takeaways`, not Title Case).
- **No decorative emojis**: No emojis in titles, headings, bullet points, or tables.
- **No em dashes**: Use commas or periods.
- **No AI vocabulary**: Ban empty words such as *crucial*, *delve*, *foster*, *leverage*, *paramount*, *pivotal*, *profound*, *showcase*, *tapestry*, *testament*, *underscore*, *utilize*, and *vital*. State direct facts, numbers, and concrete mechanisms.
- **Atomic linking**: Connect concepts using standard `[[Concept-Name]]` wikilinks.
- **Zero proprietary locks**: Plain GitHub Flavored Markdown and valid YAML frontmatter ensure notes remain readable in any text editor.
