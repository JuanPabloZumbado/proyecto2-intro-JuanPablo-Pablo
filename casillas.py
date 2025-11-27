import pygame

class Casilla:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 75
        self.altura = 75

class Camino(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 0
        self.splash = ".\SplahArts\Casillas\casilla_camino.png"
        self.colision = pygame.Rect(x,y,self.ancho, self.altura)

class Entrada(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 1
        self.splash = ".\SplahArts\Casillas\casilla_entrada.png"
        self.colision = pygame.Rect(x,y,self.ancho, self.altura)

class Salida(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 2
        self.splash = ".\SplahArts\Casillas\casilla_salida.png"
        self.colision = pygame.Rect(x,y,self.ancho, self.altura)

class Trampa(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 3
        self.splash = ".\SplahArts\Casillas\casilla_trampa.png"
        self.colision = pygame.Rect(x,y,self.ancho, self.altura)

class Liana(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 4
        self.splash = ".\SplahArts\Casillas\casilla_liana.png"
        self.colision = pygame.Rect(x,y,self.ancho, self.altura)

class Tunel(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 5
        self.splash = ".\SplahArts\Casillas\casilla_tunel.png"
        self.colision = pygame.Rect(x,y,self.ancho, self.altura)

class Muro(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 6
        self.splash = ".\SplahArts\Casillas\casilla_muro.png"
        self.colision = pygame.Rect(x,y,self.ancho, self.altura)


