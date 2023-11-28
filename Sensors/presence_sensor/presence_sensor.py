import paho.mqtt.client as mqtt
import random
import os
import time
import json
import signal
import sys
from time import sleep

host = os.environ.get("mqtt")
mqtt_username = "user1"
mqtt_password = "password1"

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGTERM, on_exit)

def presence_value():
    return random.uniform(-10, 110)

sleep(12)
message_id = 0

client = mqtt.Client()
client.username_pw_set(mqtt_username, password = mqtt_password)
client.connect(host, 1883, 60)

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
    client.publish(topic, payload)
    print(f"Published {payload} on topic {topic}")

    message_id += 1
    time.sleep(1)
                

