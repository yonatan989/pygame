import pygame
import random
import math
import os
import time
import threading
from collections import Iterable
try:
    from shapes import Ball, Bullet
except ImportError:
    from .shapes import Ball,Bullet

############################## Vars Definistion ########################################
# Constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
SKY = (143,203,239)
PINK = (255,20,147)

# Images path's'
IMAGE = r'/home/yonatan/Documents/Python/pictures/madagascar_1.jpg'
PLANE = r'/home/yonatan/Documents/Python/pictures/plane.png'
BULLET = r'/home/yonatan/Documents/Python/pictures/bullet.png'
SOUND_FILE_AFTER_KING = r'/home/yonatan/Documents/Python/sounds/King.wav'
SOUND_FILE_BEFORE_KING = r'/home/yonatan/Documents/Python/sounds/moveit.wav'
SOUND_FILE_BULLET = r'/home/yonatan/Documents/Python/sounds/bullet.wav'
SOUND_FILE_BACKGROUND = 'r/home/yonatan/Documents/Python/sounds/background.wav'
SOUND_FILE_EVIL = 'r/home/yonatan/Documents/Python/sounds/Evil.wav'

# Buttons
LEFT = 1
SCROLL = 2
RIGHT = 3

# Game Control
REFRESH_RATE = 60
ZERO = 0
NUMBER_OF_BALLS = 50
DISTANCE = 15
RADIUS = 300
SPEED = 4
KING_EXIST = False
RIGHT_CLICK = False
DOWN = True
MIN_RAD = 45 # Min distance of balls from king
MAX_RAD = 150 # Max distance of balls from king
IN_AND_OUT_SPEED = 1
BULLET_SPEED = 18
PLAY_AUDIO = True
PLANE_ADDED = False

# Changing vars
global balls_not_in_place
balls_not_in_place = True
finish = False
shot = False
no_bullets = True
add_to_angle = 0
mouse_point_list = []
bullet_mouse_point_list = []
timer_list = []
king_life = 10
only_once = True
############################## END of Var definistion ########################################


############### Initialization ##############
# Init screen
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

# Add img to screen
img = pygame.image.load(IMAGE)

# init Sound effect
if PLAY_AUDIO:
    pygame.mixer.init()

# Add clock
clock = pygame.time.Clock()

# Add Plane
player_image = pygame.image.load(PLANE).convert()
player_image.set_colorkey(PINK)

# load Bullets image
bullet_image = pygame.image.load(BULLET).convert()
bullet_image.set_colorkey(PINK)

# Create a ball list
ball_list = pygame.sprite.Group() # Create a list of objects
new_ball_list = pygame.sprite.Group() # Create a list of objects
bullet_list = pygame.sprite.Group() # Create a king list
new_bullet_list = pygame.sprite.Group()
king_list = pygame.sprite.Group()


############################## FUNCTIONS #######################################################

# Make Sound run in loops
#def play(sound, start, end):
    #sound.set_pos(start)
    #sound.play()
    #time.sleep(end - start)     # in seconds
    #sound.stop()
    #return True

def debug(whatever):
    print(whatever)
    return

# Random speed cant be 0
def rnd_speed():
    speed = random.randrange(-7,7)
    if speed == 0:
        speed = rnd_speed()
    return speed

# Create a random king ball
'''
def king_math():
    num = random.randrange(0,1000)
    return num == 7
'''

# Add a ball object
def add_ball_to_board(x,y):
    global RIGHT_CLICK
    global KING_EXIST
    if not KING_EXIST: #Stopes adding balls when the king is here
        if RIGHT_CLICK:
            isKING = True
        else:
            isKING = False
        ball = Ball(x, y, isKING)

        # When King is created
        if ball.is_king():
            if PLAY_AUDIO:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(SOUND_FILE_AFTER_KING))
            vx = 0
            vy = 0
            ball.update_v(vx, vy)
            KING_EXIST = True
            global KING_POS
            global king_ball
            king_ball = ball # Saves the king ball object
            KING_POS = king_ball.get_pos() # Saves the king ball position
            king_list.add(king_ball)
        else:
            vx = rnd_speed()
            vy = rnd_speed()
            ball.update_v(vx, vy)
            ball_list.add(ball) # Add ball to ball list

