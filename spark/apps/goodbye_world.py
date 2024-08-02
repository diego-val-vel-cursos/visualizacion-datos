from pyspark.sql import SparkSession

# Inicializa una sesión Spark.
spark = SparkSession.builder.appName("GoodbyeWorld").getOrCreate()

# Crea un DataFrame con una sola columna y una sola fila con 'Adiós Mundo'.
df = spark.createDataFrame([("Adiós Mundo",)], ["despedida"])

# Muestra el DataFrame.
df.show()

# Detiene la sesión Spark.
spark.stop()
