import json
from kafka import KafkaProducer
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

def produce_data():
    with open('/publisher/ejercicio15/data.json', 'r') as file:
        data = json.load(file)
        for entry in data:
            producer.send('temperature_topic', value=entry)
            logging.info(f"Sent data: {entry}")  # Log del mensaje enviado
            producer.flush()  # Asegura que el mensaje se envía antes de continuar

if __name__ == '__main__':
    produce_data()
