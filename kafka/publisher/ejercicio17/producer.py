import json
import time
from kafka import KafkaProducer
from datetime import datetime
import random

def produce_data():
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    sensor_ids = ["sensor_001", "sensor_002", "sensor_003"]
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        for sensor_id in sensor_ids:
            temperature = random.uniform(20.0, 30.0)  # Generar una temperatura aleatoria entre 20 y 30
            data = {"timestamp": timestamp, "sensor_id": sensor_id, "temperature": temperature}
            producer.send('temperature_topic_three', value=data)
            print(f"Sent data: {data}")  # Imprime los datos enviados para seguimiento
        time.sleep(2.5)  # Espera 2.5 segundos antes de enviar el siguiente grupo de mensajes

if __name__ == '__main__':
    produce_data()
