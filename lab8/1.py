from cv2 import getRotationMatrix2D, warpAffine
import pygame
from pygame.draw import *

pygame.init()
screen = pygame.display.set_mode((400, 400))

fps = 30


circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (0, 0, 0), (200, 200), 100, 5)
rect(screen, (0, 0, 0), (166, 233, 66, 20))
circle(screen, (255, 0, 0), (166, 166), 25)
circle(screen, (0, 0, 0), (166, 166), 12)
circle(screen, (255, 0, 0), (233, 166), 20)
circle(screen, (0, 0, 0), (233, 166), 10)
#rect(screen, (125, 125, 125), (210, 136, 75, 10))
#rect(screen, (125, 125, 125), (120, 133, 75, 10))
polygon(screen, (100, 100, 100), [(100, 100), (200, 160),
                               (200, 150), (100, 90), (100, 100)])
polygon(screen, (100, 100, 100), [(300, 105), (200, 165),
                               (200, 155), (300, 95), (300, 105)])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    for event in pygame.event.get():
        clock.tick(fps)
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()