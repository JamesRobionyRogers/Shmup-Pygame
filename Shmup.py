# Importing all the used libraries 
import pygame
import random
import time
from os import path

# Importing the required classes
from settings import *
from Player import *
from Mob import *
from Explosion import *


class Shmup():

    # Initialise pygame and create window
    pygame.mixer.pre_init(44100, -16, 1, 1024)      # initialises pygame sound effects and music
    pygame.init()                                   # initialises pygame

    # Titleing the game window
    pygame.display.set_caption("Shmup!  version 10")

    # Initialising the background music
    pygame.mixer.music.load(path.join(snd_dir, 'bg_music.ogg'))
    pygame.mixer.music.set_volume(1)

    pygame.mixer.music.play(loops=-1)

    def __init__(self):
        # Creating the game window 
        self.gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_name = pygame.font.match_font('arail')

        self.score = 0

        # Loading the window graphics (Sprite graphics are handled in the classes themselves)
        self.background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
        self.background_rect = self.background.get_rect()

        # Creating instance of the Player and adding to sprite groups (Sprite groups created in settings.py)
        self.player = Player()
        all_sprites.add(self.player)
        # Spawning mobs
        for i in range(8):
            self.newmob()

    def draw_text(self, surface, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)

        # Draw the text onto the surface
        surface.blit(text_surface, text_rect)

    def newmob(self):
        # Creating a new instance of a Mob
        m = Mob()
        # Adding the instance to the sprite groups 
        all_sprites.add(m)
        mobs.add(m)

    def draw_shield_bar(self, surface, x, y, percent):
        percent = (0 if percent < 0 else percent)       # incase the player has a negative shield
        BAR_WIDTH = 100
        BAR_HEIGHT = 12
        fill = (percent / 100 * BAR_WIDTH)
        outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, BLUE, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)

    def run(self):
        running = True
        # Game Loop
        while running:
            # Keep loop running at the right speed
            self.clock.tick(FPS)

            # Processing input (events)
            for event in pygame.event.get():
                # Check for closing window then quitting
                if event.type == pygame.QUIT:
                    running = False
                    print("QUIT")

            # Updates and Checks 
            all_sprites.update()

            # Checking if a Bullet it a Mob
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                # Adding to the score 
                self.score += 60 - hit.radius

                # Create an Explotion using the class
                expl = Explosion(hit.rect.center, 'lg')
                expl.play_sound()
                all_sprites.add(expl)
                self.newmob()

            # Checking if a Mob hit the Player
            hits = pygame.sprite.spritecollide(self.player, mobs, True, pygame.sprite.collide_circle)
            # NOTE: a list starts with nothing in it (False), so when something gets added then... (becomes True)
            for hit in hits:
                self.player.shield -= hit.radius * 2
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                self.newmob()

                # Check if the Player is dead and end the game if so 
                if self.player.shield <= 0:
                    expl = Explosion(hit.rect.center, 'lg')
                    expl.play_sound()
                    running = False

            # Draw / Rendering
            self.gameDisplay.fill(BLACK)
            self.gameDisplay.blit(self.background, self.background_rect)
            all_sprites.draw(self.gameDisplay)
            self.draw_text(self.gameDisplay, 'SCORE:  ' + str(self.score), 25, WIDTH / 2, 10)

            self.draw_shield_bar(self.gameDisplay, 5, 5, self.player.shield)

            # AFTER drawing everything, Update the full display Surface to the screen
            pygame.display.flip()



Shmup().run()

time.sleep(0.25)
pygame.quit()
quit()
