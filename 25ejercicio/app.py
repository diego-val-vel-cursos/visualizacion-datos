from flask import Flask, request, jsonify, send_file
import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from io import BytesIO
import json
import os

# Configurar la aplicación Flask
server = Flask(__name__)
app = Dash(
    server=server, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    url_base_pathname='/dashboard/'
)

# Función para cargar los datos
def load_data():
    with open('animals.json', 'r') as file:
        return json.load(file)

# Layout de Dash
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Visualización Interactiva de Poblaciones de Animales"), width=12),
        className="mb-4 text-center"
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Dropdown(
                id='zona-dropdown',
                options=[{'label': zona, 'value': zona} for zona in ['Selva', 'Sabana', 'Desierto', 'Tundra']], # Ejemplo de opciones
                placeholder="Selecciona una zona"
            ), width=6, className="mb-2"),
            dbc.Col(dbc.Input(
                id='animal-input',
                type='text',
                placeholder='Ingresa un ID o nombre',
                debounce=True
            ), width=6, className="mb-2")
        ],
        align="center"
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='animal-graph'), width=12),
        justify="center"
    ),
    dbc.Row(
            dbc.Col(dcc.RangeSlider(
                id='poblacion-slider',
                min=0,
                max=1000,
                step=50,
                value=[100, 500],
                marks={i: str(i) for i in range(0, 1001, 100)},
                verticalHeight=300
            ), width=12), justify="center"
    )
], fluid=True)

@app.callback(
    [
        Output('zona-dropdown', 'options'),
        Output('animal-graph', 'figure')
    ],
    [
        Input('zona-dropdown', 'value'),
        Input('animal-input', 'value'),
        Input('poblacion-slider', 'value')
    ]
)
def update_output(zona, animal_input, poblacion_range):
    animals = load_data()
    if zona:
        animals = [animal for animal in animals if animal['zona'] == zona]
    if animal_input:
        animals = [animal for animal in animals if str(animal['id']) == animal_input or animal['animal'].lower() == animal_input.lower()]
    if poblacion_range:
        animals = [animal for animal in animals if poblacion_range[0] <= animal['poblacion'] <= poblacion_range[1]]

    fig = go.Figure(data=[
        go.Scatter(
            x=[animal['animal'] for animal in animals],
            y=[animal['poblacion'] for animal in animals],
            mode='markers',
            marker=dict(size=[p/10 for p in [animal['poblacion'] for animal in animals]])
        )
    ])
    fig.update_layout(title='Poblaciones de Animales', xaxis_title='Animal', yaxis_title='Población')

    zona_options = [{'label': z, 'value': z} for z in set(animal['zona'] for animal in load_data())]
    return zona_options, fig

# Endpoint para obtener todos los registros
@server.route('/animals', methods=['GET'])
def get_animals():
    if not os.path.exists('animals.json'):
        return jsonify({'error': 'Database not found'}), 404
    with open('animals.json', 'r') as file:
        animals = json.load(file)
    return jsonify(animals), 200

# Endpoint para obtener un registro por ID
@server.route('/animal/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    if not os.path.exists('animals.json'):
        return jsonify({'error': 'Database not found'}), 404
    with open('animals.json', 'r') as file:
        animals = json.load(file)
        animal = next((a for a in animals if a['id'] == animal_id), None)
    if animal:
        return jsonify(animal), 200
    else:
        return jsonify({'error': 'Animal not found'}), 404

# Ruta para crear un gráfico general
@server.route('/animals/graph', methods=['GET'])
def get_animals_graph():
    if not os.path.exists('animals.json'):
        return jsonify({'error': 'Database not found'}), 404
    
    with open('animals.json', 'r') as file:
        animals = json.load(file)
    
    # Generar el gráfico
    fig = go.Figure(data=[
        go.Bar(x=[animal['id'] for animal in animals],
               y=[animal['poblacion'] for animal in animals],
               text=[animal['animal'] for animal in animals])
    ])
    fig.update_layout(title='Poblaciones de Animales por ID',
                      xaxis_title='ID',
                      yaxis_title='Población')
    
    # Convertir a imagen
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format='png')
    img_bytes.seek(0)
    
    return send_file(img_bytes, mimetype='image/png')

# Ruta para crear un gráfico por ID
@server.route('/animal/<int:animal_id>/graph', methods=['GET'])
def get_animal_graph(animal_id):
    if not os.path.exists('animals.json'):
        return jsonify({'error': 'Database not found'}), 404
    
    with open('animals.json', 'r') as file:
        animals = json.load(file)
        animal = next((item for item in animals if item['id'] == animal_id), None)
    
    if animal:
        # Generar el gráfico
        fig = go.Figure(data=[
            go.Bar(x=[animal_id],
                   y=[animal['poblacion']],
                   text=[animal['animal']])
        ])
        fig.update_layout(title=f'Población del Animal ID {animal_id}',
                          xaxis_title='ID',
                          yaxis_title='Población')
        
        # Convertir a imagen
        img_bytes = BytesIO()
        fig.write_image(img_bytes, format='png')
        img_bytes.seek(0)
        
        return send_file(img_bytes, mimetype='image/png')
    else:
        return jsonify({'error': 'Animal not found'}), 404

# Ruta para crear un registro (POST)
@server.route('/animal', methods=['POST'])
def create_animal():
    data = request.get_json()
    print(f'Received POST data: {data}')  # Aparecerá en la consola del servidor Flask

    # Comprobar y crear animals.json si no existe
    if not os.path.isfile('animals.json'):
        with open('animals.json', 'w') as file:
            json.dump([], file)  # Crear un archivo JSON vacío

    # Leer y actualizar el archivo JSON
    with open('animals.json', 'r+') as file:
        try:
            file_data = json.load(file)
        except json.JSONDecodeError:
            return jsonify({"error": "Decoding JSON has failed"}), 500
        
        file_data.append(data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
    
    return jsonify(data), 201

# Actualizar un registro por ID (PUT /animal/<id>)
@server.route('/animal/<int:animal_id>', methods=['PUT'])
def update_animal(animal_id):
    if not os.path.exists('animals.json'):
        return jsonify({'error': 'Database not found'}), 404
    
    update_data = request.get_json()
    updated = False
    with open('animals.json', 'r+') as file:
        animals = json.load(file)
        for animal in animals:
            if animal['id'] == animal_id:
                animal.update(update_data)
                updated = True
                break
        
        if not updated:
            return jsonify({'error': 'Animal not found'}), 404

        file.seek(0)
        file.truncate()
        json.dump(animals, file, indent=4)
    
    return jsonify({'message': 'Animal updated successfully'}), 200

# Eliminar un registro por ID (DELETE /animal/<id>)
@server.route('/animal/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    if not os.path.exists('animals.json'):
        return jsonify({'error': 'Database not found'}), 404

    deleted = False
    with open('animals.json', 'r+') as file:
        animals = json.load(file)
        new_animals = [animal for animal in animals if animal['id'] != animal_id]
        
        if len(new_animals) != len(animals):
            deleted = True

        if not deleted:
            return jsonify({'error': 'Animal not found'}), 404

        file.seek(0)
        file.truncate()
        json.dump(new_animals, file, indent=4)
    
    return jsonify({'message': 'Animal deleted successfully'}), 200

# Verificar que la aplicación se ejecute en el puerto 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
