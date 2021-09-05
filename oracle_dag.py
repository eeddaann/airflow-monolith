from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.oracle_hook import OracleHook
from airflow.utils.dates import days_ago
import pandas as pd

args = {
    'owner': 'xyz',
    'start_date': days_ago(2),
}

dag = DAG('example_xcom', schedule_interval="@once", default_args=args, tags=['example'])


def puller(**kwargs):
    ti = kwargs['ti']
    # get value_1
    pulled_value_1 = ti.xcom_pull(task_ids='data')
    print("VALUE IN PULLER : ", pulled_value_1)


def get_data_from_oracle(**kwargs):
    oracle_hook = OracleHook(oracle_conn_id=kwargs['oracle_conn_id'])
    return oracle_hook.get_records(sql=kwargs['sql'])

def echo():
    print("echo")
    return

def generate_data():
    df = pd.DataFrame(data={'col1': [1, 2, 3, 4], 'col2': [3, 4, 5, 7]})
    return df

push = PythonOperator(
    task_id='data',
    op_kwargs={'oracle_conn_id': 'oracle_conn_id', 'sql': 'SELECT * FROM CUSTOMERS'},
    provide_context=True,
    python_callable=get_data_from_oracle,
    dag=dag,
)

pull = PythonOperator(
    task_id='pullee',
    dag=dag,
    python_callable=puller,
    provide_context=True,
)

generate = PythonOperator(
    task_id='generate',
    dag=dag,
    python_callable= generate_data
)

echo = PythonOperator(
    task_id='echo',
    dag=dag,
    python_callable= echo
)
echo >> push
push >> pull
echo >> generate