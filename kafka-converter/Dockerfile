FROM python:3.6

WORKDIR /kafka-converter

COPY src requirements.txt ./

RUN pip3 install -r requirements.txt

ENV KC_HOST=localhost \
	KC_PORT=9092 \
	KC_MAP=localhost \
	KC_TOPICS=9092
	
CMD [ "python3", "-u", "./kafka_converter.py", "0", "--use_env" ]
