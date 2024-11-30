from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'coder2j',
    'retries' : 5,
    'retry_delay' : timedelta(minutes=2)
}

# DAG Run
with DAG(
    dag_id = 'fist_dag_v5',
    default_args = default_args,
    description = 'This is my first dag that i write',
    start_date = datetime(2024, 11, 27, 2),
    schedule_interval = '@daily',
) as dag:
    # Task instance (Bash Operator)
    task1 = BashOperator(
        task_id = 'first_task',
        bash_command = 'echo hello world, this is the first task!'
    )
    
    task2 = BashOperator(
        task_id = 'second_task',
        bash_command = 'echo hey, i am task2 and will be running after task1!'
    )
    
    task3 = BashOperator(
        task_id = 'third_task',
        bash_command = 'echo hello, i am task3 and will be running after task1!'
    )
    
    # Task Dependency Method 1
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)
    
    # Task Dependency Method 2
    # task1 >> task2
    # task1 >> task3
    
    # Task Dependency Method 3
    task1 >> [task2, task3]