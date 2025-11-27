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
        pygame.display.update()

    def mover_personaje(self, delta_x, delta_y, obstaculos):

        self.forma.x = self.forma.x + delta_x
        for obs in obstaculos:
            if obs.colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obs.left
                if delta_x < 0:
                    self.forma.left = obs.right

        self.forma.y = self.forma.y + delta_y
        for obs in obstaculos:
            if obs.colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obs.top
                if delta_y < 0:
                    self.forma.top = obs.bottom


        