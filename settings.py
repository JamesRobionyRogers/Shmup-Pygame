import pygame
from os import path

# Setting the contsants - ALL CAPS means a consistant variable
WIDTH = 480
HEIGHT = 600
FPS = 60

# Defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 65, 44)
GREEN = (55, 255, 51)
BLUE = (57, 155, 255)
YELLOW = (255, 223, 34)

# Setting up assets folders
img_dir = path.join(path.dirname(__file__), 'imgs')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Creating the sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
