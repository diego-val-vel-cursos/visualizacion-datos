import pandas as pd
from google.cloud import bigquery
import matplotlib.pyplot as plt
import seaborn as sns

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

def plot_station_capacity(df):
    # Visualización del uso de bicicletas en función de la capacidad de la estación
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='average_docks', y='total_rentals')
    plt.title('Bike Rentals vs. Station Capacity')
    plt.xlabel('Average Number of Docks at Station')
    plt.ylabel('Total Number of Rentals')
    plt.savefig('./34ejercicio/station_capacity_usage.png')

if __name__ == '__main__':
    data = fetch_data()
    plot_station_capacity(data)
