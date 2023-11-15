import paho.mqtt.publish as publish
import random
import os
import time
import json

def temperature_sensor():
    return random.uniform(15, 30)

host = os.environ.get("mqtt")
user = os.environ.get("user")
topic = f"{user}/temperature"

while True:
    data = {
        'temperature': temperature_sensor(),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    #Convert the dictionary to a JSON string
    payload = json.dumps(data)

    #Publish
    publish.single(topic, payload, hostname=host)
    print(f"Published {payload} on topic {topic}")
    time.sleep(1)


