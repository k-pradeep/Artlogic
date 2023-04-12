from datetime import datetime, timedelta
import os
from TaskA import monthlyARR
from TaskB import forecast_cash_in_bank
from convert_xlsx_csv import process_xlsx
from pathlib import Path

# The DAG object
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.bash_operator import BashOperator

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
    description="Ingests CSV files to forecast revenue generation over time",
    schedule_interval=timedelta(days=1),
    start_date=start_date,
)

# creating tasks
current_working_directory = Path(__file__).parent.parent.resolve()
data_directory = current_working_directory / "data" / "input"
xlsx_file_path = data_directory / "data.xlsx"
# File sensor
dataset_filesensor = FileSensor(
    task_id="dataset_filesensor",
    filepath=xlsx_file_path,
    poke="reschedule",
    timeout=60 * 60,  # 60 minutes
    dag=dag,
)

# Purge old output files
# delete old csv files
bash_cmd = "cd /usr/local/airflow/data/input && rm -f sheet*.csv; ls -latr"
remove_old_csv_files = BashOperator(
    task_id="remove_old_csv_files",
    bash_command=bash_cmd,
    dag=dag,
)

# delete old forecast files
purge_forecast_files_cmd = "cd /usr/local/airflow/data/output && rm -f *.csv; ls -latr"  # noqa: E501

remove_old_forecast_files = BashOperator(
    task_id="remove_old_forecast_files",
    bash_command=purge_forecast_files_cmd,
    dag=dag,
)
# start ETL
convert_xlsx_to_csv = PythonOperator(
    task_id="convert_xlsx_to_csv",
    python_callable=process_xlsx,
    dag=dag,
)

monthlyARR = PythonOperator(
    task_id="monthlyARR",
    python_callable=monthlyARR,
    dag=dag,
)

forecast_cash_in_bank = PythonOperator(
    task_id="forecast_cash_in_bank",
    python_callable=forecast_cash_in_bank,
    dag=dag,
)

# Task dependency
(
    dataset_filesensor
    >> remove_old_csv_files
    >> convert_xlsx_to_csv
    >> remove_old_forecast_files
    >> monthlyARR
    >> forecast_cash_in_bank
)
