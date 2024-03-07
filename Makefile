up:
	docker compose up -d --build

down:
	docker compose down

remove-all-volume:
	docker volume rm $(docker volume ls -q)