# select_from_postgres.py
from pyspark.sql import SparkSession

# Inicializar la sesión de Spark
spark = SparkSession.builder.appName("PostgresIntegration").getOrCreate()

# Configurar las propiedades de conexión a la base de datos
database_url = "jdbc:postgresql://spark-demo-database-1:5432/mydatabase"

properties = {
    "user": "postgres",
    "password": "securepassword",
    "driver": "org.postgresql.Driver"
}

# Leer datos de la base de datos PostgreSQL
df = spark.read.jdbc(database_url, "users", properties=properties)

# Mostrar los resultados de la consulta
df.show()

# Detener la sesión de Spark
spark.stop()
