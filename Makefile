release:
	git pull
	docker compose -f docker-compose.prod.yml up --build -d
fix-lint:
	autoflake --remove-unused-variables --in-place --recursive app
	isort app
	black app
