import pygame
import random

############### Constants ###############

# Color definition
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
SKY = (143,203,239)
PINK = (255,20,147)

# Fixed variables
MOVING_IMAGE = r'/home/yonatan/Documents/Python/pictures/dod.png'
KING_IMAGE = r'/home/yonatan/Documents/Python/pictures/dodKing.png'
Dynamic_king = r'/home/yonatan/Documents/Python/pictures/dod_King/'
HART_IMAGE = r'/home/yonatan/Documents/Python/pictures/hart.png'
BULLET = '/home/yonatan/Documents/Python/pictures/bullet.png'
KING_DIR = r'/home/yonatan/Documents/Python/pictures/dod_king'
DEVIL_IMAGE = r'/home/yonatan/Documents/Python/pictures/Devils/Devil.png'
METEOR_IMAGE = r'/home/yonatan/Documents/Python/pictures/Devils/meteor.png'
FLOWER_IMAGE = r'/home/yonatan/Documents/Python/pictures/flowers.png'
PLANE = r'/home/yonatan/Documents/Python/pictures/plane.png'
HORIZONTAL_VELOCITY = 20
VERTICAL_VELOCITY = 20
FIRING_ACCURACY = 20
vulnerability_accuracy = 20




# Defining ball object (defining ragular balls, kingball, meteors & flowers)
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, isking=False, isMeteor=False, isflower=False):
        super(Ball, self).__init__()
        self.isking = isking
        self.isMeteor = isMeteor
        self.isflower = isflower

        # Load image depending the object type
        if (self.isking): # King object
            self.image = pygame.image.load(KING_IMAGE).convert()
        elif (self.isMeteor): # Meteor object
            self.image = pygame.image.load(METEOR_IMAGE).convert()
        elif (self.isflower): # Flower object
            self.image = pygame.image.load(FLOWER_IMAGE).convert()
        else: # Random ragular ball
            rnd = random.randint(1,10)
            rndSlave = r'/home/yonatan/Documents/Python/pictures/slaves/{0}.png'.format(rnd)
            self.image = pygame.image.load(rndSlave).convert() # Load image

        self.image.set_colorkey(PINK)
        self.rect = self.image.get_rect() # save's the object location
        self.size = self.image.get_rect().size
        self.rect.x = x # Starting position
        self.rect.y = y # Starting position
        self.__vx = HORIZONTAL_VELOCITY # Horizontical speed
        self.__vy = VERTICAL_VELOCITY # Vertical speed

        if self.isking:
            self.rect.width = vulnerability_accuracy
            self.rect.height = vulnerability_accuracy
        else:
            self.rect.width = FIRING_ACCURACY
            self.rect.height = FIRING_ACCURACY

    # mutator(set) & accessor(get)
    def update_v(self, vx, vy): # Change object speed
        self.__vx = vx
        self.__vy = vy

    def update_loc(self): # Update the object location
        self.rect.x += self.__vx
        self.rect.y += self.__vy

    def get_pos(self): # Return's object location (x,y) format
        return self.rect.x, self.rect.y

    def set_pos(self, new_x, new_y): # Move's object to new position
        self.rect.x = new_x
        self.rect.y = new_y

    def change_rect(self, width, height): # Change object accuracy
        self.rect.width = width
        self.rect.height = height

    def get_v(self): # Retuen's object speed (vx,vy) format
        return self.__vx, self.__vy

    def is_king(self): # Return true if object really is king
        return self.isking

    def increase_ball_size (self, kingLives): # Increase king object size
        global vulnerability_accuracy
        vulnerability_accuracy += 30
        self.size = self.image.get_rect().size
        #print(self.size) # prints image size
        if kingLives <= 8:
            self.rect.width = vulnerability_accuracy # king width vulnerability
            self.rect.height = vulnerability_accuracy # king height vulnerability
        else:
            self.rect.width = 270 # devil width vulnerability
            self.rect.height = 270 # devil height vulnerability

        if kingLives >= 8 and kingLives <= 38: # When devil is alive
            path = DEVIL_IMAGE
        elif kingLives > 38: # When devils dies return king dod
             kingLives = 8
             path = KING_DIR + '/dodKing{0}.png'.format(kingLives)
        else: # Increase king dod size
            # print(kingLives) # prints king lives
            path = KING_DIR + '/dodKing{0}.png'.format(kingLives)
        self.image = pygame.image.load(path).convert()
        self.image.set_colorkey(PINK)

# Defining bullet object
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = pygame.image.load(BULLET).convert() # Load image
        self.image.set_colorkey(PINK)
        self.rect = self.image.get_rect() # save's the object location
        self.rect.x = x # Starting position
        self.rect.y = y # Starting position
        self.__vx = HORIZONTAL_VELOCITY # Horizontical speed
        self.__vy = VERTICAL_VELOCITY # Vertical speed
        self.rect.width = FIRING_ACCURACY # Firing width accuracy
        self.rect.height = FIRING_ACCURACY # Firing height accuracy

    # mutator(set) & accessor(get)
    def update_v(self, vx, vy):
        self.__vx = vx
        self.__vy = vy

    def update_loc(self):
        self.rect.x += self.__vx
        self.rect.y += self.__vy

    def get_pos(self):
        return self.rect.x, self.rect.y

    def set_pos(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y

    def get_v(self):
        return self.__vx, self.__vy

    def change_to_hart(self): # Convert bullet image to hart image
        self.image = pygame.image.load(HART_IMAGE).convert()
        self.image.set_colorkey(PINK)

# Defining plane object
class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Plane, self).__init__()
        self.image = pygame.image.load(PLANE).convert() # Load image
        self.image.set_colorkey(PINK)
        self.rect = self.image.get_rect() # To save the object location
        self.rect.x = x # Starting position
        self.rect.y = y # Starting position
        self.rect.width = 50 # Plane width vulnerability
        self.rect.height = 50 # Plane height vulnerability


    def update_v(self, vx, vy):
        self.__vx = vx
        self.__vy = vy

    def update_loc(self):
        self.rect.x += self.__vx
        self.rect.y += self.__vy

    def get_pos(self):
        return self.rect.x, self.rect.y

    def set_pos(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y
