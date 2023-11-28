import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
import signal
import sys
import paho.mqtt.client as mqtt
import os

#Import environment variables
host = os.environ.get("mqtt")
name = os.environ.get("user")
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")

mqtt_username = "user-gateway"
mqtt_password = "pw-gateway"

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGTERM, on_exit)

producer = KafkaProducer(bootstrap_servers=[kafka_url], value_serializer=lambda x: dumps(x).encode('utf-8'))

def on_connect(client : mqtt.Client, userdata, flags, rc):
     print(f"Conectado con código {rc}")
     client.subscribe([("temperature-sensor", 0), ("presence-sensor", 0)])

def on_message_print(client, userdata, message):
    print('Received')
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    data['user'] = name
    data['is_cleaned'] = False
    topic = "raw_data"
    producer.send(topic, value=data)
    print(f"Enviado por {topic} {data}")

client = mqtt.Client()
client.username_pw_set(mqtt_username, password = mqtt_password)
client.on_connect = on_connect
client.on_message = on_message_print

print("Starting...")

client.connect(host, 1883, 60)
client.loop_forever()
