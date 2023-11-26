from kafka import KafkaConsumer, KafkaProducer
import json
import os
from time import sleep
from json import loads
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")

# Espera 10 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

topics = ['raw_data']
consumer = KafkaConsumer(*topics, bootstrap_servers=[kafka_url], value_deserializer=lambda x: loads(x.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers=kafka_url, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print("Starting...")
for message in consumer:
    data = message.value

    sensor_type = 'temperature' if 'temperature' in data else 'presence'
    sensor_value = data[sensor_type]

    if (sensor_type == 'temperature' and 18 <= sensor_value <= 28) or (sensor_type == 'presence' and 0 <= sensor_value <= 100):
        data['is_cleaned'] = True
        print("Sended-Message: ", data)
        producer.send('clean_data', value=message.value)