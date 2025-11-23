from kafka.admin import KafkaAdminClient, NewPartitions, ConfigResource, ConfigResourceType
from kafka.errors import KafkaError

KAFKA_BROKER = "localhost:9092"

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

def main():
    print("Kafka Topic Alter Tool")
    print("===========================")
    print("Options:")
    print("1. Increase topic partitions")
    print("2. Alter topic config")

    choice = input("Select option (1 or 2): ").strip()

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

    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    main()

