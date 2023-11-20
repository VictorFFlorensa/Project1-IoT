from kafka import KafkaConsumer, KafkaProducer
import json
from time import sleep

# Espera 15 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(15)

consumer = KafkaConsumer('filtered-temperature-topic', bootstrap_servers='kafka:9092', value_deserializer=json.loads)
producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print("Starting...")
for message in consumer:
    temperature = message.value['temperature']

    # Calculate the comfort difference
    comfort_difference = 0
    if temperature < 20:
        comfort_difference = temperature - 20
    elif temperature > 25:
        comfort_difference = temperature - 25
    message.value['temperature'] = round(comfort_difference,2)

    print('Calculated comfort diff. for: ' + str(temperature))
    producer.send('comfort-difference-topic', value=message.value)
    