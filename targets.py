import pygame

LAV = (200, 191, 231)  # lavender
PINK = (255, 20, 147)
BLACK = (0, 0, 0)
GREEN_BRICK = 'images/green_brick.png'
RED_BRICK = 'images/red_brick.png'
CYAN_BRICK = 'images/cyan_brick.png'
BLACK_BRICK = 'images/black_brick.png'
HORIZONTAL_VELOCITY = 3
VERTICAL_VELOCITY = 5


class BrickError(Exception):
    """brick shouldn't exist anymore"""
    pass


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Brick, self).__init__()

    def set_surface(self, my_image, x, y):
        self.image = pygame.image.load(my_image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_pos(self):
        return self.rect.x, self.rect.y

    def hit_action(self):
        pass


class BasicBrick(Brick):
    def __init__(self, x, y):
        super(BasicBrick, self).__init__(x,y)
        self.required = True

    def hit_action(self):
        raise BrickError("brick was hit")


class GreenBrick(BasicBrick):
    def __init__(self, x, y):
        super(GreenBrick, self).__init__(x, y)
        super().set_surface(GREEN_BRICK, x, y)


class RedBrick(BasicBrick):
    def __init__(self, x, y):
        super(RedBrick, self).__init__(x, y)
        super().set_surface(RED_BRICK, x, y)


class CyanBrick(BasicBrick):
    def __init__(self, x, y):
        super(CyanBrick, self).__init__(x, y)
        super().set_surface(CYAN_BRICK, x, y)


class PermanentBrick(Brick):
    def __init__(self, x, y):
        super(PermanentBrick, self).__init__(x, y)
        super().set_surface(BLACK_BRICK, x, y)
        self.required = False

    def hit_action(self):
        pass
