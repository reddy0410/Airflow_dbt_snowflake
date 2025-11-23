from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError



# --- Step 1: Get user inputs ---
bootstrap_servers = 'localhost:9092'  # Change if needed

topic_name = input("Enter topic name: ")
partitions = int(input("Enter number of partitions: "))
replication_factor = int(input("Enter replication factor (1 for single-node Kafka): "))

# --- Step 2: Create Kafka Admin client ---
admin_client = KafkaAdminClient(
    bootstrap_servers=bootstrap_servers,
    client_id='topic_creator_script'
)

# --- Step 3: Create Topic ---
new_topic = NewTopic(
    name=topic_name,
    num_partitions=partitions,
    replication_factor=replication_factor
)

try:
    admin_client.create_topics(new_topics=[new_topic], validate_only=False)
    print(f"✅ Topic '{topic_name}' created with {partitions} partitions and replication factor {replication_factor}.")
except TopicAlreadyExistsError:
    print(f"⚠️ Topic '{topic_name}' already exists.")
except Exception as e:
    print(f"❌ Failed to create topic: {e}")

