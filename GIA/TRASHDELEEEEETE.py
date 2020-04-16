__author__ = 'Guy'

import math
import pygame
import time

screen = pygame.display.set_mode((500,500))
screen.fill((255,255,255))

locationsXY = []

LEN = 100
count = 8
for angle in range(0, 360, int(360/(count))):
    x = 250 + (math.cos(math.radians(angle)) * LEN)
    y = 250 + (math.sin(math.radians(angle)) * LEN)
    locationsXY.append([x,y])
    pygame.draw.circle(screen, (0,255,0),(int(x),int(y)), 3, 1)

print(locationsXY)


pygame.draw.circle(screen, (0,0,255),(250,250), 100, 1)


pygame.display.flip()
add_count = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    time.sleep(1)
    screen.fill((255, 255, 255))
    add_count += 5
    for angle in range(0, 360, int(360 / (count))):
        angle += add_count
        print(str(angle))
        x = 250 + (math.cos(math.radians(angle)) * LEN)
        y = 250 + (math.sin(math.radians(angle)) * LEN)
        locationsXY.append([x, y])
        pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), 3, 1)
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 100, 1)

    pygame.display.flip()

