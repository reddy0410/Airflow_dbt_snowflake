#!/usr/bin/env bash

set -e

### Variables
AIRFLOW_VERSION="2.10.3"
PYTHON_VERSION="3.11"
PG_DB="airflow"
PG_USER="airflow_user"
PG_PASS="airflow_pass"
ADMIN_USER="admin"
ADMIN_EMAIL="dataengineersnowflakedbt@gmail.com"
ADMIN_PASS="admin"

KAFKA_VERSION="3.5.1"
SCALA_VERSION="2.13"
KAFKA_INSTALL_DIR="/opt/kafka"
KAFKA_LOG_DIR="/var/lib/kafka/kraft-logs"
KAFKA_CONF_DIR="${KAFKA_INSTALL_DIR}/config/kraft"

WORK_DIR="$HOME/airflow_project"
VENV_DIR="$WORK_DIR/airflow_env"
AIRFLOW_HOME_DIR="$HOME/airflow"
SCRIPT_DIR="$WORK_DIR/scripts"
LOGFILE="$AIRFLOW_HOME_DIR/airflow_autostart.log"

REAL_USER=$(logname)

echo "1. Installing system packages..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev build-essential \
     postgresql postgresql-contrib libpq-dev curl default-jre wget git

echo "2. Creating virtual environment..."
mkdir -p "${WORK_DIR}"
cd "${WORK_DIR}"
python${PYTHON_VERSION} -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"

echo "3. Installing Airflow, kafka-python, dbt and Snowflake packages..."
pip install --upgrade pip setuptools wheel
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
curl --head --silent --fail "$CONSTRAINT_URL" > /dev/null || {
    echo "ERROR: Airflow constraint file not found for Python ${PYTHON_VERSION}. Exiting."
    exit 1
}
pip install "apache-airflow[postgres]==${AIRFLOW_VERSION}" psycopg2-binary kafka-python --constraint "${CONSTRAINT_URL}"

# Install dbt core, snowflake adapter, Airflow Snowflake provider, and DBT Cloud provider
pip install dbt-snowflake apache-airflow-providers-snowflake apache-airflow-providers-dbt-cloud

echo "4. Setting up PostgreSQL..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

DB_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${PG_DB}'")
[ "$DB_EXISTS" != "1" ] && sudo -u postgres createdb ${PG_DB}

USER_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${PG_USER}'")
[ "$USER_EXISTS" != "1" ] && sudo -u postgres psql -c "CREATE USER ${PG_USER} WITH PASSWORD '${PG_PASS}';"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${PG_DB} TO ${PG_USER};"
sudo -u postgres psql -d ${PG_DB} -c "GRANT USAGE, CREATE ON SCHEMA public TO ${PG_USER};"
sudo -u postgres psql -d ${PG_DB} -c "ALTER ROLE ${PG_USER} SET search_path TO public;"

echo "5. Configuring Airflow..."

# Configure Airflow Home
export AIRFLOW_HOME="${AIRFLOW_HOME_DIR}"
mkdir -p "${AIRFLOW_HOME}"
cd "${AIRFLOW_HOME}"

# Initialize Airflow DB
rm -f "${AIRFLOW_HOME}/airflow.db"
airflow db init
airflow db migrate

# Configure Logging to suppress deprecation warnings
# Add logging configuration to suppress warnings in airflow.cfg
sed -i "s|#logging_level = INFO|logging_level = WARNING|" "${AIRFLOW_HOME}/airflow.cfg"
sed -i "s|#log_format = [%(asctime)s] %(levelname)s - %(message)s|log_format = [%(asctime)s] %(levelname)s - %(message)s|" "${AIRFLOW_HOME}/airflow.cfg"

# Set the Airflow executor
sed -i "s/^executor = .*/executor = LocalExecutor/" "${AIRFLOW_HOME}/airflow.cfg"

# Setup PostgreSQL as the SQLAlchemy connection string
sed -i "s#^sql_alchemy_conn = .*#sql_alchemy_conn = postgresql+psycopg2://${PG_USER}:${PG_PASS}@localhost/${PG_DB}#" "${AIRFLOW_HOME}/airflow.cfg"

