import pygame 
import random

from settings import *


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.meteor_images = self.init_meteors()
        self.image_orig = random.choice(self.meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)  # 85% width / 2

        # Preventing the Mob appearing half off the screen
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)  # used to check the circle collistion


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()  # comment this line out to take out rotaing
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Randomising the Mob's location if it goes off the bottom of the screen 
        if (self.rect.top > HEIGHT + 10) or (self.rect.right < 0) or (self.rect.left > WIDTH):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(1, 8)

    def init_meteors(self):
        meteor_images = []
        meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
        # Appending the meteor images to the meteor_images list
        for img in meteor_list:
            meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

        return meteor_images
