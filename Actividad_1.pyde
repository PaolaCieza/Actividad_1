# Se importa el módulo que genera número aleatorios
import random

# Clase para los botones
class Boton:
    # Método constructor
    def __init__(self, x, y, ancho, alto, contenido):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.contenido = contenido
        self.color = (255, 255, 255)
        self.colorBorde = 0
        self.tamanoTexto = 20
        self.colorTexto = 0

    # Verifica si el mouse se encuentra sobre el botón
    def mouseEnBoton(self):
        return (self.x < mouseX < self.x + self.ancho and
                self.y < mouseY < self.y + self.alto)

    # Dibuja el botón
    def dibujar(self):
        stroke(self.colorBorde)
        fill(self.color[0], self.color[1], self.color[2])
        rect(self.x, self.y, self.ancho, self.alto)
        
        if (type(self.contenido) == str):
            fill(self.colorTexto)
            textSize(self.tamanoTexto)
            text(self.contenido, self.x + 5, self.y + 20)
        else:
            image(self.contenido, self.x, self.y, self.ancho, self.alto)

    # Cambia el color del botón cuando se clickea sobre él
    def clickeado(self):
        colorOriginal = self.color
        self.color = (0, 0, 0)
        self.dibujar()
        self.color = colorOriginal

# Cantidad de cuadros - 1 por fila o columna
cuadrosPorLado = 10

# Tiempo de delay
tiempoDelay = 50

# Genera un array que contendrá los cuadros del mapa  (filas y columnas)
mapa = [
    # Crea un array que contiene cuadrosPorLado (10) ceros: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    [0] * cuadrosPorLado
    # Repite lo anterior por cuadrosPorLado (10) veces
    for i in range(cuadrosPorLado)
]

# Se especifica el tamaño del mapa
tamanoMapa = 600 / cuadrosPorLado

# (x,y) Coordenadas iniciales del avatar
avatarX = 0
avatarY = 0

# (x,y) Coordenadas iniciales del tesoro
# El mapa es un array de 10 elementos por eso empieza a contar desde 0 y ubica al tesoro en las coordenadas (9, 9)
tesoroX = (cuadrosPorLado - 1)
tesoroY = (cuadrosPorLado - 1)

# Botones de Métodos
botonBresenham  = Boton(620, 20, 170, 25, "Bresenham")
botonDDA        = Boton(620, 60, 170, 25, "DDA")
botonMetodo3    = Boton(620, 100, 170, 25, "Metodo 3")
botonMetodo4    = Boton(620, 140, 170, 25, "Laberinto")

# Cantidad de Pasos
anchoPasos = 50
pasosBresenham  = Boton(botonBresenham.x + botonBresenham.ancho, botonBresenham.y, anchoPasos, botonBresenham.alto, "0")
pasosMetodo2    = Boton(botonDDA.x + botonDDA.ancho, botonDDA.y, anchoPasos, botonDDA.alto, "0")
pasosMetodo3    = Boton(botonMetodo3.x + botonMetodo3.ancho, botonMetodo3.y, anchoPasos, botonMetodo3.alto, "0")
pasosMetodo4    = Boton(botonMetodo4.x + botonMetodo4.ancho, botonMetodo4.y, anchoPasos, botonMetodo4.alto, "0")

# Botón de reinicio
botonReinicio = Boton(620, 550, 220, 25, "Reiniciar")

# Barra
barra       = Boton(720, 290, 20, 200, "")
barra.color = (0, 0, 0)

# Coordenadas y tamaño del deslizador de la barra
deslizador                  = Boton(barra.x - 5, barra.y + barra.alto, 30, 20, "")
deslizador.color            = (255, 0, 0)
mouseSobreDeslizador        = False
deslizadorMoviendose        = False
espacioFaltante             = 0.0

# Coordenadas y porcentaje de barra en texto
porcentajeX = barra.x
porcentajeY = barra.y - 5
porcentaje  = 0.0

# Variables para la ruta a seguir por el avatar
global rutaEncontrada, rutaRecorrida, pasosm2
iteradorRuta = 0


