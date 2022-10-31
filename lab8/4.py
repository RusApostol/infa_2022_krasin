import pygame
import random
from pygame.draw import *
from random import randint
pygame.init()

X = 1200
Y = 700


FPS = 60 #Частота кадров
screen = pygame.display.set_mode((X, Y))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():   #Создание круга с рандомным положением
    coor = []  
    for i in range(randint(1, 10)):
        x = randint(50,1150)  #Координата x
        y = randint(50,450)   #Координата y
        vx = random.randrange(-100, 100, 1)  #Скорость по x
        vy = randint(-10, 10)   #Скорость по y
        r = randint(30,50)    #Радиус круга
        color = COLORS[randint(0, 5)]   #Выбор цвета 
        circle(screen, color, (x, y), r)   #Зарисовка круга
        coor.append([x, y, vx, vy, r, color])
    return coor  #Возвращение двумерного списка координат кругов

def click(event, coor, score):  #Проверка на попадание клика в область (coor: двумерный список координат кругов; score - количество очков до щелчка)
    for i in range(len(coor)):
        if (event.pos[0] - coor[i][0])**2 + (event.pos[1] - coor[i][1])**2 <= coor[i][-2]**2:
            score += 1
            print('Click!', score)
    return score


def moving (coor):
    for i in range(len(coor)):
        if (coor[i][0] <= coor[i][-2]):
            coor[i][2] = random.randrange(0, 100, 1)
        elif (X - coor[i][0] <= coor[i][-2]):
            coor[i][2] = random.randrange(-100, 0, 1)
        elif (coor[i][1] <= coor[i][-2]):
            coor[i][3] = random.randrange(0, 100, 1)
        elif  (Y - coor[i][1] <= coor[i][-2]):
            coor[i][3] = random.randrange(-100, 0, 1)
        coor[i][0] = coor[i][0] + coor[i][2]/10
        coor[i][1] = coor[i][1] + coor[i][3]/10
        circle(screen, coor[i][-1], (int(coor[i][0]), int(coor[i][1])), coor[i][-2])
    return coor
            

pygame.display.update()
clock = pygame.time.Clock()
finished = False

score = 0

Start = False

coor = new_ball()

while not finished:   #Тело алгоритма
    clock.tick(FPS)    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif Start and  event.type == pygame.MOUSEBUTTONDOWN:
            score = click(event, coor, score)
    Start = True
    coor = moving(coor)
    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()