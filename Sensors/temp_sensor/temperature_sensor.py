import paho.mqtt.publish as publish
import random
import os
import time
import json

def temperature_sensor():
    return random.uniform(15, 30)

def get_user_name(name):
    parts = name.split("_")
    filtered_name = parts[0]
    return filtered_name

host = os.environ.get("mqtt")
print(f"MQTT Broker Host: {host}")
user = get_user_name(host)
topic = f"{user}/temperature_sensor"

while True:
    data = {
        'presence': temperature_sensor(),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    #Convert the dictionary to a JSON string
    payload = json.dumps(data)
    publish.single(topic, payload, hostname=host)
    print(f"Published {payload} on topic {topic}")
    time.sleep(1)


