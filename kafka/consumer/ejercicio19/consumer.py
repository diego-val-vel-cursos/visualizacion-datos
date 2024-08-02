import json
from kafka import KafkaConsumer
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime

# Inicialización del consumidor de Kafka
consumer = KafkaConsumer(
    'temperature_topic_by_zone_two',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Definir los colores para cada sensor
sensor_colors = {
    'sensor_001': 'red',
    'sensor_002': 'green',
    'sensor_003': 'blue',
}

# Configuración de las zonas
zones = ['Norte', 'Sur', 'Este', 'Oeste']

# Creación de la figura de Plotly con una fila y una columna por zona
fig = make_subplots(rows=1, cols=4, subplot_titles=zones)

# Agregar una traza por sensor en cada zona
for zone_index, zone in enumerate(zones, start=1):
    for sensor_id, color in sensor_colors.items():
        fig.add_trace(
            go.Scatter(
                x=[], 
                y=[], 
                mode='lines+markers', 
                name=f"{sensor_id} - {zone}",
                line=dict(color=color)
            ),
            row=1, 
            col=zone_index
        )

# Personalización de la figura
fig.update_layout(
    title='Real-Time Temperature Data from Multiple Sensors by Zone',
    xaxis_title='Time',
    yaxis_title='Temperature (°C)'
)

# Diccionario para almacenar los datos de los sensores
sensor_data = {(sensor_id, zone): {'x': [], 'y': []} for sensor_id in sensor_colors for zone in zones}

# Variable para contar mensajes y guardar el gráfico después de cierta cantidad
message_count = 0
save_every = 10

# Ruta del archivo de salida HTML
html_file = '/consumer/ejercicio19/temperature_by_zone.html'

for message in consumer:
    data = message.value
    print(f"Consumed: {data}")

    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
    sensor_id = data['sensor_id']
    temperature = data['temperature']
    zone = data['zone']

    # Agregar datos
    sensor_data[(sensor_id, zone)]['x'].append(timestamp)
    sensor_data[(sensor_id, zone)]['y'].append(temperature)

    # Encontrar la traza y actualizar los datos
    for trace in fig.data:
        if trace.name == f"{sensor_id} - {zone}":
            trace.x = sensor_data[(sensor_id, zone)]['x']
            trace.y = sensor_data[(sensor_id, zone)]['y']

    # Guardar el gráfico en formato HTML cada 'save_every' mensajes
    if message_count % save_every == 0:
        fig.write_html(html_file)

    message_count += 1
