import pygame
import sys


pygame.init()

paddle_surface = pygame.Surface((10, 100))
paddle_surface.fill((255, 255, 255))  

pygame.image.save(paddle_surface, 'paddle.png')

pygame.quit()

win_width = 800
win_height = 400
FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Ping Pong")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, up_key, down_key):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (10, 100))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.y > 0 and keys[self.up_key]:
            self.rect.y -= 5
        if self.rect.y < win_height - 100 and keys[self.down_key]:
            self.rect.y += 5

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (win_width // 2, win_height // 2)
        self.speed_x = 5 * (-1)**(pygame.time.get_ticks() % 2)
        self.speed_y = 5 * (-1)**(pygame.time.get_ticks() % 2)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.top <= 0 or self.rect.bottom >= win_height:
            self.speed_y *= -1
        
        if self.rect.left <= 0 or self.rect.right >= win_width:
            self.reset()

    def reset(self):
        self.rect.center = (win_width // 2, win_height // 2)
        self.speed_x *= -1

player1 = GameSprite('paddle.png', 30, win_height // 2 - 50, pygame.K_w, pygame.K_s)
player2 = GameSprite('paddle.png', win_width - 40, win_height // 2 - 50, pygame.K_UP, pygame.K_DOWN)
ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()

    if pygame.sprite.collide_rect(ball, player1) or pygame.sprite.collide_rect(ball, player2):
        ball.speed_x *= -1

    window.fill(black)
    all_sprites.draw(window)

    pygame.display.flip()
    clock.tick(FPS)