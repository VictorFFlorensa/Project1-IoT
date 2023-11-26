import paho.mqtt.subscribe as subscribe
import os
from time import sleep
import json
host = os.environ.get("mqtt")

# Espera 10 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

current_temperature = 20

def on_message_print(client, userdata, message):
    global current_temperature
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    received_temperature = data.get('temperature')

    if received_temperature is not None:
        if 18 <= received_temperature <= 20 and current_temperature==24:
            current_temperature = 24
            print(f"Heat Pump current_temperature: {current_temperature} °C, because received_temperature: {received_temperature}")

        elif 24 <= received_temperature <= 28 and current_temperature==20:
            current_temperature = 20
            print(f"Heat Pump current_temperature: {current_temperature} °C, because received_temperature: {received_temperature}")
    else:
        raise ValueError("Received temperature is None. Cannot process.")

print("Starting...")
while True:
    topic = "heat-pump"
    subscribe.callback(on_message_print, topic, hostname=host)    
    sleep(1)


