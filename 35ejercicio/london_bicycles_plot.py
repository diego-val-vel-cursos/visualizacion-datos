import pandas as pd
from google.cloud import bigquery
import plotly.express as px

# Configuración del cliente de BigQuery
client = bigquery.Client.from_service_account_json('./curso-421022-82d660b515a8.json')

def fetch_data():
    query = """
    WITH station_usage AS (
        SELECT 
            h.start_station_name AS station_name,
            COUNT(h.rental_id) AS num_rentals,
            s.docks_count
        FROM `bigquery-public-data.london_bicycles.cycle_hire` h
        JOIN `bigquery-public-data.london_bicycles.cycle_stations` s
        ON h.start_station_id = s.id
        GROUP BY h.start_station_name, s.docks_count
    )
    SELECT 
        station_name,
        SUM(num_rentals) AS total_rentals,
        AVG(docks_count) AS average_docks
    FROM station_usage
    GROUP BY station_name
    ORDER BY total_rentals DESC
    LIMIT 1000
    """
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    return results

def plot_station_capacity_with_plotly(df):
    # Visualización interactiva con Plotly
    fig = px.scatter(df, x='average_docks', y='total_rentals',
                     hover_data=['station_name'], title='Bike Rentals vs. Station Capacity')
    fig.update_layout(
        title={
            'text': "Bike Rentals vs. Station Capacity",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Average Number of Docks at Station',
        yaxis_title='Total Number of Rentals'
    )
    fig.write_html('./35ejercicio/station_capacity_usage_interactive.html')

if __name__ == '__main__':
    data = fetch_data()
    plot_station_capacity_with_plotly(data)
