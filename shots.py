import pygame

LAV = (200, 191, 231)  # lavender
PINK = (255, 20, 147)
MOVING_IMAGE = 'player.png'
HORIZONTAL_VELOCITY = 3
VERTICAL_VELOCITY = 5


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ball, self).__init__()
        new_image = pygame.image.load(MOVING_IMAGE)  # .convert()# _alpha()
        self.image = pygame.transform.scale(new_image,[20,20]).convert()
        self.image.set_colorkey(LAV)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__vx = HORIZONTAL_VELOCITY
        self.__vy = VERTICAL_VELOCITY

    def update_v(self, vx, vy):
        self.__vx = vx
        self.__vy = vy


    def update_loc(self):
        self.rect.x += self.__vx
        self.rect.y += self.__vy

    def get_pos(self):
        return self.rect.x, self.rect.y

    def get_v(self):
        return self.__vx, self.__vy

    def flip_x_dir(self):
        self.__vx=-self.__vx

    def flip_y_dir(self):
        self.__vy = -self.__vy

    def point_up(self):
        self.__vy = -abs(self.__vy)

    def hit_brick(self, vertical_hit, horizontal_hit):
        if vertical_hit:
            self.flip_x_dir()
        if horizontal_hit:
            self.flip_y_dir()
