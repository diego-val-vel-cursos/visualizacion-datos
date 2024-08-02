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

# Introducir valores NaN de manera artificial
np.random.seed(0)
indices = np.random.choice(iris_df.index, size=20, replace=False)
iris_df.loc[indices, 'sepal length (cm)'] = np.nan

# Imputar los valores NaN solo en columnas numéricas
for column in iris.feature_names:
    iris_df[column].fillna(iris_df[column].mean(), inplace=True)

# PERSONALIZACIÓN DE GRÁFICOS CON SEABORN: Pairplot
# Se añaden títulos, y se personalizan los colores.
sns.set(style="whitegrid")  # Establece el estilo de los gráficos de seaborn
pairplot_fig = sns.pairplot(iris_df, hue='species', palette='husl', markers=["o", "s", "D"])
pairplot_fig.fig.suptitle('Pairplot de las características del Iris por especie', y=1.02)  # Añade título al gráfico y ajusta su posición

plt.savefig('seaborn_pairplot_personalizado.png')
plt.close()

# PERSONALIZACIÓN DE GRÁFICOS CON PLOTLY: Scatter Matrix
# Se personalizan colores y se añaden títulos.
scatter_matrix_fig = px.scatter_matrix(iris_df,
                                        dimensions=iris.feature_names,
                                        color='species',
                                        title='Scatter Matrix del Iris por especie',
                                        labels={col: col.replace(' (cm)', 'cm') for col in iris_df.columns})  # Personaliza las etiquetas de los ejes
scatter_matrix_fig.update_layout(legend_title_text='Especies')  # Personaliza el título de la leyenda
scatter_matrix_fig.write_html('plotly_scatter_matrix_personalizado.html')
