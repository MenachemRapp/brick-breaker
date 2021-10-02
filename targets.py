import pygame

LAV = (200, 191, 231)  # lavender
PINK = (255, 20, 147)
BLACK = (0, 0, 0)
GREEN_BRICK = 'green_brick.png'
BLACK_BRICK = 'black_brick.png'
HORIZONTAL_VELOCITY = 3
VERTICAL_VELOCITY = 5


class BrickError(Exception):
    """brick shouldn't exist anymore"""
    pass


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Brick, self).__init__()

    def get_pos(self):
        return self.rect.x, self.rect.y

    def hit_action(self):
        pass


class BasicBrick(Brick):
    def __init__(self, x, y):
        super(BasicBrick, self).__init__(x, y)

        self.image = pygame.image.load(GREEN_BRICK).convert()
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.required = True

    def hit_action(self):
        raise BrickError("brick was hit")


class PermanentBrick(Brick):
    def __init__(self, x, y):
        super(PermanentBrick, self).__init__(x, y)

        self.image = pygame.image.load(BLACK_BRICK).convert()
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.required = False

    def hit_action(self):
        pass
