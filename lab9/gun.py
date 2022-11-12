import math
from random import choice
import random 
from pygame.draw import *
import numpy as np
import pygame

FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

G = 0.4

N = random.randint(1, 3)

class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0.0
        self.color = choice(GAME_COLORS)
        self.live = 240

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x + self.vx + self.r >= WIDTH or self.x + self.vx - self.r <= 0:
            self.vx = -self.vx // np.sqrt(3)
        if self.y - self.vy + self.r >= HEIGHT or self.y - self.vy - self.r <= 0:
            self.vy = -self.vy // np.sqrt(3)
        self.x += self.vx
        self.y -= self.vy
        self.vy -= G
        self.live -= 1

    def draw(self):
        
        """
        Drawing the Ball
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 50
        self.y = 580
        self.vx = 2
        self.ax = 0
        self.tank_l = 40
        self.tank_h = self.y

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) // 2
        new_ball.vy = - self.f2_power * math.sin(self.an) // 2
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 20

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] - self.x == 0:
                if event.pos[1] > self.y:
                    self.an = math.asin(1)
                else:
                    self.an = math.asin(1) + np.pi
            elif event.pos[0] - self.x > 0:
                self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
            elif event.pos[0] - self.x < 0:
                self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x)) + np.pi
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
    
    def move(self):
        """Переместить танк по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, стен по краям окна (размер окна 800х600).
        """
        if self.x + self.tank_l + self.vx >= WIDTH or self.x - self.tank_l + self.vx <= 0:
            self.vx = -self.vx
        self.x += self.vx
        self.vx += self.ax
             

    def draw(self):
        
        """
        Drawing the Tank and the Gun
        """
        a = self.f2_power
        b = 10
        self.x
        self.y
        polygon(screen, self.color, [(self.x, self.y),
                                     (self.x + a * math.cos(self.an), self.y + a * math.sin(self.an)),
                                     (self.x + a * math.cos(self.an) + b * math.sin(self.an),
                                      self.y + a * math.sin(self.an) - b * math.cos(self.an)),
                                     (self.x + b * math.sin(self.an), self.y - b * math.cos(self.an))])
        rect(self.screen, self.color, (self.x - self.tank_l, self.tank_h, 2 * self.tank_l, HEIGHT))

    def power_up(self):
        
        """
        Limiting power of Gun
        """
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen: pygame.Surface, x=450, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.live = 1
        self.points = 0
        self.color = RED

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(15, 20)
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """
        Drawing the Target
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
text = pygame.font.Font(None, 24)
bullet = 0
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
finished = False

sum_score = 0

for i in range(N):
    targets.append(Target(screen))
for target in targets:
    target.new_target()
    
    
    
    
while not finished:
    del_balls = []
    screen.fill(WHITE)
    for ball in balls:
        ball.draw()
    for target in targets:
        target.draw()
    gun.move()
    gun.draw()
    text_score = text.render('score: ' + str(sum_score), True, (139, 0, 255))
    screen.blit(text_score, (20, 30))
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for i in range(len(balls)):
        b = balls[i]
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                pygame.display.update()
                screen.fill(WHITE)
                gun.draw()
                for b in balls:
                    b.draw()
                if bullet <= 3:   #You have to hit the target for less than 3 shots
                    sum_score += 1
                text_score_1 = text.render('score: ' + str(sum_score), True, (139, 0, 255))
                screen.blit(text_score_1, (20, 30))
                text_score_2 = text.render('Вы уничтожили цель за ' + str(bullet) + " выстрелов", True, (0, 214, 120))
                screen.blit(text_score_2, (250, 250))
                bullet = 0
                pygame.display.update()
                clock.tick(1)
                target.live = 0
                target.hit()
                target.new_target()
        if b.live < 0:
            del_balls.append(i)
    for i in del_balls:
        balls.pop(i)
    gun.power_up()

pygame.quit()

