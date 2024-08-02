import logging
from kafka import KafkaConsumer

# Configuración del logging para ver la salida en los logs de Docker
logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer(
    'quickstart-events',  # Nombre del topic
    bootstrap_servers='kafka:9092',  # Nombre del servidor
    auto_offset_reset='earliest',  # Esto permite que el consumidor lea desde el inicio del topic
)

logging.info("Iniciando el consumidor...")

try:
    for message in consumer:
        # Imprimir el mensaje en los logs
        logging.info(f"Mensaje recibido: {message.value}")
except Exception as e:
    logging.error("Error al consumir mensajes", exc_info=True)
