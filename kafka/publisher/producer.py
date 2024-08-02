from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for _ in range(10):
    message = {'number': _}
    producer.send('quickstart-events', value=message)
    print(f'Mensaje enviado: {message}')
    time.sleep(1)

producer.flush()