# Configuración de la interfaz y el juego
def setup():
    # Tamaño de la ventana
    size(860, 600)
    
    global jugando, colocandoAvatar, colocandoTesoro, rutaEncontrada, rutaRecorrida, yaJugo, metodoBusqueda
    global imagenGrass, imagenAvatar, imagenTesoro, imagenArbol1, imagenArbol2, imagenArbol3, imagenArbol4, imagenArbol5
    global botonAvatar, botonTesoro

    # Lectura de imagenes
    imagenAvatar    = loadImage("assets/avatar.png")
    imagenGrass     = loadImage("assets/grass3.JPG")
    imagenTesoro    = loadImage("assets/treasure.PNG")
    imagenArbol1    = loadImage("assets/tree1.png")
    imagenArbol2    = loadImage("assets/tree2.png")
    imagenArbol3    = loadImage("assets/tree3.png")
    imagenArbol4    = loadImage("assets/tree4.png")
    imagenArbol5    = loadImage("assets/tree5.png")

    # Botón para colocar el avatar y el tesoro
    botonAvatar = Boton(640, 180, 70, 70, imagenAvatar)
    botonTesoro = Boton(750, 180, 70, 70, imagenTesoro)

    # Configuración inicial del juego
    jugando             = False
    colocandoAvatar     = False
    colocandoTesoro     = False
    rutaEncontrada      = []
    rutaRecorrida       = Pila()
    iteradorRuta        = 0
    metodoBusqueda      = "Ninguno"
    yaJugo              = False

# Método que se ejecuta siempre
def draw():
    # Si el usuario está jugando entonces el programa encuentra la ruta
    if jugando:
        recorrerCamino()
        delay(tiempoDelay)
    
    # Siempre se dibuja la interfaz
    dibujarInterfaz()


# Método que muestra la interfaz
def dibujarInterfaz():
    background(255)
    dibujarMapa()
    dibujarBotones()
    mostrarPorcentajeBarra()


# Método que dibuja los botones
def dibujarBotones():
    botonAvatar.dibujar()
    botonTesoro.dibujar()

    botonBresenham.dibujar()
    botonDDA.dibujar()
    botonMetodo3.dibujar()
    botonMetodo4.dibujar()

    # Dibujar los cuadrados de Pasos
    pasosBresenham.dibujar()
    pasosMetodo2.dibujar()
    pasosMetodo3.dibujar()
    pasosMetodo4.dibujar()

    dibujarDeslizador()

    botonReinicio.dibujar()

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


# Método que dibuja el deslizador
def dibujarDeslizador():
    barra.dibujar()
    global mouseSobreDeslizador

    # Variable de control que guarda si el mouse está sobre el deslizador
    mouseSobreDeslizador = deslizador.mouseEnBoton()

    # Esto agrega un efecto de hover sobre el deslizador
    if mouseSobreDeslizador:
        deslizador.colorBorde = 120
    else:
        deslizador.colorBorde = 255

    deslizador.dibujar()


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


# Muestra el porcentaje de la barra en un texto
def mostrarPorcentajeBarra():
    text(str(porcentaje) + " %", porcentajeX - 20, porcentajeY)


# Método que se ejecuta cuando se gana
def ganar():
    global yaJugo, bresenhamActivado, jugando
    print("GANASTE")
    yaJugo              = True
    jugando             = False
    metodoBusqueda      = "Ninguno"


# Método que se ejecuta cuando se pierde
def perder():
    global yaJugo, bresenhamActivado, jugando
    print("PERDISTE")
    yaJugo              = True
    jugando             = False
    metodoBusqueda      = "Ninguno"


# Método que quita el avatar del mapa
def quitarAvatar():
    global avatarX, avatarY
    avatarX = -1000/tamanoMapa
    avatarY = -1000/tamanoMapa


# Método que quita el tesoro del mapa
def quitarTesoro():
    global tesoroX, tesoroY
    tesoroX = -1000/tamanoMapa
    tesoroY = -1000/tamanoMapa


# Método que limpia el mapa de árboles
def limpiarMapa():
    for i in range(cuadrosPorLado):
        for j in range(cuadrosPorLado):
            mapa[i][j] = 0


