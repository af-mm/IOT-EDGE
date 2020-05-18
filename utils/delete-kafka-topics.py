import sys
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

if len(sys.argv) < 3:
    print('No topics given')
    print('{} host:port topic1 [topic2 [topic3]]'.format(sys.argv[0]))
    exit(0)

client = AdminClient({'bootstrap.servers': sys.argv[1]})

topics = sys.argv[2:]
fs = client.delete_topics(topics)

for topic, f in fs.items():
    try:
        f.result()
        print('Topic {} deleted'.format(topic))
    except Exception as e:
        print('Failed to delete topic {}: {}'.format(topic, e))
