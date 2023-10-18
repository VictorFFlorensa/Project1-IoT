import paho.mqtt.publish as publish
import random

def temperature_sensor():
    return random.uniform(15, 30)

publish.single(f"Dakota/temperature",
               temperature_sensor(),
               hostname="localhost")


