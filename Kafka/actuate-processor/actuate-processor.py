from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient
import json
from time import sleep
import paho.mqtt.publish as publish
import os
import signal
import sys

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

#Verificar conexión con el broker de Kafka
def wait_for_kafka():
    max_retries = 10
    retries = 0
    while retries < max_retries:
        try:
            producer = KafkaProducer(bootstrap_servers=[kafka_url])
            producer.close()
            break
        except Exception as e:
            print(f"Kafka no disponible, esperando... ({e})")
            retries += 1
            sleep(5)

    if retries == max_retries:
        print("No se pudo conectar a Kafka después de varios intentos. Saliendo...")
        exit(1)

#Verificar que el topico ha sido creado
def topic_exists(topic):
    admin_client = KafkaAdminClient(bootstrap_servers=[kafka_url])
    max_retries = 5
    retries = 0

    while retries < max_retries:
        topic_metadata = admin_client.list_topics()
        if topic in topic_metadata:
            return True
        else:
            print(f"El tópico '{topic}' no existe. Esperando 2 segundos antes de volver a intentar.")
            sleep(2)
            retries += 1

    return False


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)
    wait_for_kafka()
    if (topic_exists('clean_data')):

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

    