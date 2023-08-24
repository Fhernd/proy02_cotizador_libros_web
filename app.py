from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    titulo = request.form.get('title')

    datos = {
        'status': 'ok',
        'titulo': titulo,
        'id': 1,
    }
    
    return jsonify(datos)
