import pygame

class Usable:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class UExplorador(Usable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.splash = ".\SplahArts\explorador.png"

    def imprimir_personaje(self, screen):
        personaje = pygame.image.load(self.splash).convert_alpha
        screen.blit(personaje, (self.x, self.y))


        