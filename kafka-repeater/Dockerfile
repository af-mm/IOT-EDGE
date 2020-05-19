FROM python:3.6

WORKDIR /kafka-repeater

COPY src requirements.txt ./

RUN pip3 install -r requirements.txt

ENV KR_HOST_FROM=localhost \
	KR_PORT_FROM=9092 \
	KR_GROUP_ID_FROM=123 \
	KR_HOST_TO=localhost \
	KR_PORT_TO=9092 \
	KR_TOPIC_FROM=0 \
	KR_TOPIC_TO=0
	
CMD [ "python3", "-u", "./kafka-repeater.py", "0", "0", "--use_env" ]
