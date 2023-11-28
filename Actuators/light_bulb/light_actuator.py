import paho.mqtt.client as mqtt
import os
from time import sleep
import json
import signal
import sys

mqtt_username = "user1"
mqtt_password = "password1"

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGTERM, on_exit)

host = os.environ.get("mqtt")

# Espera 10 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

light_bulb_state = 0
topic = "light-bulb"

def on_connect(client : mqtt.Client, userdata, flags, rc):
    print(f"Conectado con código {rc}")
    client.subscribe(topic, 0)

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

client = mqtt.Client()
client.username_pw_set(mqtt_username, password = mqtt_password)
client.on_connect = on_connect
client.on_message = on_message_actuate_light_bulb

print("Starting...")

client.connect(host, 1883, 60)
client.loop_forever()
