import pygame
import random
import math
try:
    from shapes import Ball
except ImportError:
    from OOP_PYGAME.shapes import Ball

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
IMAGE = r'C:\Users\s8425597\Documents\Python\pictures\dog.jpeg'
PLANE = r'C:\Users\s8425597\Documents\Python\pictures\plane.png'
BULLET = r'C:\Users\s8425597\Documents\Python\pictures\doood.png'
SOUND_FILE = r'C:\Users\s8425597\Documents\Python\sounds\gun_shot.mp3'
REFRESH_RATE = 60
ZERO = 0
NUMBER_OF_BALLS = 50
DISTANCE = 15
KING_EXIST = False

############### Initialization ##############
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


############### FUNCTIONS ###############
def debug(whatever):
    # print(whatever)
    return

# Random speed cant be 0
def rnd_speed():
    speed = random.randrange(-3,3)
    if speed == 0:
        speed = rnd_speed()
    return speed

def add_ball_to_board(x,y, AddAKind):
    if AddAKind:
        isKING = True
    else:
        isKING = False
    ball = Ball(x, y, isKING)
    if ball.is_king():
        vx = 0
        vy = 0
        ball.update_v(vx, vy)
        global KING_EXIST
        global KING_POS
        KING_EXIST = True
        KING_POS = ball.get_pos()
        global king_ball
        king_ball = ball
    else:
        vx = rnd_speed()
        vy = rnd_speed()
        ball.update_v(vx, vy)
    ball_list.add(ball)



def create_king_circle(num_dods):
    circle_pos_list = []
    LEN = 100
    global king_ball

    X1, Y1 = king_ball.get_pos()

    for angle in range(0, 360, int(360/(num_dods))):
        print(str(angle))
        X2 = X1 + (math.cos(math.radians(angle)) * LEN)
        Y2 = Y1 + (math.sin(math.radians(angle)) * LEN)
        cir_pos = (X2,Y2)
        circle_pos_list.append(cir_pos)
    return circle_pos_list


def go_to_pos():
    i = 0
    ball_count = len(ball_list) - 1
    circlelist = create_king_circle(ball_count)
    for ball in ball_list:
        if ball.is_king() == False:
            if i < len(circlelist):
                pos_x, pos_y = circlelist[i]
            x, y = ball.get_pos()
            if pos_x > (x+3):
                vx = 3
                debug("pos x bigger")
            elif pos_x < (x-3):
                vx = -3
                debug("pos x smaller")
            else:
                vx = 0
                ball.set_pos(pos_x ,y)
                ball_count -= 0.5
            if pos_y > (y+3):
                vy = 3
                debug("pos y bigger")
            elif pos_y < (y-3):
                vy = -3
                debug("pos y smaller")
            else:
                vy = 0
                ball.set_pos(x, pos_y)
                ball_count -= 0.5
            ball.update_v(vx,vy)
            ball.update_loc()

            if i == 0:
                debug("ZERO######")
            debug("dod {} {}".format(pos_x, pos_y))
            debug("ball pos {} {}".format(x,y))
            i += 1
    if ball_count == 0:
        global balls_not_in_place
        balls_not_in_place = False
        global circlelist2
        circlelist2 = create_king_circle(len(ball_list)-1)
        global king_ball
        vx = rnd_speed()
        vy = rnd_speed()
        king_ball.update_v(vx, vy)


def stop_all_balls():
    for ball in ball_list:
        ball.update_v(0,0)

global addition
addition = 0
def continue_board(pre_king):
    global addition
    if pre_king:
        for ball in ball_list:
            ball.update_loc()
            x, y = ball.get_pos()
            if x > WINDOW_WIDTH - 1 or x < 1:
                vx, vy = ball.get_v()
                ball.update_v(-vx, vy)
            if y > WINDOW_HEIGHT - 1 or y < 1:
                vx, vy = ball.get_v()
                ball.update_v(vx, -vy)
    else:
        global king_ball
        king_ball.update_loc()
        x, y = king_ball.get_pos()
        if x > WINDOW_WIDTH - 1 or x < 1:
            vx, vy = king_ball.get_v()
            king_ball.update_v(-vx, vy)
        if y > WINDOW_HEIGHT - 1 or y < 1:
            vx, vy = king_ball.get_v()
            king_ball.update_v(vx, -vy)

        i = 0
        ball_count = len(ball_list)-1
        addition += 5
        for ball in ball_list:
            if not ball.is_king():
                LEN = 100
                X1, Y1 = king_ball.get_pos()
                ball_count = len(ball_list) - 1
                for angle in range(0, 360, int(360 /(ball_count))):
                    angle = angle + addition
                    print(str(angle))
                    X2 = X1 + (math.cos(math.radians(angle)) * LEN)
                    Y2 = Y1 + (math.sin(math.radians(angle)) * LEN)
                    cir_pos = (X2, Y2)




                    ball.set_pos(X2, X1)
                    ball.update_loc()
                i += 1


global balls_not_in_place
balls_not_in_place = True
finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and not KING_EXIST:
            x, y = pygame.mouse.get_pos()
            add_ball_to_board(x, y, True)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and not KING_EXIST:
            x, y = pygame.mouse.get_pos()
            add_ball_to_board(x, y, False)

    if KING_EXIST and balls_not_in_place:
        stop_all_balls()
        go_to_pos()
    elif KING_EXIST and not balls_not_in_place:
        continue_board(False)
    else:
        continue_board(True)
    screen.blit(img, (0, 0))
    ball_list.draw(screen)
    pygame.display.flip()
    clock.tick(REFRESH_RATE)






