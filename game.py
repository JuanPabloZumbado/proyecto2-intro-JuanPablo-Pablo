import pygame
import random
import pygame_gui

#Import de los demas archivos
import usuarios
import casillas as c
import personajes

pygame.init()

# =========================================================
# 1) CONSTANTES Y CONFIG
# =========================================================

puntuacion_escapa = []
puntuacion_caza = []

ANCHO = 1125
ALTO = 700

FONT_RETRO = pygame.font.Font("Retro Gaming.ttf", 20)
FONT_UPHEAT = pygame.font.Font("upheavtt.ttf", 32)
FONT_UPHEAT_LITLE = pygame.font.Font("upheavtt.ttf", 26)
FONT_UPHEAT_BIG = pygame.font.Font("upheavtt.ttf", 45)

CLOCK = pygame.time.Clock()
FPS = 60
COLDOWN = 500
MANAGER = pygame_gui.UIManager((ANCHO,ALTO))

screen = pygame.display.set_mode((ANCHO, ALTO))

#-----------------Editar ventana-------------------
pygame.display.set_caption("Scape Hunters")

icon = pygame.image.load(".\SplahArts\cazador.png")
icon_optimizado = icon.convert_alpha()
pygame.display.set_icon(icon_optimizado)

#-----------Creacion de espacios para el juego----------------
background = pygame.image.load(".\SplahArts\game_background.png")
background_optimizado = background.convert()

# -------- Elementos pantalla de inicio -------------------

title = pygame.image.load(".\SplahArts\ktittle_game.png")
tittle_optimizado = title.convert_alpha()

boton_empezar = pygame.image.load(".\SplahArts\kboton_empezar.png")
boton_empezar_optimizado = boton_empezar.convert_alpha()
rect_boton = boton_empezar_optimizado.get_rect()

# -------- Elementos pantalla de nombre -------------------

text_nombre_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((ANCHO / 2 - 150, ALTO / 2 - 50), (300, 50)),
    manager=MANAGER, object_id="#texto_nombre"
)

fondo_ingreso = pygame.image.load(".\SplahArts\kfondo_ingreso.png")
fondo_ingreso_optimizado = fondo_ingreso.convert_alpha()

# -------- Elementos pantalla de podio -------------------

podio_fondo = pygame.image.load(".\SplahArts\podio_fondo.png").convert_alpha()
usuario_fondo = pygame.image.load(".\SplahArts\kusuario_fondo.png").convert_alpha()

boton_escapa = pygame.image.load(".\SplahArts\kboton_escapa.png").convert_alpha()
rect_boton_escapa = boton_escapa.get_rect()

boton_caza = pygame.image.load(".\SplahArts\kboton_caza.png").convert_alpha()
rect_boton_caza = boton_caza.get_rect()

# -------- Elementos pantalla de juego -------------------

game_bar = pygame.image.load(".\SplahArts\game_bar.png").convert_alpha()

# -------- Elementos pantalla de Victoria -------------------

btn_victoria = pygame.image.load(".\SplahArts\kvictoria_volver_btn.png").convert_alpha()
btn_victoria_rect = btn_victoria.get_rect()

# -------- Elementos pantalla de Perdio -------------------

btn_rendirse = pygame.image.load(".\SplahArts\krendirse_btn.png").convert_alpha()
btn_rendirse_rect = btn_rendirse.get_rect()


# =========================================================
# 2) MAPA ALEATORIO CON CAMINO GARANTIZADO
# =========================================================

CAMINO, ENTRADA, SALIDA, TRAMPA, LIANA, TUNEL, MURO = 0,1,2,3,4,5,6

