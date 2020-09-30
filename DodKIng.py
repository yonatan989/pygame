############READ ME ##################
#UPPER_CASE = Fixed variables
#lowerCase = Daynamic variables
#list_type = list objects
#is_object = Condition variables
#add_ball_to_board = function name


########### Game stages #############
# 1 - Slaves stage
# 2 - King is here
# 3 - Slaves in circle around king
# 4 - Slaves are killed
# 5 - Increas king size
# 6 - Devils takes over king
# 7 - Meteor stage
# win - flower (kill devils with harts)
# lose - game ends


import pygame
import random
import math
import os
import time
import threading
from collections import Iterable
try:
    from shapes import Ball, Bullet, Plane
except ImportError:
    from .shapes import Ball,Bullet, Plane

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
BACKGROUND = r'/home/yonatan/Documents/Python/pictures/madagascar_1.jpg'
PLANE = r'/home/yonatan/Documents/Python/pictures/plane.png'
BULLET = r'/home/yonatan/Documents/Python/pictures/bullet.png'
CHART_BULLET_IMAGE = r'/home/yonatan/Documents/Python/pictures/chart_bullet.png'
CHART_THROPY_IMAGE = r'/home/yonatan/Documents/Python/pictures/thropy_new.png'
HART_IMAGE = r'/home/yonatan/Documents/Python/pictures/chart_hart.png'
SOUND_FILE_AFTER_KING = r'/home/yonatan/Documents/Python/sounds/King_is_here.wav'
SOUND_FILE_BEFORE_KING = r'/home/yonatan/Documents/Python/sounds/moveit.wav'
SOUND_FILE_BULLET = r'/home/yonatan/Documents/Python/sounds/bullet.wav'
SOUND_FILE_BACKGROUND = r'/home/yonatan/Documents/Python/sounds/background.wav'
SOUND_FILE_EVIL = r'/home/yonatan/Documents/Python/sounds/evil_laugh.wav'
SOUND_FILE_LONG_KISS = r'/home/yonatan/Documents/Python/sounds/originals/longkiss.wav'
SOUND_FILE_DEVILS = r'/home/yonatan/Documents/Python/sounds/resurrection.wav'
SOUND_FILE_DEVILS_FULL = r'/home/yonatan/Documents/Python/sounds/resurrection_full.wav'
SOUND_FILE_GAMEOVER = r'/home/yonatan/Documents/Python/sounds/game_over.wav'
SOUND_FILE_WIN = r'/home/yonatan/Documents/Python/sounds/champions.wav'
RECORD_FILE = r'/home/yonatan/Documents/Python/record'
RECORD = open(RECORD_FILE,'r').read()


# Buttons
LEFT = 1
SCROLL = 2
RIGHT = 3
clickType = 'LEFT'

# Game Control
PLAY_AUDIO = True # False - game with no audio, True - play audio
REFRESH_RATE = 60 # Defines the refresh rate of the screen
RADIUS = 60 # From king to slaves
MIN_RAD = 45 # Min distance of balls from king
MAX_RAD = 150 # Max distance of balls from king
SPIN_SPEED = 4 # The speed that slaves will go around king (higher = slower)
METEOR_SPEED = 7 # Speed that meteor will fall (higher = faster)
IN_AND_OUT_SPEED = 1 # Speed that slaves will go in and out of radius (higher = faster)
BULLET_SPEED = 20 # Bullet speed (higher = faster)
HART_SPEED = 10 # Hart speed (higer = faster
playerLives = 50 # Amount of lives the player has before he loses
numOfBullets= 70 # The amount of bullets the player starts with


# Changing variables
winGame = False # Defines when player wins the game (Dont touch this variable)
gameOver = False # Programs takes action to close when this is true (when we lose)
righeClick = False # Trackes when right there is right click action
kingExist = False # True when king exists
ballsNotInPlace = True # Defines when all slaves are around king
finish = False # Define when game ends
theMeteorStage = False # Defines the meteor stage time
planeAdded = False # Helps the program create the plane object only once
is_hart = False # when true bullets turns into hart
playAudioCount = 0 # This var helps the program not play the same audio multiple times
kingLives = 0 # Counts how many times king & devil where shot
gameScore = 0 # Counts the amount of meteors destroyed
goIn = False # Define if the balls will get closer to king keep out
add_to_angle = 0


