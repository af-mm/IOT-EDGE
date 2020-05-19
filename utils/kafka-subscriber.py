import argparse
import uuid
from confluent_kafka import Consumer
import json

args = argparse.ArgumentParser(description='Kafka subscriber')
args.add_argument('-H', '--host', help='host name (default = localhost)', default='localhost')
args.add_argument('-P', '--port', help='port (default = 9092)', type=int, default=9092)
args.add_argument('-G', '--group_id', help='group id (default = random uuid)', default=uuid.uuid1())
args.add_argument('topics', help='kafka topics to subscribe', nargs='+')
args = args.parse_args()

client = Consumer({
    'bootstrap.servers': '{}:{}'.format(args.host, args.port),
    'group.id': args.group_id
})

client.subscribe(args.topics)

try:
    while True:
        msg = client.poll(0.1)
        if msg is None:
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
        else:
            topic = msg.topic()
#             key = msg.key()
            payload = msg.value().decode('utf-8')
                        
            print('{}: {}'.format(topic, payload))
            try:
                print('json = {}'.format(json.loads(payload)))
            except:
                pass
#             print()
except KeyboardInterrupt:
    pass
finally:
    client.close()
