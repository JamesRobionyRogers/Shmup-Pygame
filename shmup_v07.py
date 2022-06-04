# Pygame Shmup Part 7:  Score and Drawing Text

# Pygame template - skeleton for a new pygame project
import pygame
import random
import time
from os import path

img_dir = path.join(path.dirname(__file__), 'imgs')

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
YELLOW = (255, 223, 34)

# initialise pygame and create window
pygame.init()  # initialises pygame
pygame.mixer.init()  # initialises pygame sound effects and music

# creates game window (variable a.k.a: screen)
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!  version 07")  # title of the game window
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arail')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)  # used to check the circle collistion
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        # movement [LEFT & RIGHT]
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speedx = -7         # change player speed here
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speedx = 7          # and change player speed here
        self.rect.x += self.speedx
        # boundaries
        if self.rect.right > WIDTH:  # right boundary
            self.rect.right = WIDTH
        if self.rect.left < 0:       # left boundary
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)  # 85% width / 2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)  # used to check the circle collistion

        # will not appear half off the screen
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

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
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:  # change 20 to 100
            # if it goes off the bottom, we rerandomize the sprites location
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10            # change bullet speed

    def update(self):
        self.rect.y += self.speedy
        # kill the bullet if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png', ]
for img in meteor_list:  # appending the meteor images to the meteor_images list
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):  # change amount of meteors on the screen at once
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

score = 0

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

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

# Update
    all_sprites.update()

    # check to see if a bullet it a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        m = Mob()
        mobs.add(m)
        all_sprites.add(m)
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    # a list starts with nothing in it (False), so when something gets added then... (becomes True)
    if hits:
        running = False

# Draw / Rendering
    gameDisplay.fill(BLACK)
    gameDisplay.blit(background, background_rect)
    all_sprites.draw(gameDisplay)
    draw_text(gameDisplay, 'SCORE:  ' + str(score), 25, WIDTH / 2, 10)
    # *after* drawing everything, flip the diaplay
    pygame.display.flip()


time.sleep(0.25)
pygame.quit()
quit()
