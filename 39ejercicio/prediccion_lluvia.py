import tensorflow as tf
import numpy as np
import datetime

# Generación de datos sintéticos
np.random.seed(42)
dias = np.random.randint(0, 100, (100, 10))  # 100 registros, 10 días cada uno
labels = np.where(dias.mean(axis=1) >= 50, 1, 0)  # Si el promedio >= 50, entonces llovió

# Modelo de clasificación binaria
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(10,)),  # Capa con 10 neuronas
    tf.keras.layers.Dense(1, activation='sigmoid')  # Salida binaria
])

# Compilación del modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Configuración del directorio para TensorBoard logs
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# Entrenamiento del modelo
model.fit(dias, labels, epochs=50, callbacks=[tensorboard_callback])
