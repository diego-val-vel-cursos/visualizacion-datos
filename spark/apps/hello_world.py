from pyspark.sql import SparkSession

# Inicializa una sesión Spark.
spark = SparkSession.builder.appName("HelloWorld").getOrCreate()

# Crea un DataFrame con una sola columna y una sola fila con 'Hola Mundo'.
df = spark.createDataFrame([("Hola Mundo",)], ["saludo"])

# Muestra el DataFrame.
df.show()

# Detiene la sesión Spark.
spark.stop()