# Disable loading example DAGs
sed -i "s/^load_examples = .*/load_examples = False/" "${AIRFLOW_HOME}/airflow.cfg"

# Set the web server host to be accessible from any IP
sed -i "s/^web_server_host = .*/web_server_host = 0.0.0.0/" "${AIRFLOW_HOME}/airflow.cfg"

# Rate-Limiting Configuration
# You can rate-limit the number of tasks concurrently running with the following settings
# Ensure that you adjust concurrency settings based on your workload

# Set maximum concurrency for each DAG and limit the number of tasks per DAG
sed -i "s/^dag_concurrency = .*/dag_concurrency = 16/" "${AIRFLOW_HOME}/airflow.cfg"
sed -i "s/^max_active_runs_per_dag = .*/max_active_runs_per_dag = 2/" "${AIRFLOW_HOME}/airflow.cfg"

# Set the maximum number of workers for the web server and scheduler
sed -i "s/^web_server_worker_timeout = .*/web_server_worker_timeout = 120/" "${AIRFLOW_HOME}/airflow.cfg"
sed -i "s/^scheduler.task_queued_timeout = .*/scheduler.task_queued_timeout = 600/" "${AIRFLOW_HOME}/airflow.cfg"

# Optional: If you're using CeleryExecutor, you can configure task rate limiting (if needed)
# Uncomment and modify these lines if using Celery
# sed -i "s/^celery_default_queue = .*/celery_default_queue = default/" "${AIRFLOW_HOME}/airflow.cfg"
# sed -i "s/^celery_task_rate_limit = .*/celery_task_rate_limit = 10/" "${AIRFLOW_HOME}/airflow.cfg"

# Optional: Adjust maximum retries for DAGs or tasks to handle failures gracefully
sed -i "s/^max_retries = .*/max_retries = 3/" "${AIRFLOW_HOME}/airflow.cfg"


echo "6. Creating Airflow admin user..."
airflow users create \
    --username "${ADMIN_USER}" \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email "${ADMIN_EMAIL}" \
    --password "${ADMIN_PASS}"

echo "7. Installing Kafka ${KAFKA_VERSION} in KRaft mode..."
sudo mkdir -p "${KAFKA_INSTALL_DIR}"

PRIMARY_URL="https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz"
MIRROR_URL="https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz"

if wget --spider --quiet "${PRIMARY_URL}"; then
    DOWNLOAD_URL="${PRIMARY_URL}"
else
    echo "Primary download URL failed; falling back to ${MIRROR_URL}"
    DOWNLOAD_URL="${MIRROR_URL}"
fi

sudo wget "${DOWNLOAD_URL}" -O /tmp/kafka.tgz
sudo tar -xzf /tmp/kafka.tgz -C "${KAFKA_INSTALL_DIR}" --strip-components 1

sudo mkdir -p "${KAFKA_CONF_DIR}"
sudo cp "${KAFKA_INSTALL_DIR}/config/server.properties" "${KAFKA_CONF_DIR}/server.properties"

KRAFT_CLUSTER_ID=$("${KAFKA_INSTALL_DIR}/bin/kafka-storage.sh" random-uuid)
echo "Generated KRaft cluster ID: ${KRAFT_CLUSTER_ID}"

sudo sed -i "s|#listeners=PLAINTEXT://:9092|listeners=PLAINTEXT://:9092,CONTROLLER://:9093|" "${KAFKA_CONF_DIR}/server.properties"
sudo sed -i "s|#log.dirs=/tmp/kafka-logs|log.dirs=${KAFKA_LOG_DIR}|" "${KAFKA_CONF_DIR}/server.properties"

sudo bash -c "cat >> ${KAFKA_CONF_DIR}/server.properties" <<EOL
process.roles=broker,controller
node.id=1
broker.id=1
controller.quorum.voters=1@localhost:9093
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER
log.dirs=${KAFKA_LOG_DIR}
EOL

sudo mkdir -p "${KAFKA_LOG_DIR}"
sudo chown -R ${REAL_USER}:${REAL_USER} "${KAFKA_LOG_DIR}"
sudo chown -R ${REAL_USER}:${REAL_USER} "${KAFKA_INSTALL_DIR}"

