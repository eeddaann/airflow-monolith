FROM apache/airflow:2.1.2
RUN pip install apache-airflow-providers-postgres
EXPOSE 8080:8080
COPY --chown=50000 run.sh /opt/airflow/run.sh
COPY sample_dag.py /opt/airflow/dags
ENTRYPOINT [ "/bin/sh", "-c","/opt/airflow/run.sh"]