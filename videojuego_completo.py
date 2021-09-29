import sys # Para poder usar exit()
import time # para usar sleep()
import pygame
 # Para las ventanas antes del juego:
import tkinter as tk
import os

ANCHO = 1080 # Ancho de la pantalla
ALTO = 640 # Alto de la pantalla
color_azul = (0, 0, 64) # Color azul para el fondo
azul_hex = '#000040'
color_blanco = (255, 255, 255) # Color blanco, para textos

# Clase para diferenciar entre escenas
class Escena:
    def __init__(self):
        "Inicializacion"
        self.proximaEscena = False
        self.jugando = True
        pass
    
    def leer_eventos(self, eventos):
        "Lee la lista de todos los eventos."
        pass
    
    def actualizar(self):
        "Cálculos y lógica."

    def dibujar(self, pantalla):
        "Dibuja los objetos en pantalla."
        pass

    def cambiar_escena(self, escena):
        "Selecciona la nueva escena a ser desplegada"
        self.proximaEscena = escena

class Director:
    def __init__(self, titulo = "", res = (ANCHO, ALTO)):
        # Es necesario iniciarlizar pygame de esta forma para poder mostrar textos:
        pygame.init()
        
        # inicializando pantallas
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))

        # Título de pantalla
        pygame.display.set_caption('Breakout')

        # Crear el reloj
        self.reloj = pygame.time.Clock()
        self.escena = None
        self.escenas  = {}

    def ejecutar(self, escena_inicial, fps = 60):
        self.escena = self.escenas[escena_inicial]
        jugando = True
        while jugando:
            self.reloj.tick(fps)
            eventos = pygame.event.get()
            # Para que se pueda cerrar la ventana, revisamos todos los eventos hasta que aparezca el que nos interesa
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    # Cerrar el videojuego
                    jugando = False

            self.escena.leer_eventos(eventos)
            self.escena.actualizar()
            self.escena.dibujar(self.pantalla)

            self.elegirEscena(self.escena.proximaEscena)

            if jugando:
                jugando = self.escena.jugando
            # Para actualizar los elementos en pantalla:
            pygame.display.flip()
        # Sumar 3 seg de espera de pantalla fija
        time.sleep(3)

    def elegirEscena(self, proximaEscena):
        if proximaEscena:
            if proximaEscena not in self.escenas:
                self.agregarEscena(proximaEscena)
            self.escena = self.escenas[proximaEscena]

    def agregarEscena(self, escena):
        escenaClase = 'Escena'+escena
        escenaObj = globals()[escenaClase]
        self.escenas[escena] = escenaObj()

