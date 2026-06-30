# Placement Portal Application V2

A campus recruitment management system built with Flask (API) + Vue 3 (SPA) + Bootstrap + SQLite.

## Stack
- Backend: Flask, Flask-SQLAlchemy, Flask-JWT-Extended, SQLite
- Frontend: Vue 3 (Vite), Vue Router, Axios, Bootstrap

## Roles
- **Admin** — pre-seeded on first run (`admin@ppa.com` / `admin123`). Approves companies and placement drives, manages/blacklists users, views stats.
- **Company** — self-registers, waits for admin approval before logging in, posts drives, manages applicants.
- **Student** — self-registers and logs in immediately, browses approved drives, applies, tracks status and placement history.

## Setup

### Backend
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
Runs on `http://localhost:5000`. The SQLite DB and admin user are created automatically on first run.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on `http://localhost:5173`.

## Core flow implemented
1. Student/Company registration, role-based JWT login (admin pre-seeded, companies gated on admin approval).
2. Admin dashboard: stats, company/drive approval, student/company search, blacklist (deactivate) and removal.
3. Company dashboard: profile, post drives (pending admin approval), manage applicants, update application status, close postings.
4. Student dashboard: profile, browse/search approved drives, apply (with eligibility + duplicate checks), track application status, view placement history.

## Not yet implemented (planned for later milestones)
- Celery + Redis background jobs (interview reminders, monthly reports, async CSV export)
- Redis API caching
- Charts/ATS resume screener (optional enhancement)

## Issues encountered
- None yet — log issues here as they come up during testing.
