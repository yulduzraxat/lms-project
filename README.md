# EDULIX — Learning Management System

A full-featured Learning Management System (LMS) built with Django, where teachers can create courses and quizzes, and students can enroll, track progress, and take timed quizzes.

## Features

- **Role-based accounts** — a custom User model (extending Django's `AbstractUser`) with a `role` field distinguishes students from teachers, enforced through custom decorators on protected views
- **Course management** — create courses with categories, cover images, and lessons
- **Enrollment & progress tracking** — students enroll in courses and mark lessons as complete
- **Quizzes** — teachers create quizzes with multiple-choice questions and an optional time limit; students take quizzes with a live countdown timer
- **Search, filter & sort** — search courses by keyword, filter by category, and sort by newest, popularity, or lesson count
- **Personal profile page** — each user sees their own courses (taught or enrolled) and progress in one place
- **Teacher & student dashboards** — teachers see enrolled students and their progress; students see their own course progress

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, vanilla JavaScript

## Project Structure

The project is split into three Django apps, each with a single responsibility:

- `accounts` — custom User model, authentication, and role-based permissions
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

Create a `.env` file in the project root with:

Then open `http://127.0.0.1:8000/` in your browser.

## Security Notes

- Choice-question integrity is validated on quiz submission, so a submitted answer must belong to the question it was submitted for — this prevents answer tampering
- Enrollment is verified before allowing quiz access or lesson completion
- `SECRET_KEY` and `DEBUG` are loaded from environment variables via `python-decouple`, keeping sensitive config out of version control
