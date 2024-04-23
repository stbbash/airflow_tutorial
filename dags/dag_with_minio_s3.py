from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    "owner": "bash",
    "retries": 5,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id="dag_with_minio_s3_v2",
    description="This is a dag with MinIO/S3",
    start_date=datetime(2024, 4, 21),
    schedule_interval=timedelta(days=1)  # Use timedelta for schedule_interval
) as dag:
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='airflow',
        bucket_key='data.csv', 
        aws_conn_id='minio_conn',
        mode='poke',  # Use 'poke' mode
        poke_interval=5,  # Specify the poke interval
        timeout=30
    )
