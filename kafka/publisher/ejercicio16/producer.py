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
    
    sensor_id = "sensor_001"

    while True:  # Ciclo infinito para simular un flujo de datos continuo
        temperature = random.uniform(20.0, 30.0)  # Generar una temperatura aleatoria entre 20 y 30
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')  # Timestamp actual
        data = {"timestamp": timestamp, "sensor_id": sensor_id, "temperature": temperature}
        
        producer.send('temperature_topic_two', value=data)
        time.sleep(2.5)  # Espera 2.5 segundos antes de enviar el siguiente mensaje
        print(f"Sent data: {data}")  # Imprime los datos enviados para seguimiento

if __name__ == '__main__':
    produce_data()
