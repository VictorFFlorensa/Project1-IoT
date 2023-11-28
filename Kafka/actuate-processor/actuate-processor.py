from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient
import json
from time import sleep
import paho.mqtt.publish as publish
import os
import signal
import sys

#Environment variables
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")
albert_host = os.environ.get("mqtt_albert")
tiffany_host = os.environ.get("mqtt_tiffany")
dakota_host = os.environ.get("mqtt_dakota")
tommy_host = os.environ.get("mqtt_tommy")

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)

    #Lista de tópicos a los que suscribirse
    consumer = KafkaConsumer('clean_data', bootstrap_servers=kafka_url, value_deserializer=json.loads, group_id="actuate")
    
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

    