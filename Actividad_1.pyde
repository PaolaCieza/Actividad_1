# Se importa el módulo que genera número aleatorios
import random

# Cantidad de cuadros - 1 por fila o columna
cantidadCuadros = 10

# Tiempo de delay
tiempoDelay = 50

# Genera un array que contendrá los cuadros del mapa  (filas y columnas)
mapa = [
    # Crea un array que contiene cantidadCuadros (10) ceros: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    [0] * cantidadCuadros
    # Repite lo anterior por cantidadCuadros (10) veces
    for i in range(cantidadCuadros)
]

# Se especifica el tamaño del mapa
tamanoMapa = 600 / cantidadCuadros

# (x,y) Coordenadas iniciales del avatar
avatarX = 0
avatarY = 0

# (x,y) Coordenadas iniciales del tesoro
# El mapa es un array de 10 elementos por eso empieza a contar desde 0 y ubica al tesoro en las coordenadas (9, 9)
tesoroX = (cantidadCuadros - 1)
tesoroY = (cantidadCuadros - 1)

# Coordenadas y tamaño del boton 1
boton1X     = 650
boton1Y     = 55
boton1Ancho = 100
boton1Alto  = 20

# Coordenadas y tamaño del boton 2
boton2X     = 620
boton2Y     = 180
boton2Ancho = 70
boton2Alto  = 70

# Coordenadas y tamaño del boton 3
boton3X     = 700
boton3Y     = 180
boton3Ancho = 70
boton3Alto  = 70

# Coordenadas y tamaño del boton 4
boton4X     = 610
boton4Y     = 555
boton4Ancho = 200
boton4Alto  = 20

# Coordenadas y tamaño de la barra
barraX      = 690
barraY      = 290
barraAncho  = 20
barraAlto   = 200


# Botones de Métodos
m1x=635
m1y=20
m2x=635
m2y=60
m3x=635
m3y=100
m4x=635
m4y=140

mw=125
mh=25

# Respuestas
rptm1x=610
rptm1y=540
rptm2x=660
rptm2y=540
rptm3x=710
rptm3y=540
rptm4x=760
rptm4y=540


# Coordenadas y tamaño del deslizador de la barra
deslizadorX     = barraX - 5
deslizadorY     = barraY + barraAlto
deslizadorAncho = 30
deslizadorAlto  = 20
overLever       = False
barraBloqueada  = False
yOffset         = 0.0

# Coordenadas y porcentaje de barra en texto
porcentajeX = barraX
porcentajeY = barraY - 5
porcentaje  = 0.0


# Variables para la ruta a seguir por el avatar
global rutaBresenham, rutaRecorrida
iteradorBresenham = 0


# Configuración de la interfaz y el juego
def setup():
    # Tamaño de la ventana
    size(820, 600)
    
    global jugando, colocandoAvatar, colocandoTesoro, rutaBresenham, rutaRecorrida, bresenhamActivado, yaJugo
    global imagenGrass, imagenAvatar, imagenTesoro, imagenArbol1, imagenArbol2, imagenArbol3, imagenArbol4, imagenArbol5

    # Lectura de imagenes
    imagenAvatar    = loadImage("assets/avatar.png")
    imagenGrass     = loadImage("assets/grass3.JPG")
    imagenTesoro    = loadImage("assets/treasure.PNG")
    imagenArbol1    = loadImage("assets/tree1.png")
    imagenArbol2    = loadImage("assets/tree2.png")
    imagenArbol3    = loadImage("assets/tree3.png")
    imagenArbol4    = loadImage("assets/tree4.png")
    imagenArbol5    = loadImage("assets/tree5.png")

    # Configuración inicial del juego
    jugando             = False
    colocandoAvatar     = False
    colocandoTesoro     = False
    rutaBresenham       = []
    rutaRecorrida       = Stack()
    iteradorBresenham   = 0
    bresenhamActivado   = True
    yaJugo              = False


# Método que se ejecuta siempre
def draw():
    # Si el usuario está jugando entonces el programa encuentra la ruta
    if jugando:
        encontrarCamino()
        delay(tiempoDelay)
    
    # Siempre se dibuja la interfaz
    dibujarInterfaz()


