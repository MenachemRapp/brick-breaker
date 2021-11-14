import pygame
import math
import random

LAV = (200, 191, 231)  # lavender
PINK = (255, 20, 147)
BALL = "images/ball.png"
BALL_SPEED = 7


class BallError(Exception):
    """ball shouldn't exist anymore"""
    pass


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ball, self).__init__()
        new_image = pygame.image.load(BALL)  # .convert()# _alpha()
        self.image = pygame.transform.scale(new_image, [20, 20]).convert()
        self.image.set_colorkey(LAV)
        self.rect = self.image.get_rect()
        # TODO verify values will not be zero
        self.__vy = random.uniform(BALL_SPEED * 0.1, BALL_SPEED * 0.9)
        abs_vx = math.sqrt(BALL_SPEED ** 2 - self.__vy ** 2)
        self.__vx = random.choice([abs_vx, -abs_vx])

        """ "rect" only uses int values. If we will use only round int values
        the balls will run into loops. Therefore, we want to use real/float
        values and later convert them to integers
        """
        self.real_x = x
        self.real_y = y
        self.rect.x = self.real_x
        self.rect.y = self.real_y
        self.last_object_hit = None

    def update_v(self, vx, vy):
        self.__vx = vx
        self.__vy = vy

    def update_loc(self):
        # float values
        self.real_x += self.__vx
        self.real_y += self.__vy

        # int values
        self.rect.x = self.real_x
        self.rect.y = self.real_y

    def get_pos(self):
        return self.rect.x, self.rect.y

    def get_v(self):
        return self.__vx, self.__vy

    def flip_x_dir(self):
        self.__vx = -self.__vx

    def flip_y_dir(self):
        self.__vy = -self.__vy

    def point_up(self):
        self.__vy = -abs(self.__vy)

    def point_down(self):
        self.__vy = abs(self.__vy)

    def hit_brick(self, vertical_hit, horizontal_hit, object_hit):
        if object_hit != self.last_object_hit:
            self.last_object_hit = object_hit
            if vertical_hit:
                self.flip_x_dir()
            if horizontal_hit:
                self.flip_y_dir()

    def hit_side_border(self):
        self.flip_x_dir()
        self.last_object_hit = "side"

    def hit_top_border(self):
        self.point_down()
        self.last_object_hit = "top"

    @staticmethod
    def hit_bottom_border():
        raise BallError("ball has left the border")
