import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import TensorBoard
import os
import datetime
import joblib  # Para guardar el StandardScaler

# Crear datos sintéticos
data = {
    'Producto': ['manzana', 'leche', 'pollo', 'zanahoria', 'queso', 'pera', 'res', 'lechuga'],
    'Peso': [150, 1000, 500, 200, 300, 140, 1000, 100],
    'Color': ['rojo', 'blanco', 'blanco', 'naranja', 'amarillo', 'verde', 'rojo', 'verde'],
    'Categoria': ['Frutas', 'Lácteos', 'Carnes', 'Verduras', 'Lácteos', 'Frutas', 'Carnes', 'Verduras']
}
df = pd.DataFrame(data)

# Codificación One-hot de las categorías y colores
df = pd.get_dummies(df, columns=['Color'], drop_first=True)
categories = pd.get_dummies(df['Categoria'])

# Preparar datos para el modelo
X = df.drop(['Producto', 'Categoria'], axis=1).values
y = categories.values

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, './40ejercicio/scaler.pkl')  # Guardar el escalador

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Crear un modelo de TensorFlow
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(y_train.shape[1], activation='softmax')
])

# Compilar el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Configurar TensorBoard
log_dir = os.path.join("logs", "fit", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

# Entrenar el modelo
model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), callbacks=[tensorboard_callback])

# Guardar el modelo
model.save('./40ejercicio/modelo_tensorflow.h5')
