import json
import time
from kafka import KafkaProducer
from datetime import datetime
import random

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

zones = ['Norte', 'Sur', 'Este', 'Oeste']
sensor_ids = ['sensor_001', 'sensor_002', 'sensor_003']

while True:
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    zone = random.choice(zones)
    for sensor_id in sensor_ids:
        temperature = round(random.uniform(20.0, 30.0), 2)
        message = {
            'timestamp': timestamp,
            'sensor_id': sensor_id,
            'temperature': temperature,
            'zone': zone
        }
        producer.send('temperature_topic_by_zone_two', value=message)
        print(f"Produced: {message}")
        time.sleep(0.5)  # Wait for 0.5 second before next message
