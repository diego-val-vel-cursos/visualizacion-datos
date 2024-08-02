from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

# Inicializar SparkSession
spark = SparkSession.builder.appName("WordCount").getOrCreate()

# Leer un texto grande
text_df = spark.read.text("/opt/spark-data/shakespeare.txt")

# Contar las palabras
word_counts = text_df.select(explode(split(text_df.value, "\s+")).alias("word")) \
                     .groupBy("word") \
                     .count() \
                     .orderBy("count", ascending=False)

# Mostrar los resultados
word_counts.show()

# Detener la sesión Spark
spark.stop()
