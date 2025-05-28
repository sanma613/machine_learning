from flask import Flask, render_template, request, jsonify
import pandas as pd
import sys

sys.path.append('src')
sys.path.append('src/controller')

from src.controller.results_controller import ResultsController
handler = ResultsController()

app = Flask(__name__)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Página con formulario para buscar
@app.route('/buscar', methods=['GET'])
def buscar():
    return render_template('buscar.html')

# Ruta para petición desde JavaScript (fetch)
@app.route('/api/buscar', methods=['GET'])
def api_buscar():
    id = request.args.get('id')
    if not id:
        return jsonify({"error": "ID no proporcionado"}), 400

    try:
        id = int(id)
    except ValueError:
        return jsonify({"error": "ID inválido"}), 400

    result = handler.get_result_by_id(id)

    if result is None:
        return jsonify({"error": "No se encontró ningún resultado"}), 404

    return jsonify(result)

# Ruta tradicional con formulario POST que muestra resultados en una nueva página
@app.route("/lista", methods=["GET", "POST"])
def lista():
    id = None
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            id = int(id)

    result = handler.get_result_by_id(id) if id else None
    return render_template('lista.html', result=result)

# Procesamiento del archivo CSV
@app.route('/resultados', methods=['POST'])
def procesar_archivo():
    if 'archivo' not in request.files:
        return "No se subió ningún archivo", 400

    archivo = request.files['archivo']

    if archivo.filename == '':
        return "Nombre de archivo vacío", 400

    try:
        df = pd.read_csv(archivo)
        columnas = list(df.columns)
        filas = df.head(5).values.tolist()
        return render_template('resultados.html', columnas=columnas, resultados=filas)
    except Exception as e:
        return f"Error al procesar el archivo: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
