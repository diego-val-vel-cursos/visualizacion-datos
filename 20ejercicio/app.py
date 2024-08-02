from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import plotly.graph_objects as go
import numpy as np

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Generar datos aleatorios
    x = np.arange(100)  # Generar 100 puntos de datos
    y = np.random.randn(100).cumsum()  # Generar valores Y aleatorios acumulativos

    # Crear trace
    trace = go.Scatter(x=x, y=y, mode='lines+markers')

    # Crear la figura y añadir el trace
    fig = go.Figure(trace)

    # Personalizar el layout
    fig.update_layout(title='Evolución Temporal Aleatoria',
                      xaxis_title='Tiempo',
                      yaxis_title='Valor Acumulado')

    # Generar HTML para el gráfico
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return f"<html><body>{graph_html}</body></html>"
