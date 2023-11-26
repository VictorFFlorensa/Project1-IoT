import paho.mqtt.publish as publish
import random
import os
import time
import json
import signal
import sys
from time import sleep
host = os.environ.get("mqtt")

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)

signal.signal(signal.SIGTERM, on_exit)

def presence_value():
    return random.uniform(-10, 110)

sleep(12)
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
    publish.single(topic, payload, hostname=host)
    print(f"Published {payload} on topic {topic}")

    message_id += 1
    time.sleep(1)
                

