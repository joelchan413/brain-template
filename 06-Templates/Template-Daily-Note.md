---
title: "{{date}}"
type: daily
date: {{date}}
tags: [daily, study-log, iowa-state]
courses_today: []
---

# {{date}}, Daily Plan & Study Log

> [!INFO] Day Overview
> **Focus for Today**: 

---

## Top Priorities
- [ ] 
- [ ] 
- [ ] 

---

## ️ Google Calendar Schedule & Locations
| Time | Course / Event | Location | Note Link | Status |
| :--- | :--- | :--- | :--- | :--- |
| {{start_time}} - {{end_time}} | {{course_code}} | {{location}} | [[{{lecture_note_link}}]] | ⏳ Scheduled |

---

## ️ Time-Blocked Study Sessions
| Window | Course / Topic | Objectives & Tasks | Completed? |
| :--- | :--- | :--- | :-: |
| 10:00 - 11:30 | [[COMS3110-Overview]] | Asymptotic Analysis practice problems | [ ] |
| 16:30 - 17:30 | [[CPRE3080-Overview]] | Review POSIX `fork()` syscalls & slides | [ ] |

---

## Quick Capture & In-Class Notes
- 

---

## Breakthroughs & Concepts Mastered
> [!TIP] Key Learnings
> - 

---

## Daily Note Activity (Dynamic Dataview)
```dataview
TABLE file.folder as "Folder", file.mtime as "Modified Time"
FROM ""
WHERE file.mday = date("{{date}}") AND file.name != "{{date}}"
SORT file.mtime DESC
```

---

## Daily Reflection & Shutdown
- **What went well:** 
- **What got delayed:** 
- **Tomorrow's main priority:** 
