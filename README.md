# SOA Exam Prep Platform

A comprehensive, AI-powered platform for preparing for Society of Actuaries (SOA) examinations through adaptive learning and intelligent question sequencing.

## Overview

This platform delivers personalized exam preparation for all SOA exams (P, FM, FAM, ALTAM, ASTAM, SRM, PA) using advanced adaptive testing algorithms. The system intelligently adjusts question difficulty based on learner performance, tracks skill mastery at a granular level, and provides data-driven readiness assessments.

### Key Features

- **Adaptive Testing Engine**: Uses Item Response Theory (IRT) 3-parameter logistic model combined with Bayesian Knowledge Tracing for optimal question selection
- **Comprehensive Content**: Original example questions, video lessons, and detailed explanations for all SOA exams
- **Real-Time Analytics**: Track progress across topics, identify weak areas, and receive personalized study recommendations
- **Smart Study Plans**: Automatically generated, personalized study schedules based on your exam date and available time
- **Expert Explanations**: Step-by-step solutions, common misconceptions, and conceptual frameworks
- **Video Lessons**: Professional video content covering core exam topics with timestamps and transcripts
- **Readiness Assessment**: Data-driven prediction of exam pass likelihood before test day
- **Consistent Performance Tracking**: Detects and flags unusual performance patterns to ensure valid assessments

---

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Caching**: Redis for session management and real-time analytics
- **Authentication**: JWT-based token authentication with refresh token rotation
- **APIs**: RESTful design with OpenAPI/Swagger documentation

### Frontend
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS with shadcn/ui component library
- **State Management**: React Context API + TanStack Query
- **Type Safety**: TypeScript
- **Testing**: Jest and React Testing Library

### Infrastructure
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose for local dev, ECS Fargate for production
- **Cloud**: AWS (RDS, ElastiCache, ECS, ALB, CloudFront)
- **Alternative**: Vercel (frontend) + Railway (backend)
- **CI/CD**: GitHub Actions
- **Monitoring**: CloudWatch, Sentry, optional Prometheus+Grafana

---

## Project Structure

```
soa-prep-platform/
├── backend/                    # FastAPI backend application
│   ├── alembic/               # Database migrations
│   ├── app/
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── routers/           # API route handlers
│   │   ├── services/          # Business logic (IRT, BKT, adaptive logic)
│   │   ├── database.py        # Database connection and session management
│   │   └── config.py          # Configuration management
│   ├── main.py                # Application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Multi-stage Docker build
│   └── alembic.ini            # Alembic configuration
│
├── frontend/                   # Next.js frontend application
│   ├── app/
│   │   ├── (auth)/            # Authentication routes
│   │   ├── (dashboard)/       # Dashboard routes
│   │   ├── (exam)/            # Exam routes
│   │   ├── api/               # Route handlers
│   │   └── layout.tsx         # Root layout
│   ├── components/            # React components
│   │   ├── exam/              # Exam-related components
│   │   ├── progress/          # Analytics components
│   │   └── shared/            # Reusable components
│   ├── lib/                   # Utilities and helpers
│   ├── styles/                # Global styles
│   ├── package.json           # Node dependencies
│   ├── Dockerfile             # Multi-stage Docker build
│   ├── next.config.js         # Next.js configuration
│   └── tsconfig.json          # TypeScript configuration
│
├── docs/                       # Documentation
│   ├── EXAMPLE_QUESTIONS.md   # Example questions for all exams
│   ├── VIDEO_LESSON_SCRIPTS.md # Full video lesson scripts
│   ├── ADAPTIVE_ALGORITHM.md  # Technical documentation of adaptive system
│   ├── API_DOCUMENTATION.md   # Complete API reference
│   ├── DEPLOYMENT.md          # Deployment guides (local, AWS, Vercel/Railway)
│   └── README.md              # This file
│
├── docker-compose.yml          # Local development composition
├── .github/
│   └── workflows/              # CI/CD pipelines
├── .env.example                # Environment variables template
└── .gitignore                  # Git ignore rules
```

---

## Quick Start

### Prerequisites