prime_number_list = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113] # defining the speed the meteors will fall with prime division in prime numbers
index_prime_list = len(prime_number_list) - 1 # Changes the meteor creation speed


# Sprite group lists
ball_list = pygame.sprite.Group()
new_ball_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
new_bullet_list = pygame.sprite.Group()
king_list = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
new_meteor_list = pygame.sprite.Group()
plane_list = pygame.sprite.Group()

############################## Initialization ########################################

# Init screen
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")


# Add imges to screen
BACKGROUND_IMAGE = pygame.image.load(BACKGROUND)
BULLER_CHART_IMAGE = pygame.image.load(CHART_BULLET_IMAGE).convert()
THROPY_CHART_IMAGE = pygame.image.load(CHART_THROPY_IMAGE).convert()
HART_CHART_IMAGE = pygame.image.load(HART_IMAGE).convert()
BULLET_IMAGE = pygame.image.load(BULLET).convert()
BULLER_CHART_IMAGE.set_colorkey(PINK)
THROPY_CHART_IMAGE.set_colorkey(PINK)
HART_CHART_IMAGE.set_colorkey(PINK)
BULLET_IMAGE.set_colorkey(PINK)

# Init Sound effect
if PLAY_AUDIO:
    pygame.mixer.init()
    channel1 = pygame.mixer.Channel(1)
    channel2 = pygame.mixer.Channel(2)
    channel3 = pygame.mixer.Channel(3)
    channel4 = pygame.mixer.Channel(4)

# Add clock
clock = pygame.time.Clock()

############################## FUNCTIONS #######################################################

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

# Add a ball object to board
def add_ball_to_board(x,y):
    global righeClick
    global kingExist
    if not kingExist: # Stopes adding balls when the king is here
        if righeClick: # Creates a king object on right click
            isKING = True
        else:
            isKING = False
        ball = Ball(x, y, isKING)

        # When King is created
        if ball.is_king():
            if PLAY_AUDIO:
                sound = pygame.mixer.Sound(SOUND_FILE_AFTER_KING)
                channel1.play(sound)
            vx = 0
            vy = 0
            ball.update_v(vx, vy)
            kingExist = True
            #global KING_POS
            global king_ball
            king_ball = ball # Saves the king ball object
            #KING_POS = king_ball.get_pos() # Saves the king ball position
            king_list.add(king_ball)
        else: # When ball is not king
            vx = rnd_speed()
            vy = rnd_speed()
            ball.update_v(vx, vy)
            ball_list.add(ball) # Add ball to ball list

# Add bullet object to board
def add_bullet_to_board(x,y,is_hart):

    # Change hart to bullet on meteor stage on left clicks
    if theMeteorStage:
        is_hart = False
        if clickType == 'RIGHT':
            is_hart = True

    # Create bullet or hart object
    bullet = Bullet(x, y)
    if is_hart:
        bullet.change_to_hart()
        vx = HART_SPEED
    else:
        vx = BULLET_SPEED

    vy = 0
    bullet.update_v(vx, vy)
    bullet_list.add(bullet) # Add bullet to bullet list

    # Control shot sound
    if PLAY_AUDIO:
        if is_hart:
            sound = pygame.mixer.Sound(SOUND_FILE_LONG_KISS)
            channel2.play(sound)
        else:
            sound = pygame.mixer.Sound(SOUND_FILE_BULLET)
            channel4.play(sound)

# Add meters object to board (Creates a meteor in a random place)
def add_meteor_to_board():
    global theMeteorStage
    yPos = 0
    xPos = random.randrange(0,WINDOW_WIDTH) # Meteor will be created on x axis in a random place

    # Creates meteor or flower object
    if not winGame:
        meteor = Ball(xPos, yPos, isking=False ,isMeteor=True)
    else:
        meteor = Ball(xPos, yPos, isking=False, isMeteor=False, isflower=True)

    vx = 0
    vy = METEOR_SPEED
    meteor.update_v(vx, vy)
    meteor_list.add(meteor)
    theMeteorStage = True

    # Adds plane object to board
def add_plane_to_board():
    global plane
    x, y = pygame.mouse.get_pos()
    plane = Plane(x, y)

# Counts amount of balls
def count_balls(balls_list):
    num_of_balls = 0
    for ball in balls_list:
        num_of_balls += 1
    return num_of_balls

