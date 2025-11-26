import pygame

class Usable:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class UExplorador(Usable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imagen = pygame.image.load(".\SplahArts\explorador.png").convert_alpha()
        self.forma = pygame.Rect(0,0, 65, 65)
        self.forma.center = (x, y)

    def imprimir_personaje(self, screen):
        screen.blit(self.imagen, self.forma)
        #pygame.draw.rect(screen, (39, 245, 63), self.forma, width=1)


        