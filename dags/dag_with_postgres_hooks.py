from datetime import datetime, timedelta
from airflow import DAG
import csv
import logging
from tempfile import NamedTemporaryFile

from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args = {
    'owner': 'acilrestu12',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}


def postges_to_s3(ds_nodash, next_ds_nodash):
    # Step 1: query data from PostgreSQL db and save into text file
    hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE date >= '{ds_nodash}' AND date < '{next_ds_nodash}'")
    
    # with open(f'dags/get_orders_{ds_nodash}.txt', 'w') as f:
    #     csv_writer = csv.writer(f)
    #     csv_writer.writerow([i[0] for i in cursor.description])
    #     csv_writer.writerows(cursor)

    # cursor.close()
    # conn.close()
    
    # Step 2: upload text file to S3 bucket
    # s3_hook = S3Hook(aws_conn_id='minio_conn')
    # s3_hook.load_file(
    #     filename=f'dags/get_orders_{ds_nodash}.txt',
    #     key=f'orders/get_orders_{ds_nodash}.txt',
    #     bucket_name='airflow',
    #     replace=True,
    # )
    
    with NamedTemporaryFile(mode='w', suffix=f"{ds_nodash}") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        
        logging.info('Saved orders data in the file:', f'dags/get_orders_{ds_nodash}.txt')
    
        # Step 2: upload text file to S3 bucket
        s3_hook = S3Hook(aws_conn_id='minio_conn')
        s3_hook.load_file(
            filename=f.name,
            key=f'orders/get_orders_{ds_nodash}.txt',
            bucket_name='airflow',
            replace=True,
        )
        logging.info(f'Orders file {f.name} has been pushed to S3')

    
with DAG (
    dag_id='dag_with_postgres_hooks_v06',
    default_args=default_args,
    start_date=datetime(2025, 4, 1),
    schedule_interval='0 0 * * *',
    catchup=True,
) as dag:
    task1 = PythonOperator(
        task_id='postgres_to_s3',
        python_callable=postges_to_s3,
    )