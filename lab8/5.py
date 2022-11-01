import pygame
import random
from pygame.draw import *
from random import randint
pygame.init()

X = 1200
Y = 700
print("Напишите Ваш Ник (без пробела):")
nickName = input()

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
        vx = randint(-100, 100)  #Скорость по x
        vy = randint(-100, 100)   #Скорость по y
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


def moving (coor):   #Прорисовка движения кругов
    for i in range(len(coor)):
        if (coor[i][0] <= coor[i][-2]):  #Проверка на левый край
            coor[i][2] = random.randrange(0, 100, 1)
        elif (X - coor[i][0] <= coor[i][-2]):         #Проверка на правый край
            coor[i][2] = random.randrange(-100, 0, 1)
        elif (coor[i][1] <= coor[i][-2]):            #Проверка на верхний край
            coor[i][3] = random.randrange(0, 100, 1)
        elif  (Y - coor[i][1] <= coor[i][-2]):          #Проверка на нижний край
            coor[i][3] = random.randrange(-100, 0, 1)
        coor[i][0] = coor[i][0] + coor[i][2]/10  #Добавка скорости по x
        coor[i][1] = coor[i][1] + coor[i][3]/10      #Добавка скорости по y
        circle(screen, coor[i][-1], (int(coor[i][0]), int(coor[i][1])), coor[i][-2])     #Прорисовка нового круга
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
            score = click(event, coor, score)       #Считывание нажатия и проверка на область
    Start = True
    coor = moving(coor)   #Считывание массива координат
    pygame.display.update()
    screen.fill(BLACK)
    
    

with open("best.txt", "r") as f:       #Считывание старой таблицы
    a = list(map(lambda x: [y for y in x.rstrip().split()], f.readlines()))
Find = False
for s in a:       #Поиск имени и изменение результата
    s[1] = int(s[1])
    if s[0] == nickName:
        Find = True
    if s[0] == nickName and s[1] < score:
        s[1] = score
if not Find:
    a.append([nickName, score])
a = sorted(a, key = lambda x: (-x[1], x[0]))
for s in a:
    s[1] = str(s[1])
with open("best.txt", "w") as f:         #Запись новой таблицы
    f.writelines([" ".join(x) + "\n" for x in a])
    

pygame.quit()