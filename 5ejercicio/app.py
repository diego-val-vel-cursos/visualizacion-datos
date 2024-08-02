from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
import plotly.io as pio
from datetime import datetime

app = FastAPI()

# Función auxiliar para aplicar el muestreo y calcular la media móvil
def prepare_data(df, sample_frac, window_size):
    df_sampled = df.sample(frac=sample_frac) if len(df) > 1000 else df
    df_sampled.sort_values('time', inplace=True)
    df_sampled['value_smooth'] = df_sampled['value'].rolling(window=window_size).mean()
    return df_sampled

@app.get("/optimized", response_class=HTMLResponse)
async def read_optimized():
    start_time = datetime.now()
    df = pd.read_csv('data_large.csv')

    # Aplicando muestreo y suavizado
    df_prepared = prepare_data(df, sample_frac=0.05, window_size=100)
    fig = px.line(df_prepared, x='time', y='value_smooth', title='Datos Optimizados (Muestreo y Suavizado)')

    graph_html = pio.to_html(fig, full_html=False)
    end_time = datetime.now()

    print(f"Optimized - Start: {start_time}, End: {end_time}, Duration: {end_time - start_time}")

    return f"""
    <html>
        <head>
            <title>Visualización Optimizada</title>
        </head>
        <body>
            <h1>Datos Optimizados (Muestreo y Suavizado)</h1>
            {graph_html}
        </body>
    </html>
    """

@app.get("/unoptimized", response_class=HTMLResponse)
async def read_unoptimized():
    start_time = datetime.now()
    df = pd.read_csv('data_large.csv')
    fig = px.line(df, x='time', y='value', title='Datos sin Optimización')

    graph_html = pio.to_html(fig, full_html=False)
    end_time = datetime.now()

    print(f"Unoptimized - Start: {start_time}, End: {end_time}, Duration: {end_time - start_time}")

    return f"""
    <html>
        <head>
            <title>Visualización sin Optimización</title>
        </head>
        <body>
            <h1>Datos sin Optimización</h1>
            {graph_html}
        </body>
    </html>
    """
