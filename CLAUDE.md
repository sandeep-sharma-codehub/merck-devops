# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a cloud-based application deployment pipeline project. The goal is to build and deploy a Python REST API to AWS using CI/CD with GitHub Actions.

## Requirements (from requirement.txt)

- **Python REST API** with at least two endpoints:
  - Health check endpoint
  - Data retrieval endpoint (dummy data) requiring authentication
- **Containerized** with Docker
- **Infrastructure as Code** using AWS CDK or CloudFormation
- **CI/CD pipeline** using GitHub Actions — must be fully operational
- Tests where relevant
- Enterprise-grade code and application

## Intended Tech Stack

- Python (REST API — e.g., FastAPI or Flask)
- Docker for containerization
- AWS services for hosting (e.g., ECS/Fargate, ECR, ALB)
- AWS CDK or CloudFormation for infrastructure
- GitHub Actions for CI/CD

## Build & Run Commands

```bash
# Install all dependencies (including dev)
pip install ".[dev]"

# Run API locally
uvicorn app.main:app --reload

# Run tests
pytest

# Lint and format
ruff check app/ tests/
ruff format --check app/ tests/

# Docker
docker-compose up --build

# CDK (from infra/ directory)
cd infra && pip install -r requirements.txt && cdk synth
```
