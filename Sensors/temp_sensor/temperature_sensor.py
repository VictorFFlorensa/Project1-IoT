import paho.mqtt.publish as publish
from kafka import KafkaProducer
import random
import os
import time
import json
from time import sleep
import sys
import signal

#Environment variables
mqtt_host = os.environ.get("mqtt")
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")

#Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)

def temperature_sensor():
    return random.uniform(15, 30)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)
    sleep(5)

    message_id = 0
    while True:
        data = {
            'messageID': message_id,
            'temperature': temperature_sensor(),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        #Convert the dictionary to a JSON string
        payload = json.dumps(data)

        #Publish
        topic = 'temperature-sensor'
        publish.single(topic, payload, hostname=mqtt_host)
        print(f"Published {payload} on topic {topic}")

        message_id += 1
        sleep(1)

