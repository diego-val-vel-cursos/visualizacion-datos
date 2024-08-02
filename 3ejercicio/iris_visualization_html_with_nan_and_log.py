import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Función para imprimir información del dataset
def print_dataset_info(df, message):
    print(message)
    print(df.head())
    print("\nResumen de valores NaN por columna:")
    print(df.isna().sum())
    print("-" * 50)

# Cargar el conjunto de datos Iris
iris = load_iris()
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['species'] = iris.target
iris_df['species'] = iris_df['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})

# Imprimir la información del dataset antes de introducir NaN
print_dataset_info(iris_df, "Dataset antes de introducir NaN:")

# Introducir valores NaN de manera artificial
np.random.seed(0)
indices = np.random.choice(iris_df.index, size=20, replace=False)
iris_df.loc[indices, 'sepal length (cm)'] = np.nan

# Imprimir la información del dataset después de introducir NaN y antes de la imputación
print_dataset_info(iris_df, "Dataset después de introducir NaN y antes de la imputación:")

# Imputar los valores NaN solo en columnas numéricas
for column in iris.feature_names:
    iris_df[column].fillna(iris_df[column].mean(), inplace=True)

# Imprimir la información del dataset después de imputar valores NaN
print_dataset_info(iris_df, "Dataset después de imputar valores NaN:")

# Visualización con Seaborn: Pairplot después de imputar NaN
sns.pairplot(iris_df, hue='species')
plt.suptitle('Pairplot de las características del Iris por especie después de manejar NaN')
plt.savefig('seaborn_pairplot_after_handling_nan.png')
plt.close()

# Visualización con Plotly como bono
fig = px.scatter_matrix(iris_df, dimensions=iris.feature_names, color='species')
fig.write_html('plotly_scatter_matrix.html')
