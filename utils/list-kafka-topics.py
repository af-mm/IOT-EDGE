import argparse
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

args = argparse.ArgumentParser(description='Create Kafka topics')
args.add_argument('-H', '--host', help='host name (default = localhost)', default='localhost')
args.add_argument('-P', '--port', help='port (default = 9092)', type=int, default=9092)
args = args.parse_args()

client = AdminClient({'bootstrap.servers': '{}:{}'.format(args.host, args.port)})

topics = client.list_topics().topics
print(topics)
print()

for topic in topics:
    print(topic)
