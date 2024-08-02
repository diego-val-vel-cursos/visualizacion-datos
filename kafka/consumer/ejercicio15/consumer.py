import json
from kafka import KafkaConsumer
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Incluye un group_id y establece auto_offset_reset a 'latest'
consumer = KafkaConsumer(
    'temperature_topic',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Personalización adicional del gráfico
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(
    title_text='Monitor de Temperatura del Sensor',
    title_x=0.5,
    plot_bgcolor='rgba(230, 236, 245, 0.5)',
    margin=dict(l=20, r=20, t=50, b=20),
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ),
    showlegend=False,  # Oculta la leyenda si no es necesaria
    xaxis=dict(
        title_text='Fecha y Hora',
        showline=True,
        showgrid=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        title_text='Temperatura (°C)',
        showgrid=True,
        zeroline=False,
        showline=False,
        showticklabels=True,
    )
)

# Añadir cuadrícula y rango de temperatura
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink', range=[15, 35])

trace = go.Scatter(x=[], y=[], mode='lines+markers', name='Temperatura', marker=dict(color='RoyalBlue'))
fig.add_trace(trace, secondary_y=False)

def consume_data():
    global fig
    for message in consumer:
        data = message.value
        logging.info(f"Received message: {data}")

        x_new = list(fig.data[0].x) + [data['timestamp']]
        y_new = list(fig.data[0].y) + [data['temperature']]

        fig.data[0].x = tuple(x_new)
        fig.data[0].y = tuple(y_new)

        fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))

        if len(fig.data[0].x) > 20:
            fig.data[0].x = fig.data[0].x[-20:]
            fig.data[0].y = fig.data[0].y[-20:]

        fig.write_html('/consumer/ejercicio15/sensor_temperature.html')

if __name__ == '__main__':
    consume_data()
