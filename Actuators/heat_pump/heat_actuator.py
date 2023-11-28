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

current_temperature = 20
topic = "heat-pump"

def on_connect(client : mqtt.Client, userdata, flags, rc):
    print(f"Conectado con código {rc}")
    client.subscribe(topic, 0)

def on_message_print(client, userdata, message):
    global current_temperature
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    received_temperature = data.get('temperature')

    if received_temperature is not None:
        if 18 <= received_temperature <= 20 and current_temperature==20:
            current_temperature = 24
            print(f"Heat Pump current_temperature: {current_temperature} °C, because received_temperature: {received_temperature}")

        elif 24 <= received_temperature <= 28 and current_temperature==24:
            current_temperature = 20
            print(f"Heat Pump current_temperature: {current_temperature} °C, because received_temperature: {received_temperature}")
    else:
        raise ValueError("Received temperature is None. Cannot process.")

client = mqtt.Client()
client.username_pw_set(mqtt_username, password = mqtt_password)
client.on_connect = on_connect
client.on_message = on_message_print

print("Starting...")

client.connect(host, 1883, 60)
client.loop_forever()