# Método que encuentra la ruta
def encontrarCamino():
    global avatarX, avatarY, rutaRecorrida, jugando, iteradorBresenham, bresenhamActivado, mapa, yaJugo
    
    # Array que guarda las alternativas para cambiar la posición inicial del avatar cuando se encuentra con un árbol
    alternativas = []

    # Se comprueba si el programa ganó
    if avatarX == tesoroX and avatarY == tesoroY:
        ganar()
        return

    # Si el método de búsqueda está seleccionado entonces ejecuta el método de bresenham
    if bresenhamActivado:
        bresenham(avatarX, avatarY, tesoroX, tesoroY)
    
    # Imprime en consola la posición actual del avatar
    print("Avatar en: (" + str(avatarX) + "," + str(avatarY) + ")")

    # Comprueba si la ruta tiene al menos una posición y si en la posición del avatar existe un árbol
    if len(rutaBresenham) > 1 and mapa[rutaBresenham[iteradorBresenham][0]][rutaBresenham[iteradorBresenham][1]] < 5:
        # Se guarda el recorrido del avatar
        rutaRecorrida.insertar( (avatarX, avatarY) )

        # Se cambia la posición del avatar a la siguiente posición de la ruta establecida
        avatarX = rutaBresenham[iteradorBresenham][0]
        avatarY = rutaBresenham[iteradorBresenham][1]

        # Se comprueba si el avatar llegó a su destino
        if(avatarX == tesoroX and avatarY == tesoroY):
            # Gana
            ganar()
            return
        
        # Si el avatar no ha llegado a su destino entonces se pasa a la siguiente posición de la ruta
        iteradorBresenham = iteradorBresenham + 1

        # Se cambia a False para que no establezca una nueva ruta mientras se recorra la ruta actual
        bresenhamActivado = False
        return
    else:
        # Si en la siguiente posición de la ruta existe un árbol entonces en la posición actual del mapa aumenta en 1 para que si vuelve a pasar y
        # existe el árbol se cree un nuevo árbol al llegar a 5 pasadas
        mapa[avatarX][avatarY] = mapa[avatarX][avatarY] + 1
    
    # Como encontró un árbol entonces tiene que establecer una nueva ruta
    bresenhamActivado = True

    contador = 0

    # Se busca en los 8 posibles cambios de coordenadas

    # Con este primer bucle ve si aumenta o disminuye la coordenada actual del avatar en 1 unidad en el eje x
    # x toma los valores de [-1, 0, 1]
    for x in range(-1, 2):
        # Con este segundo bucle ve si aumenta o disminuye la coordenada actual del avatar en 1 unidad en el eje y
        # y toma los valores de [-1, 0, 1]
        for y in range(-1, 2):
            # Se calcula el cambio de coordenadas
            cambioCoordenadaX = avatarX + x
            cambioCoordenadaY = avatarY + y
            
            # Se verifica si las opciones se encuentran dentro del mapa
            if 0 <= cambioCoordenadaX <= cantidadCuadros - 1 and 0 <= cambioCoordenadaY <= cantidadCuadros - 1:
                
                # Comprueba si en el cambio de coordenadas no existe un árbol y si el cambio de coordenadas no coincide con las coordenadas actuales
                if rutaRecorrida.cantidad() > 0 and mapa[cambioCoordenadaX][cambioCoordenadaY] < 5 and (cambioCoordenadaX, cambioCoordenadaY) != rutaRecorrida.ultimoElemento() and not (x == 0 and y == 0):
                    contador = contador + 1

                    # Añade el cambio de coordenada como una de las opciones a cambiar
                    alternativas.append( (x, y) )
                elif rutaRecorrida.estaVacia() and mapa[cambioCoordenadaX][cambioCoordenadaY] < 5 and not (x == 0 and y == 0):
                    contador = contador + 1

                    # Añade el cambio de coordenada como una de las opciones a cambiar
                    alternativas.append( (x, y) )
    
    # Si no encontró opciones de cambio de coordenada y recorrió toda su ruta entonces pierde
    if contador == 0 and rutaRecorrida.cantidad() > 0:
        # Toma la última posición de la ruta
        elem = rutaRecorrida.ultimoElemento()

        # Compara si en la última posición no encontró un árbol
        if mapa[elem[0]][elem[1]] < 5:
            # Aumenta en 1 la aparición del árbol en la coordenada actual del avatar
            mapa[avatarX][avatarY] = mapa[avatarX][avatarY] + 1
            
            # Mueve al avatar a la última posición de la ruta
            avatarX = elem[0]
            avatarY = elem[1]

            # Elimina la última posición
            rutaRecorrida.soltar()
            return

        # Pierde
        perder()
        return
    
    # Si no encontró opciones y no hay ruta entonces pierde
    elif contador == 0 and rutaRecorrida.cantidad() == 0:
        # Pierde
        perder()
        return
    
    # Si encuentra opciones entonces escoge la nueva posición de inicio del avatar de manera aleatoria
    aux = random.choice(alternativas)

    # Inserta a la ruta recorrida la posición del avatar
    rutaRecorrida.insertar((avatarX, avatarY))

    # Coloca al avatar en la nueva posición encontrada
    avatarX = avatarX + aux[0]
    avatarY = avatarY + aux[1]

    # Comprueba si con la nueva posición ganó
    if(avatarX == tesoroX and avatarY == tesoroY):
        # Gana
        ganar()
        return


