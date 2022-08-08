import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEMOTION
import random

pygame.mixer.init()

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Atari Breakout")
clock = pygame.time.Clock()

bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

boop_sound = pygame.mixer.Sound('res/boop.ogg')

block_surface1 = pygame.transform.scale(pygame.image.load('res/slider1.png').convert_alpha(), (100, 30))
block_surface2 = pygame.transform.scale(pygame.image.load('res/slider2.png').convert_alpha(), (100, 30))
block_surface3 = pygame.transform.scale(pygame.image.load('res/slider3.png').convert_alpha(), (100, 30))

block_surfaces = [block_surface1, block_surface2, block_surface3]

score = 0
font = pygame.font.Font('freesansbold.ttf', 20)



class Block(pygame.sprite.Sprite):
    width = 100
    height = 30

    def __init__(self, x, y):
        super(Block, self).__init__()
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        surf_index = random.randint(0, 2)
        self.surf = block_surfaces[surf_index]
        self.rect = self.surf.get_rect(topleft=self.pos)


class Slider(pygame.sprite.Sprite):
    def __init__(self):
        super(Slider, self).__init__()
        self.surf = pygame.image.load('res/slider1.png').convert_alpha()
        self.rect = self.surf.get_rect(topleft=(350, 300))


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.x = 250
        self.y = 200
        self.x_modifier = 3
        self.y_modifier = 3
        self.surf = pygame.transform.scale(pygame.image.load('res/ball.png').convert_alpha(), (17, 17))
        self.rect = self.surf.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.x += self.x_modifier
        self.rect.x = self.x
        self.y += self.y_modifier
        self.rect.y = self.y

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.x_modifier *= -1
        if self.rect.top <= 0 or self.rect.colliderect(slider.rect):
            self.y_modifier *= -1
        if self.rect.bottom >= SCREEN_HEIGHT:
            print("Game Over!")
            global gameOver
            gameOver = True


blocks_list = list()


def generate_blocks():
    cols = int(SCREEN_WIDTH / Block.width)
    rows = 5
    for row in range(1, rows + 1):
        for col in range(cols):
            # generate a block
            bl = Block(col * Block.width, row * Block.height)
            blocks_list.append(bl)


generate_blocks()

slider = Slider()
ball = Ball()

blocks_group = pygame.sprite.Group()
blocks_group.add(blocks_list)

all_sprites = pygame.sprite.Group()
all_sprites.add(ball)
all_sprites.add(slider)
all_sprites.add(blocks_list)

gameState = "waiting"
moving = False
gameOver = False


while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            gameOver = True
        elif event.type == MOUSEBUTTONDOWN:
            gameState = "started"
        elif event.type == MOUSEMOTION:
            # event.rel is a tuple of relative positions of the mouse (1,0) (-1, 1) etc
            # i want to only move the slider on the X axis so i will set the Y value to constant 0
            slider.rect.move_ip(event.rel[0], 0)

    screen.blit(bg_surface, (0, 0))
    score_text_surface = font.render("Score: " + str(score), True, (0, 255, 0), (0, 0, 128))
    score_text_rect = score_text_surface.get_rect(topleft=(SCREEN_WIDTH / 2 - 50, 10))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    screen.blit(score_text_surface, score_text_rect)

    if pygame.sprite.spritecollideany(ball, blocks_group):
        boop_sound.play()
        ball.y_modifier *= -1

    blocks_hit_list = pygame.sprite.spritecollide(ball, blocks_group, True)
    for block in blocks_hit_list:
        score += 1

    ball.update()

    if len(blocks_list) == 0:
        gameOver = True

    pygame.display.update()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.mixer.quit()
