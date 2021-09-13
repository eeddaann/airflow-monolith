# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# [START postgres_operator_howto_guide]
import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.email_operator import EmailOperator

# create_pet_table, populate_pet_table, get_all_pets, and get_birth_date are examples of tasks created by
# instantiating the Postgres Operator

with DAG(
    dag_id="postgres_operator_dag",
    start_date=datetime.datetime(2020, 2, 2),
    schedule_interval="@once",
    catchup=False,
) as dag:

    create_pet_table = PostgresOperator(
        task_id="create_pet_table",
        postgres_conn_id="postgres_demo",
        sql="""
            CREATE TABLE IF NOT EXISTS pet (
            pet_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            pet_type VARCHAR NOT NULL,
            birth_date DATE NOT NULL,
            OWNER VARCHAR NOT NULL);
          """,
    )

    create_owners_table = PostgresOperator(
        task_id="create_owners_table",
        postgres_conn_id="postgres_demo",
        sql="""
            CREATE TABLE IF NOT EXISTS owner (
            owner_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            preferred_pet_type VARCHAR NOT NULL);
          """,
    )

    populate_pet_table = PostgresOperator(
        task_id="populate_pet_table",
        postgres_conn_id="postgres_demo",
        sql="""
            INSERT INTO pet VALUES ( DEFAULT, 'Max', 'Dog', '2018-07-05', 'Jane');
            INSERT INTO pet VALUES ( DEFAULT, 'Susie', 'Cat', '2019-05-01', 'Phil');
            INSERT INTO pet VALUES ( DEFAULT, 'Lester', 'Hamster', '2020-06-23', 'Lily');
            INSERT INTO pet VALUES ( DEFAULT, 'Quincy', 'Parrot', '2013-08-11', 'Anne');
            """,
    )

    populate_owners_table = PostgresOperator(
        task_id="populate_owners_table",
        postgres_conn_id="postgres_demo",
        sql="""
            INSERT INTO owner VALUES ( DEFAULT, 'Max', 'Dog');
            INSERT INTO owner VALUES ( DEFAULT, 'Susie', 'Cat');
            INSERT INTO owner VALUES ( DEFAULT, 'Lester', 'Hamster');
            INSERT INTO owner VALUES ( DEFAULT, 'Quincy', 'Parrot');
            """,
    )

    get_all_pets = PostgresOperator(
        task_id="get_all_pets", postgres_conn_id="postgres_demo", sql="SELECT * FROM pet;"
    )

    send_email = EmailOperator(
        task_id='send_email',
        to='to@gmail.com',
        subject='Pets & owners tables created',
        html_content=""" <h3>Email Test</h3> """
    )


    create_pet_table >> populate_pet_table >> get_all_pets >> send_email
    create_owners_table >> populate_owners_table >> get_all_pets
    # [END postgres_operator_howto_guide]