def generar_mapa_aleatorio(filas=7, cols=14, p_muro=0.35, p_liana=0.08, p_tunel=0.08):
    mapa = [[MURO for _ in range(cols)] for _ in range(filas)]

    # Esquinas opuestas por pares
    pares_opuestos = [
        ((0, 0), (filas-1, cols-1)),          # sup-izq  <-> inf-der
        ((0, cols-1), (filas-1, 0))           # sup-der  <-> inf-izq
    ]

    entrada, salida = random.choice(pares_opuestos)
    er, ec = entrada
    sr, sc = salida

    mapa[er][ec] = ENTRADA
    mapa[sr][sc] = SALIDA

    # Tallar camino garantizado (random walk acercándose a salida)
    r, c = er, ec
    while (r, c) != (sr, sc):
        opciones = []
        if r > 0: opciones.append((r-1, c))
        if r < filas-1: opciones.append((r+1, c))
        if c > 0: opciones.append((r, c-1))
        if c < cols-1: opciones.append((r, c+1))

        def dist(pos):
            return abs(pos[0]-sr) + abs(pos[1]-sc)

        opciones.sort(key=dist)
        if random.random() < 0.7:
            r, c = opciones[0]
        else:
            r, c = random.choice(opciones)

        if (r, c) != (sr, sc):
            mapa[r][c] = CAMINO

    # Rellenar resto
    for i in range(filas):
        for j in range(cols):
            if mapa[i][j] in (ENTRADA, SALIDA, CAMINO):
                continue
            roll = random.random()
            if roll < p_muro:
                mapa[i][j] = MURO
            elif roll < p_muro + p_liana:
                mapa[i][j] = LIANA
            elif roll < p_muro + p_liana + p_tunel:
                mapa[i][j] = TUNEL
            else:
                mapa[i][j] = CAMINO
    return mapa

def generar_matriz_mapa(mapa):
    initial_y = 20
    mapa_obj = [[0 for _ in range(len(mapa[0]))] for _ in range(len(mapa))]
    for fila in range(len(mapa)):
        initial_x = 40
        for col in range(len(mapa[0])):
            if mapa[fila][col] == 0: casilla = c.Camino(initial_x, initial_y)
            if mapa[fila][col] == 1: casilla = c.Entrada(initial_x, initial_y)
            if mapa[fila][col] == 2: casilla = c.Salida(initial_x, initial_y)
            if mapa[fila][col] == 3: casilla = c.Trampa(initial_x, initial_y)
            if mapa[fila][col] == 4: casilla = c.Liana(initial_x, initial_y)
            if mapa[fila][col] == 5: casilla = c.Tunel(initial_x, initial_y)
            if mapa[fila][col] == 6: casilla = c.Muro(initial_x, initial_y)

            mapa_obj[fila][col] = casilla
            initial_x += 75
        initial_y += 75

    return mapa_obj

#Funcion obtener cordenadas iniciales del mapa
def initial_cords(mapa_obj):
    initial_x = 0
    initial_y = 0
    for fila in range(len(mapa_obj)):
        for col in range(len(mapa_obj[0])):
            if (mapa_obj[fila][col]).type_id == 1:
                initial_x = (mapa_obj[fila][col]).x + ((mapa_obj[fila][0]).ancho / 2)
                initial_y = (mapa_obj[fila][col]).y + ((mapa_obj[fila][0]).altura / 2)
    return initial_x, initial_y

#Funcion que optiene todos los obstaculos para el jugador que escapa
def obst_escapa(mapa_obj):
    obstaculos = []
    for fila in range(len(mapa_obj)):
        for col in range(len(mapa_obj[0])):
            if (mapa_obj[fila][col]).type_id == 4 or (mapa_obj[fila][col]).type_id == 6:
                obstaculos.append((mapa_obj[fila][col]).colision)
    return obstaculos

#---------Funcion imprimir mapa-----------
def imprimir_mapa(mapa_obj):
    screen.fill((0,0,0))
    screen.blit(background_optimizado,(0,0))

    for fila in range(len(mapa_obj)):
        for col in range(len(mapa_obj[0])):
            fondo_casilla = pygame.image.load((mapa_obj[fila][col]).splash).convert_alpha()
            screen.blit(fondo_casilla, ((mapa_obj[fila][col]).x, (mapa_obj[fila][col]).y))

    screen.blit(game_bar, (50, ALTO - 150))
    pygame.display.update()

#----------Funcion ordenar lista-------------
def ordenar_puntuacion(lista):
    if not lista: return lista
    for i in range(len(lista)):
        mayor = i
        for j in range(i + 1, len(lista)):
            if lista[j][1] > lista[mayor][1]: mayor = j
        lista[i], lista[mayor] = lista[mayor], lista[i]
    return lista

#----------Funcion de la pantalla de inicio-----------
def pantalla_de_inicio():
    screen.fill((0,0,0))
    screen.blit(background_optimizado,(0,0))
    screen.blit(tittle_optimizado, (300,50))

    screen.blit(boton_empezar_optimizado, (ANCHO / 2 - 120, ALTO / 2 + 100))
    rect_boton.left = ANCHO / 2 - 120
    rect_boton.top = ALTO / 2 + 100

    pygame.display.update()

