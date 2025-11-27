import pygame #Libreria de pygame 
import random #Libreria de random
import pygame_gui #Libreria pygame_gui

#Import de los demas archivos

import usuarios
import casillas as c
import personajes


pygame.init()

mapa = [[0,0,6,0,0,0,6,6,6,6,6,0,0,0],
        [6,6,6,0,0,0,6,0,5,0,0,0,0,2],
        [0,0,0,0,4,0,0,0,0,0,4,0,0,4],
        [0,0,6,6,6,0,0,3,0,0,0,0,0,0],
        [0,0,6,0,0,0,5,0,4,0,6,6,6,0],      #Este es un mapa de prueb apara seguir con el desarrollo
        [1,0,6,0,0,0,0,0,0,0,5,0,6,0],
        [0,0,6,0,0,0,0,0,0,0,0,0,5,0]]


puntuacion_escapa = []
puntuacion_caza = []

ANCHO = 1125
ALTO = 700

FONT_RETRO = pygame.font.Font("Retro Gaming.ttf", 20)
FONT_UPHEAT = pygame.font.Font("upheavtt.ttf", 32)
FONT_UPHEAT_LITLE = pygame.font.Font("upheavtt.ttf", 26)

CLOCK = pygame.time.Clock()
FPS = 60
COLDOWN = 500
MANAGER = pygame_gui.UIManager((ANCHO,ALTO))

screen = pygame.display.set_mode((ANCHO, ALTO))

#Editar ventana

pygame.display.set_caption("Scape Hunters")

icon = pygame.image.load(".\SplahArts\cazador.png")
icon_optimizado = icon.convert_alpha()
pygame.display.set_icon(icon_optimizado)

#Creacion de espacios para el juego

background = pygame.image.load(".\SplahArts\game_background.png")
background_optimizado = background.convert()

# -------- Elementos pantalla de inicio -------------------

title = pygame.image.load(".\SplahArts\ktittle_game.png")
tittle_optimizado = title.convert_alpha()

boton_empezar = pygame.image.load(".\SplahArts\kboton_empezar.png")
boton_empezar_optimizado = boton_empezar.convert_alpha()
rect_boton = boton_empezar_optimizado.get_rect()

# -------- Elementos pantalla de nombre -------------------

text_nombre_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((ANCHO / 2 - 150, ALTO / 2 - 50), (300, 50)), manager=MANAGER, object_id="#texto_nombre")

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

#Funcion crear mapa de objetos

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
        if (mapa_obj[fila][0]).type_id == 1:
            initial_x = (mapa_obj[fila][0]).x + ((mapa_obj[fila][0]).ancho / 2)
            initial_y = (mapa_obj[fila][0]).y + ((mapa_obj[fila][0]).altura / 2)
    return initial_x, initial_y

#Funcion que optiene todos los obstaculos para el jugador que escapa

def obst_escapa(mapa):
    obstaculos = []
    for fila in range(len(mapa)):
        for col in range(len(mapa[0])):
            if (mapa[fila][col]).type_id == 4 or (mapa[fila][col]).type_id == 6:
                obstaculos.append((mapa[fila][col]).colision)
    return obstaculos

#Funcion impirmir mapa

def imprimir_mapa(mapa):
    
    screen.fill((0,0,0))

    screen.blit(background_optimizado,(0,0))

    for fila in range(len(mapa)):
        for col in range(len(mapa[0])):
            fondo_casilla = pygame.image.load((mapa[fila][col]).splash).convert_alpha()
            screen.blit(fondo_casilla, ((mapa[fila][col]).x, (mapa[fila][col]).y))

    screen.blit(game_bar, (50, ALTO - 150))

    pygame.display.update()


#Funcion ordenar lista

def ordenar_puntuacion(lista):
    if not lista: return lista
    for i in range(len(lista)):
        mayor = i
        for j in range(i + 1, len(lista)):
            if lista[j][1] > lista[mayor][1]: mayor = j
        
        lista[i], lista[mayor] = lista[mayor], lista[i]
    
    return lista

#Funcion de la pantalla de inicio

def pantalla_de_inicio():

    screen.fill((0,0,0))
    screen.blit(background_optimizado,(0,0)) #Colocar el backgound de la pantalla de inicio

    #Colocar el titulo y el boton de la pantalla de inicio

    screen.blit(tittle_optimizado, (300,50))

    screen.blit(boton_empezar_optimizado, (ANCHO / 2 - 120, ALTO / 2 + 100))
    rect_boton.left = ANCHO / 2 - 120
    rect_boton.top = ALTO / 2 + 100

    pygame.display.update()

#Funcion para mostrar el podio de ambos modos

