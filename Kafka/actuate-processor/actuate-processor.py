from kafka import KafkaConsumer
import json
from time import sleep
import paho.mqtt.publish as publish
import os
import signal
import sys

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)

signal.signal(signal.SIGTERM, on_exit)
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

    data = message.value
    user = data.get('user')
    mqtt_host = {
        'albert': albert_host,
        'tiffany': tiffany_host,
        'dakota': dakota_host,
        'tommy': tommy_host
    }.get(user)

    if 'temperature' in data:
        topic = 'heat-pump'
    else:
        topic = 'light-bulb'

    #Publish 
    payload = json.dumps(data)
    publish.single(topic, payload, hostname=mqtt_host)
    print("Enviado por %s %s" % (topic, data))

    