# Método que se ejecuta cuando se gana
def ganar():
    global yaJugo, bresenhamActivado, jugando
    print("GANASTE")
    yaJugo              = True
    bresenhamActivado   = True
    jugando             = False


# Método que se ejecuta cuando se pierde
def perder():
    global yaJugo, bresenhamActivado, jugando
    print("PERDISTE")
    jugando             = False
    bresenhamActivado   = True
    yaJugo              = True


# Método que muestra la interfaz
def dibujarInterfaz():
    background(255)
    fill(255)
    # b1()
    dibujarBotones()
    fill(255)
    b2()
    fill(255)
    b3()
    fill(0)
    bar()
    fill(255,0,0)
    lever()
    pLever()
    fill(255)
    #b4()
    dibujarMapa()

def dibujarBotones():
    stroke(0)
    rect(m1x, m1y, mw, mh)
    rect(m2x, m2y, mw, mh)
    rect(m3x, m3y, mw, mh)
    rect(m4x, m4y, mw, mh)
    #Dibujar los cuadrados de Pasos
    rect(rptm1x, rptm1y, 50, 40)
    rect(rptm2x, rptm2y, 50, 40)
    rect(rptm3x, rptm3y, 50, 40)
    rect(rptm4x, rptm4y, 50, 40)
    #Poner texto a los botones
    fill(0)
    textSize(20)
    text("BRESENHAM", m1x+5, m1y+20)
    text("Metodo 2", m2x+5, m2y+20)
    text("Metodo 3", m3x+5, m3y+20)
    text("Metodo 4", m4x+5, m4y+20)

# Dibuja el mapa
def dibujarMapa():
    global mapa
    # Las imagenes se colocan cada tamanoMapa (10) unidades en el eje X e Y con un ancho y alto de tamanoMapa (10) unidades
    
    # Empieza en las coordenadas (0, 0)
    x, y = 0, 0
    
    # Recorre todo el mapa, celda por celda para colocar las imágenes
    for fila in mapa:
        for columna in fila:

            # Siempre coloca grass en cada celda
            image(imagenGrass, x, y, tamanoMapa, tamanoMapa)

            # Verifica si en esa celda va grass o un árbol de cualquier nivel
            image(seleccionarImagen(columna), x, y, tamanoMapa, tamanoMapa)

            # Incrementa el valor de la coordenada X en tamanoMapa (10) unidades por cada columna
            x = x + tamanoMapa

        # Incremente el valor de la coordenada Y en tamanoMapa (10) unidades por cada fila
        y = y + tamanoMapa

        # Reinicia en 0 la coordenada X porque se cambia de fila
        x = 0
    
    # Colocando el tesoro en su ubicación
    image(imagenTesoro, tesoroY * tamanoMapa, tesoroX * tamanoMapa, tamanoMapa, tamanoMapa)

    # Colocando al avatar en su ubicación
    image(imagenAvatar, avatarY * tamanoMapa, avatarX * tamanoMapa, tamanoMapa, tamanoMapa)


def b1():
    stroke(0)
    rect(m1x, m1y, mw, mh)
    textSize(20)
    # fill(0)
    # text("Busca!", boton1X+20, boton1Y+20-2)


