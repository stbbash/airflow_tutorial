from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "owner": "bash",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="dag_with_catchup_backfill_v2",
    default_args=default_args,
    description="This is our first dag that we write",
    start_date=datetime(2023, 7, 29),
    schedule_interval=timedelta(days=1),  # Use timedelta for schedule_interval
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id="first_task",  
        bash_command="echo hello world, this is sample bash command"
    )