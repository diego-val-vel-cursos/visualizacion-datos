from flask import Flask, send_file
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO
import random

app = Flask(__name__)

@app.route('/plot/<graph_type>')
def plot_graph(graph_type):
    # Generar datos aleatorios
    df = pd.DataFrame({
        'x': range(1, 101),
        'y': [random.randint(1, 100) for _ in range(1, 101)]
    })

    # Seleccionar el tipo de gráfica
    if graph_type == 'line':
        fig = go.Figure(data=[go.Scatter(x=df['x'], y=df['y'], mode='lines+markers', name='Line Graph')])
    elif graph_type == 'bar':
        fig = go.Figure(data=[go.Bar(x=df['x'], y=df['y'], name='Bar Graph')])
    elif graph_type == 'scatter':
        fig = go.Figure(data=[go.Scatter(x=df['x'], y=df['y'], mode='markers', name='Scatter Graph')])
    else:
        return "Unsupported graph type. Use 'line', 'bar', or 'scatter'.", 400

    # Configuraciones adicionales para la figura
    fig.update_layout(title=f'Random {graph_type.capitalize()} Graph',
                      xaxis_title='X Axis',
                      yaxis_title='Y Axis')

    # Convertir la figura a imagen PNG
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_bytes.seek(0)

    # Enviar la imagen como respuesta
    return send_file(img_bytes, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
