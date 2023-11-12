import paho.mqtt.publish as publish
import random
import os
import time
import json

# TODO: Data must be reported ON CHANGE, not necessarily every reading

def presence_sensor():
    return str(random.uniform(-10, 110))

def get_user_name(name):
    parts = name.split("_")
    filtered_name = parts[0]
    return filtered_name

host = os.environ.get("mqtt")
print(f"MQTT Broker Host: {host}")
user = get_user_name(host)
topic = f"{user}/presence_sensor"

while True:
    data = {
        'value': presence_sensor(),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'source': "presence"
    }
    #Convert the dictionary to a JSON string
    payload = json.dumps(data)
    publish.single(topic, payload, hostname=host)
    print(f"Published {payload} on topic {topic}")
    time.sleep(1)