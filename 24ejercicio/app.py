import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

# Datos simulados
np.random.seed(10)
data = pd.DataFrame({
    "Area": np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], size=100),
    "Salud": np.random.normal(loc=80, scale=10, size=100),
    "Bacterias": np.random.poisson(lam=5, size=100),
    "Hongos": np.random.poisson(lam=3, size=100)
})

# Layout de la aplicación Dash
app.layout = html.Div([
    html.H1("Dashboard de Monitoreo de Plantíos"),
    dcc.Dropdown(
        id='area-dropdown',
        options=[{'label': i, 'value': i} for i in data['Area'].unique()],
        value='Norte',
        style={"width": "50%"}
    ),
    dcc.Slider(
        id='bacteria-threshold',
        min=0,
        max=10,
        step=1,
        value=5,
        marks={str(i): str(i) for i in range(11)}
    ),
    dcc.Graph(id='health-boxplot'),
    dcc.Graph(id='pathogens-heatmap')
])

# Callback para actualizar el boxplot de salud
@app.callback(
    Output('health-boxplot', 'figure'),
    Input('area-dropdown', 'value')
)
def update_health_boxplot(selected_area):
    filtered_data = data[data['Area'] == selected_area]
    fig = px.box(filtered_data, y='Salud', title="Distribución de la Salud del Plantío")
    return fig

# Callback para actualizar el heatmap de patógenos
@app.callback(
    Output('pathogens-heatmap', 'figure'),
    [Input('area-dropdown', 'value'),
     Input('bacteria-threshold', 'value')]
)
def update_pathogens_heatmap(selected_area, threshold):
    filtered_data = data[(data['Area'] == selected_area) & (data['Bacterias'] >= threshold)]
    # Asegurarse de que no hay datos con 'Bacterias' por debajo del umbral
    filtered_data = filtered_data[filtered_data['Bacterias'] >= threshold]
    fig = px.density_heatmap(
        filtered_data, 
        x='Bacterias', 
        y='Hongos', 
        title="Mapa de Calor de Patógenos"
    )
    # Solo mostrar los valores desde el umbral del slider hacia arriba
    fig.update_xaxes(range=[threshold, filtered_data['Bacterias'].max()])
    return fig

# Correr el servidor
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)
