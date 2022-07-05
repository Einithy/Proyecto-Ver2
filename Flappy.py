import pygame       #Importamos la librería Pygame
from pygame.locals import *     #Con esto estamos todos los módulos locales de Pygame
import random       #Importamos la libreria Random        

pygame.init()

clock = pygame.time.Clock()     #Para que se repita la imagen cada cierto tiempo
fps = 60        

#Tamaño del entorno
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')


#Definimos las variables del juego.
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500       #milisegundos
last_pipe = pygame.time.get_ticks() - pipe_frequency

#Cargamos las imagenes.
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

# Realizamos una clase para el pájaro, en la que están los 3 sprites del mismo que nos ayudarán para su animación.
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            # Velocidad de la gravedad 
            self.vel += 0.5 
            if self.vel > 8:             #limitando el incrementro excesivo de la gravedad
                self.vel = 8        
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)    

        if game_over == False:
            # Salto del personaje
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.vel = -10
                self.clicked = True         #Bandera para la función al presionar click

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False  

            # Manejamos la animación, este será un bucle de 3 sprites que cambiará de sprite cada 5 frames.
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotacipon del personaje
            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)      #rotación de caida

# Realizamos una clase para las tuberias
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 es desde arriba y -1 desde el suelo
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()         #eliminacion de las tuberias sobrantes

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

run = True
while run:

    clock.tick(fps)     #Este método nos ayudará a manejar la tasa de fotogramas del programa

    # Agregamos el fondo
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # Agregando el suelo  
    screen.blit(ground_img, (ground_scroll, 768))

    # Colision con las tuberias
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # Verificacion del personaje en el suelo 
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        # creacion nuevas tuberias
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)        #generacion de numeros aletarorios de 2 cifras
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # Agregando el movimiento del suelo
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()         #actualizacion de las tuberias
    # Para cerrar el programa, se deberá presionar la X de la ventana de Windows
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:    #condición de inicio
            flying = True

    pygame.display.update()

pygame.quit()