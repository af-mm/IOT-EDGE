FROM python:3.6

WORKDIR /kafka-mqtt-connector

COPY src requirements.txt ./

RUN pip3 install -r requirements.txt

ENV KMC_KAFKA_HOST=localhost \
	KMC_KAFKA_PORT=9092 \
	KMC_MQTT_HOST=localhost \
	KMC_MQTT_PORT=1883 \
	KMC_KAFKA_INPUT_TOPIC=test1 \
	KMC_KAFKA_OUTPUT_TOPIC=test2
	
CMD [ "python3", "-u", "./kafka_mqtt_connector.py", "0", "0", "--use_env" ]