# Create array with circle positions
def create_king_circle(num_of_balls, move_with_king = False):
    global MIN_RAD # Minimum space between balls and king
    global MAX_RAD # Max space between balls and king
    global IN_AND_OUT_SPEED # Speed the balls will go in and out
    global add_to_angle # Make the ball's spin
    global RADIUS
    global SPIN_SPEED
    global goIn

    circle_pos_list = []
    X1, Y1 = king_ball.get_pos() # Create a center around king position
    if num_of_balls == 0: # Prevent the program from crashing when there are no balls
        num_of_balls = 1

    for angle in range(0, 360, int(360/(num_of_balls))): # Creates equal space between balls
        if move_with_king:
            if num_of_balls == 1:
                #add_to_angle += 10.8 # Make the ball's spin
                add_to_angle += 3  # Make the ball's spin

            else:
                add_to_angle += math.pi / SPIN_SPEED # Make the ball's spin
            angle += add_to_angle

        # Creates a list of balls positions
        X2 = X1 + (math.cos(math.radians(angle)) * RADIUS)
        Y2 = Y1 + (math.sin(math.radians(angle)) * RADIUS)
        cir_pos = (X2,Y2)
        circle_pos_list.append(cir_pos)

    # Makes the balls go in and out
    if RADIUS >= MAX_RAD: # When balls are to far go in
        goIn = True
    elif RADIUS <= MIN_RAD: # When balls are to close to out
        goIn = False
    if goIn:
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
        global ballsNotInPlace
        ballsNotInPlace = False
        vx = rnd_speed()
        vy = rnd_speed()
        king_ball.update_v(vx, vy)

def change_to_pos():
    global king_ball
    index = 0
    ball_count = count_balls(ball_list)
    circle_pos_list = create_king_circle(count_balls(ball_list), move_with_king=True)
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

# Makes ball's bounce from corners / destroys them
def dont_touch_corners(list_of_balls, destroy=False, is_meteor=False):
    global ball_list
    global RADIUS
    global playerLives
    if isinstance(list_of_balls, Iterable):
        for ball in list_of_balls:
            #print("Player lives left {0}".format(playerLives))
            ball.update_loc()
            x, y = ball.get_pos()

            # destroy / move ball when its close to one of the edges
            if x > WINDOW_WIDTH - 100 or x < 1:
                if destroy:
                    list_of_balls.remove(ball)
                    if is_meteor and not winGame:
                        playerLives -= 1
                vx, vy = ball.get_v()
                ball.update_v(-vx, vy)
            if y > WINDOW_HEIGHT - 1 or y < 1:
                if destroy:
                    list_of_balls.remove(ball)
                    if is_meteor and not winGame:
                        playerLives -= 1
                vx, vy = ball.get_v()
                ball.update_v(vx, -vy)

    else: # If this is the king ball let him get closer to edges
        global king_ball
        add_radius_distance = 0
        list_of_balls.update_loc()
        x, y = list_of_balls.get_pos()
        if x > WINDOW_WIDTH - 1 - add_radius_distance or x < 1 + add_radius_distance:
            vx, vy = king_ball.get_v()
            king_ball.update_v(-vx, vy)
        if y > WINDOW_HEIGHT - 1 - add_radius_distance or y < 1 + add_radius_distance:
            vx, vy = king_ball.get_v()
            king_ball.update_v(vx, -vy)

# Define when two object are collading
def ball_colliosion(ball_list, bullet_list):
    global gameScore # Add when a meteor is destroyed
    global index_prime_list # Prime list (effect meteor creation speed)
    global numOfBullets # Counts the amount of bullets left
    new_ball_list.empty() # Original ball list
    new_bullet_list.empty() # New ball list (contains balls that didn't collide

    if clickType == 'LEFT':
        for ball in ball_list:
            ball_hit_list = pygame.sprite.spritecollide(ball, bullet_list, True) # returns only balls that collided and destroyes both
            if len(ball_hit_list) == 0: # If no balls collided then add them to the new list (dont destroy them)
                new_ball_list.add(ball)
            else:
                if theMeteorStage: # Add score when meteor was hit
                    gameScore +=1
                    numOfBullets +=2 # Add bullets
                    if index_prime_list != 0:
                        index_prime_list -= 1 # Increase meteor speed
            ball_list.empty()
            for ball in new_ball_list:
                    ball_list.add(ball)
    return ball_list

