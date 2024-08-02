from google.cloud import bigquery
import plotly.express as px

# Configuración del cliente de BigQuery
client = bigquery.Client.from_service_account_json('./curso-421022-82d660b515a8.json')

'''
===
Phase 4: Visualization
===
'''

# Obtener los datos transformados
transformed_data_query = "SELECT * FROM `curso-421022.elt_demo_dataset.transformed_data`"
transformed_data = client.query(transformed_data_query).result().to_dataframe()

# Crear un gráfico interactivo con Plotly
fig = px.scatter_mapbox(
    transformed_data,
    lat="latitude",
    lon="longitude",
    color="temp",
    size="prcp",
    hover_data=['complaint_description', 'status'],
    zoom=10,
    mapbox_style="carto-positron"
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html('./36ejercicio/incident_weather_map.html')