def metodo1():
    stroke(0)
    rect(650, 460, 100, 25)
    fill(0)
    textSize(20)
    fill(0)
    text("Metodo 1", 655, 480)


def metodo2():
    stroke(0)
    rect(650, 500, 100, 25)
    fill(0)
    textSize(20)
    fill(0)
    text("Metodo 2", 655, 520)


def metodo3():
    stroke(0)
    rect(650, 540, 100, 25)
    fill(0)
    textSize(20)
    fill(0)
    text("Metodo 3", 655, 560)


def metodo4():
    stroke(0)
    rect(650, 580, 100, 25)
    fill(0)
    textSize(20)
    fill(0)
    text("Metodo 4", 655, 600)


def b2():
    rect(boton2X, boton2Y, boton2Ancho, boton2Alto)
    image(imagenAvatar, boton2X, boton2Y, boton2Ancho, boton2Alto)


def b3():
    rect(boton3X, boton3Y, boton3Ancho, boton3Alto)
    image(imagenTesoro, boton3X, boton3Y, boton3Ancho, boton3Alto)


def bar():
    rect(barraX, barraY, barraAncho, barraAlto)


def lever():
    global overLever
    if mouseX > deslizadorX and mouseY > deslizadorY and mouseX < deslizadorX+deslizadorAncho and mouseY < deslizadorY+deslizadorAlto:
        overLever = True
        if not barraBloqueada:
            stroke(120)
            fill(255, 0, 0)
    else:
        stroke(255)
        fill(255, 0, 0)
        overLever = False
    rect(deslizadorX, deslizadorY, deslizadorAncho, deslizadorAlto)


def pLever():
    text(str(porcentaje) + "%", porcentajeX-8, porcentajeY)


def b4():
    global jugando, avatarX, avatarY, tesoroX, tesoroY
    fill(255)
    noStroke()
    rect(boton1X, boton1Y, boton4Ancho, boton4Alto)
    textSize(20)
    fill(0)
    if jugando == False and yaJugo:
        if avatarX == tesoroX and avatarY == tesoroY:
            textSize(30)
            text(rutaRecorrida.size(), rptm1x+7, rptm1y+35)
        else:
            textSize(50)
            text("x", rptm1x+7, rptm1y+35)


def clearmapaAvatar():
    global avatarX, avatarY
    avatarX = -1000/tamanoMapa
    avatarY = -1000/tamanoMapa


def clearmapaTreasure():
    global tesoroX, tesoroY
    tesoroX = -1000/tamanoMapa
    tesoroY = -1000/tamanoMapa


def clearmapa():
    for i in range(cantidadCuadros):
        for j in range(cantidadCuadros):
            mapa[i][j] = 0


def putObstacles():
    global avatarX, avatarY, tesoroX, tesoroY
    v = [[(j, i) for i in range(0, cantidadCuadros)]
         for j in range(0, cantidadCuadros)]
    clearmapa()
    total = cantidadCuadros*cantidadCuadros
    objectsP = int(total*porcentaje)/100
    if avatarX == tesoroX and avatarY == tesoroY:
        avatarX = 0
        avatarY = 0
        tesoroX = cantidadCuadros-1
        tesoroY = cantidadCuadros-1
    if objectsP > total-2:
        objectsP = total-2
    v[avatarX].remove((avatarX, avatarY))
    v[tesoroX].remove((tesoroX, tesoroY))
    print(objectsP)
    while objectsP > 0:
        aux = random.choice(v)
        while len(aux) == 0:
            aux = random.choice(v)
        pos = random.choice(aux)
        if mapa[pos[0]][pos[1]] != 5 and not(pos[0] == avatarX and pos[0] == tesoroX) and not(pos[1] == avatarY and pos[1] == tesoroY):
            mapa[pos[0]][pos[1]] = 5
            objectsP -= 1
            aux.remove(pos)
        elif mapa[pos[0]][pos[1]] != 5 and avatarX == tesoroX and pos[0] == avatarX and pos[1] != avatarY and pos[1] != tesoroY:
            mapa[pos[0]][pos[1]] = 5
            objectsP -= 1
            aux.remove(pos)
        elif mapa[pos[0]][pos[1]] != 5 and avatarY == tesoroY and pos[1] == avatarY and pos[0] != avatarX and pos[0] != tesoroX:
            mapa[pos[0]][pos[1]] = 5
            objectsP -= 1
            aux.remove(pos)


