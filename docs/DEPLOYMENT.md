# Deployment Guide

Complete guide for deploying the SOA Exam Prep Platform across different environments.

---

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Environment Variables](#environment-variables)
3. [Database Migrations](#database-migrations)
4. [Production Deployment on AWS](#production-deployment-on-aws)
5. [Alternative: Vercel + Railway](#alternative-vercel--railway)
6. [SSL/TLS Setup](#ssltls-setup)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites

- Docker and Docker Compose (v20.10+)
- Python 3.11+ (for backend development)
- Node.js 20+ (for frontend development)
- Git

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/soa-prep/platform.git
   cd soa-prep-platform
   ```

2. **Create environment files:**
   ```bash
   cp .env.example .env.development
   ```

3. **Start services with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL (port 5432)
   - Redis (port 6379)
   - FastAPI backend (port 8001)
   - Next.js frontend (port 3001)

4. **Initialize database:**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the application:**
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

### Verification

Check all services are healthy:
```bash
docker-compose ps

# Expected output:
# NAME              STATUS
# soa_postgres      Up (healthy)
# soa_redis         Up (healthy)
# soa_backend       Up (healthy)
# soa_frontend      Up (healthy)
```

### Development Workflow

**Running the backend locally (without Docker):**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

**Running the frontend locally (without Docker):**
```bash
cd frontend
npm install
npm run dev
```

**Running tests:**
```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm run test
```

---

## Environment Variables

### Backend Environment Variables

Create `.env.development` and `.env.production` files:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3001,https://soa-prep.com

# Environment
ENVIRONMENT=development  # or production
DEBUG=False
LOG_LEVEL=INFO

# AWS (optional, for S3 video storage)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=soa-prep-videos

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@soa-prep.com

# Analytics
SENTRY_DSN=https://your-sentry-dsn
MIXPANEL_TOKEN=your-mixpanel-token

# Rate Limiting
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW_SECONDS=3600
```

### Frontend Environment Variables

Create `.env.local` and `.env.production`:

```env
# API
NEXT_PUBLIC_API_URL=http://localhost:8001/api/v1  # http://api.soa-prep.com/v1 in production
NEXT_PUBLIC_APP_URL=http://localhost:3001

# Analytics
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-XXXXXXXX
NEXT_PUBLIC_MIXPANEL_TOKEN=your-mixpanel-token

# Auth
NEXT_PUBLIC_AUTH_DOMAIN=soa-prep.auth0.com  # Optional, for Auth0 integration
NEXT_PUBLIC_AUTH_CLIENT_ID=your-client-id

# Feature Flags
NEXT_PUBLIC_ENABLE_BETA_FEATURES=true
NEXT_PUBLIC_ENABLE_ANALYTICS=true

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## Database Migrations

### Setting Up Alembic

Alembic is used for database schema versioning and migrations.

**Initialize Alembic (already done, but for reference):**
```bash
alembic init alembic
```

### Running Migrations

**Apply all pending migrations:**
```bash
alembic upgrade head
```

**Apply specific revision:**
```bash
alembic upgrade 1234567890ab
```

**Rollback one migration:**
```bash
alembic downgrade -1
```

**Rollback to specific revision:**
```bash
alembic downgrade 1234567890ab
```

### Creating New Migrations

**Auto-generate migration for model changes:**
```bash
alembic revision --autogenerate -m "Add new_column to users table"
```

This creates a new migration file in `backend/alembic/versions/`.

**Review the generated migration** and test it locally before deploying.

### Migration Best Practices

1. **Test migrations locally first:**
   ```bash
   docker-compose exec backend alembic upgrade head
   docker-compose exec backend alembic downgrade -1
   docker-compose exec backend alembic upgrade head
   ```

2. **Backward compatibility:** Avoid breaking changes that prevent rollback.

3. **Data migration:** For complex data transformations, create a separate migration script.

4. **Zero-downtime deployments:** Use feature flags and gradual rollouts.

---

## Production Deployment on AWS

### Architecture

```
┌─────────────────────────────────────────┐
│         CloudFront + Route 53           │
│        (CDN + DNS)                      │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   ┌────▼─────┐         ┌────▼──────┐
   │ Vercel/  │         │   ECS     │
   │S3+CF     │         │(Fargate)  │
   │Frontend  │         │ Backend   │
   └──────────┘         └────┬──────┘
                             │
        ┌────────────────────┼────────────────┐
        │                    │                │
   ┌────▼─────┐        ┌────▼──────┐   ┌────▼──────┐
   │    RDS   │        │ElastiCache │   │ S3 Videos │
   │(Postgres)│        │ (Redis)    │   │ & Assets  │
   └──────────┘        └────────────┘   └───────────┘
```

### Prerequisites

- AWS account with appropriate IAM permissions
- AWS CLI configured
- Terraform or CloudFormation knowledge (optional, for infrastructure-as-code)

### Step 1: Prepare Docker Images

**Build and push images to AWS ECR:**

```bash
# Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repositories
aws ecr create-repository --repository-name soa-prep-backend --region us-east-1
aws ecr create-repository --repository-name soa-prep-frontend --region us-east-1

# Build and tag images
docker build -t soa-prep-backend:latest ./backend
docker build -t soa-prep-frontend:latest ./frontend

# Tag for ECR
docker tag soa-prep-backend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/soa-prep-backend:latest
docker tag soa-prep-frontend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/soa-prep-frontend:latest

# Push to ECR
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/soa-prep-backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/soa-prep-frontend:latest
```

### Step 2: Set Up RDS Database

**Create RDS PostgreSQL instance:**

```bash
aws rds create-db-instance \
  --db-instance-identifier soa-prep-prod \
  --db-instance-class db.t3.small \
  --engine postgres \
  --engine-version 16.2 \
  --master-username soaadmin \
  --master-user-password <secure-password> \
  --allocated-storage 100 \
  --storage-type gp3 \
  --backup-retention-period 30 \
  --publicly-accessible false \
  --vpc-security-group-ids sg-xxxxxxxx \
  --db-subnet-group-name soa-db-subnet
```

**Wait for the database to be available, then run migrations:**
```bash
export DATABASE_URL="postgresql://soaadmin:password@soa-prep-prod.xxxxx.us-east-1.rds.amazonaws.com:5432/soa_exams"
alembic upgrade head
```

### Step 3: Set Up ElastiCache (Redis)

**Create ElastiCache cluster:**

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id soa-prep-redis \
  --cache-node-type cache.t3.small \
  --engine redis \
  --engine-version 7.0 \
  --num-cache-nodes 1 \
  --security-group-ids sg-xxxxxxxx \
  --cache-subnet-group-name soa-cache-subnet
```

### Step 4: Deploy Backend on ECS

**Create ECS cluster:**

```bash
aws ecs create-cluster --cluster-name soa-prep-prod
```

**Create task definition** (`backend-task-definition.json`):

```json
{
  "family": "soa-prep-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "soa-prep-backend",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/soa-prep-backend:latest",
      "portMappings": [
        {
          "containerPort": 8001,
          "hostPort": 8001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "ENVIRONMENT", "value": "production"},
        {"name": "LOG_LEVEL", "value": "INFO"},
        {"name": "DEBUG", "value": "False"}
      ],
      "secrets": [
        {"name": "DATABASE_URL", "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:soa/db-url"},
        {"name": "REDIS_URL", "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:soa/redis-url"},
        {"name": "SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:soa/secret-key"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/soa-prep-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "executionRoleArn": "arn:aws:iam::123456789:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789:role/ecsTaskRole"
}
```

**Register task definition and create service:**

```bash
aws ecs register-task-definition --cli-input-json file://backend-task-definition.json

aws ecs create-service \
  --cluster soa-prep-prod \
  --service-name soa-prep-backend \
  --task-definition soa-prep-backend:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx,subnet-yyyyy],securityGroups=[sg-zzzz],assignPublicIp=DISABLED}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789:targetgroup/soa-backend/xxxxx,containerName=soa-prep-backend,containerPort=8000 \
  --auto-scaling-group-name soa-prep-backend-asg
```

### Step 5: Deploy Frontend on S3 + CloudFront

**Build and deploy frontend:**

```bash
cd frontend
npm run build

# Upload to S3
aws s3 sync .next/ s3://soa-prep-frontend/
aws s3 sync public/ s3://soa-prep-frontend/public/

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id XXXXXXXXX --paths "/*"
```

Alternatively, use Vercel (see next section).

### Step 6: Configure Load Balancer and DNS

**Create Application Load Balancer:**

```bash
aws elbv2 create-load-balancer \
  --name soa-prep-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-zzzz \
  --scheme internet-facing
```

**Create target group and configure routing to ECS tasks.**

**Update Route 53 DNS:**

```bash
aws route53 change-resource-record-sets \
  --hosted-zone-id ZXXXXXXXXX \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "api.soa-prep.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "soa-prep-alb-1234567890.us-east-1.elb.amazonaws.com",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'
```

### Step 7: Monitor and Auto-Scale

**Create CloudWatch alarms:**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name soa-prep-cpu-high \
  --alarm-description "Alert when ECS CPU > 70%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 70 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789:alerts
```

**Configure Auto Scaling:**

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/soa-prep-prod/soa-prep-backend \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

aws application-autoscaling put-scaling-policy \
  --policy-name cpu-scaling \
  --service-namespace ecs \
  --resource-id service/soa-prep-prod/soa-prep-backend \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration TargetValue=70.0,PredefinedMetricSpecification={PredefinedMetricType=ECSServiceAverageCPUUtilization}
```

---

## Alternative: Vercel + Railway

This is a simpler deployment option for smaller teams.

### Frontend Deployment (Vercel)

**Step 1: Connect repository**
- Push code to GitHub
- Visit https://vercel.com and sign up
- Import your GitHub repository

**Step 2: Configure environment variables**
```
NEXT_PUBLIC_API_URL=https://api.soa-prep.com/v1
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-XXXXXXXX
```

**Step 3: Deploy**
- Vercel automatically deploys on every push to main branch
- Automatic preview deployments on pull requests

### Backend Deployment (Railway)

**Step 1: Create Railway project**
- Visit https://railway.app and sign up
- Create a new project

**Step 2: Add services**

```bash
# Link local repository to Railway
railway link

# Create PostgreSQL service
railway add postgres

# Create Redis service
railway add redis
```

**Step 3: Configure environment variables**

```bash
railway variables add DATABASE_URL $DATABASE_URL
railway variables add REDIS_URL $REDIS_URL
railway variables add SECRET_KEY $SECRET_KEY
railway variables add ENVIRONMENT production
```

**Step 4: Deploy**

```bash
# Deploy backend
railway up

# View logs
railway logs

# Shell access
railway shell
```

**Step 5: Configure domains**

In Railway dashboard:
- Add custom domain: api.soa-prep.com
- Configure DNS with your registrar

---

## SSL/TLS Setup

### Using AWS Certificate Manager

```bash
# Request certificate
aws acm request-certificate \
  --domain-name soa-prep.com \
  --subject-alternative-names api.soa-prep.com www.soa-prep.com \
  --validation-method DNS \
  --region us-east-1

# View certificate details
aws acm describe-certificate --certificate-arn arn:aws:acm:us-east-1:123456789:certificate/xxxxx
```

### Using Let's Encrypt (for Railway or self-hosted)

```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Generate certificate
certbot certonly --standalone -d soa-prep.com -d api.soa-prep.com

# Auto-renewal
certbot renew --dry-run
```

### Configure HTTPS in Load Balancer

```bash
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789:loadbalancer/app/soa-prep-alb/50dc6c495c0c9cd2 \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=arn:aws:acm:us-east-1:123456789:certificate/xxxxx \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789:targetgroup/soa-backend/xxxxx
```

### HTTP to HTTPS Redirect

```bash
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789:loadbalancer/app/soa-prep-alb/xxxxx \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=redirect,RedirectConfig="{Protocol=HTTPS,Port=443,StatusCode=HTTP_301}"
```

---

## Monitoring and Logging

### CloudWatch Logs

**Backend logging configuration** (in `.env`):
```env
LOG_LEVEL=INFO
SENTRY_DSN=https://your-sentry-dsn
```

**View logs:**
```bash
aws logs tail /ecs/soa-prep-backend --follow

# Filter logs
aws logs filter-log-events \
  --log-group-name /ecs/soa-prep-backend \
  --filter-pattern "ERROR"
```

### Prometheus + Grafana (Optional)

**Add Prometheus metrics to backend** (`backend/main.py`):

```python
from prometheus_client import Counter, Histogram, CollectRegistry
from prometheus_fastapi_instrumentator import Instrumentator

registry = CollectRegistry()
Instrumentator().instrument(app).expose(app)
```

**Deploy Prometheus and Grafana:**

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'soa-backend'
    static_configs:
      - targets: ['localhost:8001']
```

### Sentry for Error Tracking

**Configure in backend** (`backend/main.py`):

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    environment="production"
)
```

### DataDog (Optional)

```bash
# Install datadog agent
apt-get install datadog-agent

# Configure
echo "api_key: <API_KEY>" | sudo tee /etc/datadog-agent/datadog.yaml

# Start
sudo systemctl restart datadog-agent
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Test connection
docker-compose exec backend psql $DATABASE_URL

# Check migrations
docker-compose exec backend alembic current
docker-compose exec backend alembic history

# Rollback if needed
docker-compose exec backend alembic downgrade -1
```

### Redis Connection Issues

```bash
# Test connection
docker-compose exec redis redis-cli ping

# Check memory usage
docker-compose exec redis redis-cli INFO memory

# Clear cache (if needed)
docker-compose exec redis redis-cli FLUSHALL
```

### Frontend Build Issues

```bash
# Clear cache and rebuild
docker-compose exec frontend rm -rf .next node_modules
docker-compose exec frontend npm install
docker-compose exec frontend npm run build
```

### Performance Issues

```bash
# Check ECS task logs
aws ecs describe-tasks \
  --cluster soa-prep-prod \
  --tasks <task-arn>

# Monitor RDS performance
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=soa-prep-prod \
  --start-time 2026-04-15T00:00:00Z \
  --end-time 2026-04-15T12:00:00Z \
  --period 300 \
  --statistics Average
```

### SSL Certificate Issues

```bash
# Check certificate validity
aws acm describe-certificate --certificate-arn <arn>

# Renew if needed
certbot renew --force-renewal
```

---

This deployment guide covers all major deployment scenarios. Adjust based on your specific requirements and infrastructure preferences.
