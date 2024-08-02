import pandas as pd
import plotly.express as px

# Carga de datos
data = pd.read_json('user_navigation_data.json')

# Análisis simple: Duración promedio en cada página
avg_duration_per_page = data.groupby('page')['duration'].mean().reset_index()

# Visualización con Plotly
fig = px.bar(avg_duration_per_page, x='page', y='duration', title='Average Duration per Page')

# Guardar la figura como un archivo HTML
fig.write_html('website_analysis.html', auto_open=False)
