import paho.mqtt.subscribe as subscribe
import os
from time import sleep
import json

# Espera 10 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)
host = os.environ.get("mqtt")

def on_message_actuate_light_bulb(client, userdata, message):
    light_bulb_state = 0
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    presence_value = data.get('presence')

    if presence_value is not None:
        if presence_value > 50:
            light_bulb_state = 1
        elif presence_value < -50:
            light_bulb_state = 0

    print(f"Light Bulb state: {'ON' if light_bulb_state else 'OFF'}")

print("Starting...")
while True:
    subscribe.callback(on_message_actuate_light_bulb, "+", hostname=host)
    sleep(1)