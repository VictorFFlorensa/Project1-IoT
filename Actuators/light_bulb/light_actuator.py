import paho.mqtt.subscribe as subscribe
import os
from time import sleep
import json

host = os.environ.get("mqtt")

# Espera 10 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

light_bulb_state = 0

def on_message_actuate_light_bulb(client, userdata, message):
    global light_bulb_state
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    presence_value = data.get('presence')

    if presence_value is not None:
        if presence_value > 50 and light_bulb_state == 0:
            light_bulb_state = 1
            print(f"Light Bulb state: {'ON' if light_bulb_state else 'OFF'}, because presence_value: {presence_value}")

        elif presence_value <= 50 and light_bulb_state == 1:
            light_bulb_state = 0
            print(f"Light Bulb state: {'ON' if light_bulb_state else 'OFF'}, because presence_value: {presence_value}")
    else:
        raise ValueError("Received presence value is None. Cannot process.")

print("Starting...")
while True:
    topic = "light-bulb"
    subscribe.callback(on_message_actuate_light_bulb, topic, hostname=host)
    sleep(1)
