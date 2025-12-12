#!/usr/bin/env python3
import json
import random
import time
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# ----------------------------
# Kafka Configuration
# ----------------------------
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "my_topic"

# ----------------------------
# Create topic if it does not exist
# ----------------------------
admin_client = KafkaAdminClient(
    bootstrap_servers=KAFKA_BROKER,
    client_id='kafka_admin'
)

try:
    topic_list = [NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    print(f"Topic '{TOPIC_NAME}' created successfully.")
except TopicAlreadyExistsError:
    print(f"Topic '{TOPIC_NAME}' already exists.")
except Exception as e:
    print(f"Error creating topic: {e}")

# ----------------------------
# Initialize Kafka Producer
# ----------------------------
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# ----------------------------
# Sample data templates
# ----------------------------
users = ["Alice", "Bob", "Charlie", "David", "Eva"]
actions = ["login", "logout", "purchase", "view", "click"]

def generate_message():
    """Generate a random message"""
    msg = {
        "user_id": random.randint(1, 100),
        "name": random.choice(users),
        "action": random.choice(actions),
        "amount": round(random.uniform(10, 500), 2) if random.random() < 0.3 else None,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return msg

# ----------------------------
# Produce messages continuously
# ----------------------------
try:
    print(f"Producing messages to Kafka topic '{TOPIC_NAME}' at broker {KAFKA_BROKER}...")
    while True:
        message = generate_message()
        producer.send(TOPIC_NAME, value=message)
        print(f"Sent: {message}")
        time.sleep(random.uniform(0.5, 2.0))  # adjustable delay between messages

except KeyboardInterrupt:
    print("Stopping producer...")
finally:
    producer.flush()
    producer.close()
    admin_client.close()
