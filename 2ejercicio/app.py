from flask import Flask, send_file
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/plot')
def plot():
    # Generar datos aleatorios
    df = pd.DataFrame({
        'x': range(1, 101),
        'y': [i ** 0.5 for i in range(1, 101)]
    })

    # Crear una figura con Plotly
    fig = go.Figure(data=[go.Scatter(x=df['x'], y=df['y'], mode='lines+markers')])

    # Convertir la figura en PNG y enviar
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
