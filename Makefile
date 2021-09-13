docker-build-run:
	docker build -t airflow-mono:postgres . && docker run -p 8080:8080 airflow-mono:postgres

postgres-start:
	docker run --rm --name test-instance -e POSTGRES_PASSWORD=password -p 5433:5432 postgres