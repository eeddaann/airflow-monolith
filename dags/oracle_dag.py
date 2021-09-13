import datetime
import requests
from airflow import DAG
from airflow.providers.oracle.operators.oracle import OracleOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.email_operator import EmailOperator

def get_version():
    r = requests.get("http://localhost:8080/api/v1/version")
    return r.json()['version']

with DAG(
    dag_id="oracle_operator_dag",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@once",
    template_searchpath='/opt/airflow/include',
    catchup=False,
) as dag:

    create_contact_table_inline = OracleOperator(
        task_id="create_contact_table_inline",
        oracle_conn_id="oracle_demo",
        sql="""
            CREATE TABLE contacts
            ( contact_id number(10) not null,
            last_name varchar2(50) not null,
            first_name varchar2(50) not null,
            address varchar2(50),
            city varchar2(50),
            state varchar2(20),
            zip_code varchar2(10),
            CONSTRAINT contacts_pk PRIMARY KEY (contact_id)
            );
          """,
    )

    populate_contact_table = OracleOperator(
        task_id="populate_contact_table",
        oracle_conn_id="oracle_demo",
        sql="""
            INSERT INTO contacts
            (contact_id, last_name, first_name, address)
            VALUES
            (1000, 'Smith', 'Jane', '10 Somewhere St.');
            """,
    )

    create_contact_table_file = OracleOperator(
        task_id='create_contact_table_file',
        oracle_conn_id="oracle_demo",
        sql='create-contacts.sql'
    )

    populate_contact_table_file = OracleOperator(
        task_id='populate_contact_table_file',
        oracle_conn_id="oracle_demo",
        sql='insert-contacts.sql'
    )

    get_version_bash = BashOperator(
        task_id='get_version_bash',
        bash_command='curl http://localhost:8080/api/v1/version',
        retries=3,
    )

    get_version_python = PythonOperator(
        task_id='get_version_python',
        python_callable=get_version,
        provide_context=True,
    )

    get_version_http = SimpleHttpOperator(
        task_id='get_version_http',
        method='GET',
        endpoint='http://localhost:8080/api/v1/version',
        response_filter=lambda response: response.json()['version'],
        headers={},
    )

    send_email = EmailOperator(
        task_id='send_email',
        to='to@gmail.com',
        subject='Pets & owners tables created',
        html_content=""" <h3>Email Test</h3> """
    )


    create_contact_table_inline >> populate_contact_table >> send_email
    create_contact_table_file >> populate_contact_table_file >> send_email
    get_version_bash >> get_version_http
    get_version_python >> get_version_http >> send_email