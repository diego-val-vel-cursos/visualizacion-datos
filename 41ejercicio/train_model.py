import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Cargar datos
datos = pd.read_csv('./41ejercicio/movies.csv')

# Procesamiento de datos: Extraer categorías y codificarlas
categorias = datos[['categoria1', 'categoria2', 'categoria3']].values.flatten()
encoder = LabelEncoder()
categorias_codificadas = encoder.fit_transform(categorias)
datos['categoria_cod1'] = categorias_codificadas[0::3]
datos['categoria_cod2'] = categorias_codificadas[1::3]
datos['categoria_cod3'] = categorias_codificadas[2::3]

# Modelo de TensorFlow
modelo = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(3,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(encoder.classes_), activation='softmax')
])

modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Preparar datos para entrenamiento
X = datos[['categoria_cod1', 'categoria_cod2', 'categoria_cod3']]
y = datos['categoria_cod1']  # Uso simplificado de una sola categoría como objetivo

# Entrenamiento del modelo
modelo.fit(X, y, epochs=10)

# Guardar el modelo y el encoder
modelo.save('./41ejercicio/movie_recommender_model.h5')
dump(encoder, './41ejercicio/categories_encoder.joblib')
