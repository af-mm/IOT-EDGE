import argparse
import uuid
import os
import signal
from confluent_kafka import Consumer, Producer

args = argparse.ArgumentParser(description='Kafka repeater')
args.add_argument('-HF', '--host_from', help='host name from (default = localhost)', default='localhost')
args.add_argument('-PF', '--port_from', help='port from (default = 9092)', type=int, default=9092)
args.add_argument('-GF', '--group_id_from', help='group id from (default = random uuid)', default=uuid.uuid1())
args.add_argument('-HT', '--host_to', help='host name to (default = localhost)', default='localhost')
args.add_argument('-PT', '--port_to', help='port to (default = 9092)', type=int, default=9092)
args.add_argument('--use_env', help='use environment values (default = False)', action='store_true')
args.add_argument('topic_from', help='kafka topic from', default='')
args.add_argument('topic_to', help='kafka topic to', default='')
args = args.parse_args()

if args.use_env:
    args.host_from = os.getenv('KR_HOST_FROM', args.host_from)
    args.port_from = os.getenv('KR_PORT_FROM', args.port_from)
    args.group_id_from = os.getenv('KR_GROUP_ID_FROM', args.group_id_from)
    args.host_to = os.getenv('KR_HOST_TO', args.host_to)
    args.port_to = os.getenv('KR_PORT_TO', args.port_to)
    args.topic_from = os.getenv('KR_TOPIC_FROM', args.topic_from)
    args.topic_to = os.getenv('KR_TOPIC_TO', args.topic_to)

if args.topic_from == args.topic_to:
    print('ERROR: topic_from cannot be equal to topic_to')
    exit(1)

c = Consumer({
    'bootstrap.servers': '{}:{}'.format(args.host_from, args.port_from),
    'group.id': args.group_id_from
})
c.subscribe([args.topic_from, ])

p = Producer({
    'bootstrap.servers': '{}:{}'.format(args.host_to, args.port_to)
})

print()
print('----------------------------------------')
print('Kafka repeater started')
print('Args: {}'.format(args))
print('----------------------------------------')
print()

isItRunning = True

def sigterm_handler(signal, frame):
    print('SIGTERM caught')
    
    global isItRunning
    isItRunning = False
    
signal.signal(signal.SIGTERM, sigterm_handler)

try:
    while isItRunning:
        msg = c.poll(0.1)
        if msg is None:
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
        else:
            topic = msg.topic()
#             key = msg.key()
            payload = msg.value().decode('utf-8')
            
            p.produce(args.topic_to, value=payload)
            p.flush()
            
            print('{} -> {}'.format(topic, args.topic_to))
            print(payload)
#             print()
            
except KeyboardInterrupt:
    print('KeyboardInterrupt caught')
finally:
    c.close()
