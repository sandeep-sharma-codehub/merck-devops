# Merck DevOps API

Python REST API with AWS deployment pipeline. Built with FastAPI, containerized with Docker, deployed to AWS ECS via GitHub Actions CI/CD.

## Local Development

```bash
# Install dependencies
pip install ".[dev]"

# Run the API
uvicorn app.main:app --reload

# Run tests
pytest

# Lint and format check
ruff check app/ tests/
ruff format --check app/ tests/
```

## Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Get a Token

```bash
curl -X POST http://localhost:8000/api/v1/token \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo"}'
```

### Access Protected Data

```bash
curl http://localhost:8000/api/v1/data \
  -H "Authorization: Bearer <token>"
```

## AWS Deployment

### Prerequisites

- AWS CLI configured
- AWS CDK installed (`npm install -g aws-cdk`)
- GitHub repository secrets configured:
  - `AWS_ROLE_ARN` — IAM role ARN for OIDC
- GitHub repository variables:
  - `ECR_REGISTRY` — ECR registry URL
  - `ECR_REPOSITORY` — ECR repository name

### Infrastructure

```bash
cd infra
pip install -r requirements.txt
cdk synth    # Preview CloudFormation template
cdk deploy   # Deploy infrastructure
```

### CI/CD

The GitHub Actions pipeline runs automatically on push to `main`:

1. **Test** — lint, format check, pytest
2. **Build** — Docker build and push to ECR
3. **Deploy** — ECS force new deployment

## Architecture

- **VPC** with public and private subnets across 2 AZs
- **ECR** repository for Docker images
- **ECS on EC2** (t3.small) with auto-scaling group
- **ALB** internet-facing load balancer with health checks
- **Secrets Manager** for JWT secret management
