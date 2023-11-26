import paho.mqtt.subscribe as subscribe
import random
import os
from time import sleep
import json
host = os.environ.get("mqtt")


state = "ON"

def on_message_print(client, userdata, message):
    #change state

print("Starting...")
while True:
    subscribe.callback(on_message_print, "+", hostname=host)    
    sleep(1)