- Docker and Docker Compose (v20.10+)
- Git

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/soa-prep/platform.git
   cd soa-prep-platform
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env.development
   ```

3. **Start all services:**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database:**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the application:**
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8001
   - API Docs: http://localhost:8001/docs

### Verify Installation

```bash
# Check all services are healthy
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## Features in Detail

### Adaptive Testing Engine

The platform uses a sophisticated three-component algorithm:

1. **Item Response Theory (3PL Model)**: Calibrates question difficulty and learner ability on a consistent scale
2. **Bayesian Knowledge Tracing**: Tracks mastery of specific skills over time with learning rate modeling
3. **Maximum Fisher Information Selection**: Selects next question to maximize information gain about learner ability

See [`docs/ADAPTIVE_ALGORITHM.md`](docs/ADAPTIVE_ALGORITHM.md) for complete technical details including mathematical formulas and pseudocode.

### Example Questions

The platform includes 2+ carefully crafted original questions per exam with:
- Complete question text
- 5 multiple-choice answers
- Step-by-step solutions
- Difficulty ratings
- Topic tags

See [`docs/EXAMPLE_QUESTIONS.md`](docs/EXAMPLE_QUESTIONS.md) for all example questions.

### Video Lessons

Professional video content with:
- Learning objectives
- Intuitive explanations with analogies
- Worked examples
- Common mistakes section
- Visual cue descriptions for instructors

See [`docs/VIDEO_LESSON_SCRIPTS.md`](docs/VIDEO_LESSON_SCRIPTS.md) for full scripts.

### Real-Time Analytics

Track:
- Topic mastery scores (0-1 scale)
- Ability estimates ($\theta$ on IRT scale)
- Readiness scores with confidence intervals
- Weak areas with targeted improvement recommendations
- Consistency metrics to detect anomalous performance

### Study Plans

Automatically generated schedules including:
- Phase-based learning structure
- Daily study commitments in minutes
- Question targets per phase
- Milestone assessments
- Feasibility analysis based on exam date

---

## API Documentation

Complete API documentation available at:

- **OpenAPI/Swagger**: http://localhost:8001/docs (when running locally)
- **ReDoc**: http://localhost:8001/redoc
- **Markdown**: [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md)

### Key Endpoints

**Authentication**
- `POST /auth/register` - Create new account
- `POST /auth/login` - Authenticate user
- `POST /auth/refresh` - Refresh access token

**Adaptive Testing**
- `GET /questions/next` - Get next question
- `POST /questions/submit` - Submit answer
- `GET /adaptive/state` - Get session state
- `POST /adaptive/sessions` - Start new session

**Analytics**
- `GET /analytics/progress` - Overall progress
- `GET /analytics/readiness/{exam_id}` - Readiness assessment
- `GET /analytics/weaknesses` - Weak areas analysis

**Study Planning**
- `GET /study-plan/{exam_id}` - Get personalized study plan
- `PUT /study-plan/{plan_id}` - Update study plan

See [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md) for complete endpoint reference.

---

## Deployment

### Local Development

```bash
docker-compose up -d
```

