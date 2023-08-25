from flask import Flask, jsonify, render_template, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    titulo = request.form.get('title')

    driver = crear_driver()

    datos = {
        'status': 'ok',
        'titulo': titulo,
        'busca-libre': buscar_busca_libre_libreria(driver)
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


def buscar_busca_libre_libreria(driver, titulo):
    """
    Busca en la libreria Busca Libre.

    Returns:
        driver: driver de selenium.
    """
    driver.get('https://www.buscalibre.com.co/')

    # Encuentre el input con name 'q' y escriba el titulo:
    q = driver.find_element_by_name('q')
    q.send_keys(titulo)

    # Presione la tecla Enter:
    q.send_keys(Keys.ENTER)
    
    return driver.page_source
