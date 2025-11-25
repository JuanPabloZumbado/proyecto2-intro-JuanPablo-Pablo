import pygame

#Desarrollo de clases para los usuarios y cada modo de juego

class Usuarios:
    def __init__(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario
        self.puntuacion = 0

    def sumar_puntos(self, puntos): #Sistema para aumentar los puntos
        if puntos > 0:
            self.puntuacion += puntos

'''
#Clase secundaria para el modo escapa

class ModoEscapa(Usuarios):
    def __init__(self, nombre_usuario):
        super().__init__(nombre_usuario)
        self.registro_usuarios_escapa = []

    def guardar_usuario(self): #Sistema para guardar el usuario
        self.registro_usuarios_escapa.append([self.nombre_usuario, self.puntuacion])

    def puntuacion_ordenada(self): #sistema para ordenar la lista actual de usuarios del modo 
        if self.registro_usuarios_escapa != []:
            for i in range(len(self.registro_usuarios_escapa)):
                mayor = i
                for j in range(i + 1, len(self.registro_usuarios_escapa)):
                    if self.registro_usuarios_escapa[j][1] > mayor:
                        mayor = j

                #Se intercambian los valores para acomodarlos
                self.registro_usuarios_escapa[i], self.registro_usuarios_escapa[mayor] = self.registro_usuarios_escapa[mayor], self.registro_usuarios_escapa[i]




#Clase secundaria para el modo cazador

class ModoCazador(Usuarios):
    def __init__(self, nombre_usuario):
        super().__init__(nombre_usuario)
        self.registro_usuarios_cazador = []

    def guardar_usuario(self): #Sistema para guardar el usuario
        self.registro_usuarios_cazador.append([self.nombre_usuario, self.puntuacion])

    def devolver_lista

    
    def puntuacion_ordenada(self): #sistema para ordenar la lista actual de usuarios del modo 
        if self.registro_usuarios_cazador != []:
            for i in range(len(self.registro_usuarios_cazador)):
                mayor = i
                for j in range(i + 1, len(self.registro_usuarios_cazador)):
                    if self.registro_usuarios_cazador[j][1] > mayor:
                        mayor = j

                #Se intercambian los valores para acomodarlos
                self.registro_usuarios_cazador[i], self.registro_usuarios_cazador[mayor] = self.registro_usuarios_cazador[mayor], self.registro_usuarios_cazador[i]
'''

