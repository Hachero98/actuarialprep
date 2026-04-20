# ActuarialPrep Platform — System Architecture

## Overview

ActuarialPrep is a full-stack actuarial exam preparation platform featuring adaptive practice exams, a question generation engine, analytics, video lessons, and personalized study plans. It covers SOA exams P, FM, FAM, ALTAM, ASTAM, SRM, and PA.

---

## Tech Stack

| Layer        | Technology                        |
|-------------|-----------------------------------|
| Frontend    | Next.js 14 (App Router), TypeScript, Tailwind CSS |
| Backend API | Python 3.11+, FastAPI             |
| Database    | PostgreSQL 16                     |
| ORM         | SQLAlchemy 2.0 + Alembic          |
| Auth        | JWT (access + refresh tokens)     |
| Cache       | Redis (session/adaptive state)    |
| Task Queue  | Celery + Redis (async jobs)       |
| Deployment  | Docker Compose (dev), AWS/Vercel (prod) |

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENTS                              │
│   Next.js App (SSR + CSR)  │  Mobile (future)           │
└──────────────┬──────────────────────────────────────────┘
               │ HTTPS
               ▼
┌─────────────────────────────────────────────────────────┐
│                   API GATEWAY / NGINX                    │
└──────────────┬──────────────────────────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌─────────────┐  ┌─────────────────┐
│  Next.js    │  │  FastAPI         │
│  Server     │  │  Backend         │
│  (SSR/API   │  │                  │
│   proxy)    │  │  ┌────────────┐  │
└─────────────┘  │  │ Auth       │  │
                 │  │ Service    │  │
                 │  ├────────────┤  │
                 │  │ Question   │  │
                 │  │ Generator  │  │
                 │  ├────────────┤  │
                 │  │ Adaptive   │  │
                 │  │ Engine     │  │
                 │  ├────────────┤  │
                 │  │ Analytics  │  │
                 │  │ Service    │  │
                 │  ├────────────┤  │
                 │  │ Study Plan │  │
                 │  │ Service    │  │
                 │  └────────────┘  │
                 └────────┬────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌──────────┐ ┌────────┐ ┌─────────┐
        │PostgreSQL│ │ Redis  │ │ Celery  │
        │          │ │ Cache  │ │ Workers │
        └──────────┘ └────────┘ └─────────┘
```

---

## Service Architecture

### 1. Authentication Service
- JWT-based auth with access (15 min) and refresh (7 day) tokens
- Password hashing with bcrypt
- Role-based access: student, admin, content_creator
- Email verification flow

### 2. Question Generation Engine
- Template-based system with parameterized variables
- Each template defines: variable ranges, formula, solution steps, distractor logic
- Generates unlimited unique variants per template
- Difficulty calibrated 1-10 via IRT (Item Response Theory) parameters

### 3. Adaptive Learning Engine
- Bayesian Knowledge Tracing (BKT) per topic
- Item Response Theory (IRT) 3-parameter model for question selection
- Real-time ability estimation using Expected A Posteriori (EAP)
- Exam Readiness Score = weighted composite of topic mastery levels
- Personalized question selection maximizing information gain

### 4. Analytics Service
- Per-topic performance tracking
- Time-series progress visualization
- Weakness detection algorithm
- Comparative percentile rankings
- Predicted pass probability

### 5. Study Plan Service
- Gap analysis based on current mastery vs. target
- Time-allocation optimizer using topic weights from exam syllabus
- Spaced repetition scheduling
- Dynamic re-planning on each session

### 6. Video Lesson Service
- Structured curriculum per exam
- Lesson scripts with examples, analogies, and checkpoints
- Progress tracking per lesson

---

## API Route Map

| Method | Endpoint                      | Description                    |
|--------|-------------------------------|--------------------------------|
| POST   | /api/auth/register            | Create account                 |
| POST   | /api/auth/login               | Get JWT tokens                 |
| POST   | /api/auth/refresh             | Refresh access token           |
| GET    | /api/exams                    | List all exams                 |
| GET    | /api/exams/{id}/topics        | Topics for an exam             |
| POST   | /api/questions/generate       | Generate a question            |
| POST   | /api/questions/submit         | Submit an answer               |
| GET    | /api/adaptive/state           | Get current adaptive state     |
| POST   | /api/adaptive/next            | Get next adaptive question     |
| POST   | /api/sessions/start           | Start practice exam session    |
| POST   | /api/sessions/{id}/end        | End session, get results       |
| GET    | /api/analytics/progress       | User progress data             |
| GET    | /api/analytics/readiness      | Exam readiness score           |
| GET    | /api/study-plan               | Get personalized study plan    |
| GET    | /api/video-lessons            | List video lessons             |
| GET    | /api/video-lessons/{id}       | Get lesson details             |
| GET    | /api/admin/users              | Admin: list users              |
| POST   | /api/admin/templates          | Admin: create question template|
| PUT    | /api/admin/templates/{id}     | Admin: update template         |

---

## Deployment Architecture

### Development
```
docker-compose up
```
Services: postgres, redis, fastapi, nextjs, celery-worker

### Production
- Frontend: Vercel (Next.js)
- Backend: AWS ECS or Railway (FastAPI containers)
- Database: AWS RDS PostgreSQL
- Cache: AWS ElastiCache Redis
- CDN: CloudFront for static assets
- SSL: Let's Encrypt / ACM

---

## Security

- All passwords hashed with bcrypt (12 rounds)
- JWT tokens with RS256 signing
- CORS restricted to frontend origin
- Rate limiting on auth endpoints
- SQL injection prevention via parameterized queries (SQLAlchemy)
- XSS prevention via Next.js built-in escaping
- CSRF tokens on state-changing operations
