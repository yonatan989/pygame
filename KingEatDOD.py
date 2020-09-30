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
SOUND_FILE = r'/home/yonatan/Documents/Python/sounds/gun_shot.mp3'

REFRESH_RATE = 60
ZERO = 0
NUMBER_OF_BALLS = 50
DISTANCE = 15
KING_EXIST = False






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
new_ball_list = pygame.sprite.Group() # Create a list of objects
king_list = pygame.sprite.Group() # Create a king list
'''
for i in range(NUMBER_OF_BALLS):
    ball = Ball(i* DISTANCE, i*DISTANCE)
    ball_list.add(ball)
ball_list.draw(screen)
'''

# Random speed cant be 0
def rnd_speed(FAST):
    if not FAST:
        speed = random.randrange(-3,3)
        if speed == 0:
            speed = rnd_speed(False)
    else:
        rnd = random.randrange(-1,1)
        if rnd == 0:
            print(rnd)
            speed = random.randrange(-9, -5)
        else:
            print(rnd)
            speed = random.randrange(5, 9)

    return speed
# Ball will bounce when touching the walls
def dont_touch_walls(ball_list):
    for ball in ball_list:
        ball.update_loc()
        x, y = ball.get_pos()
        if x > WINDOW_WIDTH - 2 or x < 2:
            vx, vy = ball.get_v()
            ball.update_v(-vx, vy)
        if y > WINDOW_HEIGHT - 20 or y < 2:
            vx, vy = ball.get_v()
            ball.update_v(vx, -vy)

def ball_colliosion(ball_list, king_list):
    new_ball_list.empty()
    for ball in ball_list:
        ball_hit_list = pygame.sprite.spritecollide(ball, king_list, False)
        if len(ball_hit_list) == 0:
            new_ball_list.add(ball)
        ball_list.empty()
        for ball in new_ball_list:
                ball_list.add(ball)
    return ball_list

# Add a dod to the board
def add_ball_to_board(king):
    x, y = pygame.mouse.get_pos()
    if king:
        ball = Ball (x,y, isking=True)
        vx = rnd_speed(True)
        vy = rnd_speed(True)
        ball.update_v(vx, vy)
        king_list.add(ball)

    else:
        ball = Ball(x, y)
        vx = rnd_speed(False)
        vy = rnd_speed(False)
        ball.update_v(vx, vy)
        ball_list.add(ball)

finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            for i in range(1,10):
                add_ball_to_board(False)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            KING_EXIST = True
            add_ball_to_board(KING_EXIST)


    screen.blit(img, (0, 0))
    dont_touch_walls(ball_list)
    dont_touch_walls(king_list)
    ball_list.draw(screen)
    king_list.draw(screen)
    if KING_EXIST:
        ball_colliosion(ball_list, king_list)
    pygame.display.flip()
    clock.tick(REFRESH_RATE)






