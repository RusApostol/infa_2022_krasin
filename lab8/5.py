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




def new_ball():   
    ''' 
    Создание произвольного круга. 
    x, y - координата центра круга
    vx, vy - скорость движение круга
    r - радиус круга
    color - цвет закраски круга
    coor - массив значений координат, скоростей и цветов кругов
    '''
    coor = []  
    for i in range(randint(1, 10)):
        x = randint(50,1150)
        y = randint(50,450)
        vx = randint(-100, 100)
        vy = randint(-100, 100)
        r = randint(30,50)
        color = COLORS[randint(0, 5)] 
        circle(screen, color, (x, y), r)  
        coor.append([x, y, vx, vy, r, color])
    return coor



def click(event, coor, score): 
    '''
    Проверка на попадание мыши в область круга и написание Click! в командной строке
    coor - двумерный список координат кругов
    score - количество очков до щелчка мыши
    '''
    for i in range(len(coor)):
        if (event.pos[0] - coor[i][0])**2 + (event.pos[1] - coor[i][1])**2 <= coor[i][-2]**2:
            score += 1
            print('Click!', score)
    return score


def moving (coor):
    '''
    Движение кругов и отражение от границ окна
    X, Y - размеры окна 
    '''
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

while not finished:
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