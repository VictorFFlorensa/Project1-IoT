import paho.mqtt.publish as publish
import random
import os
import time
import json
host = os.environ.get("mqtt")
id = os.environ.get("sensor_id")

def presence_value():
    return random.uniform(-10, 110)

while True:
    data = {
        'sensorID' : id,
        'presence': presence_value(),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    #Convert the dictionary to a JSON string
    payload = json.dumps(data)

    #Publish 
    topic = 'mqtt_message'
    publish.single(topic, payload, hostname=host)
    print(f"Published {payload} on topic {id}")
    time.sleep(1)
                

