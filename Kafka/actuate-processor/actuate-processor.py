from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient
import json
from time import sleep
import paho.mqtt.client as mqtt
import os
import signal
import sys

mqtt_username = "user-gateway"
mqtt_password = "pw-gateway"

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGTERM, on_exit)

#Environment variables
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")
albert_host = os.environ.get("mqtt_albert")
tiffany_host = os.environ.get("mqtt_tiffany")
dakota_host = os.environ.get("mqtt_dakota")
tommy_host = os.environ.get("mqtt_tommy")

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)

users = ['albert',
        'tiffany',
        'dakota',
        'tommy']

mqtt_host = {
    'albert': albert_host,
    'tiffany': tiffany_host,
    'dakota': dakota_host,
    'tommy': tommy_host
}

# usernames = {
#     -
# }

# passwords = {
#     -
# }

mqtt_clients = {
    user: mqtt.Client()
    for user in users
}
# #TODO
# mqtt_username ={
#     username: 
#     for username in usernames
# }
# #TODO
# mqtt_password = {
#     pw: 
#     for pw in passwords
# }

for user in users:
    client = mqtt_clients[user]
    client.username_pw_set(mqtt_username, password = mqtt_password)
    host = mqtt_host[user]
    client.connect(host, 1883, 60)

# Espera 10 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)


signal.signal(signal.SIGTERM, on_exit)

#Lista de tópicos a los que suscribirse
consumer = KafkaConsumer('clean_data', bootstrap_servers=kafka_url, value_deserializer=json.loads, group_id="actuate")
    
print("Starting...")

for message in consumer:
    data = message.value
    user = data.get('user')
    client = mqtt_clients[user]

    if 'temperature' in data:
        topic = 'heat-pump'
    else:
        topic = 'light-bulb'

    #Publish 
    payload = json.dumps(data)
    client.publish(topic, payload)
    print("Enviado por %s %s" % (topic, data))