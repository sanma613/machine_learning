# archivo nuevo, por ejemplo webapp.py
from flask import Flask, render_template,request,jsonify
import pandas as pd

import sys
sys.path.append('src')
sys.path.append('src/controller')

from src.controller.results_controller import ResultsController

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar():
    return render_template('buscar.html')

@app.route("/lista", methods=["GET", "POST"])
def lista():
    
    df = pd.read_excel('casos_prueba.xlsx')

    # Filtrar por ID
    resultado = df[df['Id'] == int(id)]
    if resultado.empty:
        return jsonify({"error": "ID no encontrado"}), 404

    # Convertir a dict
    datos = resultado.to_dict(orient='records')[0]
    return jsonify(datos)       


@app.route('/resultados', methods=['POST'])
def procesar_archivo():
    if 'archivo' not in request.files:
        return "No se subió ningún archivo", 400

    archivo = request.files['archivo']

    if archivo.filename == '':
        return "Nombre de archivo vacío", 400

    try:
        df = pd.read_csv(archivo)

        # Aquí podrías aplicar tu algoritmo de clustering, guardar en DB, etc.
        # Para el ejemplo, vamos a mostrar los primeros 5 registros:
        columnas = list(df.columns)
        filas = df.head(5).values.tolist()

        return render_template('resultados.html', columnas=columnas, resultados=filas)

    except Exception as e:
        return f"Error al procesar el archivo: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
