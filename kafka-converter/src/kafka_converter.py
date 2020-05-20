import argparse
import uuid
import os
import signal
import json
from confluent_kafka import Consumer, Producer

args = argparse.ArgumentParser(description='Kafka converter')
args.add_argument('-H', '--host', help='host name (default = localhost)', default='localhost')
args.add_argument('-P', '--port', help='port (default = 9092)', type=int, default=9092)
args.add_argument('-G', '--group_id', help='group id (default = random uuid)', default=uuid.uuid1())
args.add_argument('-M', '--map', help='map table (default = empty table)')
args.add_argument('--use_env', help='use environment values (default = False)', action='store_true')
args.add_argument('topics', help='kafka topics', nargs='+')
args = args.parse_args()

if args.use_env:
    args.host = os.getenv('KC_HOST', args.host)
    args.port = os.getenv('KC_PORT', args.port)
    args.group_id = os.getenv('KC_GROUP_ID', args.group_id)
    args.map = os.getenv('KC_MAP', args.map)
    
    args.topics = []
    s = os.getenv('KC_TOPICS', '')
    s = s.replace(' ', '')
    args.topics = s.split(',')

import map
MAP = map.getMapByName(args.map)

print()
print('----------------------------------------')
print('Args: {}'.format(args))

c = Consumer({
    'bootstrap.servers': '{}:{}'.format(args.host, args.port),
    'group.id': args.group_id
})
c.subscribe(args.topics)

p = Producer({
    'bootstrap.servers': '{}:{}'.format(args.host, args.port)
})

print('Kafka converter started')
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
            
            print('IN: {} -> {}'.format(topic, payload))
            
            try:
                d = json.loads(payload)
                
                if 'uuid' not in d:
                    raise Exception('json does not contain "uuid" field')
                if 'actions' not in d:
                    raise Exception('json does not contain "actions" field')
                
            except BaseException as e:
                print('Given message is incorrect json: {}'.format(e))
                continue
            
            if d['uuid'] in MAP:
                mapEntry = MAP[d['uuid']]
            else:
                print('OUT: -> X')
                continue
            
            d['actions_tmp'] = {}
                
            for actionName in d['actions']:
                try:
                    if actionName not in mapEntry:
                        raise Exception('Given action name not supported')
                    
                    scope = {}
                    exec(mapEntry[actionName]['f'], scope)
                    if 'f' not in scope:
                        raise Exception('map function does not contain "f" function')
                    
                    d['actions'][actionName] = scope['f'](d['actions'][actionName])
                    
                    if d['actions'][actionName] is None:
                        raise Exception('map function returned None')
                    
                    d['actions_tmp'][actionName] = d['actions'][actionName]
                except BaseException as e:
                    print('uuid = {}, action = {}, error = {}'.format(d['uuid'], actionName, e))
            
            d['actions'] = d['actions_tmp']
            d.pop('actions_tmp')
            
            if len(d['actions']) == 0:
                continue
            else:
                d = json.dumps({'uuid': d['uuid'], 'actions': d['actions']}, separators=(',',':'))
                p.produce(mapEntry[actionName]['topic'], value=d)
                p.flush()
            
                print('OUT: {} -> {}'.format(mapEntry[actionName]['topic'], d))
            
except KeyboardInterrupt:
    print('KeyboardInterrupt caught')
finally:
    c.close()
