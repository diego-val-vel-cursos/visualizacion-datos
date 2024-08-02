import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from kafka import KafkaConsumer
import matplotlib.dates as mdates
from datetime import datetime

# Configuración inicial del gráfico
plt.ion()
fig, ax = plt.subplots()
plt.title('Real-Time Temperature Data with Moving Average')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.grid(True)

# Iniciar el consumidor Kafka
consumer = KafkaConsumer(
    'temperature_topic_two',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

timestamps = []
temperatures = []
window_size = 5

def calculate_moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size), 'valid') / window_size

def plot_data(timestamps, temperatures, moving_avg):
    ax.clear()
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.plot(timestamps, temperatures, label='Temperature', marker='o', color='blue')
    if len(temperatures) >= window_size:
        ax.plot(timestamps[window_size-1:], moving_avg, label='Moving Average', linestyle='--', color='red')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.draw()
    plt.pause(0.01)
    fig.savefig('/consumer/ejercicio16/temperature_plot.png')

for message in consumer:
    data = message.value
    print(f"Received data: {data}")  # Imprime los datos recibidos para seguimiento
    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
    temperature = data['temperature']
    
    timestamps.append(timestamp)
    temperatures.append(temperature)
    
    if len(temperatures) >= window_size:
        moving_avg = calculate_moving_average(temperatures, window_size)
        plot_data(timestamps, temperatures, moving_avg)

plt.ioff()
plt.show()
