import pygame

LAV = (200, 191, 231)  # lavender
PINK = (255, 20, 147)
MOVING_IMAGE = 'player.png'
HORIZONTAL_VELOCITY = 3
VERTICAL_VELOCITY = 5


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ball, self).__init__()
        self.image = pygame.image.load(MOVING_IMAGE).convert_alpha()
        self.image.set_colorkey(LAV)
        self.image = pygame.transform.smoothscale(self.image,[20,20])
        #self.image = self.image.fit(0.5)
        self.image.set_colorkey(LAV)
        self.rect = self.image.get_rect()#.fit([20,20])
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