def dda():
    pass


def bresenham(coordenadaAvatarX, coordenadaAvatarY, coordenadaTesoroX, coordenadaTesoroY):
    global rutaBresenham, iteradorBresenham
    iteradorBresenham = 1
    rutaBresenham = []

    # Se calcula la distancia que hay entre coordenadas con sus respectivos ejes
    distanciaX = coordenadaTesoroX - coordenadaAvatarX
    distanciaY = coordenadaTesoroY - coordenadaAvatarY

    # Se verifica si las distancias son negativas o positivas para comprobar en qué cuadrante se encuentra la ruta 
    # a seguir y así encontrar el vector unitario que indica la dirección de la ruta a seguir

    # Si la ruta se encuentra en el primer cuadrante entonces el vector unitario será (1, 1)
    # Si la ruta se encuentra en el segundo cuadrante entonces el vector unitario será (-1, 1)
    # Si la ruta se encuentra en el tercer cuadrante entonces el vector unitario será (-1, -1)
    # Si la ruta se encuentra en el cuarto cuadrante entonces el vector unitario será (1, -1)

    # Esto le indica cómo moverse en diagonal
    movimientoInclinadoX = 1 if distanciaX >= 0 else -1
    movimientoInclinadoY = 1 if distanciaY >= 0 else -1

    # Se pasa todo al primer cuadrante solo para usar un solo bucle
    distanciaX = abs(distanciaX)
    distanciaY = abs(distanciaY)

    # Comprueba qué distancia es mayor para así indicarle al avatar en qué eje se debe mover sí o sí en una 1 unidad
    # mientras que para la distancia menor se moverá AVECES en 1 unidad en el eje respectivo

    # Esto indica cómo moverse en línea recta
    if distanciaX >= distanciaY:

        # Eje X: (1, 0) o (-1, 0)
        movimientoRectoEjeXX = movimientoInclinadoX
        movimientoRectoEjeXY = 0

        # Eje Y: (0, 1) o (0, -1)
        movimientoRectoEjeYX = 0
        movimientoRectoEjeYY = movimientoInclinadoY
    else:
        # Intercambia las distancias con el fin de usar el mismo algoritmo para el otro caso
        distanciaX, distanciaY = distanciaY, distanciaX

        # Eje Y: (0, 1) o (0, -1)
        movimientoRectoEjeXX = 0
        movimientoRectoEjeXY = movimientoInclinadoX

        # Eje X: (1, 0) o (-1, 0)
        movimientoRectoEjeYX = movimientoInclinadoY
        movimientoRectoEjeYY = 0

    # Nota: en el algoritmo original no se hace las vainas raras que se hacen aquí

    # Constante que verifica en cada iteración del bucle si el avatar se movió en el eje menor en una unidad o no.
    # Para saber de dónde sale el 2 * dy - dx revisar: https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#Derivation
    constanteP = 2 * distanciaY - distanciaX

    # Parte desde el "origen" (0, 0)
    # x = 0
    y = 0

    print("Ruta establecida:")

    # Se realiza el bucle para buscar la ruta
    # Desde X = 0 hasta X = distanciaX
    for x in range(distanciaX + 1):

        # Avanza de manera diagonal o recta según la constante P
        coordenadaX = coordenadaAvatarX + x * movimientoRectoEjeXX + y * movimientoRectoEjeYX
        coordenadaY = coordenadaAvatarY + x * movimientoRectoEjeXY + y * movimientoRectoEjeYY

        # Inserta la coordenada siguiente en la lista rutaBresenham
        rutaBresenham.append( ( coordenadaX, coordenadaY ) )

        print("\tPosicion N " + str(x + 1) + ": (" + str(coordenadaX) + ", " + str(coordenadaY) + ")")

        # Con esto verifica si el avatar se movió 1 unidad o no en el eje menor
        # Pero como sí o sí se hacen los cálculos como si dx fuese mayor entonces se incrementa en Y aveces
        if constanteP >= 0:
            y = y + 1
            # Este cálculo se hace por el algoritmo
            constanteP = constanteP - 2 * distanciaX
        # Este cálculo se hace por el algoritmo
        constanteP = constanteP + 2 * distanciaY


