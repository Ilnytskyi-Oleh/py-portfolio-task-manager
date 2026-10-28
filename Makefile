COMPOSE ?= docker compose
PROFILE_DEV = --profile dev
PROFILE_PROD = --profile prod

.DEFAULT_GOAL := help

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-18s\033[0m %s\n", $$1, $$2}'

env: ## Create .env from example if missing
	@test -f .env || cp .env.example .env

build-dev: env ## Build development images
	$(COMPOSE) $(PROFILE_DEV) build

build-prod: env ## Build production images
	$(COMPOSE) $(PROFILE_PROD) build

up-dev: env ## Start development stack
	$(COMPOSE) $(PROFILE_DEV) up -d --build

up-prod: env ## Start production stack
	$(COMPOSE) $(PROFILE_PROD) up -d --build

down: ## Stop and remove containers
	$(COMPOSE) $(PROFILE_DEV) $(PROFILE_PROD) down

down-volumes: ## Stop containers and remove volumes
	$(COMPOSE) $(PROFILE_DEV) $(PROFILE_PROD) down -v

logs: ## Follow web-dev logs
	$(COMPOSE) $(PROFILE_DEV) logs -f web-dev

logs-prod: ## Follow web-prod logs
	$(COMPOSE) $(PROFILE_PROD) logs -f web-prod

shell: ## Open Django shell in web-dev
	$(COMPOSE) $(PROFILE_DEV) exec web-dev python manage.py shell

bash: ## Open bash in web-dev
	$(COMPOSE) $(PROFILE_DEV) exec web-dev bash

migrate: ## Run migrations in web-dev
	$(COMPOSE) $(PROFILE_DEV) exec web-dev python manage.py migrate

seed: ## Load demo data in web-dev
	$(COMPOSE) $(PROFILE_DEV) exec web-dev python manage.py seed_demo

createsuperuser: ## Create Django superuser in web-dev
	$(COMPOSE) $(PROFILE_DEV) exec web-dev python manage.py createsuperuser

lint: ## Run flake8 locally
	. .venv/bin/activate && flake8 tasks config manage.py

test: ## Run Django tests locally (SQLite)
	. .venv/bin/activate && \
		DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test tests

test-docker: ## Run tests inside web-dev container
	$(COMPOSE) $(PROFILE_DEV) exec web-dev \
		env DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test tests

.PHONY: help env build-dev build-prod up-dev up-prod down down-volumes \
	logs logs-prod shell bash migrate seed createsuperuser lint test test-docker