#------Funcion para mostrar el podio de ambos modos------
def pantalla_de_podio():
    screen.fill((0,0,0))
    screen.blit(background_optimizado,(0,0))

    screen.blit(podio_fondo, (30, 20))
    screen.blit(podio_fondo, (ANCHO / 2 + 30, 20))

    texto_modo_escapa = FONT_UPHEAT.render("MODO ESCAPA", True, (166, 144, 114))
    screen.blit(texto_modo_escapa, (175, 60))

    if puntuacion_escapa:
        y_inicial = 100
        ord_punt_escapa = ordenar_puntuacion(puntuacion_escapa)
        for usu in range(len(ord_punt_escapa)):
            if usu < 5:
                texto_podio = FONT_RETRO.render(
                    f"{usu + 1} Lugar: {ord_punt_escapa[usu][0]} - {ord_punt_escapa[usu][1]}",
                    True, (204, 186, 159)
                )
                screen.blit(texto_podio,(100, y_inicial))
                y_inicial += 50

    texto_modo_cazador = FONT_UPHEAT.render("MODO CAZADOR", True, (166, 144, 114))
    screen.blit(texto_modo_cazador, (ANCHO / 2 + 175, 60))

    if puntuacion_caza:
        y_inicial = 100
        ord_punt_caza = ordenar_puntuacion(puntuacion_caza)
        for usu in range(len(ord_punt_caza)):
            if usu < 5:
                texto_podio = FONT_RETRO.render(
                    f"{usu + 1} Lugar: {ord_punt_caza[usu][0]} - {ord_punt_caza[usu][1]}",
                    True, (204, 186, 159)
                )
                screen.blit(texto_podio,(ANCHO / 2 + 100, y_inicial))
                y_inicial += 50

    screen.blit(usuario_fondo, (ANCHO / 2 - 240, ALTO / 2 + 175))

    texto_usuario = FONT_UPHEAT_LITLE.render(
        f"{usuario.nombre_usuario} - Puntos: {usuario.puntuacion}",
        True, (204, 186, 159)
    )
    screen.blit(texto_usuario, (ANCHO / 2 - 190, ALTO / 2 + 230))

    texto_elegir = FONT_UPHEAT.render("ESCOGE UN MODO DE JUEGO:", True, (255, 255, 255))
    screen.blit(texto_elegir, (ANCHO / 2 - 200, ALTO / 2 + 125))

    screen.blit(boton_escapa, (30, ALTO / 2 + 210))
    rect_boton_escapa.left = 30
    rect_boton_escapa.top = ALTO / 2 + 210

    screen.blit(boton_caza, (ANCHO / 2 + 275, ALTO / 2 + 210))
    rect_boton_caza.left = ANCHO / 2 + 275
    rect_boton_caza.top = ALTO / 2 + 210

    pygame.display.update()

#Funcion para obtener la casilla de Salida

def initial_cords_enemy(mapa_obj):
    initial_x = 0
    initial_y = 0
    for fila in range(len(mapa_obj)):
        for col in range(len(mapa_obj[0])):
            if (mapa_obj[fila][col]).type_id == 2:
                initial_x = (mapa_obj[fila][col]).x + ((mapa_obj[fila][0]).ancho / 2)
                initial_y = (mapa_obj[fila][col]).y + ((mapa_obj[fila][0]).altura / 2)
    return initial_x, initial_y

#Funcion para pbtener los obstaculos del enemigo

def obst_cazador(mapa_obj):
    obstaculos = []
    for fila in range(len(mapa_obj)):
        for col in range(len(mapa_obj[0])):
            if (mapa_obj[fila][col]).type_id == 5 or (mapa_obj[fila][col]).type_id == 6:
                obstaculos.append((mapa_obj[fila][col]).colision)
    return obstaculos

# ---------------------------------------------------------
# Helpers mínimos para detectar salida
# ---------------------------------------------------------
def casilla_actual(rect_personaje, mapa_obj):
    for fila in mapa_obj:
        for cas in fila:
            if cas.colision.collidepoint(rect_personaje.center):
                return cas
    return None

def llego_a_salida(personaje, mapa_obj):
    cas = casilla_actual(personaje.forma, mapa_obj)
    return cas and cas.type_id == SALIDA


# =========================================================
# 4) CREAR MAPA ALEATORIO INICIAL
# =========================================================
mapa = generar_mapa_aleatorio()
mapa_obj = generar_matriz_mapa(mapa)
initial_x_p, initial_y_p = initial_cords(mapa_obj)
obstaculos_escapa = obst_escapa(mapa_obj)


