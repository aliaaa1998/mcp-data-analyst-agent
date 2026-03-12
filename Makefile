.PHONY: up down logs test lint format migrate seed demo clean

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

migrate:
	alembic upgrade head

seed:
	python scripts/seed_data.py

demo:
	curl -X POST http://localhost:8000/api/v1/demo/load-data

clean:
	rm -rf .pytest_cache .ruff_cache artifacts/charts/*.png
