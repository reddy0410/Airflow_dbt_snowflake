from kafka.admin import KafkaAdminClient
from kafka.errors import KafkaError, UnknownTopicOrPartitionError, GroupIdNotFoundError

# 🔧 Kafka Bootstrap Server
KAFKA_BROKER = "localhost:9092"

def delete_topic(topic_name):
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        admin.delete_topics([topic_name])
        print(f"✅ Topic '{topic_name}' deleted successfully.")
    except UnknownTopicOrPartitionError:
        print(f"⚠️ Topic '{topic_name}' does not exist.")
    except KafkaError as e:
        print(f"❌ Kafka error deleting topic: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def delete_consumer_group(group_id):
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        admin.delete_consumer_groups([group_id])
        print(f"✅ Consumer group '{group_id}' deleted successfully.")
    except GroupIdNotFoundError:
        print(f"⚠️ Consumer group '{group_id}' does not exist.")
    except KafkaError as e:
        print(f"❌ Kafka error deleting group: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("Kafka Delete Tool")
    print("=======================")
    print("1. Delete a Kafka Topic")
    print("2. Delete a Consumer Group")

    choice = input("Select an option (1/2): ").strip()

    if choice == "1":
        topic = input("Enter the topic name to delete: ").strip()
        confirm = input(f"⚠️ Are you sure you want to delete topic '{topic}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            delete_topic(topic)
        else:
            print("❌ Deletion cancelled.")

    elif choice == "2":
        group = input("Enter the consumer group ID to delete: ").strip()
        confirm = input(f"⚠️ Are you sure you want to delete group '{group}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            delete_consumer_group(group)
        else:
            print("❌ Deletion cancelled.")

    else:
        print("❌ Invalid option.")

if __name__ == "__main__":
    main()