# Método que coloca los árboles cuando el deslizador es movido
def colocarArboles():
    global avatarX, avatarY, tesoroX, tesoroY
    
    # Realiza un mapeo de las coordenadas del mapa
    coordenadas = [ [ (j, i) for i in range(cuadrosPorLado) ] for j in range(cuadrosPorLado) ]

    limpiarMapa()

    totalCuadros = cuadrosPorLado * cuadrosPorLado

    # Calcula la cantidad de árboles a colocar
    cantidadArboles = int(totalCuadros * porcentaje) / 100

    # Si el avatar ganó entonces lo devuelve al inicio y el tesoro también
    if avatarX == tesoroX and avatarY == tesoroY:
        avatarX = 0
        avatarY = 0
        tesoroX = cuadrosPorLado - 1
        tesoroY = cuadrosPorLado - 1

    # Si los árboles tienen que ocupar todo el mapa entonces deja espacio para el avatar y el tesoro
    if cantidadArboles > totalCuadros - 2:
        cantidadArboles = totalCuadros - 2
    
    # Remueve de los posibles lugares de aparición de árboles las coordenadas del avatar y del tesoro
    coordenadas[avatarX].remove((avatarX, avatarY))
    coordenadas[tesoroX].remove((tesoroX, tesoroY))

    # Realiza un bucle para colocar los árboles
    while cantidadArboles > 0:
        # Escoge una fila del mapa manera aleatoria
        filaEscogida = random.choice(coordenadas)

        # Si por azares del destino la fila está vacía entonces vuelve a escoger otra fila
        while len(filaEscogida) == 0:
            filaEscogida = random.choice(coordenadas)

        # De la fila escogida se escoge una coordenada de manera aleatoria
        coordenadaEscogida = random.choice(filaEscogida)

        # Coloca el árbol en la posición escogida
        mapa[coordenadaEscogida[0]][coordenadaEscogida[1]] = 5

        # Como ya colocó ese árbol entonces disminuye la cantidad de árboles a colocar
        cantidadArboles = cantidadArboles - 1

        # Elimina de las opciones a escoger las coordenadas del árbol colocado
        filaEscogida.remove(coordenadaEscogida)


# Método que encuentra la ruta
def recorrerCamino():
    global avatarX, avatarY, rutaRecorrida, jugando, iteradorRuta, mapa, yaJugo, metodoBusqueda, rutaEncontrada
    
    # Array que guarda las alternativas para cambiar la posición inicial del avatar cuando se encuentra con un árbol
    alternativas = []

    # Se comprueba si el programa ganó
    if avatarX == tesoroX and avatarY == tesoroY:
        ganar()
        return

    # Si el método de búsqueda está seleccionado entonces ejecuta el método de bresenham
    if metodoBusqueda == "Bresenham":
        bresenham(avatarX, avatarY, tesoroX, tesoroY)
    elif metodoBusqueda == "DDA":
        dda(avatarX, avatarY, tesoroX, tesoroY)
    elif metodoBusqueda == "Laberinto":
        busquedaLaberinto()
        return

    # Comprueba si la ruta tiene al menos una posición y si en la posición del avatar existe un árbol
    if len(rutaEncontrada) > 1 and mapa[rutaEncontrada[iteradorRuta][0]][rutaEncontrada[iteradorRuta][1]] < 5:
        # Se guarda el recorrido del avatar
        rutaRecorrida.insertar( (avatarX, avatarY) )

        # Se cambia la posición del avatar a la siguiente posición de la ruta establecida
        avatarX = rutaEncontrada[iteradorRuta][0]
        avatarY = rutaEncontrada[iteradorRuta][1]

        # Imprime en consola la posición actual del avatar
        print("Avatar en: (" + str(avatarX) + "," + str(avatarY) + ")")

        # Se comprueba si el avatar llegó a su destino
        if(avatarX == tesoroX and avatarY == tesoroY):
            # Gana
            ganar()
            return
        
        # Si el avatar no ha llegado a su destino entonces se pasa a la siguiente posición de la ruta
        iteradorRuta = iteradorRuta + 1

        # Se cambia a False para que no establezca una nueva ruta mientras se recorra la ruta actual
        if metodoBusqueda == "Bresenham":
            metodoBusqueda = "b"
        elif metodoBusqueda == "DDA":
            metodoBusqueda = "d"
        elif metodoBusqueda == "Laberinto":
            metodoBusqueda = "l"

        return
    else:
        # Si en la siguiente posición de la ruta existe un árbol entonces en la posición actual del mapa aumenta en 1 para que si vuelve a pasar y
        # existe el árbol se cree un nuevo árbol al llegar a 5 pasadas
        mapa[avatarX][avatarY] = mapa[avatarX][avatarY] + 1
    
    # Como encontró un árbol entonces tiene que establecer una nueva ruta
    if metodoBusqueda == "b":
        metodoBusqueda = "Bresenham"
    elif metodoBusqueda == "d":
        metodoBusqueda = "DDA"
    elif metodoBusqueda == "l":
        metodoBusqueda = "Laberinto"

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
            if 0 <= cambioCoordenadaX <= cuadrosPorLado - 1 and 0 <= cambioCoordenadaY <= cuadrosPorLado - 1:
                
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
    posicionEscogida = random.choice(alternativas)

    # Inserta a la ruta recorrida la posición del avatar
    rutaRecorrida.insertar((avatarX, avatarY))

    # Coloca al avatar en la nueva posición encontrada
    avatarX = avatarX + posicionEscogida[0]
    avatarY = avatarY + posicionEscogida[1]

    # Comprueba si con la nueva posición ganó
    if(avatarX == tesoroX and avatarY == tesoroY):
        # Gana
        ganar()
        return

