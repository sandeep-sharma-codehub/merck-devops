#!/usr/bin/env bash
set -euo pipefail

# Step 2: Push initial Docker image and start ECS Service
# Run this AFTER "cdk deploy" has created the infrastructure.
#
# Usage: ./scripts/initial-deploy.sh [aws-region]

REGION="${1:-us-east-1}"
REPO_NAME="merck-devops-api"
CLUSTER="MerckDevOpsStack-Cluster"
SERVICE="MerckDevOpsStack-Service"

echo "==> Getting ECR repository URI..."
ECR_URI=$(aws ecr describe-repositories \
  --repository-names "$REPO_NAME" \
  --region "$REGION" \
  --query 'repositories[0].repositoryUri' \
  --output text)

ECR_REGISTRY=$(echo "$ECR_URI" | cut -d'/' -f1)

echo "    ECR URI: $ECR_URI"
echo "    Registry: $ECR_REGISTRY"

echo "==> Logging in to ECR..."
aws ecr get-login-password --region "$REGION" | \
  docker login --username AWS --password-stdin "$ECR_REGISTRY"

echo "==> Building Docker image (linux/amd64)..."
docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  -t "$ECR_URI:latest" \
  --push \
  .

echo "==> Scaling ECS service to 1 and deploying..."
aws ecs update-service \
  --cluster "$CLUSTER" \
  --service "$SERVICE" \
  --desired-count 1 \
  --force-new-deployment \
  --region "$REGION" \
  --query 'service.{Status:status,Desired:desiredCount}' \
  --output table

echo "==> Waiting for service to stabilize..."
aws ecs wait services-stable \
  --cluster "$CLUSTER" \
  --services "$SERVICE" \
  --region "$REGION"

echo "==> Done! Service is healthy."

ALB_DNS=$(aws elbv2 describe-load-balancers \
  --query "LoadBalancers[?contains(LoadBalancerName,'Merck')].DNSName" \
  --output text \
  --region "$REGION")

echo ""
echo "API is live at: http://$ALB_DNS"
echo "  Health check: curl http://$ALB_DNS/health"
