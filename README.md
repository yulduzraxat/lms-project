# EDULIX — Learning Management System

A full-featured Learning Management System (LMS) built with Django, where teachers can create courses and quizzes, and students can enroll, track progress, and take timed quizzes.

## Features

- **Role-based accounts** — students and teachers with separate permissions, powered by a signal-driven profile system
- **Course management** — create courses with categories, cover images, and lessons
- **Enrollment & progress tracking** — students enroll in courses and mark lessons as complete
- **Quizzes** — teachers create quizzes with multiple-choice questions and an optional time limit; students take quizzes with a live countdown timer
- **Search, filter & sort** — search courses by keyword, filter by category, and sort by newest, popularity, or lesson count
- **Teacher & student dashboards** — teachers see enrolled students and their progress; students see their own course progress

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, vanilla JavaScript

## Project Structure

The project is split into three Django apps, each with a single responsibility:

- `accounts` — user authentication and roles (student/teacher)
- `courses` — courses, lessons, enrollments, and progress
- `quizzes` — quizzes, questions, choices, and submissions

## Setup

```bash
git clone https://github.com/yulduzraxat/lms-project.git
cd lms-project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

## Security Notes

- Choice-question integrity is validated on quiz submission to prevent answer tampering
- Enrollment is verified before allowing quiz access or lesson completion
- User profiles are created automatically via Django signals, so accounts created through any method always have a valid profile
