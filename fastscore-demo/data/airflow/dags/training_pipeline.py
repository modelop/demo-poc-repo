from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 5, 21, 12),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

}

dag = DAG(
    'training_pipeline', catchup=False, default_args=default_args, schedule_interval=None)

t1 = BashOperator(
    task_id='pull_and_test_training_data',
    bash_command='echo t1',
    dag=dag)

t2 = BashOperator(
    task_id='generate_features',
    bash_command='echo t2',
    retries=3,
    dag=dag)

t3 = BashOperator(
    task_id='test_feature_integrity',
    bash_command='echo t3',
    retries=3,
    dag=dag)


t4 = BashOperator(
    task_id='train_model',
    bash_command='echo t4',
    retries=3,
    dag=dag)

t5 = BashOperator(
    task_id='validate_model',
    bash_command='cd /usr/local/airflow/processing && python3 t_task5.py',
    retries=3,
    dag=dag)

t6 = BashOperator(
    task_id='publish_model',
    bash_command='bash -x /usr/local/airflow/processing/train.sh ',
    retries=3,
    dag=dag)

t1 >> t2 >> t3 >> t4 >> t5 >> t6
