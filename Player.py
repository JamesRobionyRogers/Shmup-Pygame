import pygame
from settings import *

from Bullet import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image = pygame.transform.scale(self.player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)  # used to check the circle collistion
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser_2.wav'))
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # movement [LEFT & RIGHT]
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speedx = -7         # change player speed here
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speedx = 7          # and change player speed here
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        # boundaries
        if self.rect.right > WIDTH:  # right boundary
            self.rect.right = WIDTH
        if self.rect.left < 0:       # left boundary
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot_sound.play()
            self.shoot_sound.set_volume(0.8)
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