def busquedaLaberinto():
    #SE BUSCARÁ EL CAMINO MAS CORTO ENUMERANDO CADA CASILLA DISPONIBLE DESDE EL TESORO HASTA EL AVATARY LUEGO SE RECORRERÁ EL CAMINO EN REVERSA
    global mapeadoM2, tesoroX, tesoroY, avatarX, avatarY, pasosm2
    
    #COMPROBAR SI YA GANÓ
    if avatarX == tesoroX and avatarY == tesoroY:
        ganar()
        return
    
    #SI NO HA GANADO SE INICIA EL ETIQUETADO
    mapeadoM2 = [[0] * cuadrosPorLado
    for i in range(cuadrosPorLado)]
    #mapear arboles
    for i in range(cuadrosPorLado):
        for j in range(cuadrosPorLado):
            if mapa[i][j] == 5:
                mapeadoM2[i][j] = 'x'
    
    #Establecer tesoro(Inicio del Laberinto)
    mapeadoM2[tesoroX][tesoroY] = 0
    
    #empezar a enumerar los caminos
    numerar(tesoroX, tesoroY)
    
    partidaX = avatarX
    partidaY = avatarY
    print(mapeadoM2)
    
    while pasosm2 < mapeadoM2[partidaX][partidaY]:
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= avatarX+x <= cuadrosPorLado - 1 and 0 <= avatarY+y <= cuadrosPorLado - 1:
                    if mapeadoM2[avatarX+x][avatarY+y] == mapeadoM2[avatarX][avatarY]-1:
                        avatarX += x
                        avatarY += y
                        pasosm2 += 1
    if pasosm2 == 0:
        perder()
    else:
        ganar()
    print(pasosm2)

def numerar(actualX, actualY):
    global mapeadoM2, pasosm2, tesoroX, tesoroY
    for x in range(-1, 2):
        for y in range(-1, 2):
            if 0 <= actualX+x <= cuadrosPorLado - 1 and 0 <= actualY+y <= cuadrosPorLado - 1:
                if mapeadoM2[actualX+x][actualY+y] != 'x' and (actualX+x != tesoroX or actualY+y != tesoroY):
                    if mapeadoM2[actualX+x][actualY+y]==0 or mapeadoM2[actualX+x][actualY+y] > mapeadoM2[actualX][actualY] + 1:
                        mapeadoM2[actualX+x][actualY+y] = mapeadoM2[actualX][actualY] + 1
                        numerar(actualX+x, actualY+y)

def dda(coordenadaAvatarX, coordenadaAvatarY, coordenadaTesoroX, coordenadaTesoroY):
    global rutaEncontrada, iteradorRuta
    iteradorRuta = 0
    rutaEncontrada = []
    dx = coordenadaTesoroX - coordenadaAvatarX
    dy = coordenadaTesoroY - coordenadaAvatarY

    if abs(dx) >= abs(dy):
        res = abs(dx)
    else:
        res = abs(dy)
    
    ax = float(dx) / float(res)
    ay = float(dy) / float(res)

    i = 1
    x = coordenadaAvatarX
    y = coordenadaAvatarY
    
    while i <= res:
        x = x + ax
        y = y + ay
        i = i + 1
        rutaEncontrada.append( (int(round(x)), int(round(y))) )


def bresenham(coordenadaAvatarX, coordenadaAvatarY, coordenadaTesoroX, coordenadaTesoroY):
    global rutaEncontrada, iteradorRuta
    iteradorRuta = 1
    rutaEncontrada = []

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

        # Inserta la coordenada siguiente en la lista rutaEncontrada
        rutaEncontrada.append( ( coordenadaX, coordenadaY ) )

        print("\tPosicion N " + str(x + 1) + ": (" + str(coordenadaX) + ", " + str(coordenadaY) + ")")

        # Con esto verifica si el avatar se movió 1 unidad o no en el eje menor
        # Pero como sí o sí se hacen los cálculos como si dx fuese mayor entonces se incrementa en Y aveces
        if constanteP >= 0:
            y = y + 1
            # Este cálculo se hace por el algoritmo
            constanteP = constanteP - 2 * distanciaX
        # Este cálculo se hace por el algoritmo
        constanteP = constanteP + 2 * distanciaY


