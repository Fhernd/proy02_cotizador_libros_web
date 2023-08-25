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

    # Realizar la búsqueda con este selector CSS "div.box-producto":
    divs = driver.find_elements(By.CSS_SELECTOR, 'div.box-producto')

    libros = []

    for div in divs:
        # Extraer el valor del atribut "src" de la primera etiqueta img:
        img = div.find_element(By.TAG_NAME, 'img')
        src = img.get_attribute('src')

        # Extraer el texto de este selector CSS 'h3.nombre':
        nombre = div.find_element(By.CSS_SELECTOR, 'h3.nombre')
        nombre = nombre.text

        # Extraer el texto del selector div.autor:
        autor = div.find_element(By.CSS_SELECTOR, 'div.autor')
        autor = autor.text

        # Extraer el texto del div con clases 'autor color-dark-gray metas hide-on-hover':
        otros_datos = div.find_element(By.CSS_SELECTOR, 'div.autor.color-dark-gray.metas.hide-on-hover')
        otros_datos = otros_datos.text

        # Extraer el texto del elemento p con clases 'precio-ahora hide-on-hover margin-0 font-size-medium':
        precio = div.find_element(By.CSS_SELECTOR, 'p.precio-ahora.hide-on-hover.margin-0.font-size-medium')
        precio = precio.text

        libros.append({
            'src': src,
            'nombre': nombre,
            'autor': autor,
            'otros_datos': otros_datos,
            'precio': precio
        })
    
    return libros
