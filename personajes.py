import pygame
import random

class Personaje:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class UExplorador(Personaje):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imagen = pygame.image.load(".\SplahArts\explorador.png").convert_alpha()
        self.forma = pygame.Rect(0,0, 65, 65)
        self.forma.center = (x, y)

        self.velocidad = 5 # Asegúrate de que la velocidad esté definida
        
        # --- NUEVOS ATRIBUTOS DE MEMORIA ---
        self.last_dx = 0
        self.last_dy = 0

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

class UCazador(Personaje):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imagen = pygame.image.load(".\\SplahArts\\cazador_per.png").convert_alpha()
        self.forma = pygame.Rect(0,0, 65, 65)
        self.forma.center = (x, y)
        
    def imprimir_personaje(self, screen):
        screen.blit(self.imagen, self.forma)
        pygame.display.update()

    # El método mover_personaje debe ser copiado de la clase UExplorador
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

class EnemigoCazador(Personaje):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.imagen = pygame.image.load(".\SplahArts\cazador_per.png").convert_alpha()
        self.forma = pygame.Rect(0,0, 65, 65)
        self.forma.center = (x, y)

        self.velocidad = 3


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

    def seguir_jugador(self, jugador, obstaculos):
        
        opciones_movimiento = {
            'arriba': (0, -self.velocidad),
            'abajo': (0, self.velocidad),
            'izquierda': (-self.velocidad, 0),
            'derecha': (self.velocidad, 0),
        }
        
        mejor_dx = 0
        mejor_dy = 0
        min_distancia = float('inf') # Distancia inicial infinita
        

        target_x = jugador.forma.centerx
        target_y = jugador.forma.centery


        for dx, dy in opciones_movimiento.values():
            

            rect_previo = self.forma.move(dx, dy)
            

            colision = False
            for obs in obstaculos:
                if obs.colliderect(rect_previo):
                    colision = True
                    break

            if not colision:
                
                nueva_x = rect_previo.centerx
                nueva_y = rect_previo.centery
                distancia = abs(nueva_x - target_x) + abs(nueva_y - target_y)
                

                if distancia < min_distancia:
                    min_distancia = distancia
                    mejor_dx = dx
                    mejor_dy = dy


        if (mejor_dx != 0 or mejor_dy != 0):
            self.mover_personaje(mejor_dx, mejor_dy, obstaculos)

    def tocar_personaje(self, jugador):
        if (jugador.forma).colliderect(self.forma): return True
        else: return False

class EnemigoExplorador(UExplorador):
    def __init__(self, x, y):
        super().__init__(x, y)

    def buscar_salida(self, cazador, salida_rect, obstaculos):
        
        self.velocidad = 5
        DISTANCIA_AMENAZA = 150 
        
        opciones_movimiento = {
            'arriba': (0, -self.velocidad),
            'abajo': (0, self.velocidad),
            'izquierda': (-self.velocidad, 0),
            'derecha': (self.velocidad, 0),
        }
        
        # ... (Código existente para EVALUACIÓN DE AMENAZA y definir objetivo) ...
        
        distancia_cazador_actual = abs(self.forma.centerx - cazador.forma.centerx) + \
                                   abs(self.forma.centery - cazador.forma.centery)
        
        if distancia_cazador_actual < DISTANCIA_AMENAZA:
            objetivo_evasion = True
            mejor_distancia_objetivo = -float('inf') 
        else:
            objetivo_evasion = False
            mejor_distancia_objetivo = float('inf') 

        target_x = cazador.forma.centerx if objetivo_evasion else salida_rect.centerx
        target_y = cazador.forma.centery if objetivo_evasion else salida_rect.centery

        # --- ESTRUCTURA DE BÚSQUEDA ---
        
        best_moves = [] 
        valid_moves = [] 
        
        
        for dx, dy in opciones_movimiento.values():
            rect_previo = self.forma.move(dx, dy)
            colision = False
            
            for obs in obstaculos:
                if obs.colliderect(rect_previo):
                    colision = True
                    break
            
            if not colision:
                valid_moves.append((dx, dy))
                
                nueva_x = rect_previo.centerx
                nueva_y = rect_previo.centery
                distancia = abs(nueva_x - target_x) + abs(nueva_y - target_y)
                
                # Lógica de Prioridad y Empates
                is_new_best = False
                if objetivo_evasion:
                    if distancia > mejor_distancia_objetivo:
                        is_new_best = True
                else:
                    if distancia < mejor_distancia_objetivo:
                        is_new_best = True

                if is_new_best:
                    mejor_distancia_objetivo = distancia
                    best_moves = [(dx, dy)] 
                elif distancia == mejor_distancia_objetivo:
                    best_moves.append((dx, dy)) 
        
        
        final_dx, final_dy = 0, 0
        
        reverse_move = (-self.last_dx, -self.last_dy)
        
        if len(best_moves) > 0 and reverse_move in best_moves:
            
            filtered_best_moves = [move for move in best_moves if move != reverse_move]
            
            if filtered_best_moves:
                best_moves = filtered_best_moves # Usar el camino óptimo sin reversión
        
        
        if best_moves:
            final_dx, final_dy = random.choice(best_moves)
            self.mover_personaje(final_dx, final_dy, obstaculos)
            
        elif valid_moves:
            final_dx, final_dy = random.choice(valid_moves)
            self.mover_personaje(final_dx, final_dy, obstaculos)
            
        self.last_dx = final_dx
        self.last_dy = final_dy

    def reiniciar_personaje(self, x, y):
        self.forma.x = x - 30
        self.forma.y = y - 30

    def tocar_personaje(self, jugador):
        if (jugador.forma).colliderect(self.forma): return True
        else: return False