from confluent_kafka import Consumer, Producer
import sys
import uuid

if len(sys.argv) != 5:
    print('{} hostFrom:portFrom topicFrom hostTo:portTo topicTo'.format(sys.argv[0]))
    exit(0)
    
hostFrom = sys.argv[1]
topicFrom = sys.argv[2]
hostTo = sys.argv[3]
topicTo = sys.argv[4]

c = Consumer({
    'bootstrap.servers': hostFrom,
    'group.id': uuid.uuid1()
})
c.subscribe([topicFrom, ])

p = Producer({
    'bootstrap.servers': hostTo
})

try:
    while True:
        msg = c.poll(0.1)
        if msg is None:
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
        else:
            topic = msg.topic()
#             key = msg.key()
            payload = msg.value()
            
            p.produce(topicTo, value=payload)
            p.flush()
            
            print('{} -> {}'.format(topic, topicTo))
            print(payload)
            print()
            
except KeyboardInterrupt:
    pass
finally:
    c.close()