# Define when king and bullets are collading
def king_colliosion(king_ball, bullet_list):
    global kingLives
    new_bullet_list.empty()
    king_hit = False
    for bullet in bullet_list:
        bullet_hit_list = pygame.sprite.spritecollide(king_ball, bullet_list, False) # destroyes only bullet
        #print(bullet_hit_list)
        if len(bullet_hit_list) == 0:
            new_bullet_list.add(bullet)
        bullet_list.empty()
        if len(bullet_hit_list) >= 1:
            king_hit = True
            #print("king_was_hit")
        for bullet in new_bullet_list:
            bullet_list.add(bullet)

    if king_hit and not theMeteorStage:
        kingLives += 1 # king was shot
        king_ball.increase_ball_size(kingLives)
    elif king_hit and theMeteorStage and clickType == 'RIGHT':
        kingLives += 1 # king was shot only if its hart (after the meteor stage)
        king_ball.increase_ball_size(kingLives)
    return bullet_list

'''
def meteor_colliosion (plane, meteor_list):
    plane.set_pos = pygame.mouse.get_pos()
    new_meteor_list.empty()
    plane_hit = False
    for meteor in meteor_list:
        meteor_hit_list = pygame.sprite.spritecollide(plane, meteor_list, False)
        meteor_list.empty()
        if len(meteor_hit_list) == 0:
            new_meteor_list.add(meteor)
        meteor_list.empty()
        if len(meteor_hit_list) >= 1:
            player_hit = True
            #print("Player was hit!!!!!!")
        for meteor in new_meteor_list:
            meteor_list.add(meteor)
    return meteor_list
'''
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
        dont_touch_corners(ball_list, destroy=False)

    else:
        global king_ball
        dont_touch_corners(king_ball, destroy=False)
        dont_touch_corners(bullet_list, destroy=True)
        if theMeteorStage:
            dont_touch_corners(meteor_list, destroy=True, is_meteor=True)

# Bullet shot function
def shot_bullet():
    global is_hart
    global numOfBullets
    bulletXPos, bulletYPos = pygame.mouse.get_pos()

    if count_balls(ball_list) == 0 and kingExist:
        # Shot harts if there are no balls left else shot bullet
        if not theMeteorStage:
            is_hart = True

        # Shot only if there are bullets left and its the meteor stage
        elif numOfBullets > 0 and theMeteorStage:
            numOfBullets -=1

    add_bullet_to_board(bulletXPos, bulletYPos, is_hart)


############################## Actual Program #############################################
while not finish:

    for event in pygame.event.get(): # Stop the program
        if event.type == pygame.QUIT:
            finish = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT: # Add king to board
            righeClick = True
            x, y = pygame.mouse.get_pos()
            add_ball_to_board(x, y)

            # Shots harts on right click in meteor stage
            if theMeteorStage and numOfBullets > 0:
                clickType = 'RIGHT'
                shot_bullet()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT: # And not kingExist
            x, y = pygame.mouse.get_pos()
            add_ball_to_board(x, y)

            # Change hart to bullets on meteor stage
            if theMeteorStage:
                is_hart = False

            # Play audio before king exists
            if len(ball_list) == 1 and PLAY_AUDIO and not kingExist:
                sound = pygame.mixer.Sound(SOUND_FILE_BEFORE_KING)
                channel1.play(sound)

            # Shot only in all balls are in place
            elif kingExist and not ballsNotInPlace:
                clickType = 'LEFT'
                shot_bullet()

    # Move balls toward king
    if kingExist and ballsNotInPlace:
        the_king_is_here()

    # Take actions after all balls are in place
    elif kingExist and not ballsNotInPlace:
        continue_board(pre_king=False)
        king_is_moving()
        # Remove mouse point
        pygame.mouse.set_visible(False)
        # Add Plane to game
        if not planeAdded:
            add_plane_to_board()
            planeAdded = True

    else:
        continue_board(pre_king=True) # Now check that meteors and bullets are not touching edges

    # draw objects on board
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    ball_list.draw(screen)
    bullet_list.draw(screen)
    king_list.draw(screen)
    plane_list.draw(screen)
    if planeAdded:
        screen.blit(plane.image, pygame.mouse.get_pos()) # Draw plain after all balls are in circle
    if theMeteorStage:
        meteor_list.draw(screen)
        ball_colliosion(bullet_list, meteor_list)
    if kingExist:
        ball_colliosion(ball_list, bullet_list)
    if count_balls(ball_list) == 0 and kingExist: # Test collation with king after there are no balls
        king_colliosion(king_ball,bullet_list)

    # Turn king into devil
    if kingLives >= 8:
        if playAudioCount == 0:
            if PLAY_AUDIO:
                sound = pygame.mixer.Sound(SOUND_FILE_EVIL)
                channel1.play(sound)
            playAudioCount = 1

            # Count down timer
            start = time.time()
            timer_count = 0
        if time.time() - start >= 7:
            timer_count = timer_count + 1 # Start counting for meteors after 7 seconds
            meteor_creation_speed = prime_number_list[index_prime_list]
            #print(meteor_creation_speed)

            # Create meteor when timer_count divies with the prime number
            if (timer_count) % meteor_creation_speed == 0:
                add_meteor_to_board()
            if playAudioCount == 1:
                if PLAY_AUDIO:
                    sound = pygame.mixer.Sound(SOUND_FILE_DEVILS_FULL)
                    channel3.play(sound)
                playAudioCount = 2
            if playAudioCount == 2 and winGame and PLAY_AUDIO:
                sound = pygame.mixer.Sound(SOUND_FILE_WIN)
                channel3.play(sound)
                playAudioCount = 3

    # While game is not over display amount of lives left
    if playerLives >= 0:

