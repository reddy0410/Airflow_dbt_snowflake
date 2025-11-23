from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata
from kafka.admin import KafkaAdminClient
from kafka.errors import KafkaError
import sys

KAFKA_BROKER = "localhost:9092"

def get_topic_partitions(topic_name):
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        topic_metadata = admin.describe_topics([topic_name])
        partitions = [p['partition'] for p in topic_metadata[0]['partitions']]
        return partitions
    except Exception as e:
        print(f"❌ Failed to fetch partitions: {e}")
        sys.exit(1)

def reset_offsets(group_id, topic, reset_type, specific_offset=None):
    partitions = get_topic_partitions(topic)

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BROKER,
        group_id=group_id,
        enable_auto_commit=False
    )

    topic_partitions = [TopicPartition(topic, p) for p in partitions]

    consumer.assign(topic_partitions)

    print(f"\n🔁 Resetting offsets for group '{group_id}' on topic '{topic}' with strategy '{reset_type}'\n")

    offsets = {}
    for tp in topic_partitions:
        if reset_type == "earliest":
            consumer.seek_to_beginning(tp)
            new_offset = consumer.position(tp)
        elif reset_type == "latest":
            consumer.seek_to_end(tp)
            new_offset = consumer.position(tp)
        elif reset_type == "specific":
            if specific_offset is None:
                print("❌ Specific offset not provided.")
                return
            new_offset = specific_offset
            consumer.seek(tp, new_offset)
        else:
            print("❌ Invalid reset type. Use 'earliest', 'latest', or 'specific'.")
            return

        offsets[tp] = OffsetAndMetadata(new_offset, None)
        print(f"🔧 Partition {tp.partition} → New offset: {new_offset}")

    # Commit offsets
    consumer.commit(offsets=offsets)
    print("\n✅ Offsets successfully reset and committed.")
    consumer.close()

def main():
    topic = input("Enter Kafka topic name: ").strip()
    group_id = input("Enter consumer group ID: ").strip()
    reset_type = input("Reset type (earliest/latest/specific): ").strip().lower()

    specific_offset = None
    if reset_type == "specific":
        try:
            specific_offset = int(input("Enter specific offset to set: ").strip())
        except ValueError:
            print("❌ Invalid offset.")
            return

    reset_offsets(group_id, topic, reset_type, specific_offset)

if __name__ == "__main__":
    main()

