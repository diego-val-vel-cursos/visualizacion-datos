from google.cloud import bigquery
from google.cloud.exceptions import NotFound

# Configuración del cliente de BigQuery
client = bigquery.Client.from_service_account_json('./curso-421022-82d660b515a8.json')

print('Iniciando la fase de extracción...')

'''
===
Phase 1: Extract
===
'''

# Consulta para extraer datos meteorológicos de la NOAA
weather_query = """
SELECT 
  stn,
  wban,
  date,
  temp,
  prcp,
  visib
FROM 
  `bigquery-public-data.noaa_gsod.gsod2020`
WHERE
  stn IN (SELECT DISTINCT stn FROM `bigquery-public-data.noaa_gsod.stations` WHERE state = 'TX')
LIMIT 1000
"""

# Consulta para extraer datos de solicitudes de servicios de Austin
incident_query = """
SELECT 
  complaint_description,
  latitude,
  longitude,
  status,
  created_date
FROM 
  `bigquery-public-data.austin_311.311_service_requests`
WHERE
  created_date BETWEEN '2020-01-01' AND '2020-12-31'
LIMIT 1000
"""

# Ejecutar las consultas y cargar los datos en DataFrames de pandas
weather_data = client.query(weather_query).result().to_dataframe()
incident_data = client.query(incident_query).result().to_dataframe()

print('Extracción completada.')

print('Iniciando la fase de carga...')

'''
===
Phase 2: Load
===
'''

# Definición de la referencia al dataset
dataset_id = 'elt_demo_dataset'
dataset_ref = client.dataset(dataset_id, project='curso-421022')

# Verifica si el dataset existe, si no, lo crea
try:
    client.get_dataset(dataset_ref)
    print("Dataset ya existe.")
except NotFound:
    # Crear el dataset si no existe
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client.create_dataset(dataset, timeout=30)
    print("Dataset creado.")

# Definición de las referencias a las tablas
weather_table_ref = dataset_ref.table('weather_data')
incident_table_ref = dataset_ref.table('incident_data')

# Crear las tablas si no existen
for table_ref in [weather_table_ref, incident_table_ref]:
    try:
        client.get_table(table_ref)
        print(f"Tabla {table_ref.table_id} ya existe.")
    except NotFound:
        schema = []
        if table_ref.table_id == 'weather_data':
            schema = [
                bigquery.SchemaField("stn", "STRING"),
                bigquery.SchemaField("wban", "STRING"),
                bigquery.SchemaField("date", "DATE"),
                bigquery.SchemaField("temp", "FLOAT"),
                bigquery.SchemaField("prcp", "FLOAT"),
                bigquery.SchemaField("visib", "FLOAT"),
            ]
        elif table_ref.table_id == 'incident_data':
            schema = [
                bigquery.SchemaField("complaint_description", "STRING"),
                bigquery.SchemaField("latitude", "FLOAT"),
                bigquery.SchemaField("longitude", "FLOAT"),
                bigquery.SchemaField("status", "STRING"),
                bigquery.SchemaField("created_date", "TIMESTAMP"),
            ]
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Tabla {table_ref.table_id} creada.")

# Carga de los DataFrames a BigQuery
client.load_table_from_dataframe(weather_data, weather_table_ref).result()
client.load_table_from_dataframe(incident_data, incident_table_ref).result()

print('Carga completada.')

print('Iniciando la fase de transformación...')

'''
===
Phase 3: Transform
===
'''

# Transformación usando SQL en BigQuery
transform_query = """
CREATE OR REPLACE TABLE elt_demo_dataset.transformed_data AS
SELECT 
  i.complaint_description,
  i.latitude,
  i.longitude,
  i.status,
  w.temp,
  w.prcp,
  w.visib
FROM 
  elt_demo_dataset.incident_data AS i
JOIN 
  elt_demo_dataset.weather_data AS w
ON 
  EXTRACT(DATE FROM i.created_date) = w.date
"""

# Ejecutar la consulta de transformación
client.query(transform_query).result()

print('Transformación completada.')
