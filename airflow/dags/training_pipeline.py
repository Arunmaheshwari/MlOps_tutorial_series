from __future__ import annotations
import json
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow.operators.python import pythonOperator




from src.pipeline.training_pipeline import TrainingPipeline
import numpy as np

training_pipeline = TrainingPipeline()


with DAG(                                                   # DAG: Direct Acyclic Graph
    "gemstone_training_pipeline",
    default_args = {"retries": 2},
    description = "It is my training pipeline",
    schedule = "@weekly",
    start_date = pendulum.datetime(2024, 11, 30, tz = "UTC"),
    catchup = False,
    tags = ["machine_learning", "classification", "gemstone"],


) as dag:
    
    dag.doc_md = __doc__

    def data_ingestion(**kwargs):
        ti = kwargs["ti"]
        train_data_path, test_data_path = training_pipeline.start_data_ingestion()
        ti.xcom_push("data_ingestion_artifact", {"train_data_path": train_data_path, "test_data_path": test_data_path})

    def data_transformation(**kwargs):
        ti = kwargs["ti"]
        data_ingestion_artifact = ti.xcom_pull(task_ids = "data_ingestion", key = "data_ingestion_artifact")
        train_arr, test_arr = training_pipeline.start_data_transformation(data_ingestion_artifact['train_data_path'])
        train_arr = train_arr.tolist()
        test_arr = test_arr.tolist()
        ti.xcom_push("data_transformation_artifact", {"train_arr": train_arr, "test_arr": test_arr})


    def model_trainer(**kwargs):
        ti = kwargs['ti']
        data_transformation_artifact = ti.xcom_pull(task_ids = "data_transformation", key = "data_transformation_artifact" )
        train_arr = np.array(data_transformation_artifact['train_arr'])
        test_arr = np.array(data_transformation_artifact['test_arr'])
        training_pipeline.start_model_training(train_arr, test_arr)


    def push_data_to_s3(**kwargs):
        import os
        bucket_name = os.getenv("BUCKET_NAME")
        artifact_folder = "/app/artifacts"
        os.system(f"aws s3 sync {artifact_folder} s3:/{bucket_name}/artifact")


    

    data_ingestion_task = pythonOperator(
        task_id = "data_ingestion",
        python_callable = data_ingestion,
    )
    data_ingestion_task.doc_md = dedent(
        """\
    #### Ingestion task
    this task creates a train and test file.
    """
    )

    data_transform_task = pythonOperator(
        task_id = "data_transformation",
        python_callable = data_transformation,
    )
    data_transform_task.doc_md = dedent(
        """\
    #### transformation task
    this task performs the transformation.
    """
    )

    model_trainer_task = pythonOperator(
        task_id = "model_trainer",
        python_callable = model_trainer,
    )
    model_trainer_task.doc_md = dedent(
        """\
    #### model_trainer task
    this task performs the training.
    """
    )


    push_data_to_s3_task = pythonOperator(
        task_id = "push_data_to_s3",
        python_callable = push_data_to_s3,
    )


data_ingestion_task >> data_transform_task >> model_trainer_task >> push_data_to_s3_task