"${KAFKA_INSTALL_DIR}/bin/kafka-storage.sh" format -t ${KRAFT_CLUSTER_ID} -c "${KAFKA_CONF_DIR}/server.properties"

SERVICE_KAFKA="/etc/systemd/system/kafka.service"
sudo bash -c "cat <<EOL > ${SERVICE_KAFKA}
[Unit]
Description=Apache Kafka (KRaft mode) Broker & Controller
After=network.target

[Service]
Type=simple
User=${REAL_USER}
ExecStart=${KAFKA_INSTALL_DIR}/bin/kafka-server-start.sh ${KAFKA_CONF_DIR}/server.properties
ExecStop=${KAFKA_INSTALL_DIR}/bin/kafka-server-stop.sh
Restart=on-failure
Environment=JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

[Install]
WantedBy=multi-user.target
EOL"

sudo systemctl daemon-reload
sudo systemctl enable kafka
sudo systemctl start kafka

echo "8. Creating Airflow startup script..."
mkdir -p "${SCRIPT_DIR}"
cat <<EOT > "${SCRIPT_DIR}/start_airflow.sh"
#!/bin/bash

export AIRFLOW_HOME="$HOME/airflow"
source "$HOME/airflow_project/airflow_env/bin/activate"

LOGFILE="$AIRFLOW_HOME/airflow_autostart.log"

# Run Airflow DB migration in case there are changes
airflow db migrate >> "$LOGFILE" 2>&1

# Start scheduler in background
airflow scheduler >> "$LOGFILE" 2>&1 &

# Start webserver in foreground
exec airflow webserver --workers 2 >> "$LOGFILE" 2>&1
EOT

chmod +x "${SCRIPT_DIR}/start_airflow.sh"

echo "9. Setting up Airflow systemd service..."
SERVICE_FILE="/etc/systemd/system/airflow.service"
sudo bash -c "cat <<EOT > ${SERVICE_FILE}
[Unit]
Description=Apache Airflow Webserver + Scheduler
After=network.target postgresql.service kafka.service

[Service]
User=${REAL_USER}
WorkingDirectory=${WORK_DIR}
ExecStart=${SCRIPT_DIR}/start_airflow.sh
Restart=on-failure
RestartSec=10
Environment=PATH=${VENV_DIR}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=AIRFLOW_HOME=${AIRFLOW_HOME_DIR}
Environment=AIRFLOW__CORE__EXECUTOR=LocalExecutor

[Install]
WantedBy=multi-user.target
EOT"

sudo systemctl daemon-reload
sudo systemctl enable airflow
sudo systemctl start airflow

echo "10. (Optional) Create Snowflake connection in Airflow"
echo "Run the following command manually (adjust with your credentials):"
echo ""
echo "airflow connections add 'snowflake_default' \\" 
echo "  --conn-type snowflake \\" 
echo "  --conn-login <SNOWFLAKE_USER> \\" 
echo "  --conn-password <SNOWFLAKE_PASSWORD> \\" 
echo "  --conn-host <SNOWFLAKE_ACCOUNT>.snowflakecomputing.com \\" 
echo "  --conn-schema <SNOWFLAKE_WAREHOUSE> \\" 
echo "  --conn-extra '{\"account\": \"<SNOWFLAKE_ACCOUNT>\", \"warehouse\": \"<WAREHOUSE>\", \"database\": \"<DATABASE>\", \"role\": \"<ROLE>\"}'"
echo ""

echo "11. (Optional) Create DBT Cloud connection in Airflow"
echo "Run the following command manually (adjust with your credentials):"
echo ""
echo "airflow connections add 'dbt_cloud_default' \\" 
echo "  --conn-type http \\" 
echo "  --conn-host https://cloud.getdbt.com \\" 
echo "  --conn-login <DBT_API_TOKEN> \\" 
echo "  --conn-extra '{\"account\": \"<DBT_ACCOUNT>\", \"job_id\": <DBT_JOB_ID>}'"
echo ""

echo "Installation Complete!"
echo "-----------------------------------------------"
echo "Airflow UI:      http://<your-vm-ip>:8080"
echo "PostgreSQL DB:   ${PG_DB}"
echo "Kafka installed at: ${KAFKA_INSTALL_DIR}"
echo "Airflow home:    ${AIRFLOW_HOME_DIR}"
