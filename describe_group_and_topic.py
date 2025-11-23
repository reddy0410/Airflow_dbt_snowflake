from kafka.admin import KafkaAdminClient
from kafka.errors import KafkaError

# 🔧 Update this with your Kafka broker address
KAFKA_BROKER = "localhost:9092"

def describe_topic(topic_name):
    print(f"\n🔍 Describing Topic: {topic_name}")
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        topic_metadata = admin.describe_topics([topic_name])

        for topic in topic_metadata:
            print(f"  Topic: {topic['topic']}")
            print(f"  Partitions: {len(topic['partitions'])}")
            for partition in topic['partitions']:
                print(f"    - Partition: {partition['partition']}")
                print(f"      Leader: {partition['leader']}")
                print(f"      Replicas: {partition['replicas']}")
                print(f"      ISR: {partition['isr']}")
    except KafkaError as e:
        print(f"❌ Kafka error while describing topic: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def describe_consumer_group(group_id):
    print(f"\n🔍 Describing Consumer Group: {group_id}")
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        group_info = admin.describe_consumer_groups([group_id])

        if not group_info:
            print(f"❌ Group '{group_id}' not found.")
            return

        group = group_info[0]
        print(f"  Group State: {group.state}")
        print(f"  Members: {len(group.members)}")

        if not group.members:
            print("  ⚠️ No active members in this group.")
            return

        for idx, member in enumerate(group.members, start=1):
            print(f"\n  🧑 Member {idx}:")
            print(f"    ID:     {member.member_id}")
            print(f"    Host:   {member.client_host}")
            print(f"    Client: {member.client_id}")

            assignment = member.member_assignment
            if assignment and assignment.topic_partitions:
                print(f"    Assigned Partitions:")
                for topic, partitions in assignment.topic_partitions.items():
                    for p in partitions:
                        print(f"      - {topic}-{p}")
            else:
                print("    Assigned partitions: None")
    except KafkaError as e:
        print(f"❌ Kafka error while describing group: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    topic = input("Enter Kafka topic name: ").strip()
    group_id = input("Enter consumer group ID: ").strip()

    if not topic or not group_id:
        print("❌ Both topic and group ID are required.")
        return

    describe_topic(topic)
    describe_consumer_group(group_id)

if __name__ == "__main__":
    main()

