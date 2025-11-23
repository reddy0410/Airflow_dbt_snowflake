import threading
import time
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient
from kafka.errors import KafkaError

KAFKA_BROKER = "localhost:9092"

def check_consumer_group_exists(group_id):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        admin_client.describe_consumer_groups([group_id])
        return True
    except KafkaError as e:
        err_str = str(e).lower()
        if "group does not exist" in err_str or "unknown" in err_str:
            return False
        print(f"❌ Kafka error checking group: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error checking group: {e}")
        return False

def create_consumer_instance(topic, group_id, instance_id):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[KAFKA_BROKER],
        group_id=group_id,
        enable_auto_commit=False,
        max_poll_records=500,
        max_partition_fetch_bytes=1 * 1024 * 1024,
        fetch_max_bytes=50 * 1024 * 1024,
        session_timeout_ms=10000,
        request_timeout_ms=305000,
        auto_offset_reset='earliest',
        value_deserializer=lambda m: m.decode('utf-8'),
        key_deserializer=lambda m: m.decode('utf-8') if m else None
    )

    print(f"🟢 Consumer {instance_id} joined group '{group_id}' on topic '{topic}'")

    time.sleep(5)

    assigned = consumer.assignment()
    if assigned:
        parts = [f"{p.topic}-{p.partition}" for p in assigned]
        print(f"✅ Consumer {instance_id} assigned partitions: {parts}")
    else:
        print(f"⚠️ Consumer {instance_id} got no partition")

    consumer.close()
    print(f"🔴 Consumer {instance_id} closed.")

def main():
    print("🔧 Kafka Consumer Group Simulator")

    topic = input("Enter Kafka topic name: ").strip()
    group_id = input("Enter Kafka consumer group ID: ").strip()
    num_consumers = input("Enter number of consumer instances to simulate: ").strip()

    if not topic or not group_id or not num_consumers.isdigit():
        print("❌ Invalid input.")
        return

    num_consumers = int(num_consumers)

    if check_consumer_group_exists(group_id):
        print(f"⚠️ Consumer group '{group_id}' already exists. Exiting.")
        return

    threads = []
    for i in range(num_consumers):
        t = threading.Thread(target=create_consumer_instance, args=(topic, group_id, i + 1))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n✅ All {num_consumers} consumers initialized and closed.")

if __name__ == "__main__":
    main()

