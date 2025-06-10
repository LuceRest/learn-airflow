from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime


default_args = {
    'owner': 'acilrestu12',
    'start_date': datetime(2023, 1, 1),
    # Add other default args like retries, etc.
}

with DAG(
    dag_id='dag_ml_pipeline_docker_operator_v04',
    default_args=default_args,
    description='Run ML pipeline with docker operator in Airflow locally',
    schedule_interval=None,  # Set your desired schedule interval or use None for manual triggering
) as dag:
    
    dataset_creation_task = BashOperator(
        task_id="faked_dataset_creation_task",
        bash_command="""
echo "Hey the dataset is ready, let's trigger the training process"
"""
    )

    model_train_and_publish_task = DockerOperator(
        task_id='docker_model_train_and_publish_task',
        # docker_url="unix://var/run/docker.sock",  # Use the default Docker socket
        docker_url="tcp://docker-socket-proxy:2375",  # Use the default Docker socket (Apabila menggunakan Airflow di Docker)
        api_version='auto',  # Use 'auto' to let Docker select the appropriate API version
        auto_remove=True,  # Remove the container when the task completes
        image='regression-training-image:v1.0',  # Replace with your Docker image and tag
        container_name="training_my_awesome_model",
        environment={
            'MINIO_ENDPOINT': 'host.docker.internal:9000',
            'MINIO_ACCESS_KEY_ID': 'eusjVTfD4arPjGIWAlvV',
            'MINIO_SECRET_ACCESS_KEY': 'xyEH4owdbqrO5FdsU0OI7NKU1aPsSlXbt4J3H5HV',
            'MINIO_BUCKET_NAME': 'learn-ml-pipeline',
        },  # Set environment variables inside the contain
        command=['python', 'train_and_publish.py'],  # Replace with the command you want to run inside the container
        # network_mode='bridge',  # Specify the network mode if needed
        # volumes=['/host/path:/container/path'],  # Mount volumes if needed
        dag=dag,
    )

    dataset_creation_task >> model_train_and_publish_task



