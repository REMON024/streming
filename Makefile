.PHONY: dev build down logs migrate seed test-backend test-streaming test-frontend lint-go clean

dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

up:
	docker compose up -d

build:
	docker compose build

down:
	docker compose down

down-v:
	docker compose down -v

logs:
	docker compose logs -f

migrate:
	docker compose run --rm backend dotnet ef database update --project src/StreamingPlatform.Infrastructure --startup-project src/StreamingPlatform.API

seed:
	docker compose run --rm backend dotnet run --project tools/Seeder

test-backend:
	cd apps/backend && dotnet test

test-streaming:
	cd apps/streaming && go test ./...

test-frontend:
	cd apps/frontend && pnpm test

lint-go:
	cd apps/streaming && golangci-lint run

clean:
	docker compose down -v --remove-orphans
	rm -rf apps/frontend/.next apps/frontend/node_modules
	rm -rf apps/streaming/streaming-server
