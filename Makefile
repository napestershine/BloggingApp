# Makefile for BloggingApp Docker operations
.PHONY: help up up-dev down logs rebuild build-api build-web clean test health status

# Default target
help: ## Show this help message
	@echo "BloggingApp Docker Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Environment setup
.env:
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.example..."; \
		cp .env.example .env; \
		echo "Please edit .env file with your configuration"; \
	fi

# Production commands
up: .env ## Start production services (db, api, web)
	docker compose up --build -d

down: ## Stop all services
	docker compose down

# Development commands  
up-dev: .env ## Start development services with hot reload
	docker compose -f compose.yml -f compose.dev.yml up --build

down-dev: ## Stop development services
	docker compose -f compose.yml -f compose.dev.yml down

# Testing commands
test: .env ## Run tests in CI environment
	docker compose -f compose.yml -f compose.ci.yml up --build --abort-on-container-exit
	docker compose -f compose.yml -f compose.ci.yml down

test-api: .env ## Run API tests only
	docker compose -f compose.yml -f compose.ci.yml up --build db api --abort-on-container-exit
	docker compose -f compose.yml -f compose.ci.yml down

test-web: .env ## Run Web tests only  
	docker compose -f compose.yml -f compose.ci.yml up --build web --abort-on-container-exit
	docker compose -f compose.yml -f compose.ci.yml down

# Build commands
build: ## Build all images
	docker compose build

build-api: ## Build API image only
	docker compose build api

build-web: ## Build Web image only
	docker compose build web

# Utility commands
logs: ## Show logs from all services
	docker compose logs -f

logs-dev: ## Show logs from development services
	docker compose -f compose.yml -f compose.dev.yml logs -f

logs-api: ## Show API logs only
	docker compose logs -f api

logs-web: ## Show Web logs only
	docker compose logs -f web

logs-db: ## Show database logs only
	docker compose logs -f db

# Health and status commands
health: ## Check health of all services
	@echo "Checking service health..."
	@docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
	@echo ""
	@echo "Health checks:"
	@docker compose exec api python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health'); print('✅ API healthy')" 2>/dev/null || echo "❌ API unhealthy"
	@docker compose exec web node -e "const http = require('http'); const req = http.request({hostname: '0.0.0.0', port: 3000, path: '/api/health', timeout: 5000}, (res) => process.exit(res.statusCode === 200 ? 0 : 1)); req.on('error', () => process.exit(1)); req.end();" && echo "✅ Web healthy" || echo "❌ Web unhealthy" 2>/dev/null

status: ## Show status of all services
	docker compose ps

# Cleanup commands
clean: ## Remove stopped containers and unused images
	docker compose down --remove-orphans
	docker system prune -f

clean-all: ## Remove all containers, images, and volumes (DESTRUCTIVE)
	docker compose down --volumes --remove-orphans
	docker system prune -af

# Database commands
db-shell: ## Connect to database shell
	docker compose exec db psql -U $$(grep POSTGRES_USER .env | cut -d= -f2) -d $$(grep POSTGRES_DB .env | cut -d= -f2)

db-backup: ## Backup database
	@mkdir -p backups
	docker compose exec db pg_dump -U $$(grep POSTGRES_USER .env | cut -d= -f2) $$(grep POSTGRES_DB .env | cut -d= -f2) > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backups/ directory"

# Development helpers
shell-api: ## Open shell in API container
	docker compose exec api /bin/bash

shell-web: ## Open shell in Web container  
	docker compose exec web /bin/sh

# Docker system info
docker-info: ## Show Docker system information
	@echo "Docker version:"
	@docker --version
	@echo ""
	@echo "Docker Compose version:"
	@docker compose version
	@echo ""
	@echo "Docker system info:"
	@docker system df