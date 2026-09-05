---
name: unslop
description: Mandatory writing filter and text refactoring skill that strips AI tells, bans decorative emojis, bans em dashes, removes corporate AI vocabulary, enforces sentence case headings, cuts conversational filler, and injects direct human voice and concrete mechanics.
---

# Unslop Writing Filter Skill

Use this skill to audit, edit, and refactor text into direct, natural, and precise human prose free from generative AI tells and chatbot filler. This skill is both an active editing tool (invoked via `unslop`, `unslop this note`, or `clean up AI writing`) and a permanent writing standard for every response and note in the vault.

## Triggering prompts
- `unslop`
- `unslop this note`
- `clean up AI writing`
- `remove AI slop`
- `make this sound human`
- `refactor writing`

---

## Core rules and guidelines

### 1. Ban decorative emojis
- Never place emojis in titles, headers (`#`, `##`, `###`), table cells, bullet points, or callout labels.
- Remove decorative icons like `# 📝 Notes`, `## 🎯 Objectives`, or `- ⚡ Fast`.
- Emojis distract from technical density and serve as an immediate visual tell of machine generation.

### 2. Ban em dashes
- Never use em dashes (`—` or `--`) in prose or titles.
- Em dashes are the most common rhythmic signature of generative language models.
- Replace em dashes with commas, periods, semicolons, or parentheses. If two ideas are independent, split them into two distinct sentences.

### 3. Enforce sentence case headings
- All markdown headings must use sentence case:
  - ✅ `# In-depth lecture takeaways`
  - ✅ `## Key learning objectives`
  - ❌ `# In-Depth Lecture Takeaways`
  - ❌ `## Key Learning Objectives`
- Proper nouns, acronyms, and course codes retain standard capitalization (`COM S 3110`, `Linux`, `CPU`, `POSIX`).

### 4. Remove AI vocabulary
Ban inflated corporate and pseudo-intellectual vocabulary. Replace them with simple, concrete words:

| Banned AI word | Plain human replacement |
| :--- | :--- |
| *crucial*, *pivotal*, *paramount*, *vital* | *important*, *necessary*, *needed*, *central* |
| *delve*, *dive into* | *examine*, *investigate*, *inspect*, *look at* |
| *foster*, *bolster* | *support*, *build*, *encourage*, *improve* |
| *leverage*, *utilize* | *use*, *apply*, *rely on* |
| *profound* | *deep*, *major*, *significant* |
| *showcase*, *underscore* | *show*, *highlight*, *demonstrate*, *prove* |
| *tapestry*, *testament* | *system*, *network*, *evidence*, *record* |
| *nuanced* | *detailed*, *subtle*, *specific* |
| *plethora*, *myriad* | *many*, *numerous*, *multiple* |
| *beacon*, *cornerstone*, *linchpin* | *foundation*, *basis*, *core element* |
| *seamless*, *bespoke* | *smooth*, *custom*, *tailored* |
| *interplay* | *interaction*, *relationship*, *connection* |

### 5. Cut inline-header restatements
Avoid bold label prefixes that merely repeat what the sentence states:
- ❌ `**Overview:** This overview summarizes the course policies.`
- ✅ `The course policies cover attendance, late submissions, and exams.`
- ❌ `**Performance:** The performance of the system scales linearly.`
- ✅ `System throughput scales linearly with added worker nodes.`

### 6. Cut conversational filler and sycophancy
Eliminate preamble, polite throat-clearing, cheerleading, and closing sign-offs:
- ❌ *"Sure! I would be thrilled to help you with that!"*
- ❌ *"Great question! Let us dive into the concepts..."*
- ❌ *"I hope this helps! Please let me know if you need anything else!"*
- ✅ State direct facts, numbers, code examples, and concrete mechanics immediately.

### 7. Natural rhythm, active voice, and concrete mechanics
- Mix short and long sentences. Avoid repetitive syntactic cadence (e.g. subject-verb-object followed by a participial phrase).
- Use active voice: clearly state who or what performed the action.
- Anchor claims in measurable numbers, exact system call names, register identifiers, or formal mathematical definitions rather than vague generalizations.

---

## Execution workflow

When asked to unslop a note or drafted text:
1. Scan for decorative emojis and strip them.
2. Replace all em dashes with commas or split sentences.
3. Convert all heading lines to standard sentence case.
4. Replace words from the banned vocabulary table with plain alternatives.
5. Remove redundant bold labels and conversational filler.
6. Verify technical precision and atomic linking with `[[WikiLinks]]`.
