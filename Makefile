.PHONY: help install dev test lint format clean docker-build docker-up docker-down docker-logs docker-restart docker-clean

# Colors
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m

help:
	@echo "$(GREEN)CKTT AI Agent Platform - Docker Commands$(NC)"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "$(YELLOW)Development$(NC)"
	@echo "  install        Install dependencies"
	@echo "  dev           Run development server"
	@echo "  test          Run tests"
	@echo "  lint          Run linters"
	@echo "  format        Format code"
	@echo ""
	@echo "$(YELLOW)Docker$(NC)"
	@echo "  docker-build  Build Docker images"
	@echo "  docker-up     Start Docker services"
	@echo "  docker-down   Stop Docker services"
	@echo "  docker-logs   View Docker logs"
	@echo "  docker-restart Restart Docker services"
	@echo "  docker-clean  Clean Docker resources"
	@echo "  docker-push   Push images to registry"
	@echo ""
	@echo "$(YELLOW)Maintenance$(NC)"
	@echo "  clean         Clean build artifacts"

# Development commands
install:
	poetry install

dev:
	poetry run uvicorn apps.agent_api.src.agent_api.main:app --reload

test:
	poetry run pytest

lint:
	poetry run ruff check .

format:
	poetry run ruff format .
	poetry run black .

clean:
	poetry run rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Docker commands
docker-build:
	@echo "$(GREEN)Building Docker images...$(NC)"
	docker-compose build --no-cache

docker-build-nocache:
	@echo "$(GREEN)Building Docker images (no cache)...$(NC)"
	docker-compose build --no-cache

docker-up:
	@echo "$(GREEN)Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo "API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Nginx: http://localhost:80"

docker-down:
	@echo "$(YELLOW)Stopping Docker services...$(NC)"
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-logs-api:
	docker-compose logs -f api

docker-logs-worker:
	docker-compose logs -f worker

docker-restart:
	docker-compose restart

docker-clean:
	@echo "$(YELLOW)Cleaning Docker resources...$(NC)"
	docker-compose down -v
	docker system prune -f

docker-ps:
	docker-compose ps

# Build and push images for publishing
docker-push:
	@echo "$(GREEN)Building and pushing images...$(NC)"
	docker-compose build
	docker-compose push

# Full deployment
deploy: docker-build docker-up
	@echo "$(GREEN)Deployment complete!$(NC)"
	@echo "Visit http://localhost:8000/docs for API documentation"

# Check services health
health:
	@echo "$(GREEN)Checking services health...$(NC)"
	@curl -s http://localhost:8000/health && echo " API: OK" || echo " API: FAILED"
	@docker-compose exec -T redis redis-cli ping > /dev/null 2>&1 && echo " Redis: OK" || echo " Redis: FAILED"
	@docker-compose exec -T postgres pg_isready > /dev/null 2>&1 && echo " Postgres: OK" || echo " Postgres: FAILED"

check:
	poetry run ruff check .
	poetry run mypy .
	poetry run pytest
