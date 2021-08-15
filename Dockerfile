FROM apache/airflow:2.1.2
COPY sample_dag.py /opt/airflow/dags
EXPOSE 8080:8080
COPY --chown=50000 run.sh /opt/airflow/run.sh
ENTRYPOINT [ "/bin/sh", "-c","/opt/airflow/run.sh"]