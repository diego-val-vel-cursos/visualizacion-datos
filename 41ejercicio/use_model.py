import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from joblib import load

# Obtener la ruta del directorio del script
dir_script = os.path.dirname(os.path.realpath(__file__))

# Cargar el modelo y el encoder
modelo = tf.keras.models.load_model(os.path.join(dir_script, 'movie_recommender_model.h5'))
encoder = load(os.path.join(dir_script, 'categories_encoder.joblib'))

# Simulación de nuevos usuarios
nuevos_usuarios = np.random.randint(0, len(encoder.classes_), (10, 3))
predicciones = modelo.predict(nuevos_usuarios)
categorias_predichas = np.argmax(predicciones, axis=1)

# Contar frecuencias de categorías predichas
(unique, counts) = np.unique(categorias_predichas, return_counts=True)
frecuencias = dict(zip(encoder.inverse_transform(unique), counts))

# Visualización de resultados
plt.figure(figsize=(10, 5))
plt.bar(frecuencias.keys(), frecuencias.values())
plt.xlabel('Categoría')
plt.ylabel('Número de Usuarios Nuevos')
plt.title('Preferencias de Categoría para Usuarios Nuevos')
plt.xticks(rotation=45)
plt.savefig(os.path.join(dir_script, 'user_preferences.png'))  # Guardar gráfico como archivo PNG
