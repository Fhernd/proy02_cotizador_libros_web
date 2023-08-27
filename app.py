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
    libreria = request.args.get('libreria', default=None)  # Valor por defecto None si no se envía el parámetro.
    print('Libreria:', libreria)

    driver = crear_driver()

    resultado_busqueda = []
    
    if libreria == "buscaLibre":
        resultado_busqueda = buscar_busca_libre_libreria(driver, titulo)
    elif libreria == "libreriaNacional":
        print('Buscando en libreria nacional')
        resultado_busqueda = buscar_libreria_nacional(driver, titulo)

    datos = {
        'status': 'ok',
        'titulo': titulo,
        'resultado': resultado_busqueda
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
    # Recuperar el valor del atributo "href" de la primera etiqueta a:
    a = libro.find_element(By.TAG_NAME, 'a')
    url = a.get_attribute('href')
    
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
        'url': url,
        'imagen': src if src else 'https://statics.cdn1.buscalibre.com/no_image/ni9.__RS180x180__.jpg',
        'nombre': nombre,
        'autor': autor,
        'otrosDatos': otros_datos,
        'precio': precio
    }
    

def buscar_libreria_nacional(driver, titulo):
    url = 'https://librerianacional.com/'
    
    driver.get(url)
    
    # Esperar 5 segundos:
    time.sleep(5)
    
    # Pulsar 13 veces la tecla TAB:
    for i in range(13):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)
    
    # Encontrar el elemento input con las clases "form-control form-search ng-pristine ng-invalid ng-touched":
    q = driver.switch_to.active_element
    
    # Escribir el titulo en el input:
    q.send_keys(titulo)
    
    # Presionar la tecla Enter:
    q.send_keys(Keys.ENTER)
    
    # Esperar 5 segundos:
    time.sleep(5)
    
    # Encontrar todos los elementos div con las clases "row mx-0 mx-sm-2 mx-md-3":
    libros_encontrados = driver.find_elements(By.CSS_SELECTOR, 'div.row.mx-0.mx-sm-2.mx-md-3')
    
    libros = []
    
    for libro in libros_encontrados:
        # Encontrar la primera etiqueta img y extraer el valor del atributo "src":
        img = libro.find_element(By.TAG_NAME, 'img')
        img = img.get_attribute('src')
        
        # Extraer el nombre del libro desde la etiqueta a con clases "book-title":
        nombre = libro.find_element(By.CSS_SELECTOR, 'a.book-title')
        nombre = nombre.text
        
        # Encontrar con esta expresion XPath "//div[starts-with(text(), 'Autor: ')]":
        autor = libro.find_element(By.XPATH, "//div[starts-with(text(), 'Autor: ')]")
        
        autor = autor.text.replace('Autor: ', '')
        
        # Encuentre el span con la clase "text--bold":
        precio = libro.find_element(By.CSS_SELECTOR, 'span.text--bold')
        precio = precio.text
        
        print(
            'img:', img,
            'nombre:', nombre,
            'autor:', autor,
            'precio:', precio
        )
        
        libros.append({
        'url': 'pendiente',
        'imagen': img if img else 'https://statics.cdn1.buscalibre.com/no_image/ni9.__RS180x180__.jpg',
        'nombre': nombre,
        'autor': autor,
        'precio': precio
        })
    
    return libros
