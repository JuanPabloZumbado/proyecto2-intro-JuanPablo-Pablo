import pygame #Libreria de pygame 
import random #Libreria de random
import pygame_gui #Libreria pygame_gui

#Import de los demas archivos

import usuarios


pygame.init()

ANCHO = 1125
ALTO = 700

FONT_RETRO = pygame.font.Font("Retro Gaming.ttf", 20)
FONT_UPHEAT = pygame.font.Font("upheavtt.ttf", 32)
FONT_UPHEAT_LITLE = pygame.font.Font("upheavtt.ttf", 26)

CLOCK = pygame.time.Clock()
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

    texto_modo_cazador = FONT_UPHEAT.render("MODO CAZADOR", True, (166, 144, 114))
    screen.blit(texto_modo_cazador, (ANCHO / 2 + 175, 60))

    screen.blit(usuario_fondo, (ANCHO / 2 - 240, ALTO / 2 + 175))

    texto_usuario = FONT_UPHEAT_LITLE.render(f"{usuarioCaza.nombre_usuario} - Puntos: {usuarioCaza.puntuacion}", True, (166, 144, 114))
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
                        '''
                        Se hacen dos objetos porque como se ocupa ingresar el nombre de primero no se puede evaluar
                        donde guardar el usuario.

                        '''
                        usuarioEscapa = usuarios.ModoEscapa(event.text) #Creacion del objeto usuario para modo escapa
                        usuarioCaza = usuarios.ModoCazador(event.text) #Creacion del objeto usuario para modo Caza
                        mostrar_ingreso = False
                    else:
                        usuarioEscapa = usuarios.ModoEscapa("JUGADOR")
                        usuarioCaza = usuarios.ModoCazador("JUGADOR") #En caso de no ingresar nada se pone un nombre predeterminado
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
                        if rect_boton_caza.collidepoint(event.pos):
                            mostrar_podio = False
                            modo_caza = True

            else: 
                screen.fill((0,0,0))

                screen.blit(background_optimizado,(0,0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            
                pygame.display.update()

pygame.quit()

