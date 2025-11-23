from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata
from kafka.errors import KafkaError
import sys

KAFKA_BROKER = "localhost:9092"

def reset_offsets(group_id, topic, reset_type="earliest"):
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_BROKER,
            group_id=group_id,
            enable_auto_commit=False,
            consumer_timeout_ms=5000  # Exit poll if no messages for 5 seconds
        )
        
        partitions = consumer.partitions_for_topic(topic)
        if not partitions:
            print(f"❌ No partitions found for topic '{topic}'. Exiting.")
            consumer.close()
            return

        topic_partitions = [TopicPartition(topic, p) for p in partitions]
        consumer.assign(topic_partitions)

        offsets = {}
        for tp in topic_partitions:
            if reset_type == "earliest":
                consumer.seek_to_beginning(tp)
            elif reset_type == "latest":
                consumer.seek_to_end(tp)
            else:
                print("❌ Invalid reset_type; use 'earliest' or 'latest'.")
                consumer.close()
                return
            
            pos = consumer.position(tp)
            print(f"Partition {tp.partition}: setting offset to {pos}")
            offsets[tp] = OffsetAndMetadata(pos, None)

        consumer.commit(offsets=offsets)
        print(f"✅ Offsets reset to '{reset_type}' for group '{group_id}' on topic '{topic}'.")
        consumer.close()

    except KafkaError as e:
        print(f"❌ Kafka error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python reset_offsets.py <group_id> <topic> <earliest/latest>")
        sys.exit(1)
    
    group_id, topic, reset_type = sys.argv[1], sys.argv[2], sys.argv[3].lower()
    reset_offsets(group_id, topic, reset_type)