class EscenaNivel1(Escena):
    def __init__(self):
        Escena.__init__(self)
        self.bolita = Bolita()
        self.jugador = Paleta()
        self.muro = Muro(92)

        self.puntuacion = 0
        self.vidas = 3
        self.esperando_saque = True

        # Ajustar repetición de evento con la tecla presionada y que así la barrita se mueva de forma constante
        pygame.key.set_repeat(30)
    
    def leer_eventos(self, eventos):
        for evento in eventos:
        # Buscar eventos del teclado
            if evento.type == pygame.KEYDOWN:
                self.jugador.update(evento)
                if self.esperando_saque == True and evento.key == pygame.K_SPACE:
                    self.esperando_saque = False
                    if self.bolita.rect.centerx < ANCHO / 2:
                        self.bolita.speed = [3, -3]
                    else:
                        self.bolita.speed = [-3, -3]
    def actualizar(self):
        # Actualizar posición de la bolita
        if self.esperando_saque == False:
            self.bolita.update()
        else:
            self.bolita.rect.midbottom = self.jugador.rect.midtop

        # Colisión entre bolita y jugador
        if pygame.sprite.collide_rect(self.bolita, self.jugador):
            self.bolita.speed[1] = -self.bolita.speed[1]

        # Colisión de la bolita con el muro
        lista = pygame.sprite.spritecollide(self.bolita, self.muro, False) # spritecollide permite eliminar los elementos si le pasamos True, o no, si le pasamos False
        if lista:
            self.ladrillo = lista[0]
            cx = self.bolita.rect.centerx
            if cx < self.ladrillo.rect.left or cx > self.ladrillo.rect.right:
                self.bolita.speed[0] = -self.bolita.speed[0]
            else:
                self.bolita.speed[1] = -self.bolita.speed[1]
            self.muro.remove(self.ladrillo) # Eliminación manual del ladrillo
            self.puntuacion +=10 # Se suma puntuación final por cada ladrillo eliminado

        # Revisar si la bolita sale de la pantalla y comprobar las vidas que le quedan al jugador
        if self.bolita.rect.top > ALTO:
            self.vidas -= 1
            self.esperando_saque = True
        
        # Orden final para terminar el juego cuando nos quedamos sin vidas:
        if self.vidas <= 0:
            self.cambiar_escena('JuegoTerminado')
    
    def dibujar(self, pantalla):
        # Rellenar la pantalla
        pantalla.fill(color_azul)

        # Mostrar puntuación
        self.mostrar_puntuacion(pantalla)

        # Mostrar vidas
        self.mostrar_vidas(pantalla)

        # Dibujar bolita en pantalla
        pantalla.blit(self.bolita.image,self.bolita.rect)

        # Dibujar paleta en pantalla
        pantalla.blit(self.jugador.image,self.jugador.rect)

        # Dibujar los ladrillos en el fondo
        self.muro.draw(pantalla)

    # Función para ver cuantos puntos se consiguen:
    def mostrar_puntuacion(self, pantalla):
        fuente = pygame.font.SysFont('Consolas', 20)
        texto = fuente.render(str(self.puntuacion).zfill(5), True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.topleft = [0, 0]
        pantalla.blit(texto, texto_rect) # Dibujar en pantalla

    def mostrar_vidas(self, pantalla):
        fuente = pygame.font.SysFont('Consolas', 20)
        cadena = "Vidas: " + str(self.vidas).zfill(2)
        texto = fuente.render(cadena, True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.topright = [ANCHO, 0]
        pantalla.blit(texto, texto_rect) # Dibujar en pantalla

# Clase que abarca la escena final, para acabar el juego, tras dejar ir la bolita:
class EscenaJuegoTerminado(Escena):
    def actualizar(self):
        self.jugando = False
        
    def dibujar(self, pantalla):
        fuente = pygame.font.SysFont('Arial', 72)
        texto = fuente.render('Juego terminado :(', True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.center = [ANCHO / 2, ALTO / 2]
        pantalla.blit(texto, texto_rect) # Dibujar en pantalla

# Clase para la bola del juego
class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen de la bola
        self.image = pygame.image.load('imagenes/bolita.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial centrada en pantalla
        self.rect.centerx = int((ANCHO / 2) - 50)
        self.rect.centery = int((ALTO / 2) + 100)
        # Establecer velocidad inicial [x,y]
        self.speed = [3, 3]

    def update(self):
        # No se evita que salga por debajo de la pantalla, si pasa se pierde el juego
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Evitar que salga por la derecha
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Mover en base a posición actual y velocidad
        self.rect.move_ip(self.speed)

# Clase paleta del jugador
class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen de la bola
        self.image = pygame.image.load('imagenes/paleta.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial centrada en pantalla
        self.rect.midbottom = (ANCHO / 2, ALTO - 20)
        # Establecer velocidad inicial [x,y]
        self.speed = [0, 0]

    def update(self, evento):
        # Buscar si se presionó flecha izquierda/derecha
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-5, 0]
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [5, 0]
        else:
            self.speed = [0, 0]
        # Mover en base a posición actual y velocidad
        self.rect.move_ip(self.speed)

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen de la bola
        self.image = pygame.image.load('imagenes/ladrillo.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posicion inicial, provista externamente
        self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
    def __init__(self, cantidadLadrillos):
        pygame.sprite.Group.__init__(self) # sprite.Group es un contenedor de Sprite

        pos_x = 0
        pos_y = 20
        for i in range(cantidadLadrillos):
            ladrillo = Ladrillo((pos_x, pos_y))
            self.add(ladrillo)

            pos_x += ladrillo.rect.width 
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height 

# PARTE DEL JUEGO:
def juego():
    
    director = Director('Breakout', (ANCHO, ALTO))
    director.agregarEscena('Nivel1')
    director.ejecutar('Nivel1')

# PARTE DE LAS VENTANAS ANTES DE ENTRAR A JUGAR:
def ventanas():
   
    def newWindow():
        nuevaVentana = tk.Tk()
        nuevaVentana.geometry('640x360+600+300')
        nuevaVentana.resizable(0,0)
        nuevaVentana.configure(background=azul_hex)
        cadena = "PYGAME"
        etiqueta1 = tk.Label(nuevaVentana,text=cadena, font=("Arial Bold", 26), bg=azul_hex, fg="green")

        etiqueta1.pack(fill = tk.X, padx=10,pady=10, side = tk.TOP) # fill llena toda la línea

        cadena2 = "Nice game, would you like to continue playing?"

        etiqueta2 = tk.Label(nuevaVentana,text=cadena2, font=("Arial Bold", 15), bg=azul_hex, fg="white")

        etiqueta2.pack(fill = tk.X, padx=10,pady=10, side = tk.TOP)

        boton = tk.Button(nuevaVentana,text="Play again", bg="black", font=("Arial", 30), fg="white", command = lambda:[nuevaVentana.destroy(), play()])
        boton.pack(padx=20,pady=20)

        boton2 = tk.Button(nuevaVentana,text="No, thanks", bg="black", font=("Arial", 30), fg="white", command = nuevaVentana.destroy)
        boton2.pack(padx=20,pady=20)

    # Función que ejecuta el juego y una vez acabe, o lo cerremos, nos preguntará si queremos echar otra partida ejecutando de nuevo esta función, y por tanto, el juego
    def play():

        juego()
        newWindow()


    ventana = tk.Tk()
    ventana.title('Breakout')
    # Ancho x Alto
    ventana.geometry('640x360+600+300')
    ventana.resizable(0,0)
    ventana.configure(background=azul_hex)
    #cadena = "En este juego tendrás que rebotar la pelota contra una pared de ladrillos hasta que no quede ninguno.. Cuidado! Solo tendrás 3 vidas para conseguirlo"
    cadena = "PYGAME"
    etiqueta1 = tk.Label(ventana,text=cadena, font=("Arial Bold", 26), bg=azul_hex, fg="green")

    etiqueta1.pack(fill = tk.X, padx = 10,pady = 10, side = tk.TOP) # fill llena toda la línea

    boton = tk.Button(ventana,text="Play", bg="black", font=("Arial", 30), fg="white", command = lambda:[ventana.destroy(), play()])
    boton.pack(padx = 20, pady = 20)
    boton.place(x = 200, y = 140)

    boton2 = tk.Button(ventana,text="Quit", bg="black", font=("Arial", 30), fg="white", command = ventana.destroy)
    boton2.pack(padx = 20, pady = 20)
    boton2.place(x = 340, y = 140)

    # Genera la ventana indefinidamente hasta que la cerremos manualmente
    ventana.mainloop()

ventanas()