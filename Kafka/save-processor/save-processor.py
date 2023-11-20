import json
import os
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from json import loads
from time import sleep
from validateData import get_fields

bucket = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
org = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
influx_url = os.environ.get("DOCKER_INFLUXDB_INIT_URL")
token = os.environ.get("DOCKER_INFLUXDB_INIT_TOKEN")
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")

# Espera 15 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

# Lista de tópicos a los que suscribirse (output for multiple topics not working for now)
topics = ['raw_data']
consumer = KafkaConsumer(*topics, bootstrap_servers=[kafka_url], value_deserializer=lambda x: loads(x.decode('utf-8')))

#Conectar a InfluxDB
client = InfluxDBClient(url=influx_url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

print("Starting...")
for message in consumer:
    result = get_fields(message.value)
    if result:
        user, sensor_type, sensor_value, boolean, timestamp = result

    p = Point("IOT_DATA")
    p.tag("isFiltered", boolean)
    p.tag("user", user)
    p.tag("sensor", sensor_type)
    p.field(sensor_type, sensor_value)
    p.time(timestamp)

    # Escribir el punto en la base de datos
    write_api.write(bucket="iotproject", record=p)

    # Mostrar por pantalla confirmación de envío
    print("Guardados los datos del tópico " + message.topic + " en InfluxDB.")


    