from flask import Flask, jsonify, render_template, request
from selenium import webdriver

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


def crear_driver():
    """
    Crea el driver de selenium.

    Returns:
        driver: driver de selenium.
    """
    driver = webdriver.Firefox()
    return driver
