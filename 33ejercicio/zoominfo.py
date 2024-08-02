import pandas as pd
from google.cloud import bigquery
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración del cliente de BigQuery
client = bigquery.Client.from_service_account_json('./curso-421022-82d660b515a8.json')

def fetch_data():
    query = """
    SELECT ZI_C_STATE AS STATE, ZI_C_INDUSTRIES AS INDUSTRY, COUNT(*) as NUM_COMPANIES
    FROM `zoominfo-public.zi_dataset_companies_under_1000_employees_offering_tuition.zi-companies-under-1000-employees-offering-tuition`
    WHERE ZI_C_STATE IS NOT NULL
    GROUP BY ZI_C_STATE, ZI_C_INDUSTRIES
    ORDER BY NUM_COMPANIES DESC
    LIMIT 100
    """
    query_job = client.query(query)
    results = query_job.result().to_dataframe()
    return results

def plot_data(df):
    # Visualización de los datos
    plt.figure(figsize=(12, 8))
    bar_plot = sns.barplot(data=df, x='STATE', y='NUM_COMPANIES', hue='INDUSTRY', dodge=False)
    plt.title('Distribución de Empresas por Estado e Industria')
    plt.xlabel('Número de Empresas')
    plt.ylabel('Estado')
    plt.legend(title='Industria')
    
    # Rotar las etiquetas del eje X para que estén verticales
    bar_plot.set_xticklabels(bar_plot.get_xticklabels(), rotation=90)
    
    plt.tight_layout()
    plt.savefig('./33ejercicio/zoominfo_chart.png')

if __name__ == '__main__':
    data = fetch_data()
    plot_data(data)
