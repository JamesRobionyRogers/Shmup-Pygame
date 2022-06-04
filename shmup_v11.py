# Pygame Shmup Part 11:  Player Lives
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl

import pygame
import random
import time
from os import path

img_dir = path.join(path.dirname(__file__), 'imgs')
snd_dir = path.join(path.dirname(__file__), 'snd')

# setting the contsants - ALL CAPS means a consistant variable
WIDTH = 480
HEIGHT = 600
FPS = 60

# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 65, 44)
GREEN = (55, 255, 51)
BLUE = (57, 155, 255)
YELLOW = (255, 223, 34)

# initialise pygame and create window
pygame.mixer.pre_init(44100, -16, 1, 1024)  # initialises pygame sound effects and music
pygame.init()  # initialises pygame


# creates game window (variable a.k.a: screen)
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!  version 11")  # title of the game window
clock = pygame.time.Clock()


font_name = pygame.font.match_font('arail')


def draw_text(surf, text, size, x, y, font_type):
    font_type = pygame.font.match_font(font_type)
    font = pygame.font.Font(font_type, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:  # incase any sort of bug happens
        pct = 0
    BAR_WIDTH = 100
    BAR_HEIGHT = 12
    fill = (pct / 100 * BAR_WIDTH)
    outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)  # 2 corrosponds to the thickness (giving it a border look)
    draw_text(gameDisplay, f'{int(fill)}%', 20, 135, 9.5, 'chakra petch')


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i  # 10 pixel spacing between ships  -  change + to - for revecing the side the ships are taken away from
        img_rect.y = y
        surf.blit(img, img_rect)


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
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
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
            shoot_sound.play()
            shoot_sound.set_volume(0.8)
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


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
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:  # change 25 to 100
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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0  # change to -1
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75  # change how long the explosion animation takes

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png', ]
for img in meteor_list:  # appending the meteor images to the meteor_images list
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(9):
    filename = f'regularExplosion0{i}.png'  # 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    filename = f'sonicExplosion0{i}.png'  # 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)


# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser_2.wav'))
expl_sounds = []
for snd in ['expl_1.wav', 'expl_2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_death_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
# background music
pygame.mixer.music.load(path.join(snd_dir, 'bg_music.ogg'))
pygame.mixer.music.set_volume(1)

# sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):  # spawning mobs
    newmob()

score = 0
pygame.mixer.music.play(loops=-1)


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


# Update / Checks
    all_sprites.update()

    # check to see if a bullet it a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        # explosion sound
        expl_snd = random.choice(expl_sounds)
        expl_snd.set_volume(0.35)
        expl_snd.play()

        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()

    # Player Death  -  check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:  # a list starts with nothing in it (False), so when something gets added then... (becomes True)
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()

        if player.shield <= 0:
            player_death_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # if the player died and the explosion has finnished playing
    if player.lives == 0 and not death_explosion.alive():  # player has no more lives and explosio finnished playing
        running = False

# Draw / Rendering
    gameDisplay.fill(BLACK)
    gameDisplay.blit(background, background_rect)
    all_sprites.draw(gameDisplay)

    draw_text(gameDisplay, f'SCORE:  {str(score)}', 25, WIDTH / 2, 10, 'ariel')
    draw_shield_bar(gameDisplay, 8, 8, player.shield)
    draw_lives(gameDisplay, WIDTH - 100, 8, player.lives, player_mini_img)

    pygame.display.flip()  # AFTER drawing everything, flip the diaplay

# time.sleep(3)
pygame.quit()
quit()


# Suggestions:
#
# - Move Foward and Backwords aswell as the already done right & left