See [`docs/DEPLOYMENT.md#local-development-setup`](docs/DEPLOYMENT.md#local-development-setup) for detailed setup.

### Production Deployment

Two recommended options:

#### Option 1: AWS (ECS + RDS + ElastiCache)

```bash
# Build and push images to ECR
docker build -t soa-prep-backend:latest ./backend
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag soa-prep-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/soa-prep-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/soa-prep-backend:latest

# Create RDS, ElastiCache, ECS services
# See docs/DEPLOYMENT.md#production-deployment-on-aws for complete guide
```

#### Option 2: Vercel + Railway (Simpler)

```bash
# Frontend to Vercel
# - Connect GitHub repo to Vercel
# - Set environment variables
# - Deploy (automatic on push)

# Backend to Railway
railway login
railway link
railway add postgres
railway add redis
railway variables add DATABASE_URL ...
railway up
```

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for complete deployment guides.

---

## Development

### Running Backend Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

### Running Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm run test

# Coverage
docker-compose exec backend pytest --cov=app
```

### Database Migrations

```bash
# Create migration for model changes
docker-compose exec backend alembic revision --autogenerate -m "Add new field"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback one migration
docker-compose exec backend alembic downgrade -1
```

---

## Configuration

### Environment Variables

#### Backend
```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=http://localhost:3001
```

#### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3001
```

See `.env.example` and [`docs/DEPLOYMENT.md#environment-variables`](docs/DEPLOYMENT.md#environment-variables) for complete configuration reference.

---

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines

- Follow PEP 8 for Python code
- Follow Airbnb style for JavaScript/TypeScript
- Add tests for new features
- Update documentation
- Run linters before committing

### Testing

```bash
# Backend
pytest
black --check app
pylint app
mypy app

# Frontend
npm run test
npm run lint
npm run type-check
```

---

## Exams Covered

The platform provides comprehensive preparation for:

- **Exam P**: Probability
- **Exam FM**: Financial Mathematics
- **Exam FAM**: Financial, Accounting, and Management
- **Exam ALTAM**: Advanced Long-Term Actuarial Mathematics
- **Exam ASTAM**: Advanced Short-Term Actuarial Mathematics
- **Exam SRM**: Statistics for Risk Management
- **Exam PA**: Predictive Analytics

---

## Performance & Scale

### Expected Capabilities

- **Concurrent Users**: 10,000+ simultaneous users (with AWS scaling)
- **Questions Served**: 1,000+ questions per second
- **Session Length**: Average 90-120 minutes per adaptive session
- **Question Load Time**: < 200ms p95 latency
- **Database Connections**: Optimized connection pooling (20-40 connections)
- **Cache Hit Rate**: > 85% for common queries

### Benchmarks

On local development setup:
- Question selection algorithm: < 50ms
- IRT ability estimation: < 20ms
- BKT knowledge update: < 10ms

---

## Troubleshooting

### Common Issues

**Postgres connection fails**
```bash
docker-compose logs postgres
# Check credentials in .env
```

**Redis connection fails**
```bash
docker-compose exec redis redis-cli ping
```

**Frontend won't load**
```bash
docker-compose logs frontend
# Check NEXT_PUBLIC_API_URL points to correct backend
```

See [`docs/DEPLOYMENT.md#troubleshooting`](docs/DEPLOYMENT.md#troubleshooting) for detailed troubleshooting.

---

## Documentation

- **API Reference**: [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md)
- **Adaptive Algorithm**: [`docs/ADAPTIVE_ALGORITHM.md`](docs/ADAPTIVE_ALGORITHM.md)
- **Deployment Guides**: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)
- **Example Questions**: [`docs/EXAMPLE_QUESTIONS.md`](docs/EXAMPLE_QUESTIONS.md)
- **Video Lesson Scripts**: [`docs/VIDEO_LESSON_SCRIPTS.md`](docs/VIDEO_LESSON_SCRIPTS.md)

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Support

For issues, questions, or feedback:

- **GitHub Issues**: https://github.com/soa-prep/platform/issues
- **Email**: support@soa-prep.com
- **Documentation**: https://docs.soa-prep.com

---

## Roadmap

### Q2 2026
- [ ] Mobile app (iOS/Android) via React Native
- [ ] Proctored practice exams with timer
- [ ] AI-powered tutoring chat
- [ ] Peer discussion forums

### Q3 2026
- [ ] Advanced spaced repetition scheduling
- [ ] Custom exam creation for instructors
- [ ] Integration with university systems (Canvas, Blackboard)
- [ ] Multi-language support

### Q4 2026
- [ ] Predictive pass/fail modeling with neural networks
- [ ] VR exam simulation environments
- [ ] Integration with professional development tracking
- [ ] Corporate team management and analytics

---

## Acknowledgments

- Developed with guidance from actuarial professionals and experienced SOA exam takers
- Built with open-source technologies: FastAPI, Next.js, PostgreSQL, Redis
- Inspired by educational research on adaptive learning and item response theory

---

**Last Updated**: April 15, 2026
**Version**: 1.0.0
