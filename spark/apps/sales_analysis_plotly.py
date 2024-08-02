from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg
import plotly.express as px

# Iniciar la sesión Spark
spark = SparkSession.builder \
    .master("spark://spark-master:7077") \
    .appName("SalesDataAnalysisPlotly") \
    .getOrCreate()

# Leer el archivo de datos
df = spark.read.csv('/opt/spark-data/sales_data.csv', header=True, inferSchema=True)
df.show()

# Preprocesamiento de los datos (eliminación de valores nulos y filtrado)
df_clean = df.dropna()

# Análisis Exploratorio
# Suma total de ventas por producto
total_sales = df_clean.groupBy("Product").agg(sum("Quantity").alias("Total Sold"))
total_sales.show()

# Precio promedio por producto
avg_price = df_clean.groupBy("Product").agg(avg("Price").alias("Average Price"))
avg_price.show()

# Convertir Spark DataFrame a Pandas DataFrame para visualización
total_sales_pd = total_sales.toPandas()
avg_price_pd = avg_price.toPandas()

# Visualización con Plotly: Total de ventas por producto
fig_sales = px.bar(total_sales_pd, x='Product', y='Total Sold', title='Total Sales by Product',
                   color='Product', template='plotly_dark', text='Total Sold')
fig_sales.update_layout(
    title_text='Total Sales by Product',
    title_x=0.5,
    xaxis_title="Product",
    yaxis_title="Units Sold",
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_sales.write_html('/opt/spark-data/total_sales_output.html')

# Visualización con Plotly: Precio promedio por producto
fig_avg_price = px.bar(avg_price_pd, x='Product', y='Average Price', title='Average Price by Product',
                       color='Product', template='plotly_dark', text='Average Price')
fig_avg_price.update_layout(
    title_text='Average Price by Product',
    title_x=0.5,
    xaxis_title="Product",
    yaxis_title="Average Price ($)",
    plot_bgcolor='rgba(0,0,0,0)'
)
fig_avg_price.write_html('/opt/spark-data/avg_price_output.html')

# Detener la sesión de Spark
spark.stop()
