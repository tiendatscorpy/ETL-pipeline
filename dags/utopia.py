from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.utils.task_group import TaskGroup

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

from utils.extract_features import extract_features
from utils.scale_features import scale_features
import os

default_args = {
    "owner": "dylan.nguyen",
    "depends_on_past": False,
    "email": ["dat.t.nguyen@aalto.fi"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2021, 1, 1),
}

# only list directories
INPUT_FOLDER = "/opt/airflow/input_folder"
TEMP_FOLDER = "/opt/airflow/temp_folder"
OUTPUT_FOLDER = "/opt/airflow/output_folder"

with DAG(
    "transform_gtzan_data",
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
) as dag:
    t1 = BashOperator(
        task_id="clean_up_temp_and_output",
        bash_command=f"rm -rfv {TEMP_FOLDER}/* && rm -rfv {OUTPUT_FOLDER}/*",
    )

    t2 = PythonOperator(
        task_id=f"extract_features",
        python_callable=extract_features,
        op_kwargs={"input_folder": INPUT_FOLDER, "output_folder": TEMP_FOLDER},
        dag=dag,
    )

    t3 = PythonOperator(
        task_id=f"scale_features",
        python_callable=scale_features,
        op_kwargs={"input_folder": TEMP_FOLDER, "output_folder": OUTPUT_FOLDER},
        dag=dag,
    )

    t4 = BashOperator(
        task_id="clean_up_temp_folder", bash_command=f"rm -rfv {TEMP_FOLDER}/*"
    )

    t1 >> t2 >> t3 >> t4