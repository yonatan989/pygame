import pygame
import random
try:
    from shapes import Ball
except ImportError:
    from .shapes import Ball

# Constants
WINDOW_WIDTH = 678
WINDOW_HEIGHT = 381
# Colors
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
SKY = (143,203,239)
PINK = (255,20,147)
# Buttons
LEFT = 1
SCROLL = 2
RIGHT = 3
# Images path'
IMAGE = r'/home/yonatan/Documents/Python/pictures/dog.jpeg'
PLANE = r'C:\Users\s8425597\Documents\Python\pictures\plane.png'
BULLET = r'C:\Users\s8425597\Documents\Python\pictures\doood.png'
SOUND_FILE = r'/home/yonatan/Documents/Python/sounds/HailToTheKing.mp3'
REFRESH_RATE = 60
ZERO = 0
NUMBER_OF_BALLS = 50
DISTANCE = 15






# Init screen
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

# Add img to screen
img = pygame.image.load(IMAGE)

# Add clock
clock = pygame.time.Clock()

# Create a ball list
ball_list = pygame.sprite.Group() # Create a list of objects
'''
for i in range(NUMBER_OF_BALLS):
    ball = Ball(i* DISTANCE, i*DISTANCE)
    ball_list.add(ball)
ball_list.draw(screen)
'''

# Random speed cant be 0
def rnd_speed():
    speed = random.randrange(-3,3)
    if speed == 0:
        speed = rnd_speed()
    return speed



finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            for i in range(1,100):
                x, y = pygame.mouse.get_pos()
                ball = Ball(x,y)
                vx = rnd_speed()
                vy = rnd_speed()
                ball.update_v(vx,vy)
                ball_list.add(ball)

    for ball in ball_list:
        ball.update_loc()
        x, y = ball.get_pos()
        if x > WINDOW_WIDTH-1 or x < 1:
            vx, vy = ball.get_v()
            ball.update_v(-vx,vy)
        if y > WINDOW_HEIGHT-20 or y < 1:
            vx, vy = ball.get_v()
            ball.update_v(vx,-vy)
    screen.blit(img, (0, 0))
    ball_list.draw(screen)
    pygame.display.flip()
    clock.tick(REFRESH_RATE)






