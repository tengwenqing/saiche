import pygame
import sys
from pygame.locals import *
import time
import random

WINDOW_WIDTH = 486
WINDOW_HEIGHT = 700

# 期望FPS
DEFAULT_FPS = 60
# 每次循环的耗时时间
DEFAULT_DELAY = 1.0 / DEFAULT_FPS - 0.002


class Car:
    def __init__(self, window):
        self.window = window
        self.reset()

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move_left(self):
        self.x -= WINDOW_WIDTH / 3
        if self.x < (WINDOW_WIDTH / 3 - self.width) / 2:
            self.x = (WINDOW_WIDTH / 3 - self.width) / 2

    def move_right(self):
        self.x += WINDOW_WIDTH / 3
        if self.x > WINDOW_WIDTH - self.width / 2 * 3:
            self.x = WINDOW_WIDTH - self.width / 2 * 3

    def reset(self):
        self.img = pygame.image.load("img/car.png")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = (WINDOW_WIDTH / 3 - self.width) / 2
        self.y = WINDOW_HEIGHT - self.height - 50


class Stone:
    def __init__(self, window):
        self.window = window
        self.reset()
        self.stones = []

    def move(self):
        self.y += 10
        if self.y > WINDOW_HEIGHT:
            self.reset()

    def display(self):
        self.window.blit(self.img, (self.x, self.y))
        for stone in self.stones:
            if stone.y > WINDOW_HEIGHT:
                self.stones.remove(stone)

    def reset(self):
        self.img = pygame.image.load("img/stone.png")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        left = WINDOW_WIDTH / 6 - self.width / 2
        middle = WINDOW_WIDTH / 2 - self.width / 2
        right = WINDOW_WIDTH - WINDOW_WIDTH / 9 - self.width
        coordinate = [left, middle, right]
        self.x = random.choice(coordinate)
        self.y = -self.width


class Bomb:
    def __init__(self, window, x, y):
        self.window = window
        self.images = []
        for i in range(1, 14):
            self.images.append(pygame.image.load("bomb/image {}.png".format(i)))
        self.index = 0
        self.img = self.images[self.index]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x - self.width / 2
        self.y = y - self.height / 2

        self.is_destroyed = False

    def display(self):
        if self.index >= len(self.images):
            self.is_destroyed = True
            return
        self.img = self.images[self.index]
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.window.blit(self.img, (self.x, self.y))

        self.index += 1


if __name__ == '__main__':
    # 初始化
    pygame.init()

    # 设置窗口大小
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # 设置窗口标题
    pygame.display.set_caption("赛车游戏")

    # 设置真实的FPS
    fps = 0
    #设置时间
    score = 0

    # 加载背景图片
    bg = pygame.image.load("img/s.png")

    # 加载字体
    font = pygame.font.Font("font/happy.ttf", 20)
    finish_text = font.render("游戏结束", True, (0xff, 0, 0))
    ft_width = finish_text.get_width()
    ft_height = finish_text.get_height()
    ft_x = (WINDOW_WIDTH - ft_width) / 2
    ft_y = (WINDOW_HEIGHT - ft_height) / 2 - 50

    # 加载小车
    car = Car(window)
    # 加载石头
    stones = []
    for i in range(2):
        stones.append(Stone(window))

    # 加载爆炸
    bombs = []

    # 游戏结束的标志
    is_over = False

    while True:
        # 开始时间
        start = time.time()
        # 渲染
        window.blit(bg, (0, 0))
        # 渲染文本
        fps_test = font.render("FPS: %d" % fps, True, (0x33, 0xCC, 0x33))
        score_test = font.render("score: %d" % score, True, (0x33, 0xCC, 0x33))
        # 显示文本
        window.blit(fps_test, (400, 10))
        window.blit(score_test, (20, 10))

        # 若游戏结束
        if is_over:
            window.blit(finish_text, (ft_x, ft_y))
        if not is_over:
            # 加载车
            car.display()
            # 显示石头
            for stone in stones:
                stone.display()
                stone.move()
                score += 3

            # 车的矩形
            car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
            # 石头的矩形
            for stone in stones:
                stone_rect = pygame.Rect(stone.x, stone.y, stone.width, stone.height)
                collide = pygame.Rect.colliderect(car_rect, stone_rect)
                if collide:
                    bombs.append(Bomb(window, car.x + car.width / 2, car.y + car.height / 2))
                    is_over = True

        for bomb in bombs:
            if bomb.is_destroyed:
                bombs.remove(bomb)
            bomb.display()

        # 刷新图像
        pygame.display.flip()

        ####事件捕捉
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    # 小车向左移动
                    car.move_left()
                if event.key == K_RIGHT:
                    # 小车向右移动
                    car.move_right()
                if event.key == K_RETURN and is_over:
                    # 重置状态
                    for stone in stones:
                        stone.reset()
                        score = 0
                    is_over = False

        # 结束时间
        end = time.time()
        # 消耗时间
        cost = end - start

        if cost < DEFAULT_DELAY:
            sleep = DEFAULT_DELAY - cost
        else:
            sleep = 0

        # 睡眠
        time.sleep(sleep)

        end = time.time()

        fps = 1.0 / (end - start)
