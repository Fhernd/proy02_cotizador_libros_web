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
        'buscaLibre': buscar_busca_libre_libreria(driver, titulo)
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

    libros = []

    # Realizar la búsqueda con este selector CSS "div.box-producto":
    libros_encontrados = driver.find_elements(By.CSS_SELECTOR, 'div.box-producto')

    for libro in libros_encontrados:
        libros.append(extraer_datos_libro_busca_libre(libro))

    paginadores = driver.find_elements(By.CSS_SELECTOR, 'span.pagnLink')

    if len(paginadores):
        for i, p in enumerate(paginadores):
            titulo_modificado = titulo.replace(' ', '+').lower()
            url = f'https://www.buscalibre.com.co/libros/search?q={titulo_modificado}&page={i + 2}'

            driver.get(url)

            time.sleep(5)

            libros_encontrados = driver.find_elements(By.CSS_SELECTOR, 'div.box-producto')

            for libro in libros_encontrados:
                libros.append(extraer_datos_libro_busca_libre(libro))
    
    return libros


def extraer_datos_libro_busca_libre(libro):
    # Extraer el valor del atribut "src" de la primera etiqueta img:
    img = libro.find_element(By.TAG_NAME, 'img')
    src = img.get_attribute('src')

    # Extraer el texto de este selector CSS 'h3.nombre':
    nombre = libro.find_element(By.CSS_SELECTOR, 'h3.nombre')
    nombre = nombre.text

    # Extraer el texto del selector div.autor:
    autor = libro.find_element(By.CSS_SELECTOR, 'div.autor')
    autor = autor.text

    # Extraer el texto del div con clases 'autor color-dark-gray metas hide-on-hover':
    otros_datos = libro.find_element(By.CSS_SELECTOR, 'div.autor.color-dark-gray.metas.hide-on-hover')
    otros_datos = otros_datos.text

    # Extraer el texto del elemento p con clases 'precio-ahora hide-on-hover margin-0 font-size-medium':
    try:
        precio = libro.find_element(By.CSS_SELECTOR, 'p.precio-ahora.hide-on-hover.margin-0.font-size-medium')
        precio = precio.text
    except:
        precio = -1

    return {
        'src': src,
        'nombre': nombre,
        'autor': autor,
        'otros_datos': otros_datos,
        'precio': precio
    }