def add_bullet_to_board(x,y):
    bullet = Bullet(x, y)
    # When King is created
    if PLAY_AUDIO:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(SOUND_FILE_BULLET))
    vx = BULLET_SPEED
    vy = 0
    bullet.update_v(vx, vy)
    bullet_list.add(bullet) # Add bullet to bullet list

# Sum of balls
def count_balls(balls_list):
    num_of_balls = 0
    for ball in balls_list:
        num_of_balls += 1
    return num_of_balls

# Create array with circle positions
def create_king_circle(num_of_balls, move_with_king = False):
    global DOWN
    global MIN_RAD
    global MAX_RAD
    global IN_AND_OUT_SPEED
    global add_to_angle # Make the ball's spin
    global RADIUS
    global king_ball
    global SPEED
    #SPEED = num_of_balls -1
    circle_pos_list = []

    X1, Y1 = king_ball.get_pos() # Create a center from king position
    if num_of_balls == 0: # Prevent the program from crashing when there are no balls
        num_of_balls = 1
    for angle in range(0, 360, int(360/(num_of_balls))):
        if move_with_king:
            if num_of_balls == 1:
                add_to_angle += 10.8 # Make the ball's spin
            else:
                add_to_angle += math.pi / SPEED # Make the ball's spin
            angle += add_to_angle

        X2 = X1 + (math.cos(math.radians(angle)) * RADIUS)
        Y2 = Y1 + (math.sin(math.radians(angle)) * RADIUS)
        cir_pos = (X2,Y2)
        circle_pos_list.append(cir_pos)

    # Makes the balls go in and out

    if RADIUS >= MAX_RAD:
        DOWN = True
    elif RADIUS <= MIN_RAD:
        DOWN = False
    if DOWN:
        RADIUS -= IN_AND_OUT_SPEED
    else:
       RADIUS += IN_AND_OUT_SPEED

    return circle_pos_list

# Change ball speed to match pos
def change_speed_to_pos( ball, ball_x, ball_y, pos_x, pos_y):
    if pos_x > (ball_x + 3):
        vx = 3
    elif pos_x < (ball_x - 3):
        vx = -3
    else:
        vx = 0
        ball.set_pos(pos_x, ball_y)
    if pos_y > (ball_y + 3):
        vy = 3
    elif pos_y < (ball_y - 3):
        vy = -3
    else:
        vy = 0
        ball.set_pos(ball_x, pos_y)
    return vx, vy

# Moves all balle's towards the king ball
def go_to_pos():
    global king_ball
    index = 0
    ball_count = count_balls(ball_list)
    circle_pos_list = create_king_circle(ball_count)
    for ball in ball_list:
        if not ball.is_king():
            if index < len(circle_pos_list):
                pos_x, pos_y = circle_pos_list[index]
            x, y = ball.get_pos()
            vx, vy = change_speed_to_pos(ball, x, y ,pos_x, pos_y)
            if vx == 0 and vy == 0: # Check if the ball has got to position
                ball_count -= 1
            ball.update_v(vx,vy)
            ball.update_loc()
            index += 1
    if ball_count == 0:
        global balls_not_in_place
        balls_not_in_place = False
        vx = rnd_speed()
        vy = rnd_speed()
        king_ball.update_v(vx, vy)

def change_to_pos():
    global king_ball
    index = 0
    ball_count = count_balls(ball_list)
    circle_pos_list = create_king_circle(count_balls(ball_list), True)
    for ball in ball_list:
        if not ball.is_king():
            if index < len(circle_pos_list):
                pos_x, pos_y = circle_pos_list[index]
            ball.set_pos(pos_x, pos_y)
            vx, vy = 0, 0
            ball.update_v(vx, vy)
            ball.update_loc()
            index += 1

# Stops all balls
def stop_all_balls():
    for ball in ball_list:
        ball.update_v(0,0)

