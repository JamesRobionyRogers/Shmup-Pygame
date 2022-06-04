import pygame

from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10            # change bullet speed

    def update(self):
        self.rect.y -= self.speedy
        # Kill the bullet if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
