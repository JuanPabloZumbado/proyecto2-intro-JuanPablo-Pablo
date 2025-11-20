import pygame #Libreria de pygame 
import random #Libreria de random

pygame.init()

screen = pygame.display.set_mode((1125, 700))

pygame.display.set_caption("Scape Hunters")

icon = pygame.image.load(".\SplahArts\cazador.png")
icon_optimizado = icon.convert_alpha()

background = pygame.image.load(".\SplahArts\game_background.png")
background_optimizado = background.convert()

title = pygame.image.load(".\SplahArts\ktittle_game.png")
tittle_optimizado = title.convert_alpha()

boton_empezar = pygame.image.load(".\SplahArts\kboton_empezar.png")
boton_empezar_optimizado = boton_empezar.convert_alpha()

pygame.display.set_icon(icon_optimizado)
running = True
while running:
    screen.fill((0,0,0))

    screen.blit(background_optimizado,(0,0))

    screen.blit(tittle_optimizado, (300,50))

    screen.blit(boton_empezar_optimizado, (350,450))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

pygame.quit()

