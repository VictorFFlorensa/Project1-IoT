from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer
from kafka.errors import TopicAlreadyExistsError
import time
import os
kafka_url = os.environ.get("DOCKER_KAFKA_INIT_TOKEN")


def create_topic(topic, partitions):
    admin_client = KafkaAdminClient(bootstrap_servers=[kafka_url])

    # Verificar si el tema ya existe
    topic_metadata = admin_client.list_topics()
    topic_exists = topic in topic_metadata

    if not topic_exists:
        new_topic = NewTopic(name=topic, num_partitions=partitions, replication_factor=1)
        try:
            admin_client.create_topics(new_topics=[new_topic], validate_only=False)
            print(f"Tema '{topic}' creado con éxito.")
        except TopicAlreadyExistsError:
            print(f"Tema '{topic}' ya existe. No es necesario crearlo nuevamente.")
    else:
        print(f"Tema '{topic}' ya existe. No es necesario crearlo nuevamente.")


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
            time.sleep(5)

    if retries == max_retries:
        print("No se pudo conectar a Kafka después de varios intentos. Saliendo...")
        exit(1)


if __name__ == "__main__":
    # Esperar a que Kafka esté disponible antes de intentar crear temas
    wait_for_kafka()

    # Crear los temas con la cantidad de particiones necesarias
    create_topic("raw_data", 3)
    create_topic("clean_data", 3)

    print("Fin del programa.")