obstaculos_escapa.append(pygame.Rect(35, 0, 5, ALTO))
obstaculos_escapa.append(pygame.Rect(1090, 0, 5, ALTO))
obstaculos_escapa.append(pygame.Rect(0, 15, ANCHO, 5))
obstaculos_escapa.append(pygame.Rect(0, 545, ANCHO, 5))

# =========================================================
# 5) VARIABLES DE MOVIMIENTO / ESTADO
# =========================================================

mover_derecha = False
mover_izquierda = False
mover_arriba = False
mover_abajo = False

victoria = False
perdio = False
inicio_juego = True 
mostrar_ingreso = True
mostrar_inicio = True
mostrar_podio = True
modo_escapa = False
modo_caza = False

running = True

# timer para puntaje escapa
start_time = 0
dificultad_mult = 1.5

# =========================================================
# 6) LOOP PRINCIPAL
# =========================================================
while running:
    if mostrar_inicio:

        pantalla_de_inicio()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_boton.collidepoint(event.pos):
                    mostrar_inicio = False

    else: 
        if mostrar_ingreso:

            UI_REFRESH_RATE = CLOCK.tick(60)/1000

            screen.fill((0,0,0))
            screen.blit(background_optimizado,(0,0))
            screen.blit(fondo_ingreso_optimizado, (ANCHO / 2 - 390, ALTO / 2 - 300)) 

            texto_ingreso = FONT_UPHEAT.render("INGRESE SU NOMBRE (10 CARAC MAX):", True, (166, 144, 114))
            screen.blit(texto_ingreso, (ANCHO / 2 - 290, ALTO / 2 - 125))

            texto_press_enter = FONT_RETRO.render("Presionar ENTER para seguir", True, (166, 144, 114))
            screen.blit(texto_press_enter, (ANCHO / 2 - 185, ALTO / 2 + 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Este if evalua que el text box se complete y se aprete enter para seguir el codigo

                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#texto_nombre":
                    #Se evalua si el espacio esta lleno o si es menor a 10 carac en caso de q no, se pone nombre default
                    if event.text and len(event.text) <= 10:
                        usuario = usuarios.Usuarios(event.text)
                    else:
                        usuario = usuarios.Usuarios("JUGADOR")  #En caso de no ingresar nada se pone un nombre predeterminado
                    mostrar_ingreso = False

                MANAGER.process_events(event)

            MANAGER.update(UI_REFRESH_RATE)
            MANAGER.draw_ui(screen)
            pygame.display.update()

        else: 
            if mostrar_podio:

                pantalla_de_podio()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        # ---------------- NUEVA PARTIDA ESCAPA ----------------
                        if rect_boton_escapa.collidepoint(event.pos):
                            mostrar_podio = False
                            modo_escapa = True

                            # regenerar mapa aleatorio por partida
                            mapa = generar_mapa_aleatorio()
                            mapa_obj = generar_matriz_mapa(mapa)
                            initial_x_p, initial_y_p = initial_cords(mapa_obj)
                            initial_x_e, initial_y_e = initial_cords_enemy(mapa_obj)
                            obstaculos_escapa = obst_escapa(mapa_obj)
                            obstaculos_cazador = obst_cazador(mapa_obj)
                            obstaculos_escapa += [
                                pygame.Rect(35, 0, 5, ALTO),
                                pygame.Rect(1090, 0, 5, ALTO),
                                pygame.Rect(0, 15, ANCHO, 5),
                                pygame.Rect(0, 545, ANCHO, 5),
                            ]

                            obstaculos_cazador += [
                                pygame.Rect(35, 0, 5, ALTO),
                                pygame.Rect(1090, 0, 5, ALTO),
                                pygame.Rect(0, 15, ANCHO, 5),
                                pygame.Rect(0, 545, ANCHO, 5),
                            ]

                            personaje = personajes.UExplorador(initial_x_p, initial_y_p)
                            enemigo = personajes.EnemigoCazador(initial_x_e, initial_y_e)
                            start_time = pygame.time.get_ticks()

                        # ---------------- NUEVA PARTIDA CAZA ----------------
                        if rect_boton_caza.collidepoint(event.pos):
                            mostrar_podio = False
                            modo_caza = True

                            # regenerar mapa aleatorio por partida
                            mapa = generar_mapa_aleatorio()
                            mapa_obj = generar_matriz_mapa(mapa)
                            initial_x_p, initial_y_p = initial_cords(mapa_obj)
                            obstaculos_escapa = obst_escapa(mapa_obj)
                            obstaculos_escapa += [
                                pygame.Rect(35, 0, 5, ALTO),
                                pygame.Rect(1090, 0, 5, ALTO),
                                pygame.Rect(0, 15, ANCHO, 5),
                                pygame.Rect(0, 545, ANCHO, 5),
                            ]

                            personaje = personajes.UExplorador(initial_x_p, initial_y_p)
                            start_time = pygame.time.get_ticks()

            else:
                # =====================================================
                # MODO ESCAPA
                # =====================================================
                if modo_escapa:
                    CLOCK.tick(FPS)

                    imprimir_mapa(mapa_obj)

                    #Calcular movimiento del jugador

                    delta_x = 0
                    delta_y = 0

                    if mover_derecha:
                        delta_x = 5
                    if mover_izquierda:
                        delta_x = -5
                    if mover_arriba:
                        delta_y = -5
                    if mover_abajo:
                        delta_y = 5

                    #Mover personaje
                    personaje.mover_personaje(delta_x, delta_y, obstaculos_escapa)
                    enemigo.seguir_jugador(personaje, obstaculos_cazador)
                    personaje.imprimir_personaje(screen)
                    enemigo.imprimir_personaje(screen)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False


                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_a:
                                mover_izquierda = True
                            if event.key == pygame.K_d:
                                mover_derecha = True
                            if event.key == pygame.K_w:
                                mover_arriba = True
                            if event.key == pygame.K_s:
                                mover_abajo = True

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_a:
                                mover_izquierda = False
                            if event.key == pygame.K_d:
                                mover_derecha = False
                            if event.key == pygame.K_w:
                                mover_arriba = False
                            if event.key == pygame.K_s:
                                mover_abajo = False

                    # ---- VICTORIA ESCAPA (llega a salida) ----
                    if llego_a_salida(personaje, mapa_obj):
                        victoria = True
                        modo_escapa = False

                    if enemigo.tocar_personaje(personaje):
                        perdio = True
                        modo_escapa = False

                    pygame.display.update()

                # =====================================================
                # MODO CAZA (placeholder tuyo)
                # =====================================================
                else:
                    if victoria:
                        screen.fill((0,0,0))
                        screen.blit(background_optimizado,(0,0)) #Colocar el backgound de la pantalla

                        screen.blit(podio_fondo, (ANCHO / 2 - 250, ALTO / 2 - 200))

                        texto_victoria = FONT_UPHEAT_BIG.render("GANASTE!", True, (255, 255, 255))
                        screen.blit(texto_victoria, (ANCHO / 2 - 90, ALTO / 2 - 100))

                        screen.blit(btn_victoria, (ANCHO / 2 - 70, ALTO / 2))
                        btn_victoria_rect.left = ANCHO / 2 - 70
                        btn_victoria_rect.top = ALTO / 2

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if btn_victoria_rect.collidepoint(event.pos):
                                    tiempo = (pygame.time.get_ticks() - start_time) / 1000
                                    puntos = max(0, int(10000/tiempo * dificultad_mult))
                                    usuario.puntuacion = puntos
                                    puntuacion_escapa.append((usuario.nombre_usuario, usuario.puntuacion))

                                    victoria = False
                                    mostrar_inicio = True
                                    mostrar_ingreso = True
                                    mostrar_podio = True

                        pygame.display.update()

                    if perdio:
                        screen.fill((0,0,0))
                        screen.blit(background_optimizado,(0,0)) #Colocar el backgound de la pantalla

                        screen.blit(podio_fondo, (ANCHO / 2 - 250, ALTO / 2 - 200))

                        texto_victoria = FONT_UPHEAT_BIG.render("PERDIO!", True, (255, 255, 255))
                        screen.blit(texto_victoria, (ANCHO / 2 - 90, ALTO / 2 - 100))

                        screen.blit(btn_rendirse, (ANCHO / 2 - 70, ALTO / 2 + 30))
                        btn_rendirse_rect.left = ANCHO / 2 - 70
                        btn_rendirse_rect.top = ALTO / 2 + 30

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:

                                if btn_rendirse_rect.collidepoint(event.pos):
                                    start_time = pygame.time.get_ticks()

                                    perdio = False
                                    mostrar_inicio = True
                                    mostrar_ingreso = True
                                    mostrar_podio = True
                                    

                        pygame.display.update()

pygame.quit()
