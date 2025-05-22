DC = docker compose

.PHONY: start stop clean kafka-build

start:
	@echo "Starting Docker Compose services..."
	@COMPOSE_BAKE=true $(DC) --env-file .env up -d --force-recreate

stop:
	@echo "Stopping Docker Compose services..."
	@$(DC) down

clean:
	@echo "Stopping and removing all containers, networks, and volumes..."
	@$(DC) down -v
	@docker system prune -af
