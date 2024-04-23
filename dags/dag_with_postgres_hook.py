from datetime import datetime, timedelta
import csv
import logging
import os  # Import the os module
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook  
from airflow.providers.amazon.aws.hooks.s3 import S3Hook 
from tempfile import NamedTemporaryFile

# Get the current working directory
current_dir = os.getcwd()

default_args = {
    "owner": "bash",
    "retries": 5,
    "retry_delay": timedelta(minutes=5)
}

def postgres_to_s3():
    # STEP 1: query data from PostgreSQL db and save into text file
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date <= '2022-05-01'")  # Corrected date format
    with NamedTemporaryFile(mode="w", suffix=".txt", dir=current_dir + "/dags/") as file:
    # with open("dags/get_orders.txt", "w") as file:
        csv_writer = csv.writer(file)  # Pass the file object to csv.writer()
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)  # Use writerows to write all rows
        file.flush()
        cursor.close()
        conn.close()
        logging.info("Saved orders data in text file get_orders.txt")
        # STEP 2: upload text file into S3
        s3_hook = S3Hook(aws_conn_id="minio_conn")
        s3_hook.load_file(
            filename= file.name,
            key= "orders/get_orders.txt",
            bucket_name= "airflow",
            replace= True
        )
        logging.info("Uploaded %s to S3", file.name)

with DAG(
    default_args=default_args,
    dag_id="dag_with_postgres_hook_v3",
    description="This is a dag with Postgres Hook",
    start_date=datetime(2024, 4, 21),
    schedule_interval=timedelta(days=1)  # Use timedelta for schedule_interval
) as dag:
    task1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3
    )
    task1
