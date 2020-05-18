from confluent_kafka import Producer
import sys

if len(sys.argv) != 4:
    print('{} host:port topic payload'.format(sys.argv[0]))
    exit(0)

client = Producer({
    'bootstrap.servers': sys.argv[1]
})

topic = sys.argv[2]
payload = sys.argv[3]

client.produce(topic, value=payload)
client.flush()
