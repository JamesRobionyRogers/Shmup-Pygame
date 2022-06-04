import pygame
from settings import *

from Bullet import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.player_mini_img = pygame.transform.scale(self.player_img, (25, 19))
        self.image = pygame.transform.scale(self.player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.player_mini_img.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shield_up_sound = pygame.mixer.Sound(path.join(snd_dir, 'powerup_shield_up.wav'))
        self.shield_down_sound = pygame.mixer.Sound(path.join(snd_dir, 'powerup_shield_down.wav'))
        self.shoot_delay = 250
        self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser_2.wav'))
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_sound = pygame.mixer.Sound(path.join(snd_dir, 'powerup_gun.wav'))
        self.power_timer = pygame.time.get_ticks()

        # DEBUGGING: pygame.draw.circle(self.image, RED, self.rect.center, self.radius)  # used to check the circle collistion


    def update(self):
        # Timeout for power-ups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()
            self.shield_down_sound.play()
        # Unhide the player if currently hidden 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        # Movement [LEFT & RIGHT]
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speedx = -7         # change player speed here
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speedx = 7          # and change player speed here
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        # Boundaries
        if self.rect.right > WIDTH:  # right boundary
            self.rect.right = WIDTH        
        if self.rect.left < 0:       # left boundary
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()
        self.power_sound.play()
        self.power_sound.set_volume(0.8)
        

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.last_shot) > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.shoot_sound.play()
                self.shoot_sound.set_volume(0.8)

            if self.power >= 2:
                bullet1 = Bullet(self.rect.left + 4, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                self.shoot_sound.play()
                self.shoot_sound.set_volume(0.8)

    def hide(self):
        # Hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

