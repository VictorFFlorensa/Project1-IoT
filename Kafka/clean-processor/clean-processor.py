from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient
import json
import os
from time import sleep
from json import loads
import signal
import sys

#Environment variables
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")


# Manejar finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)

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

    topics = ['raw_data']
    consumer = KafkaConsumer(*topics, bootstrap_servers=[kafka_url], value_deserializer=lambda x: loads(x.decode('utf-8')), group_id="clean")
    producer = KafkaProducer(bootstrap_servers=kafka_url, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    print("Starting...")
    for message in consumer:
        data = message.value

        sensor_type = 'temperature' if 'temperature' in data else 'presence'
        sensor_value = data[sensor_type]

        if (sensor_type == 'temperature' and 18 <= sensor_value <= 28) or (sensor_type == 'presence' and 0 <= sensor_value <= 100):
            data['is_cleaned'] = True
            print("Sended-Message: ", data)
            if (topic_exists('clean_data')):
                producer.send('clean_data', value=data)