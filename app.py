# archivo nuevo, por ejemplo webapp.py
from flask import Flask, render_template
import sys
sys.path.append('src')
from src.controller.results_controller import ResultsController

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultados')
def resultados():
    # Aquí podrías procesar datos o leer resultados
    return render_template('resultados.html')

@app.route('/buscar')
def buscar():
    return render_template('results_controller.py', ResultsController.get_result_by_id())

if __name__ == '__main__':
    app.run(debug=True)
