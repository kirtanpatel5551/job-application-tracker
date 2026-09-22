# Job Application Tracker

A portfolio-ready full-stack project for tracking job applications, statuses, companies, locations, and notes.

## Stack
- Backend: Python, FastAPI, SQLAlchemy, JWT
- Database: PostgreSQL (SQLite fallback for quick local run)
- Frontend: React + Vite
- Testing: PyTest
- DevOps: Docker Compose

## Features
- User registration and login
- JWT authentication
- Create, read, update, and delete job applications
- Filter applications by status
- Dashboard summary counts
- React frontend
- PostgreSQL-ready persistence
- Docker Compose setup
- Backend tests

## Quick start with Docker
1. Copy `.env.example` to `.env`.
2. Run:
   `docker compose up --build`
3. Frontend: `http://localhost:5173`
4. API docs: `http://localhost:8000/docs`

## Run backend without Docker
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

By default, the backend uses SQLite if `DATABASE_URL` is not set.

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

## Run tests
```bash
cd backend
pytest
```

## Suggested GitHub description
Full-stack job application tracker built with FastAPI, React, PostgreSQL, JWT authentication, Docker, and PyTest.

> Portfolio note: Review and understand the code before discussing it in interviews. Customize the UI, README, and features to make the project your own.
