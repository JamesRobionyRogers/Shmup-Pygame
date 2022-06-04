# Pygame Shmup Part 1:  Player Sprite and Controls

# Pygame template - skeleton for a new pygame project
import pygame
import random
import os

# setting the contsants - ALL CAPS means a consistant variable
WIDTH = 480
HEIGHT = 600
FPS = 60

# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialise pygame and create window
pygame.init()  # initialises pygame
pygame.mixer.init()  # initialises pygame sound effects and music

# creates game window (variable a.k.a: screen)
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!  version 01")  # title of the game window
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        # movement [LEFT & RIGHT]
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speedx = -8         # change speed here
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speedx = 8          # and change speed here
        self.rect.x += self.speedx
        # boundaries
        if self.rect.right > WIDTH:  # right boundary
            self.rect.right = WIDTH
        if self.rect.left < 0:       # left boundary
            self.rect.left = 0


# sprite group
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window then quitting
        if event.type == pygame.QUIT:
            running = False
            print("QUIT")

    # Update
    all_sprites.update()

    # Rendering / Draw
    gameDisplay.fill(BLACK)
    all_sprites.draw(gameDisplay)
    # *after* drawing everything, flip the diaplay
    pygame.display.flip()


pygame.quit()
quit()
