import pygame
import random

# Constants
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
SKY = (143,203,239)
PINK1 = (255,20,147)
PINK2 = (255,0,140)
HORIZONTAL_VELOCITY = 20
VERTICAL_VELOCITY = 20
MOVING_IMAGE = r'/home/yonatan/Documents/Python/pictures/dod.png'
KING_IMAGE = r'/home/yonatan/Documents/Python/pictures/dodKing.png'
BULLET = '/home/yonatan/Documents/Python/pictures/bullet.png'
#SLAVES = r'/home/yonatan/Documents/Python/pictures/slaves'



class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, isking=False):
        super(Ball, self).__init__()
        self.isking = isking
        if (self.isking):
            self.image = pygame.image.load(KING_IMAGE).convert()
        else:
            rnd = random.randint(1,10)
            rndSlave = r'/home/yonatan/Documents/Python/pictures/slaves/{0}.png'.format(rnd)
            self.image = pygame.image.load(rndSlave).convert() # Load image
        self.image.set_colorkey(PINK1)
        #self.image.set_colorkey(PINK2)# Remove Color from background
        self.rect =  self.image.get_rect() # To save the object location
        self.rect.x = x # Starting position
        self.rect.y = y # Starting position
        self.__vx = HORIZONTAL_VELOCITY # Horizontical speed
        self.__vy = VERTICAL_VELOCITY # Vertical speed

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

    def crown_king(self):
        self.isking == True

    def is_king(self):
        return self.isking

# Create a bullet object
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = pygame.image.load(BULLET).convert() # Load image
        self.image.set_colorkey(PINK1)
        self.rect =  self.image.get_rect() # To save the object location
        self.rect.x = x # Starting position
        self.rect.y = y # Starting position
        self.__vx = HORIZONTAL_VELOCITY # Horizontical speed
        self.__vy = VERTICAL_VELOCITY # Vertical speed

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
