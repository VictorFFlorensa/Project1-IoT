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



if __name__ == "__main__":
    # Crear los temas con la cantidad de particiones necesarias
    create_topic("raw_data", 3)
    create_topic("clean_data", 3)

    print("Fin del programa.")
