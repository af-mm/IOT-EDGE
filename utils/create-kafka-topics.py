import argparse
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

args = argparse.ArgumentParser(description='Create Kafka topics')
args.add_argument('-H', '--host', help='host name (default = localhost)', default='localhost')
args.add_argument('-P', '--port', help='port (default = 9092)', type=int, default=9092)
args.add_argument('-N', '--num_partitions', help='number of partitions (default = 1)', type=int, default=1)
args.add_argument('-R', '--replication_factor', help='replication factor (default = 1)', type=int, default=1)
args.add_argument('topics', help='kafka topics to create', nargs='+')
args = args.parse_args()

client = AdminClient({'bootstrap.servers': '{}:{}'.format(args.host, args.port)})

newTopics = []
for topic in args.topics:
    t = NewTopic(topic, num_partitions=args.num_partitions, replication_factor=args.replication_factor)
    newTopics.append(t)
 
fs = client.create_topics(newTopics)
 
for topic, f in fs.items():
    try:
        f.result()
        print('Topic "{}" created'.format(topic))
    except Exception as e:
        print('Failed to create topic "{}": {}'.format(topic, e))
