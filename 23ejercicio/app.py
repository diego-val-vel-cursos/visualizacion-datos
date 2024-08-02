import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Inicialización de la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Generación de datos aleatorios
def generate_data(n_points=30):
    x = np.linspace(0, 10, n_points)
    y = np.sin(x) + np.random.normal(size=n_points)
    df = pd.DataFrame({
        "x": x,
        "y": y
    })
    return df

# Layout de la aplicación
app.layout = html.Div([
    dcc.Graph(id='live-graph', style={"height": "60vh"}),
    dcc.Slider(
        id='data-slider',
        min=10,
        max=100,
        step=5,
        value=30,
        marks={str(n): str(n) for n in range(10, 101, 10)}
    ),
    html.Div(id='slider-output-container')
])

# Callback para actualizar el gráfico
@app.callback(
    Output('live-graph', 'figure'),
    Input('data-slider', 'value')
)
def update_graph(data_points):
    df = generate_data(n_points=data_points)
    fig = px.line(df, x="x", y="y", title="Gráfico Dinámico")
    return fig

# Correr el servidor
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)
