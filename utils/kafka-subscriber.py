from confluent_kafka import Consumer
import json
import sys
import uuid

if len(sys.argv) < 3:
    print('No topics given')
    print('{} host:port topic1 [topic2 [topic3]]'.format(sys.argv[0]))
    exit(0)

client = Consumer({
    'bootstrap.servers': sys.argv[1],
    'group.id': uuid.uuid1()
})

client.subscribe(sys.argv[2:])

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
            payload = msg.value()
                        
            print('{}: {}'.format(topic, payload))
            try:
                print('json = {}'.format(json.loads(payload)))
            except:
                pass
            print()
except KeyboardInterrupt:
    pass
finally:
    client.close()
