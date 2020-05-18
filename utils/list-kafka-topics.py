from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import sys
from config import CFG

if len(sys.argv) != 2:
    print('{} host:port'.format(sys.argv[0]))
    exit(0)

client = AdminClient({'bootstrap.servers': sys.argv[1]})

topics = client.list_topics().topics
print(topics)
print()

for topic in topics:
    print(topic)
