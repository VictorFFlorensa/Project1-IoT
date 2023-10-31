from kafka import KafkaConsumer, KafkaProducer
import json
from time import sleep

# Espera 15 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(15)


consumer = KafkaConsumer('temperature-topic', bootstrap_servers='kafka:9092', value_deserializer=json.loads)
producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print("Starting...")
for message in consumer:
    temperature = message.value['temperature']
    if 18 <= temperature <= 27:
        print("Temperature processed: " + str(message.value['temperature']))
        producer.send('filtered-temperature-topic', value=message.value)
    else:
        print("Temperature discarded: " + str(message.value['temperature']))