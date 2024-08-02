from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.graph_objects as go

app = FastAPI()

# Función para cargar o inicializar el DataFrame
def load_data():
    try:
        # Intenta cargar los datos desde un archivo CSV existente
        return pd.read_csv('data.csv', index_col=0)
    except FileNotFoundError:
        # Si el archivo no existe, crea un DataFrame vacío sin columnas predefinidas
        return pd.DataFrame()

data = load_data()  # Cargar datos al iniciar la aplicación

@app.get("/", response_class=HTMLResponse)
def get_heatmap():
    if data.empty:
        return "No data available"
    # Utilización de Figure y Layout para configurar y mostrar un mapa de calor
    fig = go.Figure(data=go.Heatmap(
        z=data.values,  # Trace: Heatmap usando los valores del DataFrame
        x=data.columns,  # Ejes X del Heatmap
        y=data.index     # Ejes Y del Heatmap
    ))
    # Configuración del Layout para personalizar el título del gráfico
    fig.update_layout(title='Mapa de Calor de Intensidades')
    return HTMLResponse(fig.to_html())

@app.post("/add-data/")
async def add_data(request: Request):
    new_data = await request.json()
    if 'row' not in new_data or 'column' not in new_data or 'value' not in new_data:
        raise HTTPException(status_code=400, detail="Data must include 'row', 'column', and 'value'")
    
    # Asegurar que la columna exista
    if new_data['column'] not in data.columns:
        data[new_data['column']] = pd.NA  # Añadir la columna si no existe

    # Actualizar los datos en el DataFrame
    data.loc[new_data['row'], new_data['column']] = new_data['value']
    
    # Guardar los cambios en el CSV, asegurando que no haya índices indeseados y el formato numérico sea consistente
    data.to_csv('data.csv', float_format='%.2f')

    return {"message": "Data added successfully"}

# Ruta adicional para verificar y recargar el DataFrame (útil para depuración o actualización manual)
@app.get("/reload-data/")
def reload_data():
    global data
    data = load_data()
    return {"message": "Data reloaded successfully"}
