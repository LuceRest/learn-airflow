from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'acilrestu12',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    
}

with DAG(
    dag_id='dag_with_catchup_backfill_v02',
    default_args=default_args,
    start_date=datetime(2025, 3, 25),
    schedule_interval='@daily',
    catchup=False, # Set to False to disable backfilling
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "Task 1 executed"',
    )