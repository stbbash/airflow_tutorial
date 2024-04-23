from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "bash",
    "retries": 5,
    "retry_delay": timedelta(minutes=5)
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids="get_name", key="last_name")
    age = ti.xcom_pull(task_ids="get_age", key="age")
    print(f"Hello world! my name is {first_name} {last_name}, and I am {age} years old")

def get_name(ti):
    ti.xcom_push(key="first_name", value="Donatus")
    ti.xcom_push(key="last_name", value="Ajaezu")
    
def get_age(ti):
    ti.xcom_push(key="age", value=20)
    
with DAG(
    default_args=default_args,
    dag_id="dag_with_python_operator_v6",
    description="This is our first dag that we write using python operator",
    start_date=datetime(2023, 10, 6),
    schedule_interval=timedelta(days=1)  # Use timedelta for schedule_interval
) as dag:
    task1 = PythonOperator(
        task_id = "greet",
        python_callable = greet,
        # op_kwargs = {"age": 30}
    )
    task2 = PythonOperator(
        task_id = "get_name",
        python_callable = get_name,
    )
    task3 = PythonOperator(
        task_id = "get_age",
        python_callable = get_age,
    )
    
    [task3, task2] >> task1