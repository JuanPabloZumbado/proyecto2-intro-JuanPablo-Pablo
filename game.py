import pygame #Libreria de pygame 
import random #Libreria de random
import pygame_gui #Libreria pygame_gui

#Import de los demas archivos

import usuarios


pygame.init()

ANCHO = 1125
ALTO = 700

#FONT_RETRO = pygame.font.Font(".\Fonts\Retro Gaming.ttf", 32)
FONT_UPHEAT = pygame.font.Font(None, 40)

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

text_nombre_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((ANCHO / 2, ALTO / 2), (300, 50)), manager=MANAGER, object_id="#texto_nombre")

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

#Funcion de la pantalla de ingresar usuario

def pantalla_de_ingreso():

    screen.fill((0,0,0))
    screen.blit(background_optimizado,(0,0)) #Colocar el backgound de la pantalla

    texto_ingreso = FONT_UPHEAT.render("INGRESE SU NOMBRE (MAX 10 CARAC)", True, (128, 81, 24))
    screen.blit(texto_ingreso, (ANCHO / 2 - 220, ALTO / 2 - 200))

    pygame.display.update()


mostrar_ingreso = True
mostrar_inicio = True
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

            UI_REFRESH_RATE = CLOCK.tick(60)/1000 #Tiempo de refresco de frames del UI

            pantalla_de_ingreso()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                MANAGER.process_events(event)

            MANAGER.update(UI_REFRESH_RATE)

            MANAGER.draw_ui(screen)

        else: 
            screen.fill((0,0,0))

            screen.blit(background_optimizado,(0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.update()

pygame.quit()

