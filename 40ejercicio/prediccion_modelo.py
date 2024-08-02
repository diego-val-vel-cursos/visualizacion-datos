import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import joblib  # Para cargar el StandardScaler

# Cargar el modelo y el escalador guardados
model = load_model('./40ejercicio/modelo_tensorflow.h5')
scaler = joblib.load('./40ejercicio/scaler.pkl')

# Leer nuevos datos de productos
nuevos_datos = pd.read_csv('./40ejercicio/nuevos_productos.csv')
productos = nuevos_datos['Producto'].copy()

# Preprocesar los nuevos datos aplicando codificación en caliente
nuevos_datos = pd.get_dummies(nuevos_datos.drop(['Producto'], axis=1), columns=['Color'])

# Asegurar que solo las columnas que el modelo fue entrenado para ver están presentes
expected_columns = ['Peso', 'Color_blanco', 'Color_naranja', 'Color_amarillo', 'Color_verde']  # Ajustado a las columnas reales
nuevos_datos = nuevos_datos.reindex(columns=expected_columns, fill_value=0)

# Escalar los datos usando el escalador cargado
nuevos_datos_scaled = scaler.transform(nuevos_datos)

# Hacer predicciones con el modelo
predicciones = model.predict(nuevos_datos_scaled)
categorias = np.argmax(predicciones, axis=1)

# Decodificar las categorías predichas en nombres utilizando las etiquetas de categoría de los datos de entrenamiento
categorias_decodificadas = ['Frutas', 'Lácteos', 'Carnes', 'Verduras']  # Ajusta según tus etiquetas reales
categorias_nombres = [categorias_decodificadas[i] for i in categorias]

# Mostrar los resultados
for i, (producto, categoria) in enumerate(zip(productos, categorias_nombres)):
    print(f"{i+1}. Producto: {producto}, Categoría: {categoria}")
