import paho.mqtt.publish as publish
import random

def presence_sensor():
    return str(random.uniform(-10, 110))

publish.single(f"Albert/presence",
               presence_sensor(),
               hostname="localhost")


