from time import sleep
from json import dumps
from kafka import KafkaProducer
import paho.mqtt.subscribe as subscribe
import os

# Espera 15 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

def on_message_print(client, userdata, message):
    #producer.send('temperature-topic', value=message)
    print("%s %s" % (message.topic, message.payload.decode("utf-8")))

def get_user_name(name):
    parts = name.split("_")
    filtered_name = parts[0]
    return filtered_name

host = os.environ.get("mqtt")
print(f"MQTT Broker Host: {host}")
user = get_user_name(host)
topic = f"{user}/+"

print("Starting...")
while True:
    subscribe.callback(on_message_print, topic, hostname=host)
    sleep(2)



