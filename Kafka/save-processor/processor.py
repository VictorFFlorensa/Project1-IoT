from kafka import KafkaConsumer, KafkaProducer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from time import sleep
import asyncio

# Espera 15 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)

# Lista de tópicos a los que suscribirse (output not working for now)
topics = ['raw_albert_temperature', 'raw_albert_presence']
consumer = KafkaConsumer(*topics, bootstrap_servers='kafka:9092', value_deserializer=json.loads)

# Setup InfluxDB
bucket = "iotproject"
org = "udl"
url = "http://influxdb:8086"
token = "WyvjhFL01fiWmoxTGhm5zO6JoYqSbdki15Mid9NsRs4NsulPnQ3XWd7elgWWEP9nz8FPWFo4WXQw_lxj78C-SA=="
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
    

print("Starting...")
for message in consumer:
    # Crear un nuevo punto
    p = Point("IOT_DATA")

    # Agregar tags
    topic_parts = message.topic.split("_")
    p.tag("data_type", topic_parts[0])
    p.tag("user", topic_parts[1])
    p.tag("sensor", topic_parts[2])

    # Agregar los datos de temperatura o presencia y el timeStamp
    payload = json.loads(message.value)

    # Usar un sufijo en el campo "value" según el tipo de datos
    value_field_name = "value_temperature" if 'temperature' in payload else "value_presence"
    
    p.field(value_field_name, payload.get('temperature') or payload.get('presence'))
    p.time(payload['timestamp'])

    # Escribir el punto en la base de datos
    write_api.write(bucket=bucket, record=p)

    # Mostrar por pantalla confirmación de envío
    print("Guardados los datos del tópico " + message.topic + " en InfluxDB.")


    