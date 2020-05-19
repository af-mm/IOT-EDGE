python3 utils/create-kafka-topics.py -P 29093 edge-0001-input edge-0001-output

python3 utils/create-kafka-topics.py -P 29092 edge-input edge-output
python3 utils/create-kafka-topics.py -P 29092 mqtt-input mqtt-output
python3 utils/create-kafka-topics.py -P 29092 modbus-input modbus-output

