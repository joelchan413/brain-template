---
title: "Academic Hub"
type: moc
tags: [hub, moc, dashboard, academic]
created: 2026-09-01
---

# Academic hub

Welcome to your central Personal Knowledge Management (PKM) command center.

> [!INFO] Workspace overview
> This vault organizes coursework, evergreen concepts, lecture archives, and exam preparation using atomic linking and spaced repetition.

---

## Active courses

```dataview
TABLE schedule as "Schedule", instructors as "Instructor", institution as "Institution"
FROM "02-Courses"
WHERE type = "course_moc"
SORT file.name ASC
```

---

## Upcoming assignments and deliverables

```dataview
TABLE course as "Course", due_date as "Due Date", priority as "Priority", status as "Status"
FROM "02-Courses"
WHERE type = "assignment" AND status != "completed"
SORT due_date ASC
```

---

## Exam preparation radar

```dataview
TABLE course as "Course", exam_date as "Exam Date", target_grade as "Target", status as "Status"
FROM "02-Courses"
WHERE type = "exam_prep"
SORT exam_date ASC
```

---

## Recent daily notes

```dataview
TABLE date as "Date", courses_today as "Classes"
FROM "01-Daily"
WHERE type = "daily"
SORT file.name DESC
LIMIT 7
```

---

## Concept graph index

```dataview
TABLE file.folder as "Folder", file.mtime as "Last Updated"
FROM "03-Concepts"
WHERE type = "concept"
SORT file.name ASC
```
