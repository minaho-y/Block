import math
import pygame
import random
import sys

import pygame.event

### 画面定義(X軸,Y軸,横,縦)
SCREEN  = pygame.Rect(0, 0, 800, 600) # 画面サイズ

BALL_SIZE = 18
P_WIDTH = 100
P_HEIGHT = 10
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 25
B_TOP = 50
BLOCK_LOWS = 6
BLOCK_COLS = 14
BLOCK_OFFSET_X = int((SCREEN.width - (BLOCK_WIDTH * BLOCK_COLS)) / 2)

# 画像のパス
PADDLE_IMAGE_PATH = "paddle_04.png"
BALL_IMAGE_PATH = "ballYellow_02.png"
BLOCK_IMAGE_PATH = "tileBlue_02.png"

class Paddle(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (P_WIDTH, P_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN.bottom - 20   # パドルのy座標
        self.rect.left = SCREEN.width / 2 - self.rect.width / 2
        
    def update(self):
        # パドルの移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        self.rect.clamp_ip(SCREEN)      # ゲーム画面内のみで移動

class Ball(pygame.sprite.Sprite):
    def __init__(self, filename, paddle, blocks, speed, angle_left, angle_right):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        self.dx = self.dy =  0      # ボールの速度
        self.paddle = paddle        # パドルへの参照
        self.blocks = blocks        # ブロックグループへの参照
        self.update = self.start    # ゲーム開始状態に更新
        self.speed = speed
        self.angle_left = angle_left    # パドルへの反射方向
        self.angle_right = angle_right

    def start(self):
        # ボールの初期位置（パドルの上）
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top

        # スペースキーでボール射出
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.dx = 0
            self.dy = -self.speed
            self.update = self.move


    # ボールの挙動
    def move(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

        # 壁との反射
        if self.rect.left < SCREEN.left:    # 左側
            self.rect.left = SCREEN.left
            self.dx = -self.dx
        if self.rect.right > SCREEN.right:  # 右側
            self.rect.right = SCREEN.right
            self.dx = -self.dx
        if self.rect.top < SCREEN.top:      # 上側
            self.rect.top = SCREEN.top
            self.dy = -self.dy

        # パドルとの反射(左端:135度方向, 右端:45度方向, それ以外:線形補間)
        if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
            (x1, y1) = (self.paddle.rect.left - self.rect.width, self.angle_left)
            (x2, y2) = (self.paddle.rect.right, self.angle_right)
            x = self.rect.left      # ボールが当たった位置
            y = (float(y2-y1)/(x2-x1)) * (x-x1) + y1    # 線形補間
            angle = math.radians(y)
            self.dx = self.speed * math.cos(angle)
            self.dy = -self.speed * math.sin(angle)

        # ボールを落とした場合
        if self.rect.top > SCREEN.bottom:
            self.update = self.start    # ボールを初期状態に

        # ボールと衝突したブロックリストを取得
        blocks_collided = pygame.sprite.spritecollide(self, self.blocks, True)
        if blocks_collided:
            oldrect = self.rect
            for block in blocks_collided:
                # ボールが左からブロックへ衝突
                if oldrect.left < block.rect.left and oldrect.right < block.rect.right:
                    self.rect.right = block.rect.left
                    self.dx = -self.dx

                # ボールが右からブロックへ衝突
                if oldrect.left > block.rect.left and oldrect.right > block.rect.right:
                    self.rect.left = block.rect.right
                    self.dx = -self.dx

                # ボールが上からブロックへ衝突
                if oldrect.top < block.rect.top and oldrect.bottom < block.rect.bottom:
                    self.rect.bottom = block.rect.top
                    self.dy = -self.dy

                # ボールが下からブロックへ衝突
                if oldrect.top > block.rect.top and oldrect.bottom > block.rect.bottom:
                    self.rect.top = block.rect.bottom
                    self.dy = -self.dy

    # def draw(self):
    #     pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

class Block(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = BLOCK_OFFSET_X + x * self.rect.width
        self.rect.top = y * self.rect.height + B_TOP

def main():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    # 描画用のスプライトグループ
    group = pygame.sprite.RenderUpdates()

    # 衝突判定用のスプライトグループ
    blocks = pygame.sprite.Group()

    # スプライトグループに追加
    Paddle.containers = group
    Ball.containers = group
    Block.containers = group, blocks

    paddle = Paddle(PADDLE_IMAGE_PATH)

    # ブロックの作成 (14 x 10)
    for y in range(0, BLOCK_LOWS):
        for x in range(0,BLOCK_COLS):
            Block(BLOCK_IMAGE_PATH, x, y)

    Ball(BALL_IMAGE_PATH, paddle, blocks, 5, 135, 45)

    clock = pygame.time.Clock()

    running = True

    while(running):
        clock.tick(60)  # フレームレート
        screen.fill((0, 20, 0))

        # 全てのスプライトグループを更新
        group.update()
        # 全てのスプライトグループを描画
        group.draw(screen)
        # 画面更新
        pygame.display.update()

        # イベント処理
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:
                running = False
            # キーイベント
            if event.type == pygame.KEYDOWN:
                # Escキーが押されたら終了
                if event.key == pygame.K_ESCAPE:
                    running = False
    # 終了処理
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()