# EDULIX — Learning Management System

A full-featured Learning Management System (LMS) built with Django, where teachers can create courses and quizzes, and students can browse, purchase, enroll, track progress, and take timed quizzes.

## Features

- **Role-based accounts** — a custom User model (extending Django's `AbstractUser`) with a `role` field distinguishes students from teachers. New sign-ups are always created as students; teacher accounts are assigned through the admin panel to prevent privilege escalation
- **Course management** — create courses with categories, cover images, pricing, and lessons
- **Cart & checkout** — students can add paid courses to a cart, check out with a simulated card payment, and confirm the purchase with a one-time verification code
- **Enrollment & progress tracking** — students enroll in courses (free or after checkout) and mark lessons as complete
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
- `courses` — courses, lessons, enrollments, progress, cart, and checkout
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

## Notes on the Payment Flow

The checkout flow (card entry → verification code → success) is a **simulated** payment process built for demonstration purposes — no real payment provider is connected. The verification code is printed to the server console instead of being sent by SMS, standing in for a real SMS gateway (e.g. Eskiz, Twilio) that would be used in production.

## Security Notes

- Only administrators can promote a user to `teacher` via the admin panel — self-registration always creates a `student` account
- Choice-question integrity is validated on quiz submission, so a submitted answer must belong to the question it was submitted for — this prevents answer tampering
- Enrollment is verified before allowing quiz access or lesson completion
- `SECRET_KEY` and `DEBUG` are loaded from environment variables via `python-decouple`, keeping sensitive config out of version control
