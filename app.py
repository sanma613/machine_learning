from flask import Flask, render_template, request, jsonify
import pandas as pd
import sys
import json

sys.path.append('src')
sys.path.append('src/controller')

from src.controller.results_controller import ResultsController
from src.model.result_model import ClusteringResult

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

    handler = ResultsController()
    result = handler.get_result_by_id(id)

    if result is None:
        return jsonify({"error": "No se encontró ningún resultado"}), 404

    return jsonify(result.to_dict())

# Ruta tradicional con formulario POST que muestra resultados en una nueva página
@app.route("/lista", methods=["GET", "POST"])
def lista():
    handler = ResultsController()
    result = None
    result_id = None
    results_list = []

    try:
        results_list = handler.list_all_titles()
    except Exception as e:
        return f"Error al obtener los resultados: {e}", 500

    if request.method == "POST":
        result_id = request.form.get("id")
        if result_id:
            try:
                result_id = int(result_id)
                result = handler.get_result_by_id(result_id)
                if not result:
                    return "No se encontró un resultado con ese ID", 404
            except ValueError:
                return "ID inválido", 400
            except Exception as e:
                return f"Error al buscar el resultado: {e}", 500

    return render_template("lista.html", result=result, result_id=result_id, results_list=results_list)

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

@app.route('/modificar', methods=['GET', 'POST'])
def modificar():
    handler = ResultsController()
    result = None
    original_result = None
    updated_result = None
    error = None

    # Manejar solicitud GET (mostrar formulario con datos actuales)
    if request.method == 'GET':
        result_id = request.args.get('id')
        if result_id:
            try:
                result_id = int(result_id)
                result = handler.get_result_by_id(result_id)
                if not result:
                    return "No se encontró un resultado con ese ID", 404
            except ValueError:
                return "ID inválido", 400
            except Exception as e:
                return f"Error al cargar el resultado: {e}", 500

    # Manejar solicitud POST (actualizar datos)
    if request.method == 'POST':
        try:
            result_id = int(request.form.get('id'))
            original_result = handler.get_result_by_id(result_id)
            if not original_result:
                return "No se encontró un resultado con ese ID", 404

            # Convertir coordinates a un formato compatible con PostgreSQL array
            coordinates = request.form.get('coordinates')
            if coordinates:
                # Remover corchetes y espacios, y convertir a formato de array PostgreSQL
                coordinates = coordinates.strip('[]').replace(' ', '')
                coordinates = '{' + coordinates + '}'
            else:
                coordinates = '{}'

            clustering_result = ClusteringResult(
                id=result_id,
                title=request.form.get('title'),
                n_clusters=int(request.form.get('n_clusters')),
                used_iterations=int(request.form.get('used_iterations')),
                coordinates=coordinates,
                assigned_cluster=int(request.form.get('assigned_cluster')) if request.form.get('assigned_cluster') else None,
                is_centroid='is_centroid' in request.form,
                centroid_label=request.form.get('centroid_label')
            )
            success = handler.update_result(result_id, clustering_result)
            if success:
                updated_result = handler.get_result_by_id(result_id)  # Obtener el estado actualizado
            else:
                error = "No se pudo actualizar el resultado"
        except ValueError as e:
            error = "Datos inválidos proporcionados"
        except Exception as e:
            error = f"Error al actualizar el resultado: {e}"

        # Recargar los datos actuales para mostrar en el formulario en caso de error
        if error:
            result = handler.get_result_by_id(result_id)

    return render_template('modificar.html', result=result, original_result=original_result, updated_result=updated_result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
