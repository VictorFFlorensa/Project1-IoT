import paho.mqtt.subscribe as subscribe
import os
from time import sleep
import json
import signal
import sys

#Environment Variables
host = os.environ.get("MQTT_HOST")

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)

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


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)
    print("Starting...")

    current_temperature = 20
    topic = "heat-pump"
    subscribe.callback(on_message_print, topic, hostname=host) 

    while True:   
        sleep(1)


