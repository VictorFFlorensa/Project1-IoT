import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
import paho.mqtt.subscribe as subscribe
import os
host = os.environ.get("mqtt")
name = os.environ.get("user")
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")

# Espera 10 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

producer = KafkaProducer(bootstrap_servers=[kafka_url], value_serializer=lambda x: dumps(x).encode('utf-8'))

def on_message_print(client, userdata, message):
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    data['user'] = name
    data['is_cleaned'] = False
    topic = "raw_data"
    producer.send(topic, value=data)
    print("Enviado por %s %s" % ("raw_data", data))


print("Starting...")
while True:
    subscribe.callback(on_message_print, "+", hostname=host)    
    sleep(1)