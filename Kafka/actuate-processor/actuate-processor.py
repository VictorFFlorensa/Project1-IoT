from kafka import KafkaConsumer
import json
import paho.mqtt.publish as publish
import os
import signal
import sys

#Environment variables
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")
albert_host = os.environ.get("MQTT_ALBERT")
tiffany_host = os.environ.get("MQTT_TIFFANY")
dakota_host = os.environ.get("MQTT_DAKOTA")
tommy_host = os.environ.get("MQTT_TOMMY")

# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)

    #Lista de tópicos a los que suscribirse
    consumer = KafkaConsumer('clean_data', bootstrap_servers=kafka_url, value_deserializer=json.loads, group_id="actuate")
    
    print("Starting...")
    for message in consumer:

        data = message.value
        user = data.get('user')
        mqtt_host = {
            'albert': albert_host,
            'tiffany': tiffany_host,
            'dakota': dakota_host,
            'tommy': tommy_host
        }.get(user)

        if 'temperature' in data:
            topic = 'heat-pump'
        else:
            topic = 'light-bulb'

        #Publish 
        payload = json.dumps(data)
        publish.single(topic, payload, hostname=mqtt_host)
        print("Enviado por %s %s" % (topic, data))

    