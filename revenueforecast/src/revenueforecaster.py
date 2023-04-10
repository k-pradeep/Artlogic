from datetime import datetime, timedelta
import os
from TaskA import monthlyARR
# The DAG object
from airflow import DAG

# Operators; we need this operate!
from airflow.operators.python_operator import PythonOperator


# Default Arguments used by script

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["pradeep.k0810@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

current_date = datetime.now()
start_date = current_date + timedelta(-1)


# Creating a DAG object
dag = DAG(
    os.path.basename(__file__),
    default_args=default_args,
    description="My First Airflow Script",
    schedule_interval=timedelta(days=1),
    start_date=start_date,
)

# creating tasks
t1 = PythonOperator(
    task_id="TaskA",
    python_callable=monthlyARR,
    dag=dag,
)

# creating dependency or Tree
# t1.set_downstream(t2)
