import paho.mqtt.publish as publish
import random
import os
import time
import json
from time import sleep
host = os.environ.get("mqtt")

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
    topic = 'mqtt_message'
    publish.single(topic, payload, hostname=host)
    print(f"Published {payload} on topic {message_id}")

    message_id += 1
    time.sleep(1)

