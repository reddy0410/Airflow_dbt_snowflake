from kafka.admin import KafkaAdminClient, NewPartitions, ConfigResource, ConfigResourceType
from kafka.errors import KafkaError
from kafka import KafkaConsumer
import threading
import time

KAFKA_BROKER = "localhost:9092"
CONSUMER_TIMEOUT = 30  # Timeout in seconds after which consumers will exit automatically

def increase_partitions(topic, new_count):
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        meta = admin.describe_topics([topic])
        current_count = len(meta[0]["partitions"])
        if new_count <= current_count:
            print(f"❌ New partition count must be greater than current count ({current_count})")
            return
        admin.create_partitions({topic: NewPartitions(total_count=new_count)})
        print(f"✅ Partitions increased from {current_count} to {new_count} for '{topic}'.")
    except KafkaError as e:
        print(f"❌ Kafka error increasing partitions: {e}")

def alter_topic_config(topic, key, value):
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        config_resource = ConfigResource(ConfigResourceType.TOPIC, topic)
        admin.alter_configs({config_resource: {key: value}})
        print(f"✅ Topic '{topic}' config '{key}' set to '{value}'.")
    except KafkaError as e:
        print(f"❌ Kafka error altering config: {e}")

def consumer_task(consumer_id, topic, group_id):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id=group_id,
        enable_auto_commit=True,
        auto_offset_reset='earliest'
    )
    print(f"🟢 Consumer {consumer_id} started in group '{group_id}' on topic '{topic}'")
    try:
        message_count = 0
        start_time = time.time()
        while time.time() - start_time < CONSUMER_TIMEOUT:
            records = consumer.poll(timeout_ms=1000)  # poll with 1 second timeout
            if records:
                for tp, messages in records.items():
                    for message in messages:
                        print(f"Consumer {consumer_id} received message: {message.value.decode('utf-8')}")
                        message_count += 1
        print(f"🛑 Consumer {consumer_id} stopped after consuming {message_count} messages.")
    except Exception as e:
        print(f"Consumer {consumer_id} error: {e}")
    finally:
        consumer.close()

def launch_multiple_consumers(topic, group_id, count):
    threads = []
    for i in range(count):
        t = threading.Thread(target=consumer_task, args=(i+1, topic, group_id), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.5)  # stagger start times a bit
    print(f"🟢 Launched {count} consumer(s) in group '{group_id}' for topic '{topic}'")

    # Wait for threads to finish (or timeout)
    for t in threads:
        t.join()
    print("🟢 All consumers have finished. Exiting...")

def main():
    print("Kafka Topic Alter & Consumer Launcher Tool")
    print("===========================================")
    print("Options:")
    print("1. Increase topic partitions")
    print("2. Alter topic config")
    print("3. Launch multiple consumers in a group")

    choice = input("Select option (1-3): ").strip()

    if choice == "1":
        topic = input("Topic name: ").strip()
        try:
            new_count = int(input("New total partition count: ").strip())
        except ValueError:
            print("❌ Invalid number.")
            return
        increase_partitions(topic, new_count)

    elif choice == "2":
        topic = input("Topic name: ").strip()
        key = input("Config key (e.g., retention.ms): ").strip()
        value = input("Config value: ").strip()
        alter_topic_config(topic, key, value)

    elif choice == "3":
        topic = input("Topic name: ").strip()
        group_id = input("Consumer group ID: ").strip()
        try:
            count = int(input("Number of consumers to launch: ").strip())
            if count < 1:
                raise ValueError
        except ValueError:
            print("❌ Number of consumers must be a positive integer.")
            return
        launch_multiple_consumers(topic, group_id, count)

    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    main()

