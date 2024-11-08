import os
from kafka.admin import KafkaAdminClient
from kafka import KafkaConsumer, KafkaProducer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from json import loads
from time import sleep
import signal
import sys

#Environment variables
bucket = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
org = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
influx_url = os.environ.get("DOCKER_INFLUXDB_INIT_URL")
token = os.environ.get("DOCKER_INFLUXDB_INIT_TOKEN")
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")

#Manejar la finalización del programa
def on_exit(signum, frame):
    print("Programa detenido manualmente.")
    sys.exit(0)
    


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)
    
    #Lista de tópicos a los que suscribirse
    topics = ['clean_data','raw_data']
    consumer = KafkaConsumer(*topics, bootstrap_servers=[kafka_url], value_deserializer=lambda x: loads(x.decode('utf-8')), group_id="save")

    #Conectar a InfluxDB
    client = InfluxDBClient(url=influx_url, username=username, password=password, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    print("Starting...")
    for message in consumer:
        data = message.value
        user = data.get('user')
        sensor_type = data.get('temperature') and 'temperature' or data.get('presence') and 'presence'
        sensor_value = data[sensor_type]
        isCleaned = data.get('is_cleaned')
        timestamp = data.get('timestamp')

        p = Point("IOT_DATA")
        p.tag("isCleaned", isCleaned)
        p.tag("user", user)
        p.field(sensor_type, sensor_value)
        p.time(timestamp)

        # Escribir el punto en la base de datos
        write_api.write(bucket="iotproject", record=p)

        # Mostrar por pantalla confirmación de envío
        print("Guardados los datos en InfluxDB: ", message.value)