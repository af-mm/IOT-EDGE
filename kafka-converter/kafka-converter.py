from confluent_kafka import Consumer, Producer
import sys
import uuid
import json
import paho.mqtt.client as mqtt

if len(sys.argv) != 3:
    print('{} host:port topic'.format(sys.argv[0]))
    exit(0)
    
host = sys.argv[1]
topic = sys.argv[2]

c = Consumer({
    'bootstrap.servers': host,
    'group.id': uuid.uuid1()
})
c.subscribe([topic, ])

# p = Producer({
#     'bootstrap.servers': host
# })


map = {
    'device-0001' : {
        'light1': '''
def f(d):
    if ('a' in d) and ('b' in d) and ('c' in d):
        return '{},{},{}'.format(d['a'], d['b'], d['c'])
    return d
                ''',


        'light2': '''
def f(d):
    if ('a' in d) and ('b' in d) and ('c' in d):
        return '{},{},{}'.format(d['c'], d['b'], d['a'])
    return d
                '''
    }
}

mqttMap = {
    'device-0001' : {
        'light1': 'l001/light1',
        'light2': 'l001/light2'
    }
}

externalClient = mqtt.Client();
externalClient.connect('localhost', 1024, 60)


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
            
            try:
                d = json.loads(payload)
            except:
                continue
            
            if 'uuid' in d and 'actions' in d:
                uuid = d['uuid']
                actions = d['actions']
                
                if uuid in map:
                    for name in actions:
                        if name in map[uuid]:
                            vars = {}
                            exec(map[uuid][name], vars)
                            
                            if 'f' in vars:
                                r = vars['f'](actions[name])
                                
                                if r != None:
                                    externalClient.publish(mqttMap[uuid][name], json.dumps(r))
            
            
            
            
#             p.produce('mqtt_input', value=payload)
#             p.flush()
#             
#             print('{} -> {}'.format(topic, topicTo))
#             print(payload)
#             print()
            
except KeyboardInterrupt:
    pass
finally:
    c.close()
