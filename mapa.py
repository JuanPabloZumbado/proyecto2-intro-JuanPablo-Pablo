import casillas as c

def generar_matriz_mapa(mapa):
    initial_x = 20
    initial_y = 20
    mapa_obj = [[0 for _ in range(len(mapa))] for _ in range(len(mapa[0]))]
    for fila in range(len(mapa)):
        for col in range(len(mapa[0])):
            if mapa[fila][col] == 0:  c.Camino(initial_x, initial_y)
            if mapa[fila][col] == 1: c.Entrada(initial_x, initial_y)
            if mapa[fila][col] == 2: c.Salida(initial_x, initial_y)
            if mapa[fila][col] == 3: c.Trampa(initial_x, initial_y)
            if mapa[fila][col] == 4: c.Liana(initial_x, initial_y)
