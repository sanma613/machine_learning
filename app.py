# archivo nuevo, por ejemplo webapp.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultados')
def resultados():
    # Aquí podrías procesar datos o leer resultados
    return render_template('resultados.html')

if __name__ == '__main__':
    app.run(debug=True)
