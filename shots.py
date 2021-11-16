import pygame
import math
import random

LAV = (200, 191, 231)  # lavender
BALL = "images/ball.png"
BALL_SPEED = 7


class BallError(Exception):
    """ball shouldn't exist anymore"""
    pass


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ball, self).__init__()

        # set ball image
        new_image = pygame.image.load(BALL)
        self.image = pygame.transform.scale(new_image, [20, 20]).convert()
        self.image.set_colorkey(LAV)
        self.rect = self.image.get_rect()

        # set ball speed
        self.__vy = random.uniform(BALL_SPEED * 0.1, BALL_SPEED * 0.9)
        abs_vx = math.sqrt(BALL_SPEED ** 2 - self.__vy ** 2)
        self.__vx = random.choice([abs_vx, -abs_vx])

        # set ball location
        """ "rect" only uses int values. If we will use only round int values
        the balls will run into loops. Therefore, we want to use real/float
        values and later convert them to integers
        """
        self.real_x = x
        self.real_y = y
        self.rect.x = self.real_x
        self.rect.y = self.real_y

        # set last hit object by the ball
        self.last_object_hit = None

    def update_v(self, vx, vy):
        """
        update ball speed
        :param vx: horizontal speed
        :param vy: vertical speed
        """
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

    def flip_x_dir(self):  # isn't used anymore
        """
        flip ball direction horizontally
        """
        self.__vx = -self.__vx

    def flip_y_dir(self):   # isn't used anymore
        """
        flip ball direction vertically
        """
        self
        self.__vy = -self.__vy

    def point_up(self):
        """
        flip ball so it will point up
        """
        self.__vy = -abs(self.__vy)

    def point_down(self):
        """
        flip ball so it will point down
        """
        self.__vy = abs(self.__vy)

    def point_right(self):
        """
        flip ball so it will point up
        """
        self.__vx = abs(self.__vx)

    def point_left(self):
        """
        flip ball so it will point down
        """
        self.__vx = -abs(self.__vx)

    def hit_brick(self, vertical_hit, horizontal_hit, object_hit):
        """
        action when ball hits a brick
        :param vertical_hit: hit the brick from the top or bottom
        :param horizontal_hit: hit the brick from the side
        :param object_hit: the brick that was hit
        """
        if object_hit != self.last_object_hit:
            self.last_object_hit = object_hit
            if vertical_hit:
                if vertical_hit == "top":
                    self.point_up()
                else:  # bottom
                    self.point_down()

            if horizontal_hit:
                if horizontal_hit == "left":
                    self.point_left()
                else:  # right
                    self.point_right()

    def hit_side_border(self, side_name):
        """
        action when the ball hits the side border
        """
        if side_name == "right":
            self.point_left()
        elif side_name == "left":
            self.point_right()

        self.last_object_hit = "side"

    def hit_top_border(self):
        """
        action when the ball hits the top border
        """
        self.point_down()
        self.last_object_hit = "top"

    @staticmethod
    def hit_bottom_border():
        raise BallError("ball has left the border")
