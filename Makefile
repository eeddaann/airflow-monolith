docker-build-run:
	docker build -t airflow-mono . && docker run -p 8080:8080 airflow-mono

docker-save:
	docker save airflow-mono | gzip > airflow-mono.tar.gz