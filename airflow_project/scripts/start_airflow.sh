#!/bin/bash

export AIRFLOW_HOME="/home/dataengineersnowflakedbt/airflow"
source "/home/dataengineersnowflakedbt/airflow_project/airflow_env/bin/activate"

LOGFILE="/home/dataengineersnowflakedbt/airflow/airflow_autostart.log"

# Run Airflow DB migration in case there are changes
airflow db migrate >> "/home/dataengineersnowflakedbt/airflow/airflow_autostart.log" 2>&1

# Start scheduler in background
airflow scheduler >> "/home/dataengineersnowflakedbt/airflow/airflow_autostart.log" 2>&1 &

# Start webserver in foreground
exec airflow webserver --workers 2 >> "/home/dataengineersnowflakedbt/airflow/airflow_autostart.log" 2>&1
