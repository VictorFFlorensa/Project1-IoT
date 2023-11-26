import paho.mqtt.publish as publish
import random
import os
import time
import json
from time import sleep
import sys
import signal
host = os.environ.get("mqtt")

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)

signal.signal(signal.SIGTERM, on_exit)

def temperature_sensor():
    return random.uniform(15, 30)

sleep(12)
message_id = 0

while True:
    data = {
        'messageID': message_id,
        'temperature': temperature_sensor(),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Convert the dictionary to a JSON string
    payload = json.dumps(data)

    # Publish
    topic = 'temperature-sensor'
    publish.single(topic, payload, hostname=host)
    print(f"Published {payload} on topic {topic}")

    message_id += 1
    time.sleep(1)

