import json
from kafka import KafkaConsumer
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import datetime

# Iniciar el consumidor Kafka
consumer = KafkaConsumer(
    'temperature_topic_three',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Configurar los colores de las trazas para cada sensor
colors = {
    'sensor_001': 'red',
    'sensor_002': 'green',
    'sensor_003': 'blue',
}

# Crear figuras para cada sensor
traces = {
    sensor_id: go.Scatter(
        x=[], y=[], mode='lines+markers', name=sensor_id, line={'color': color}
    ) for sensor_id, color in colors.items()
}

# Configuración inicial de la figura de Plotly
layout = go.Layout(
    title='Real-Time Temperature Data from Multiple Sensors',
    xaxis=dict(title='Time'),
    yaxis=dict(title='Temperature (°C)'),
    showlegend=True
)

fig = go.Figure(layout=layout)
for trace in traces.values():
    fig.add_trace(trace)

# Función para actualizar la figura con nuevos datos
def update_fig(sensor_id, timestamp, temperature):
    for i, trace in enumerate(fig.data):
        if trace.name == sensor_id:
            trace.x = trace.x + (timestamp,)
            trace.y = trace.y + (temperature,)
            break

# Bucle de lectura de mensajes
for message in consumer:
    data = message.value
    print(f"Received data: {data}")  # Imprimir el mensaje recibido en la consola

    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
    sensor_id = data['sensor_id']
    temperature = data['temperature']

    update_fig(sensor_id, timestamp, temperature)

    # Actualizar y guardar la figura
    plot(fig, filename='/consumer/ejercicio17/sensor_temperature.html', auto_open=False)
