FROM apache/airflow:2.1.2
RUN pip install apache-airflow-providers-oracle
COPY instantclients /tmp/instantclients
EXPOSE 8080:8080
COPY --chown=50000 run.sh /opt/airflow/run.sh
USER root
RUN apt-get update && apt-get install -y alien libaio1 && alien -i /tmp/instantclients/oracle-instantclient-basic-21.3.0.0.0-1.x86_64.rpm && alien -i /tmp/instantclients/oracle-instantclient-devel-21.3.0.0.0-1.x86_64.rpm
RUN alien -i /tmp/instantclients/oracle-instantclient-sqlplus-21.3.0.0.0-1.x86_64.rpm && export LD_LIBRARY_PATH=/usr/lib/oracle/21/client64/lib/${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
USER airflow
COPY dags /opt/airflow/dags
COPY include /opt/airflow/include
ENTRYPOINT [ "/bin/sh", "-c","/opt/airflow/run.sh"]