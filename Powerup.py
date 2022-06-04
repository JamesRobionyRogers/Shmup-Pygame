import pygame 
import random

from settings import *

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.powerup_images = self.init_powerups()
        self.image = self.powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4            # change bullet speed

    def update(self):
        self.rect.y += self.speedy
        # Kill the bullet if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

    # TODO: Add powerup images
    def init_powerups(self):
        powerup_images = {}
        powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_silver.png')).convert()
        powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

        return powerup_images

