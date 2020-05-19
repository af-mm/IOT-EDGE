import argparse
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

args = argparse.ArgumentParser(description='Delete Kafka topics')
args.add_argument('-H', '--host', help='host name (default = localhost)', default='localhost')
args.add_argument('-P', '--port', help='port (default = 9092)', type=int, default=9092)
args.add_argument('topics', help='kafka topics to create', nargs='+')
args = args.parse_args()

client = AdminClient({'bootstrap.servers': '{}:{}'.format(args.host, args.port)})

fs = client.delete_topics(args.topics)

for topic, f in fs.items():
    try:
        f.result()
        print('Topic "{}" deleted'.format(topic))
    except Exception as e:
        print('Failed to delete topic "{}": {}'.format(topic, e))