# Método que se ejecuta cuando el click izquierdo del mouse es presionado
def mousePressed():
    global colocandoTesoro, colocandoAvatar, mouseSobreDeslizador, deslizadorMoviendose, espacioFaltante, jugando, mapa, yaJugo, metodoBusqueda, pasosm2
    global avatarX, avatarY, tesoroX, tesoroY

    # Con estos ifs se comprueba si el mouse está sobre un botón
    # Les da un efecto de 'botón presionado' y realizan sus respectivas acciones

    if botonBresenham.mouseEnBoton():
        yaJugo              = False
        jugando             = True
        metodoBusqueda      = "Bresenham"
        botonBresenham.clickeado()

    if botonDDA.mouseEnBoton():
        yaJugo              = False
        jugando             = True
        metodoBusqueda      = "DDA"
        botonDDA.clickeado()

    if botonMetodo3.mouseEnBoton():
        botonMetodo3.clickeado()

    if botonMetodo4.mouseEnBoton():
        yaJugo = False
        jugando = True
        metodoBusqueda = "Laberinto"
        pasosm2=0
        botonMetodo4.clickeado()

    if botonAvatar.mouseEnBoton():
        yaJugo = False
        botonAvatar.clickeado()
        quitarAvatar()
        colocandoAvatar = True

    if botonTesoro.mouseEnBoton():
        yaJugo = False
        botonTesoro.clickeado()
        quitarTesoro()
        colocandoTesoro = True

    if botonReinicio.mouseEnBoton():
        botonReinicio.clickeado()
        yaJugo = False
        colocarArboles()

    deslizadorMoviendose = mouseSobreDeslizador

    # Cuando se hace click sobre el mapa hace cosas
    if (mouseX/tamanoMapa) < cuadrosPorLado and (mouseY/tamanoMapa) < cuadrosPorLado:
        yaJugo = False

        # Si hay un árbol en el lugar donde se clickeó entonces lo quita
        if mapa[mouseY / tamanoMapa][mouseX / tamanoMapa] == 5:
            mapa[mouseY / tamanoMapa][mouseX / tamanoMapa] = 0
        # caso contrario...
        else:
            mapa[mouseY / tamanoMapa][mouseX / tamanoMapa] = 5

        # Si se presionó el botón para colocar al avatar entonces el lugar donde se clickeó en el mapa es donde se coloca
        if colocandoAvatar:
            avatarX = mouseY / tamanoMapa
            avatarY = mouseX / tamanoMapa

            # Si existe un árbol entonces lo quita 
            if (0 <= mapa[avatarX][avatarY] <= 5):
                mapa[avatarX][avatarY] = 0

            print("Avatar colocado en: (" + str(avatarX) + ", " + str(avatarY) + ")")
            colocandoAvatar = False
        
        # lo mismo pero para el tesoro
        elif colocandoTesoro:
            tesoroX = mouseY / tamanoMapa
            tesoroY = mouseX / tamanoMapa
            
            # Si existe un árbol entonces lo quita 
            if (0 <= mapa[tesoroX][tesoroY] <= 5):
                mapa[tesoroX][tesoroY] = 0

            print("Tesoro colocado en: (" + str(tesoroX) + ", " + str(tesoroY) + ")")
            colocandoTesoro = False

    espacioFaltante = mouseY - deslizador.y


# Método que se ejecuta cuando el click izquierdo del mouse se mantiene presionado
def mouseDragged():
    global porcentaje, yaJugo

    # Se comprueba si el deslizador se está moviendo
    if deslizadorMoviendose:
        # Aún no se está jugando
        yaJugo = False

        # Vainas para que el deslizador se mueva
        deslizador.y = mouseY - espacioFaltante

        # y que no se salga de la barra
        if deslizador.y < barra.y:
            deslizador.y = barra.y

        if deslizador.y > barra.y + barra.alto:
            deslizador.y = barra.y + barra.alto

        # Se calcula el porcentaje que colocó el usuario
        porcentaje = (float( barra.y + barra.alto - deslizador.y) * 100.0) / float(barra.alto)

        colocarArboles()


def mouseReleased():
    deslizadorMoviendose = False


# Creación de la estructura de datos 'Pila'
class Pila:
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
