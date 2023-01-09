from airflow import models

from airflow.operators.python_operator import PythonOperator
from airflow.operators import bash_operator
from datetime import datetime, timedelta
from dependencies.reddit_data import *
from dependencies.bigquery import *

YESTERDAY = datetime.now() - timedelta(days=1)
    
default_args = {
    'owner': 'Tomas Tong',
    'depends_on_past': False,
    'email': ['tomi-tomi92@hotmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': YESTERDAY, 
}
    
with models.DAG(
        'reddit_to_bigquery',
        catchup=False,
        default_args=default_args,
        schedule_interval=None) as dag:
    
    def _extract_data():
        upload_to_bucket()
        
    def _load_data():
        load_bigquery()
        
    extract = PythonOperator(
        task_id = "extract_reddit",
        python_callable = _extract_data)

    load = PythonOperator(
        task_id = "load_bigquery",
        python_callable = _load_data)

    print_dag_run_conf = bash_operator.BashOperator(
        task_id='print_dag_run_conf', bash_command='echo {{ dag_run.id }}')

    extract >> load
        
        
        
        

