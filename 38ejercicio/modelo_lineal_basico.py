import tensorflow as tf
import numpy as np
import datetime

# Datos de entrenamiento
x_train = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
y_train = np.array([-1.0, 1.0, 3.0, 5.0, 7.0, 9.0], dtype=float)

# Creando un modelo simple con una capa
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])

# Compilando el modelo con un optimizador y una función de pérdida
model.compile(optimizer='sgd', loss='mean_squared_error')

# Configuración del directorio para TensorBoard logs
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# Entrenamiento del modelo
model.fit(x_train, y_train, epochs=100, callbacks=[tensorboard_callback])
