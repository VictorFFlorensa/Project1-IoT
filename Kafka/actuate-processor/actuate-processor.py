from kafka import KafkaConsumer
import json
from time import sleep
import paho.mqtt.publish as publish
import os
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")
albert_host = os.environ.get("mqtt_albert")
tiffany_host = os.environ.get("mqtt_tiffany")
dakota_host = os.environ.get("mqtt_dakota")
tommy_host = os.environ.get("mqtt_tommy")

# Espera 10 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

consumer = KafkaConsumer('raw_data', bootstrap_servers=kafka_url, value_deserializer=json.loads)

print("Starting...")
for message in consumer:

    #Publish 
    data = message.value
    user = data.get('user')
    mqtt_host = {
        'albert': albert_host,
        'tiffany': tiffany_host,
        'dakota': dakota_host,
        'tommy': tommy_host
    }.get(user)

    topic = data.get('temperature') and 'heat-pump' or data.get('presence') and 'light-bulb'
    #publish.single(topic, payload, hostname=mqtt_host)