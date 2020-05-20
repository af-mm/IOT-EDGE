import argparse
import uuid
import os
import signal
import json
import hashlib
import paho.mqtt.client as mqtt
from confluent_kafka import Consumer, Producer
import map

args = argparse.ArgumentParser(description='Kafka MQTT connector')
args.add_argument('-KH', '--kafka_host', help='Kafka host name (default = localhost)', default='localhost')
args.add_argument('-KP', '--kafka_port', help='Kafka port (default = 9092)', type=int, default=9092)
args.add_argument('-KG', '--kafka_group_id', help='Kafka group id (default = random uuid)', default=uuid.uuid1())
args.add_argument('-MH', '--mqtt_host', help='Mqtt host name (default = localhost)', default='localhost')
args.add_argument('-MP', '--mqtt_port', help='Mqtt port (default = 1883)', type=int, default=1883)
args.add_argument('--use_env', help='use environment values (default = False)', action='store_true')
args.add_argument('kafka_input_topic', help='kafka input topic')
args.add_argument('kafka_output_topic', help='kafka output topic')
args = args.parse_args()

if args.use_env:
    args.kafka_host = os.getenv('KMC_KAFKA_HOST', args.kafka_host)
    args.kafka_port = os.getenv('KMC_KAFKA_PORT', args.kafka_port)
    args.kafka_group_id = os.getenv('KMC_KAFKA_GROUP_ID', args.kafka_group_id)
    args.mqtt_host = os.getenv('KMC_MQTT_HOST', args.mqtt_host)
    args.mqtt_port = int(os.getenv('KMC_MQTT_PORT', args.mqtt_port))
    args.kafka_input_topic = os.getenv('KMC_KAFKA_INPUT_TOPIC', args.kafka_input_topic)
    args.kafka_output_topic = os.getenv('KMC_KAFKA_OUTPUT_TOPIC', args.kafka_output_topic)

print()
print('----------------------------------------')
print('Args: {}'.format(args))

c = Consumer({
    'bootstrap.servers': '{}:{}'.format(args.kafka_host, args.kafka_port),
    'group.id': args.kafka_group_id
})
c.subscribe([args.kafka_input_topic, ])

p = Producer({
    'bootstrap.servers': '{}:{}'.format(args.kafka_host, args.kafka_port)
})

MQTT_MSG_QUEUE = []
MQTT_MSG_CACHE = set()

def getMessageHash(topic, message):
    return hashlib.md5('{}:{}'.format(topic, message).encode('utf-8')).hexdigest()

def on_connect(client, userdata, flags, rc):
    print('Mqtt connected with result code {}'.format(rc))
    
    client.subscribe([('#', 0)])
    
def on_message(client, userdata, message):
    global MQTT_MSG_CACHE
     
    topic = message.topic
    payload = message.payload.decode('utf8')
                
    h = getMessageHash(topic, payload)
    if h in MQTT_MSG_CACHE:
        MQTT_MSG_CACHE.remove(h)
    else:
        print('IN MQTT: {}: {}'.format(topic, payload))
        
        MQTT_MSG_QUEUE.append((topic, payload))

mqttClient = mqtt.Client();
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.connect( args.mqtt_host,
                    args.mqtt_port,
                    60)

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
        mqttClient.loop(0.001)
        
        if len(MQTT_MSG_QUEUE) > 0:
            for m in MQTT_MSG_QUEUE:
                mqttTopic, mqttMessage = m
                
                if mqttTopic not in map.BACKWARD_MAP:
                    continue
                
                d = {
                    'uuid': map.BACKWARD_MAP[mqttTopic]['uuid'],
                    'actions': {
                        map.BACKWARD_MAP[mqttTopic]['action']: mqttMessage
                    }                    
                }
                d = json.dumps(d, separators=(',',':'))
                
                p.produce(args.kafka_output_topic, value=d)
                p.flush()
                
                print('OUT KAFKA: {}: {}'.format(args.kafka_output_topic, d))
                
            MQTT_MSG_QUEUE = []
        
        msg = c.poll(0.001)
        if msg is None:
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
        else:
            topic = msg.topic()
#             key = msg.key()
            payload = msg.value().decode('utf-8')
            
            print('IN KAFKA: {} -> {}'.format(topic, payload))
            
            try:
                d = json.loads(payload)
                
                if 'uuid' not in d:
                    raise Exception('json does not contain "uuid" field')
                if 'actions' not in d:
                    raise Exception('json does not contain "actions" field')
                
            except BaseException as e:
                print('Given message is incorrect json: {}'.format(e))
                continue
            
            if d['uuid'] not in map.FORWARD_MAP:
                print('OUT MQTT: -> X')
                continue
                
            for actionName in d['actions']:
                try:
                    if actionName not in map.FORWARD_MAP[d['uuid']]:
                        raise Exception('Given action name not supported')
                    
                    mqttTopic = map.FORWARD_MAP[d['uuid']][actionName]
                    mqttMessage = d['actions'][actionName]
                    
                    mqttClient.publish(mqttTopic, mqttMessage)
                    
                    MQTT_MSG_CACHE.add(getMessageHash(mqttTopic, mqttMessage))
                    
                    print('OUT MQTT: {}: {}'.format(mqttTopic, mqttMessage))
                except BaseException as e:
                    print('uuid = {}, action = {}, error = {}'.format(d['uuid'], actionName, e))
            
except KeyboardInterrupt:
    print('KeyboardInterrupt caught')
finally:
    c.close()
