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

class Entrada(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 1
        self.splash = ".\SplahArts\Casillas\casilla_entrada.png"

class Salida(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 2
        self.splash = ".\SplahArts\Casillas\casilla_salida.png"

class Trampa(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 3
        self.splash = ".\SplahArts\Casillas\casilla_trampa.png"

class Liana(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 4
        self.splash = ".\SplahArts\Casillas\casilla_liana.png"

class Tunel(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 5
        self.splash = ".\SplahArts\Casillas\casilla_tunel.png"

class Muro(Casilla):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type_id = 6
        self.splash = ".\SplahArts\Casillas\casilla_muro.png"


