import pygame

LAV = (200, 191, 231)  # lavender
PINK = (255, 20, 147)
BLACK = (0,0,0)

MOVING_IMAGE = 'paddle.png'
HORIZONTAL_VELOCITY = 3
VERTICAL_VELOCITY = 5


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Paddle, self).__init__()
        self.image = pygame.image.load(MOVING_IMAGE).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__speed = HORIZONTAL_VELOCITY

    def update_speed(self, speed):
        self.__speed = speed

    def move_right(self):
        self.rect.x += self.__speed

    def move_left(self):
        self.rect.x -= self.__speed

    def get_pos(self):
        return self.rect.x, self.rect.y

    def get_speed(self):
        return self.__speed

    def update_loc(self,x):
        self.rect.x = x
