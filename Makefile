.PHONY: run down


run:
	docker compose down && docker compose up -d --build

down:
	docker compose down
