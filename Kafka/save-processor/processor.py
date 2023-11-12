from kafka import KafkaConsumer, KafkaProducer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from time import sleep
import random
import time

# Espera 15 segundos para dar tiempo a que Kafka se inicie
print("Esperando a que Kafka se inicie...")
sleep(10)
consumer = KafkaConsumer('albert_temperature_sensor', bootstrap_servers='kafka:9092', value_deserializer=json.loads)
#producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Setup InfluxDB
bucket = "iotproject"
org = "udl"
url = "http://influxdb:8086"
token = "WyvjhFL01fiWmoxTGhm5zO6JoYqSbdki15Mid9NsRs4NsulPnQ3XWd7elgWWEP9nz8FPWFo4WXQw_lxj78C-SA=="
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


print("Starting...")
while True:
    value = random.uniform(20, 25)
    timeStamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Crear un nuevo punto
    p = Point("IOT_DATA")

    # Asignar timestamp específico
    p.time(timeStamp)

    # Agregar tags
    p.tag("data_type", "raw")
    p.tag("user", "albert")
    p.tag("sensor", "temperature")
    
    # Agregar el campo de temperatura
    p.field("value", value)

    # Escribir el punto en la base de datos
    write_api.write(bucket=bucket, record=p)

    # Mostrar por pantalla confirmación de envío
    print("%s %s" % ("temperature", value))
    sleep(1)


#for message in consumer:
    #print(f"Received message from topic {message.topic}: {str(message.value)}")
    