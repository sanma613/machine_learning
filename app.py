from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import pandas as pd
import sys
import json

sys.path.append('src')
sys.path.append('src/controller')

from src.controller.results_controller import ResultsController
from src.model.result_model import ClusteringResult

app = Flask(__name__)

# Página principal (menú)
@app.route('/')
def menu():
    return render_template('menu.html', menu_url=url_for('menu'))

# Ruta para crear la base de datos
@app.route('/crear_base_datos', methods=['POST'])
def crear_base_datos():
    handler = ResultsController()
    crear = request.form.get('crear')
    
    if crear == 'yes':
        try:
            handler.create_table()
            return render_template('index.html', mensaje="Base de datos creada exitosamente", menu_url=url_for('menu'))
        except Exception as e:
            return render_template('index.html', error=f"Error al crear la base de datos: {e}", menu_url=url_for('menu'))
    return redirect(url_for('menu'))

# Nueva ruta para crear la tabla directamente desde el menú
@app.route('/crear_tabla', methods=['GET', 'POST'])
def crear_tabla():
    handler = ResultsController()
    mensaje = None
    error = None

    if request.method == 'POST':
        try:
            handler.create_table()
            mensaje = "Tabla creada exitosamente en la base de datos de Neon.tech."
        except Exception as e:
            error = f"Error al crear la tabla: {e}"

    return render_template('crear_tabla.html', mensaje=mensaje, error=error, menu_url=url_for('menu'))

# Ruta para subir y procesar archivo CSV
@app.route('/subir_archivo', methods=['GET', 'POST'])
def subir_archivo():
    if request.method == 'POST':
        if 'archivo' not in request.files:
            return "No se subió ningún archivo", 400

        archivo = request.files['archivo']
        if archivo.filename == '':
            return "Nombre de archivo vacío", 400

        try:
            df = pd.read_csv(archivo)
            columnas = list(df.columns)
            filas = df.head(5).values.tolist()
            return render_template('resultados.html', columnas=columnas, resultados=filas, menu_url=url_for('menu'))
        except Exception as e:
            return f"Error al procesar el archivo: {e}", 500
    return render_template('index.html', menu_url=url_for('menu'))

# Página con formulario para buscar
@app.route('/buscar', methods=['GET'])
def buscar():
    return render_template('buscar.html', menu_url=url_for('menu'))

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

    return render_template("lista.html", result=result, result_id=result_id, results_list=results_list, menu_url=url_for('menu'))
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
        return render_template('resultados.html', columnas=columnas, resultados=filas, menu_url=url_for('menu'))
    except Exception as e:
        return f"Error al procesar el archivo: {e}", 500

# Ruta para modificar un usuario
@app.route('/modificar_usuario', methods=['GET', 'POST'])
def modificar_usuario():
    handler = ResultsController()
    result = None
    error = None
    result_id = None
    formatted_coordinates = ''

    if request.method == 'GET':
        result_id = request.args.get('id')
        if not result_id:
            error = "No se proporcionó un ID. Por favor, seleccione un resultado desde la lista."
            return redirect(url_for('lista'))
        try:
            result_id = int(result_id)
            result = handler.get_result_by_id(result_id)
            if not result:
                error = f"No se encontró un resultado con el ID {result_id}"
                return redirect(url_for('lista'))
            # Format coordinates list to string (e.g., "[1.0, 2.0, 3.0, 4.0]" -> "1.0,2.0,3.0,4.0")
            if result.coordinates and isinstance(result.coordinates, list):
                formatted_coordinates = ','.join(map(str, result.coordinates))
        except ValueError:
            error = "ID inválido, debe ser un número entero"
            return redirect(url_for('lista'))
        except Exception as e:
            error = f"Error al cargar el resultado: {e}"
            return redirect(url_for('lista'))

    if request.method == 'POST':
        result_id = request.form.get('id')
        if not result_id:
            error = "No se proporcionó un ID para actualizar. Por favor, intente de nuevo desde la lista."
            return redirect(url_for('lista'))
        try:
            result_id = int(result_id)
            result = handler.get_result_by_id(result_id)
            if not result:
                error = f"No se encontró un resultado con el ID {result_id}"
                return redirect(url_for('lista'))

            # Procesar coordenadas
            coordinates = request.form.get('coordinates', '')
            if coordinates:
                coordinates = coordinates.split(',')
                coordinates = [float(coord.strip()) for coord in coordinates if coord.strip()]
                coordinates = '{' + ','.join(map(str, coordinates)) + '}'
            else:
                coordinates = '{}'

            # Crear el objeto ClusteringResult con los datos del formulario
            updated_result = ClusteringResult(
                id=result_id,
                title=request.form.get('title'),
                n_clusters=int(request.form.get('n_clusters')),
                used_iterations=int(request.form.get('used_iterations')),
                coordinates=coordinates,
                assigned_cluster=int(request.form.get('assigned_cluster')) if request.form.get('assigned_cluster') else None,
                is_centroid='is_centroid' in request.form,
                centroid_label=request.form.get('centroid_label') or None
            )

            # Actualizar el resultado en la base de datos
            success = handler.update_result(result_id, updated_result)
            if success:
                return redirect(url_for('lista'))
            else:
                error = "No se pudo actualizar el resultado en la base de datos"
        except ValueError as e:
            error = f"Datos inválidos proporcionados: {e}"
        except Exception as e:
            error = f"Error al actualizar el resultado: {e}"

    return render_template('modificar.html', result=result, error=error, result_id=result_id, 
                          formatted_coordinates=formatted_coordinates, menu_url=url_for('menu'))

# Ruta para mostrar el formulario de crear usuario
@app.route('/crear_usuario', methods=['GET'])
def show_crear_usuario():
    return render_template('crear_usuario.html', menu_url=url_for('menu'))

# Ruta para procesar la creación de un usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    handler = ResultsController()
    try:
        title = request.form.get('title')
        n_clusters = int(request.form.get('n_clusters'))
        used_iterations = int(request.form.get('used_iterations'))
        
        coordinates = request.form.get('coordinates')
        if coordinates:
            coordinates = coordinates.strip('[]').replace(' ', '')
            coordinates = '{' + coordinates + '}'
        else:
            coordinates = '{}'

        assigned_cluster = request.form.get('assigned_cluster')
        assigned_cluster = int(assigned_cluster) if assigned_cluster else None
        is_centroid = 'is_centroid' in request.form
        centroid_label = request.form.get('centroid_label')

        clustering_result = ClusteringResult(
            id=None,
            title=title,
            n_clusters=n_clusters,
            used_iterations=used_iterations,
            coordinates=coordinates,
            assigned_cluster=assigned_cluster,
            is_centroid=is_centroid,
            centroid_label=centroid_label
        )

        success = handler.create_result(clustering_result)
        if success:
            return redirect(url_for('menu'))
        else:
            return "Error al crear el usuario", 500
    except Exception as e:
        return f"Error al crear el usuario: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)