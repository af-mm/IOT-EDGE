import argparse
from confluent_kafka import Producer

args = argparse.ArgumentParser(description='Kafka publisher')
args.add_argument('-H', '--host', help='host name (default = localhost)', default='localhost')
args.add_argument('-P', '--port', help='port (default = 9092)', type=int, default=9092)
args.add_argument('topic', help='Kafka topic')
args.add_argument('message', help='Kafka message')
args = args.parse_args()

client = Producer({
    'bootstrap.servers': '{}:{}'.format(args.host, args.port)
})

client.produce(args.topic, value=args.message)
client.flush()
