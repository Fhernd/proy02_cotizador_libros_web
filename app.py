import time
from flask import Flask, jsonify, render_template, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


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
        'busca-libre': buscar_busca_libre_libreria(driver, titulo)
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
    q = driver.find_element(By.NAME, 'q')
    q.send_keys(titulo)

    # Presione la tecla Enter:
    q.send_keys(Keys.ENTER)

    # Esperar 5 segundos:
    time.sleep(5)

    # Validar si el elemento section con id 'noEncontrado' existe:
    no_encontrado = driver.find_elements(By.ID, 'noEncontrado')

    if no_encontrado:
        return []

    # Busque los elementos span que tengan la clase 'pagnLink':
    paginadores = driver.find_elements(By.CSS_SELECTOR, 'span.pagnLink')

    libros = []

    # Realizar la búsqueda con este selector CSS "div.box-producto":
    divs = driver.find_elements(By.CSS_SELECTOR, 'div.box-producto')

    for div in divs:
        libros.append(extraer_datos_libro_busca_libre(div))
    
    return libros
