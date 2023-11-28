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



if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)
    print("Starting...")

    light_bulb_state = 0
    topic = "light-bulb"
    subscribe.callback(on_message_print, topic, hostname=host)

    while True:
        sleep(1)
