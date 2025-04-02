from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'acilrestu12',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id='dag_with_cron_expression_v03',
    default_args=default_args,
    start_date=datetime(2025, 3, 1),
    # schedule_interval='0 0 * * *',  # Cron expression for daily execution at midnight
    # schedule_interval='10 2-4 * * *',  # Cron expression for execution every 10 minutes between 2 AM and 4 AM
    schedule_interval= '10 2-4 * * Tue,Fri', # Cron expression for execution every 10 minutes between 2 AM and 4 AM on Tuesdays and Fridays
    catchup=True,
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "DAG with cron expression executed"',
    )