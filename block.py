import pygame
import random

pygame.init()

screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Paddle():
    def __init___(self):
        self.width = 100
        self.height = 10
        self.rect = pygame.Rect(screen_width // 2 - self.width // 2, screen_height - 20, self.width, self.height)
        

# paddle_width = 100
# paddle_height = 10
# paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 20, paddle_width, paddle_height)

class Ball():
    def __init__(self):
        self.diameter = 10
        self.rect = pygame.Rect(screen_width // 2 - self.diameter // 2, screen_height // 2 - self.diameter // 2, self.diameter, self.diameter)
        # self = pygame.Rect(screen_width // 2 - self.diameter // 2, screen_height // 2 - self.diameter // 2, self.diameter, self.diameter)
        self.speed_x = 3 * random.choice((1, -1))
        self.speed_y = 3 * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

paddle = Paddle()

# ball_diameter = 10
# ball = pygame.Rect(screen_width // 2 - ball_diameter // 2, screen_height // 2 - ball_diameter // 2, ball_diameter, ball_diameter)
# ball_speed_x = 3 * random.choice((1, -1))
# ball_speed_y = 3 * random.choice((1, -1))

ball = Ball()

block_list = []
block_width = 60
block_height = 20
for i in range(6):
    for j in range(5):
        block_list.append(pygame.Rect(i * (block_width + 10) + 10, j * (block_height + 10) + 10, block_width, block_height))

# ゲームのループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # パドルの操作
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.move_ip(5, 0)

    # ボールの動き
    # ball.move_ip(ball_speed_x, ball_speed_y)
    ball.move()

    # ボールが画面の端に当たったら反射
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    # ボールがパドルに当たったら反射
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # ボールがブロックに当たったらブロックを消去して反射
    for block in block_list[:]:
        if ball.colliderect(block):
            block_list.remove(block)
            ball_speed_y *= -1
            break
    
    # ボールが画面下にいったらリセット
    if ball.bottom >= screen_height:
        ball = pygame.Rect(screen_width // 2 - ball_diameter // 2, screen_height // 2 - ball_diameter // 2, ball_diameter, ball_diameter)
        ball_speed_x = 3 * random.choice((1, -1))
        ball_speed_y = 3 * random.choice((1, -1))

    # 画面の描画
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for block in block_list:
        pygame.draw.rect(screen, WHITE, block)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()