import pandas as pd
import numpy as np
from datetime import datetime
import time

# Inicio del log
start_time = datetime.now()
print(f"Inicio de la generación de datos: {start_time}")

# Generación inicial de grandes volúmenes de datos
data = {'time': pd.date_range(start="2020-01-01", periods=1000000, freq='T'), 'value': np.random.rand(1000000)}
df = pd.DataFrame(data)
df.to_csv('data_large.csv', index=False)

# Ciclo para generar datos en tiempo real
for _ in range(100):  # Generamos 100 puntos de datos como ejemplo
    new_data = {'time': datetime.now(), 'value': np.random.rand()}
    new_df = pd.DataFrame([new_data])
    new_df.to_csv('data_large.csv', mode='a', header=False, index=False)
    time.sleep(0.1)  # Pausa de 0.1 segundos para simular tiempo real

# Final del log
end_time = datetime.now()
print(f"Fin de la generación de datos: {end_time}")
print(f"Duración: {end_time - start_time}")
