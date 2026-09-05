---
title: "{{course_code}} - {{course_name}}"
type: course_moc
tags: [course, moc, {{semester}}]
course_code: "{{course_code}}"
semester: "{{semester}}"
professor: "{{professor}}"
schedule: "{{schedule}}"
office_hours: "{{office_hours}}"
syllabus_link: "{{syllabus_url}}"
---

# 🎓 {{course_code}}: {{course_name}} ({{semester}})

> [!INFO] Course Overview
> **Professor**: {{professor}} | **Class Time**: {{schedule}}
> **Grade Breakdown**: Exams (40%), Assignments (35%), Quizzes (15%), Participation (10%)

---

## 🎯 Key Milestones & Exam Dates
- [ ] **Midterm Exam**: `YYYY-MM-DD` 
- [ ] **Final Project Due**: `YYYY-MM-DD` 
- [ ] **Final Exam**: `YYYY-MM-DD` 

---

## 📚 Lecture Index (Dynamic Dataview)
```dataview
TABLE date as "Date", status as "Review Status", tags as "Topics"
FROM "02-Courses/{{course_code}}/Lectures"
SORT date ASC
```

---

## 📝 Assignments & Problem Sets (Dynamic Dataview)
```dataview
TABLE due_date as "Due Date", status as "Status", priority as "Priority"
FROM "02-Courses/{{course_code}}/Assignments" OR "02-Courses/{{course_code}}/Deliverables"
SORT due_date ASC
```

---

## 🧪 Practice Quizzes & Exam Prep
```dataview
TABLE mastery_score as "Mastery", last_reviewed as "Last Reviewed"
FROM "02-Courses/{{course_code}}/Exams"
SORT last_reviewed DESC
```

---

## 🧠 Mastered Concept Graph
- [[Core-Concept-1]]
- [[Core-Concept-2]]
- [[Core-Concept-3]]