def mousePressed():
    global colocandoTesoro, colocandoAvatar, overLever, barraBloqueada, yOffset, jugando, mapa, yaJugo
    global avatarX, avatarY, tesoroX, tesoroY
    if mouseX > m1x and mouseY > m1y and mouseX < m1x+mw and mouseY < m1y+mh:
        yaJugo = False
        jugando = True
        fill(0)
        b1()
    if mouseX > boton2X and mouseY > boton2Y and mouseX < boton2X+boton2Ancho and mouseY < boton2Y+boton2Alto:
        yaJugo = False
        fill(0)
        b2()
        clearmapaAvatar()
        colocandoAvatar = True
    if mouseX > boton3X and mouseY > boton3Y and mouseX < boton3X+boton3Ancho and mouseY < boton3Y+boton3Alto:
        yaJugo = False
        fill(0)
        b3()
        clearmapaTreasure()
        colocandoTesoro = True
    if mouseX > boton4X and mouseY > boton4Y and mouseX < boton4X+boton4Ancho and mouseY < boton4Y+boton4Alto:
        yaJugo = False
        fill(0)
        b4()
        putObstacles()

    if overLever:
        barraBloqueada = True
        fill(255, 0, 0)
    else:
        barraBloqueada = False

    if (mouseX/tamanoMapa) < cantidadCuadros and (mouseY/tamanoMapa) < cantidadCuadros:
        yaJugo = False
        if mapa[mouseY/tamanoMapa][mouseX/tamanoMapa] == 5:
            mapa[mouseY/tamanoMapa][mouseX/tamanoMapa] = 0
        else:
            mapa[mouseY/tamanoMapa][mouseX/tamanoMapa] = 5

        if colocandoAvatar:
            avatarX = mouseY/tamanoMapa
            avatarY = mouseX/tamanoMapa
            if(mapa[avatarX][avatarY] >= 0 and mapa[avatarX][avatarY] <= 5):
                mapa[avatarX][avatarY] = 0
            print("AVATAR: "+str(avatarX) + ' ' + str(avatarY))
            colocandoAvatar = False
        elif colocandoTesoro:
            tesoroX = mouseY/tamanoMapa
            tesoroY = mouseX/tamanoMapa
            if(mapa[tesoroX][tesoroY] >= 0 and mapa[tesoroX][tesoroY] <= 5):
                mapa[tesoroX][tesoroY] = 0
            print("TREASURE: "+str(tesoroX) + ' ' + str(tesoroY))
            colocandoTesoro = False
    yOffset = mouseY - deslizadorY


def mouseDragged():
    global deslizadorY, porcentaje, yaJugo
    if barraBloqueada:
        yaJugo = False
        deslizadorY = mouseY - yOffset
        if deslizadorY < barraY:
            deslizadorY = barraY
        if deslizadorY > barraY + barraAlto:
            deslizadorY = barraY + barraAlto
        porcentaje = (float(barraY+barraAlto-deslizadorY)
                      * 100.0) / float(barraAlto)
        print(porcentaje)
        putObstacles()


def mouseReleased():
    barraBloqueada = False


# Método que retorna la imagen del valor del árbol
def seleccionarImagen(celda):
    return {
        0: imagenGrass,     # No existe árbol
        1: imagenArbol1,    # Árbol nivel 1
        2: imagenArbol2,    # Árbol nivel 2
        3: imagenArbol3,    # Árbol nivel 3
        4: imagenArbol4,    # Árbol nivel 4
        5: imagenArbol5     # Árbol nivel 5
    }.get(celda, imagenArbol5)  # Si el valor del parámetro es un número que no se encuentra en el intervalo [0 - 5] entonces retorno un árbol de nivel 5


# Creación de la estructura de datos 'Pila'
class Stack:
    # Método constructor
    def __init__(self):
        self.lista = []

    # Devuelve True o False si está vacío o no respectivamente
    def estaVacia(self):
        return self.lista == []

    # Inserta un elemento a la lista en la última posición
    def insertar(self, item):
        self.lista.append(item)

    # Devuelve y elimina el último elemento de la lista
    def soltar(self):
        return self.lista.pop()

    # Devuelve el último elemento de la lista
    def ultimoElemento(self):
        return self.lista[len(self.lista)-1]

    # Devuelve la cantidad de elementos de la lista
    def cantidad(self):
        return len(self.lista)