def pantalla_de_podio():

    screen.fill((0,0,0))
    screen.blit(background_optimizado,(0,0))

    screen.blit(podio_fondo, (30, 20)) #Podio del modo Escapa
    screen.blit(podio_fondo, (ANCHO / 2 + 30, 20)) #Podio del modo Cazador

    texto_modo_escapa = FONT_UPHEAT.render("MODO ESCAPA", True, (166, 144, 114))
    screen.blit(texto_modo_escapa, (175, 60))

    if puntuacion_escapa:
        y_inicial = 100
        ord_punt_escapa = ordenar_puntuacion(puntuacion_escapa)
        for usu in range(len(ord_punt_escapa)):
            if usu < 5:
                texto_podio = FONT_RETRO.render(f"{usu + 1} Lugar: {ord_punt_escapa[usu][0]} - {ord_punt_escapa[usu][1]}", True, (204, 186, 159))
                screen.blit(texto_podio,(100, y_inicial))
                y_inicial += 50



    texto_modo_cazador = FONT_UPHEAT.render("MODO CAZADOR", True, (166, 144, 114))
    screen.blit(texto_modo_cazador, (ANCHO / 2 + 175, 60))

    if puntuacion_caza:
        y_inicial = 100
        ord_punt_caza = ordenar_puntuacion(puntuacion_caza)
        for usu in range(len(ord_punt_caza)):
            if usu < 5:
                texto_podio = FONT_RETRO.render(f"{usu + 1} Lugar: {ord_punt_caza[usu][0]} - {ord_punt_caza[usu][1]}", True, (204, 186, 159))
                screen.blit(texto_podio,(ANCHO / 2 + 100, y_inicial))
                y_inicial += 50

    screen.blit(usuario_fondo, (ANCHO / 2 - 240, ALTO / 2 + 175))

    texto_usuario = FONT_UPHEAT_LITLE.render(f"{usuario.nombre_usuario} - Puntos: {usuario.puntuacion}", True, (204, 186, 159))
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



mapa_obj = generar_matriz_mapa(mapa)
initial_x_p, initial_y_p = initial_cords(mapa_obj)
obstaculos_escapa = obst_escapa(mapa_obj)

obstaculos_escapa.append(pygame.Rect(35, 0, 5, ALTO))
obstaculos_escapa.append(pygame.Rect(1090, 0, 5, ALTO))
obstaculos_escapa.append(pygame.Rect(0, 15, ANCHO, 5))
obstaculos_escapa.append(pygame.Rect(0, 545, ANCHO, 5))

#Variables de movimiento del personaje

mover_derecha = False
mover_izquierda = False
mover_arriba = False
mover_abajo = False

#Variables de apricion de pantallas

victoria = False
inicio_juego = True 
mostrar_ingreso = True
mostrar_inicio = True
mostrar_podio = True
modo_escapa = False
modo_caza = False
running = True
while running:
    if mostrar_inicio:

        pantalla_de_inicio() #Mostrar pantalla de inicio

        #Calcular eventos para ver si se apreta el boton

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_boton.collidepoint(event.pos):
                    mostrar_inicio = False
    else: 
        if mostrar_ingreso:

            '''
            Aqui no se realizo la elaboracion de la pagnia por separado en una funcion porque hacerlo
            por separado afectaba el correcto funcionamiento del pygame_gui
            
            '''

            UI_REFRESH_RATE = CLOCK.tick(60)/1000 #Tiempo de refresco de frames del UI

            screen.fill((0,0,0))
            screen.blit(background_optimizado,(0,0)) #Colocar el backgound de la pantalla

            screen.blit(fondo_ingreso_optimizado, (ANCHO / 2 - 390, ALTO / 2 - 300)) 

            #Texto del para que ingrese el texto
            texto_ingreso = FONT_UPHEAT.render("INGRESE SU NOMBRE (10 CARAC MAX):", True, (166, 144, 114))
            screen.blit(texto_ingreso, (ANCHO / 2 - 290, ALTO / 2 - 125))

            #Texto explicativo de como proseguir
            texto_press_enter = FONT_RETRO.render("Presionar ENTER para seguir", True, (166, 144, 114))
            screen.blit(texto_press_enter, (ANCHO / 2 - 185, ALTO / 2 + 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Este if evalua que el text box se complete y se aprete enter para seguir el codigo
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#texto_nombre":
                    #Se evalua si el espacio esta lleno o si es menor a 10 carac en caso de q no, se pone nombre default
                    if event.text and len(event.text) <= 10:
                        usuario = usuarios.Usuarios(event.text) #Creacion del objeto usuario 
                        mostrar_ingreso = False
                    else:
                        usuario = usuarios.Usuarios("JUGADOR") #En caso de no ingresar nada se pone un nombre predeterminado
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
                        if rect_boton_escapa.collidepoint(event.pos):
                            mostrar_podio = False
                            modo_escapa = True
                            personaje = personajes.UExplorador(initial_x_p, initial_y_p)
                        if rect_boton_caza.collidepoint(event.pos):
                            mostrar_podio = False
                            modo_caza = True

            else:
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

                    personaje.imprimir_personaje(screen)

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


                    pygame.display.update()
                else:
                    if victoria:
                        screen.fill((0,0,0))
                        screen.blit(background_optimizado,(0,0)) #Colocar el backgound de la pantalla

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        pygame.display.update()

            

pygame.quit()

