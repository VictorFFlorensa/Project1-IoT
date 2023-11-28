import paho.mqtt.publish as publish
from kafka import KafkaProducer
import random
import os
import time
import json
import signal
import sys
from time import sleep

#Environment variables
mqtt_host = os.environ.get("mqtt")
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")

#Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)

#Verificar conexión con el broker de Kafka
def wait_for_kafka():
    max_retries = 10
    retries = 0
    while retries < max_retries:
        try:
            producer = KafkaProducer(bootstrap_servers=[kafka_url])
            producer.close()
            break
        except Exception as e:
            print(f"Kafka no disponible, esperando... ({e})")
            retries += 1
            sleep(5)

    if retries == max_retries:
        print("No se pudo conectar a Kafka después de varios intentos. Saliendo...")
        exit(1)

def presence_value():
    return random.uniform(-10, 110)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)
    #Wait for kafka to start sending messages by mqtt
    wait_for_kafka()
    sleep(5)

    message_id = 0
    while True:
        data = {
            'messageID': message_id,
            'presence': presence_value(),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        #Convert the dictionary to a JSON string
        payload = json.dumps(data)

        #Publish 
        topic = 'presence-sensor'
        publish.single(topic, payload, hostname=mqtt_host)
        print(f"Published {payload} on topic {topic}")

        message_id += 1
        sleep(1)
                

