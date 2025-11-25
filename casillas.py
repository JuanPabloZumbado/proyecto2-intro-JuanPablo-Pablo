class Casilla:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 0
        self.altura = 0

class Camino(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 0

class Entrada(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 1

class Salida(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 2

class Trampa(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 3

class Liana(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 4

class Tunel(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 5

class Muro(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 6


