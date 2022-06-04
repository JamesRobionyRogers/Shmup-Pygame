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
from Powerup import *


class Shmup():

    # Initialise pygame and create window
    pygame.mixer.pre_init(44100, -16, 1, 1024)      # initialises pygame sound effects and music
    pygame.init()                                   # initialises pygame

    # Titleing the game window
    pygame.display.set_caption("Shmup!  Version 11")

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
        # # Spawning mobs
        # for i in range(MOB_NUM):
        #     self.newmob()

    def draw_text(self, surface, text, size, x, y, font_type):
        font_type = pygame.font.match_font(font_type)
        font = pygame.font.Font(font_type, size)
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
        pygame.draw.rect(surface, WHITE, outline_rect, 2)   # 2 corrosponds to the thickness (giving it a border look)
        # Displaying the percentage of shield left 
        self.draw_text(self.gameDisplay, f'{int(fill)}%', 20, 135, 9.5, 'chakra petch')

    def draw_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 35 * i     # 10 pixel spacing between ships. Change + to - for reversing the side the ships are taken away from
            img_rect.y = y
            surf.blit(img, img_rect)

    def game_over_screen(self):
        self.gameDisplay.blit(self.background, self.background_rect)
        self.draw_text(self.gameDisplay, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4, 'kenvector')
        self.draw_text(self.gameDisplay, "A & D to move  -  Space Bar to fire", 22, WIDTH / 2, HEIGHT / 2, 'kenvector')
        self.draw_text(self.gameDisplay, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3/4, 'kenvector')
        self.draw_text(self.gameDisplay, f'SCORE:  {str(self.score)}', 25, WIDTH / 2, 10, 'ariel')
        pygame.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                # Checking for quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Checking for play again event
                if event.type == pygame.KEYUP:
                    waiting = False

    def reset_sprite_groups(self):
        all_groups = [all_sprites, mobs, bullets, powerups]
        for group in all_groups:
            for sprite in group.sprites():
                sprite.kill()


    def run(self):
        game_over = True 
        running = True
        # Game Loop
        while running:
            if game_over:
                # Process game over 
                self.game_over_screen() 

                # Reset the game for another round 
                game_over = False
                
                # Resetting the sprite groups
                # all_sprites = pygame.sprite.Group()
                # mobs = pygame.sprite.Group()
                # bullets = pygame.sprite.Group()
                # powerups = pygame.sprite.Group()

                self.reset_sprite_groups()
                self.player = Player()
                all_sprites.add(self.player)

                for i in range(MOB_NUM):
                    self.newmob()

                self.score = 0

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

            # Meteor Death - Checking if a Bullet hit a Mob
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                # Adding to the score 
                self.score += 60 - hit.radius

                # Create an Explosion using the class
                expl = Explosion(hit.rect.center, 'lg')
                expl.play_sound()
                all_sprites.add(expl)

                # Powerup Spawning - Random chance of spawning a Powerup
                if random.random() < 0.1:
                    powerup = Powerup(hit.rect.center)
                    all_sprites.add(powerup)
                    powerups.add(powerup)

                self.newmob()
                    

            # Player Death - Checking if a Mob hit the Player
            hits = pygame.sprite.spritecollide(self.player, mobs, True, pygame.sprite.collide_circle)
            for hit in hits:
                self.player.shield -= hit.radius * 2
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
                self.newmob()

                # Check if the Player is dead and end the game if so 
                if self.player.shield <= 0:
                    death_explosion = Explosion(hit.rect.center, 'player')
                    death_explosion.play_sound('player')
                    all_sprites.add(death_explosion)
                    self.player.hide()
                    self.player.lives -= 1
                    self.player.shield = 100


            # Powerup Collection - Checking if a Powerup was collected
            hits = pygame.sprite.spritecollide(self.player, powerups, True)
            for hit in hits:
                if hit.type == 'shield':
                    self.player.shield += random.randrange(10, 30)
                    if self.player.shield >= 100:
                        self.player.shield = 100

                if hit.type == 'gun':
                    self.player.powerup()

            # Playing the full player explosion when the player dies 
            if self.player.lives == 0 and not death_explosion.alive():
                game_over = True

            # Draw / Rendering
            self.gameDisplay.fill(BLACK)
            self.gameDisplay.blit(self.background, self.background_rect)
            all_sprites.draw(self.gameDisplay)

            # Draw the score and lives
            self.draw_text(self.gameDisplay, 'SCORE:  ' + str(self.score), 25, WIDTH / 2, 10, 'ariel')
            self.draw_shield_bar(self.gameDisplay, 5, 5, self.player.shield)
            self.draw_lives(self.gameDisplay, WIDTH - 100, 5, self.player.lives, self.player.player_mini_img)  # player_lives_img reffers to setting.py

            # AFTER drawing everything, Update the full display Surface to the screen
            pygame.display.flip()



Shmup().run()

time.sleep(0.25)
pygame.quit()
quit()
