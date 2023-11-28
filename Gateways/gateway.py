import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient
import signal
import sys
import paho.mqtt.subscribe as subscribe
import os

#Import environment variables
host = os.environ.get("mqtt")
name = os.environ.get("user")
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")

#Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)


#Verificar que el topico ha sido creado
def topic_exists(topic):
    admin_client = KafkaAdminClient(bootstrap_servers=[kafka_url])
    max_retries = 5
    retries = 0

    while retries < max_retries:
        topic_metadata = admin_client.list_topics()
        if topic in topic_metadata:
            return True
        else:
            print(f"El tópico '{topic}' no existe. Esperando 2 segundos antes de volver a intentar.")
            sleep(2)
            retries += 1

    return False


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)
    if (topic_exists('raw_data')):

        producer = KafkaProducer(bootstrap_servers=[kafka_url], value_serializer=lambda x: dumps(x).encode('utf-8'))

        def on_message_print(client, userdata, message):
            payload = message.payload.decode('utf-8')
            data = json.loads(payload)
            data['user'] = name
            data['is_cleaned'] = False
            topic = 'raw_data'
            producer.send(topic, value=data)
            print("Enviado por %s %s" % ("raw_data", data))


        print("Starting...")
        subscribe.callback(on_message_print, ["temperature-sensor", "presence-sensor"], hostname=host)

        while True:
            sleep(1)