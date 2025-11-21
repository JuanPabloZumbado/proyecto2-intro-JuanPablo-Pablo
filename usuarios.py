import pygame

#Desarrollo de clases para los usuarios y cada modo de juego

class Usuarios:
    def __init__(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario
        self.puntuacion = 0

    def sumar_puntos(self, puntos): #Sistema para aumentar los puntos
        if puntos > 0:
            self.puntuacion += puntos

#Clase secundaria para el modo escapa

class ModoEscapa(Usuarios):
    def __init__(self, nombre_usuario, puntuacion):
        super().__init__(nombre_usuario, puntuacion)
        self.registro_usuarios_escapa = []

    def guardar_usuario(self): #Sistema para guardar el usuario
        self.registro_usuarios_escapa.append((self.nombre_usuario, self.puntuacion))

#Clase secundaria para el modo cazador

class ModoCazador(Usuarios):
    def __init__(self, nombre_usuario, puntuacion):
        super().__init__(nombre_usuario, puntuacion)
        self.registro_usuarios_cazador = []

    def guardar_usuario(self): #Sistema para guardar el usuario
        self.registro_usuarios_cazador.append((self.nombre_usuario, self.puntuacion))