# Makes ball's bounce from corners
def dont_touch_corners(ball_list, destroy):
    if isinstance(ball_list, Iterable):
        for ball in ball_list:
            ball.update_loc()
            x, y = ball.get_pos()
            if x > WINDOW_WIDTH - 1 or x < 1:
                if destroy:
                    ball_list.remove(ball)
                vx, vy = ball.get_v()
                ball.update_v(-vx, vy)
            if y > WINDOW_HEIGHT - 1 or y < 1:
                if destroy:
                    ball_list.remove(ball)
                vx, vy = ball.get_v()
                ball.update_v(vx, -vy)

    else: # If this is the king ball
        ball_list.update_loc()
        x, y = ball_list.get_pos()
        if x > WINDOW_WIDTH - 1 or x < 1:
            vx, vy = ball_list.get_v()
            ball_list.update_v(-vx, vy)
        if y > WINDOW_HEIGHT - 1 or y < 1:
            vx, vy = ball_list.get_v()
            ball_list.update_v(vx, -vy)

def ball_colliosion(ball_list, bullet_list):
    new_ball_list.empty()
    new_bullet_list.empty()
    for ball in ball_list:
        ball_hit_list = pygame.sprite.spritecollide(ball, bullet_list, True)
        if len(ball_hit_list) == 0:
            new_ball_list.add(ball)
        ball_list.empty()
        for ball in new_ball_list:
                ball_list.add(ball)
    return ball_list

def king_colliosion(king_ball, bullet_list):
    global king_life
    king_life -= 1
    new_bullet_list.empty()
    for bullet in bullet_list:
        king_hit_list = pygame.sprite.spritecollide(king_ball, bullet_list, False)
        if len(king_hit_list) == 0:
            new_bullet_list.add(bullet)
        bullet_list.empty()
        king_ball.increase_ball_size(king_life)
        for bullet in new_bullet_list:
            bullet_list.add(bullet)
    return bullet_list


# Action's after king ball is created
def the_king_is_here():
    stop_all_balls()
    # debug(len(create_king_circle(count_balls(ball_list))))
    #    debug(create_king_circle(count_balls(ball_list)))
    go_to_pos()

'''
def move_in_arch(pos_x, pos_y):
    speed = 3
    angle = 1
    velocity_y = -1
    velocity_x = 1
    pos_x += velocity_x
    pos_y += velocity_y
    return  pos_x, pos_y
'''
def king_is_moving():
    change_to_pos()

def continue_board(pre_king):
    if pre_king:
        dont_touch_corners(ball_list, False)

    else:
        global king_ball
        dont_touch_corners(king_ball, False)
        dont_touch_corners(bullet_list, True)

# Bullet shut function
def shot_bullet():
    x, y = pygame.mouse.get_pos()
    add_bullet_to_board(x, y)


############################## Actual Program #############################################
while not finish:

    for event in pygame.event.get(): # Stop the program
        if event.type == pygame.QUIT:
            finish = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT: # Add king to board
            RIGHT_CLICK = True
            x, y = pygame.mouse.get_pos()
            add_ball_to_board(x, y)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT: # And not KING_EXIST
            x, y = pygame.mouse.get_pos()
            add_ball_to_board(x, y)
            if len(ball_list) == 1 and PLAY_AUDIO and not KING_EXIST:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound(SOUND_FILE_BEFORE_KING))

            elif KING_EXIST and not balls_not_in_place: # Shot only in all heads are in place
                shot_bullet()

    if KING_EXIST and balls_not_in_place:
        the_king_is_here()
    elif KING_EXIST and not balls_not_in_place:
        continue_board(False)
        king_is_moving()

        # Remove mouse point
        pygame.mouse.set_visible(False)

        # Add Plane to game
        mouse_point = (pygame.mouse.get_pos())
        screen.blit(player_image, mouse_point)
        pygame.display.flip()
        if only_once:
            only_once = False
            pygame.mixer.Channel(2).play(pygame.mixer.Sound(SOUND_FILE_EVIL))

    else:
        continue_board(True)
    screen.blit(img, (0, 0))
    ball_list.draw(screen)
    bullet_list.draw(screen)
    king_list.draw(screen)
    print(bullet_list)
    if KING_EXIST:
        ball_colliosion(ball_list, bullet_list)
    pygame.display.flip()
    print(count_balls(ball_list))
    if count_balls(ball_list) == 0 and KING_EXIST:
        king_colliosion(king_ball,bullet_list)

    clock.tick(REFRESH_RATE)