############################## Defining text boxes on screen #######################################################

        # Display player lives
        liveFont = pygame.font.SysFont("Times New Roman", 30)
        liveNumLabel = liveFont.render("Number Of Lives:", 1, BLACK)
        liveDisplay = liveFont.render(str(playerLives), 1, BLACK)
        screen.blit(HART_CHART_IMAGE,(200, 10))
        screen.blit(liveDisplay, (270, 15))

        # Display bullets left
        bulletsFont = pygame.font.SysFont("Times New Roman", 30)
        bulletsNumLabel = bulletsFont.render("Bullets Left:", 1, BLACK)
        bulletsDisplay = bulletsFont.render(str(numOfBullets), 1, BLACK)
        screen.blit(BULLER_CHART_IMAGE, (200, 40))
        screen.blit(bulletsDisplay, (280, 60))

        # Display game score
        scoreFont = pygame.font.SysFont("Times New Roman", 30)
        scoreNumLabel = scoreFont.render("Score:", 1, BLACK)
        scoreDisplay = scoreFont.render(str(gameScore), 1, BLACK)
        screen.blit(scoreNumLabel, (200, 100))
        screen.blit(scoreDisplay, (300, 100))

        # Display devil lives
        devilFont = pygame.font.SysFont("Times New Roman", 30)
        devilNumLabel = scoreFont.render("Devil live:", 1, BLACK)
        if kingLives >= 8 and kingLives <= 38: # Display only after devil is created
            devil_live = ((kingLives - 8) * -1) + 30
            devilDisplay = devilFont.render(str(devil_live), 1, BLACK)
            screen.blit(devilNumLabel, (200, 180))
            screen.blit(devilDisplay, (330, 180))

        # Display game record
        recordFont = pygame.font.SysFont("Times New Roman", 30)
        recordNumLabel = scoreFont.render("Record:", 1, BLACK)
        recordDisplay = recordFont.render(str(RECORD), 1, BLACK)
        screen.blit(recordNumLabel, (200, 140))
        screen.blit(recordDisplay, (300, 140))
        screen.blit(THROPY_CHART_IMAGE, (330, 120))

############################## End Text box definition #######################################################
    # On victory!
    if kingLives > 38:
        winGame = True
        if gameScore > int(RECORD) or RECORD == '':
            WRITE = open(RECORD_FILE, 'w')  # Write the new record to record file
            WRITE.write(str(gameScore))
            WRITE.close()
            print("Record was Broken!!!")

    # When game is over
    if playerLives <= 0:
        if not gameOver:
            game_count_down = time.time()
            gameOver = True
            if PLAY_AUDIO:
                sound = pygame.mixer.Sound(SOUND_FILE_GAMEOVER)
                channel3.play(sound)
        if time.time() - game_count_down >= 3:
            if gameScore > int(RECORD) or RECORD == '':
                WRITE = open(RECORD_FILE, 'w') # Write the new record to record file
                WRITE.write(str(gameScore))
                WRITE.close()
                print("Record was Broken!!!")
            quit()

    # Refresh screen
    pygame.display.flip()
    clock.tick(REFRESH_RATE)