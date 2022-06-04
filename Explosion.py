import pygame
import random

from settings import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.explosion_anim = self.init_explotions()[0]
        self.explosion_sounds = self.init_explotions()[1]
        self.image = self.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0  # change to -1
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75  # change how long the explosion animation takes

    def update(self):
        now = pygame.time.get_ticks()
        # Updating the animation to the next frame
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # Killling the animation when it reaches the end
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            
            # Setting vairables for next frame of animation
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    def play_sound(self, type='mob'):
        expl_snd = random.choice(self.explosion_sounds[type])
        expl_snd.set_volume(0.35)
        expl_snd.play()


    def init_explotions(self):
        # Initialising explosion animation
        explosion_anim = {}
        explosion_anim['lg'] = []
        explosion_anim['sm'] = []
        explosion_anim['player'] = []
        for i in range(9):
            # Meteor Explotions
            filename = 'regularExplosion0{}.png'.format(i)
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = pygame.transform.scale(img, (75, 75))
            explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            explosion_anim['sm'].append(img_sm)

            # Player Explotions
            filename = f'sonicExplosion0{i}.png'
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            explosion_anim['player'].append(img)

        # Initialising explosion sound
        explosion_sounds = {}
        explosion_sounds['mob'] = []
        explosion_sounds['player'] = []
        # Appending Mob explosion sounds
        for snd in ['expl_1.wav', 'expl_2.wav']:
            explosion_sounds['mob'].append(pygame.mixer.Sound(path.join(snd_dir, snd)))
        # Appending the player explosion sound
        explosion_sounds['player'].append(pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg')))

        return (explosion_anim, explosion_sounds)
