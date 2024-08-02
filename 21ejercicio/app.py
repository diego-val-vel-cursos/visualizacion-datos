from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_graph():
    # Datos para el gráfico
    categorias = ['Tecnología', 'Ropa', 'Alimentos', 'Hogar']
    ventas = [15000, 23000, 18000, 22000]

    # Crear gráfico de barras
    bar_trace = go.Bar(
        x=categorias,
        y=ventas,
        name='Ventas por Categoría',
        marker_color='rgb(55, 83, 109)'
    )

    # Calcular porcentajes para el gráfico de pie
    total_ventas = sum(ventas)
    porcentajes = [x / total_ventas * 100 for x in ventas]

    # Crear gráfico de pie
    pie_trace = go.Pie(
        labels=categorias,
        values=porcentajes,
        name='Proporción de Ventas'
    )

    # Crear la figura para contener ambos gráficos
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]])

    # Añadir los trazos a la figura
    fig.add_trace(bar_trace, row=1, col=1)
    fig.add_trace(pie_trace, row=1, col=2)

    # Actualizar layout de la figura
    fig.update_layout(
        title_text="Análisis de Ventas por Categoría",
        annotations=[dict(text='Barras', x=0.2, y=1.1, font_size=12, showarrow=False),
                     dict(text='Pastel', x=0.8, y=1.1, font_size=12, showarrow=False)]
    )

    # Convertir la figura a HTML
    return HTMLResponse(fig.to_html())
