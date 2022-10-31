import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 60 #Частота кадров
screen = pygame.display.set_mode((1200, 700))

RED = (255, 0, 0)   #Создание массива цветов
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():   #Создание круга с рандомным положением
    x = randint(50,1150)  #Координата x
    y = randint(50,450)   #Координата y
    r = randint(30,50)    #Радиус круга
    color = COLORS[randint(0, 5)]   #Выбор цвета 
    circle(screen, color, (x, y), r)  #Прорисовка шара
    coor = [x, y, r]
    return coor

def click(event, coor, score):  #Проверка на попадание клика в область круга
    if (event.pos[0] - coor[0])**2 + (event.pos[1] - coor[1])**2 <= coor[2]**2:
        score += 1   #Добавка очка
        print('Click!', score)
    return score

pygame.display.update()
clock = pygame.time.Clock()
finished = False

score = 0

Start = False

while not finished:   #Тело алгоритма
    clock.tick(FPS)    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif Start and  event.type == pygame.MOUSEBUTTONDOWN:
            score = click(event, coor, score)
    Start = True
    coor = new_ball()
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()