import sys
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

if len(sys.argv) < 3:
    print('No topics given')
    print('{} host:port topic1 [topic2 [topic3]]'.format(sys.argv[0]))
    exit(0)

client = AdminClient({'bootstrap.servers': sys.argv[1]})

newTopics = []
for i in range(2, len(sys.argv)):
    t = NewTopic(sys.argv[i], num_partitions=1, replication_factor=1)
    newTopics.append(t)

fs = client.create_topics(newTopics)

for topic, f in fs.items():
    try:
        f.result()
        print('Topic {} created'.format(topic))
    except Exception as e:
        print('Failed to create topic {}: {}'.format(topic, e))
