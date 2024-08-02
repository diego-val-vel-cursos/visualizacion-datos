import plotly.express as px
import pandas as pd

def crear_grafico_barras():
    data = {
        'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        'Rotaciones': [20, 15, 25, 22, 30, 10, 5, 12, 20, 15, 28, 10]
    }
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Mes', y='Rotaciones', title='Rotación Mensual de Personal',
                 labels={'Rotaciones': 'Número de Rotaciones', 'Mes': 'Mes del Año'},
                 color='Rotaciones', color_continuous_scale=px.colors.sequential.Viridis)
    fig.write_html('./47ejercicio/grafico_barras.html')

def crear_grafico_dispersión():
    data = {
        'Departamento': ['Ventas', 'Marketing', 'Operaciones', 'Finanzas', 'RRHH'],
        'Satisfacción': [3.5, 4.0, 3.0, 4.5, 3.8],
        'Rotación': [20, 15, 25, 10, 18]
    }
    df = pd.DataFrame(data)
    fig = px.scatter(df, x='Satisfacción', y='Rotación', color='Departamento',
                     size='Rotación', hover_data=['Departamento'],
                     title='Satisfacción vs. Rotación por Departamento',
                     labels={'Satisfacción': 'Nivel de Satisfacción', 'Rotación': 'Número de Rotaciones'})
    fig.write_html('./47ejercicio/grafico_dispersión.html')

def crear_mapa_de_calor():
    data = {
        'Mes': ['Enero', 'Enero', 'Enero', 'Febrero', 'Febrero', 'Febrero'],
        'Nivel': ['Junior', 'Mid', 'Senior', 'Junior', 'Mid', 'Senior'],
        'Rotación': [5, 10, 5, 3, 7, 5]
    }
    df = pd.DataFrame(data)
    # Corrección aquí: especificar correctamente los argumentos para pivot()
    df = df.pivot(index='Mes', columns='Nivel', values='Rotación')
    fig = px.imshow(df, aspect="auto", color_continuous_scale='Viridis',
                    labels=dict(x="Nivel de Empleo", y="Mes", color="Rotación"),
                    title='Mapa de Calor de Rotación por Nivel de Empleo')
    fig.write_html('./47ejercicio/mapa_de_calor.html')

if __name__ == "__main__":
    crear_grafico_barras()
    crear_grafico_dispersión()
    crear_mapa_de_calor()
