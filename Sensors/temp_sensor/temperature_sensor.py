import paho.mqtt.publish as publish
import random
import os
import time
import json
host = os.environ.get("mqtt")
id = os.environ.get("sensor_id")

def temperature_sensor():
    return random.uniform(15, 30)

while True:
    data = {
        'sensorID' : id,
        'temperature': temperature_sensor(),
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    #Convert the dictionary to a JSON string
    payload = json.dumps(data)

    #Publish
    topic = 'mqtt_message'
    publish.single(topic, payload, hostname=host)
    print(f"Published {payload} on topic {id}")
    time.sleep(1)


