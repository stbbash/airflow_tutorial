from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "owner": "bash",
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="our_first_dag_v5",
    default_args=default_args,
    description="This is our first dag that we write",
    start_date=datetime(2023, 7, 29, 2),
    schedule_interval=timedelta(days=1)  # Use timedelta for schedule_interval
) as dag:
    task1 = BashOperator(
        task_id="first_task",  
        bash_command="echo hello world, this is the first task!"
    )
    task2 = BashOperator(
        task_id="second_task",  
        bash_command="echo hey, this is the second task after first task!"
    )
    task3 = BashOperator(
        task_id="third_task",  
        bash_command="echo hey, this is the third task after first task!"
    )

    """ TASK DEPENDENCIES METHOD 1 """
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)

    """ TASK DEPENDENCIES METHOD 2 """
    task1 >> task2
    task1 >> task3
    
    """ TASK DEPENDENCIES METHOD 3 """
    task1 >> [task2, task3]