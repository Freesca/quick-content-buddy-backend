.PHONY: help build up down restart logs logs-django logs-ollama logs-ngrok shell-django shell-ollama ps clean pull-model ngrok-url test

# Colori per output
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m # No Color

help: ## Mostra questo messaggio di aiuto
	@echo "$(GREEN)Comandi disponibili:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

build: ## Build dei container
	@echo "$(GREEN)Building containers...$(NC)"
	docker-compose build

up: ## Avvia tutti i container
	@echo "$(GREEN)Starting all containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Containers started!$(NC)"
	@echo "$(YELLOW)Django: http://localhost:8000$(NC)"
	@echo "$(YELLOW)Ngrok Dashboard: http://localhost:4040$(NC)"

down: ## Ferma tutti i container
	@echo "$(RED)Stopping all containers...$(NC)"
	docker-compose down

restart: down up ## Riavvia tutti i container

logs: ## Mostra i log di tutti i container
	docker-compose logs -f

logs-django: ## Mostra i log solo di Django
	docker-compose logs -f web

logs-ollama: ## Mostra i log solo di Ollama
	docker-compose logs -f ollama

logs-ngrok: ## Mostra i log solo di Ngrok
	docker-compose logs -f ngrok

shell-django: ## Apri una shell nel container Django
	docker exec -it django /bin/bash

shell-ollama: ## Apri una shell nel container Ollama
	docker exec -it ollama /bin/bash

ps: ## Mostra lo status dei container
	docker-compose ps

clean: ## Rimuove container, volumi e immagini
	@echo "$(RED)Removing all containers, volumes and images...$(NC)"
	docker-compose down -v --rmi all

pull-model: ## Scarica il modello llama3.2 in Ollama
	@echo "$(GREEN)Pulling llama3.2 model...$(NC)"
	docker exec -it ollama ollama pull llama3.2
	@echo "$(GREEN)Model downloaded!$(NC)"

pull-fast-model: ## Scarica modello veloce llama3.2:1b
	@echo "$(GREEN)Pulling fast model llama3.2:1b...$(NC)"
	docker exec -it ollama ollama pull llama3.2:1b
	@echo "$(GREEN)Fast model downloaded!$(NC)"

list-models: ## Lista tutti i modelli Ollama disponibili
	docker exec -it ollama ollama list

ngrok-url: ## Mostra l'URL pubblico di Ngrok
	@echo "$(GREEN)Ngrok Public URL:$(NC)"
	@curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | grep -o 'https://[^"]*' || echo "$(RED)Ngrok not running or URL not available$(NC)"

test: ## Testa l'health check di Django
	@echo "$(GREEN)Testing Django health check...$(NC)"
	@curl -s http://localhost:8000/api/health/ | python3 -m json.tool || echo "$(RED)Django not responding$(NC)"

test-ollama: ## Testa Ollama
	@echo "$(GREEN)Testing Ollama...$(NC)"
	@curl -s -X POST http://localhost:8000/api/test-ollama/ \
		-H "Content-Type: application/json" \
		-d '{"prompt": "Say hello in Italian"}' | python3 -m json.tool || echo "$(RED)Test failed$(NC)"

dev: ## Avvia in modalità development (con log in tempo reale)
	docker-compose up

rebuild: clean build up ## Rebuild completo (pulisce tutto e ricostruisce)

migrate: ## Esegue le migrazioni Django
	docker exec -it django python manage.py migrate

makemigrations: ## Crea nuove migrazioni Django
	docker exec -it django python manage.py makemigrations

createsuperuser: ## Crea un superuser Django
	docker exec -it django python manage.py createsuperuser

collectstatic: ## Raccoglie i file statici
	docker exec -it django python manage.py collectstatic --noinput

shell-python: ## Apri la shell Python di Django
	docker exec -it django python manage.py shell