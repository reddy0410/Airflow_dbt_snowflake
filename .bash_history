ls -ltr
vi installer.sh
chmod 755 installer.sh
bash installer.sh
ps aux | grep kafka.Kafka
ps -ef
ps -ef |grep kafka
cd /opt/
ls -ltr
cd kafka/
ls -ltr
sudo systemctl status kafka
ls -l /opt/kafka/bin/kafka-server-start.sh
java -version
cat /opt/kafka/logs/server.log
sudo journalctl -u kafka.service -b --no-pager
which java
readlink -f /usr/bin/java
sudo vi /etc/systemd/system/kafka.service
sudo systemctl daemon-reload
sudo systemctl restart kafka
sudo systemctl status kafka
JAVA_BIN_PATH=$(readlink -f $(which java))
JAVA_HOME=$(dirname $(dirname $JAVA_BIN_PATH))
echo $JAVA_HOME
sudo systemctl status kafka
sudo systemctl status airflow
sudo journalctl -u kafka.service -b --no-pager
cd /etc/kaf
cd /etc/kafka
pwd
cd /etc/
ls -ltr
cd /opt/kafka
ls -ltr
cd config/
ls -ltr
more server.properties
ls -ltr /etc/systemd/system/kafka.service
date
sudo vi /etc/systemd/system/kafka.service
sudo journalctl -u kafka.service -b --no-pager
sudo systemctl daemon-reload
sudo systemctl restart kafka
sudo systemctl status kafka
sudo systemctl restart kafka
sudo journalctl -u kafka.service -b --no-pager
sudo systemctl status postgrey
sudo vi /etc/systemd/system/kafka.service
cd
ls -ltr
vi create_kafka_topic.py
chmod 755 create_kafka_topic.py
python3 create_kafka_topic.py
python -c "from kafka.admin import KafkaAdminClient; print('Kafka module is available')"
python3 -c "from kafka.admin import KafkaAdminClient; print('Kafka module is available')"
pwd
ls -ltr
cd airflow_project
ls -ltr
cd scripts/
ls -ltr
cat start_airflow.sh
cd
ls -ltr
vi create_kafka_topic.py 
python3 create_kafka_topic.py 
vi create_kafka_topic.py 
python3 create_kafka_topic.py 
vi create_kafka_topic.py 
source "/home/dataengineersnowflakedbt/airflow_project/airflow_env/bin/activate"
pwd
ls -ltr
python3 create_kafka_topic.py 
cat create_kafka_topic.py
ls -ltr
cat create_kafka_topic.py
vi create_kafka_consumer_group.py
source "/home/dataengineersnowflakedbt/airflow_project/airflow_env/bin/activate"
ls -ltr
chmod 755 create_kafka_consumer_group.py
ls -ltr
python3 create_kafka_consumer_group.py
rm create_kafka_consumer_group.py
vi create_kafka_consumer_group.py
python3 create_kafka_consumer_group.py
rm create_kafka_consumer_group.py
vi create_kafka_consumer_group.py
python3 create_kafka_consumer_group.py
rm create_kafka_consumer_group.py
vi create_kafka_consumer_group.py
python3 create_kafka_consumer_group.py
rm create_kafka_consumer_group.py
vi create_kafka_consumer_group.py
python3 create_kafka_consumer_group.py
ls -ltr
python3 create_kafka_topic.py
cat create_kafka_consumer_group.py
more create_kafka_consumer_group.py
vi create_kafka_consumer_group.py
vi describe_group_and_topic.py
ls -ltr
chmod 755 create_kafka_consumer_group.py describe_group_and_topic.py
ls -ltr
python3 describe_group_and_topic.py
vi describe_group_and_topic.py
rm describe_group_and_topic.py
vi describe_group_and_topic.py
chmod 755 create_kafka_consumer_group.py describe_group_and_topic.py
python3 describe_group_and_topic.py
vi describe_group_and_topic_updated.py
python3 describe_group_and_topic_updated.py
vi reset_kafka_offsets.py
chmod 755 reset_kafka_offsets.py
python3 reset_kafka_offsets.py
vi kafka_delete_tool.py
vi kafka_topic_alter.py
python3 reset_kafka_offsets.py
vi offset_new.py
python3 offset_new.py sravanthi sravanthi-con-grp earliest
ls -ltr
chmod 755 describe_group_and_topic_updated.py kafka_delete_tool.py kafka_topic_alter.py offset_new.py
ls -ltr
python3 kafka_topic_alter.py
python3 describe_group_and_topic_updated.py
ls -ltr
vi kafka_topic_group_alter_updated.py 
python3 kafka_topic_group_alter_updated.py 
python3 describe_group_and_topic_updated.py
rm kafka_topic_group_alter_updated.py 
vi kafka_topic_group_alter_updated.py 
python3 describe_group_and_topic_updated.py
python3 kafka_topic_group_alter_updated.py 
rm kafka_topic_group_alter_updated.py 
vi kafka_topic_group_alter_updated.py 
python3 kafka_topic_group_alter_updated.py 
ls -ltr
kafkaps -ef \l
ps -ef |kafka
ps -ef |grep kafka
ls -ltr
wc -l installer.sh
python3 create_kafka_topic.py
cd /opt/kafka/
ls -ltr
cd config/
ls -ltr
date
more server.properties
ls -ltr
cd /sys/
ls -ltr
cd 
exit
ls -ltr
pwd
ls -ltr
git remote add origin https://github.com/reddy0410/Airflow_dbt_snowflake.git
git init
git add .
git push -u origin main 
git remote add origin https://github.com/reddy0410/Airflow_dbt_snowflake.git
ls -ltre
ls ltr
ls -ltr
git push -u origin main 
git branch -M main
git push -u origin main
echo "# Airflow_dbt_snowflake" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/reddy0410/Airflow_dbt_snowflake.git
git push -u origin main
ls -ltr
git push -u origin main
pwd
git init
ls -lta
git remote add origin https://github.com/reddy0410/Airflow_dbt_snowflake.git
git add .
git commit -m "Initial commit"
git config --global user.email "dataengineersnowflakedbt@gmail.com"
git config --global user.name "Venkat L"
git add .
