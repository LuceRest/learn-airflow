# Use an official Python runtime as a parent image
FROM python:3.9.7

# Set environment variables for AWS credentials (replace with your credentials)
ENV MINIO_ACCESS_KEY_ID=eusjVTfD4arPjGIWAlvV
ENV MINIO_SECRET_ACCESS_KEY=xyEH4owdbqrO5FdsU0OI7NKU1aPsSlXbt4J3H5HV
ENV MINIO_ENDPOINT=host.docker.internal:9000
ENV MINIO_BUCKET_NAME=learn-ml-pipeline

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the training and model publishing script
CMD ["python", "train_and_publish.py"]
