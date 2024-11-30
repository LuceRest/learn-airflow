from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'ARest',
    'retries' : 5,
    'retry_delay' : timedelta(minutes=2)
}

# Function yg akan dijalankan di task
def greet(ti):        # it -> task instance
    # Mengambil value dari XCOM
    first_name = ti.xcom_pull(task_ids = 'get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids = 'get_name', key='last_name')
    age = ti.xcom_pull(task_ids = 'get_age', key='age')

    print(f'Hello World! My name is {first_name} {last_name}'
          f'and I am {age} years old!')

# Function untuk mengambil value parameter name melalui XCOM
def get_name(ti):
    # Mengirim value ke task selanjutnya melalui XCOM
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Fridname')

# Function untuk mengambil value parameter age melalui XCOM
def get_age(ti):
    # Mengirim value ke task selanjutnya melalui XCOM
    ti.xcom_push(key='age', value=19)
    

with DAG (
    dag_id = 'fist_dag_using_python_operator_v06',
    default_args = default_args,
    description = 'First dag using python operator',
    start_date = datetime(2024, 12, 1, 2),
    schedule_interval = '@daily',
) as dag:
    # Task instance (Python Operator)
    task1 = PythonOperator(
        task_id = 'greet',
        python_callable = greet,
        # op_kwargs = {'age' : 20}
    )
    
    task2 = PythonOperator(
        task_id = 'get_name',
        python_callable = get_name,
        # op_kwargs = {'name': 'Tom', 'age' : 20}
    )
    
    task3  = PythonOperator(
        task_id = 'get_age',
        python_callable = get_age,
        # op_kwargs = {'name': 'Tom', 'age' : 20}
    )
    
    # Task dependency
    [task2, task3] >> task1