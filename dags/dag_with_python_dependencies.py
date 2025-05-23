from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'acilrest12',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

def get_sklearn():
    import sklearn
    print(f"sklearn version: {sklearn.__version__}")

def get_matplotlib():
    import matplotlib
    print(f"matplotlib version: {matplotlib.__version__}")
    
    
with DAG (
    default_args=default_args,
    dag_id='dag_with_python_dependencies_v03',
    start_date=datetime(2025, 4, 1),
    schedule_interval='@daily',
) as dag:
    # task1 = PythonOperator(
    #     task_id='get_sklearn',
    #     python_callable=get_sklearn,
    #     dag=dag,
    # )
    
    get_sklearn = PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn,
    )
    
    get_matplotlib = PythonOperator(
        task_id='get_matplotlib',
        python_callable=get_matplotlib,
    )
    
    get_sklearn >> get_matplotlib
    