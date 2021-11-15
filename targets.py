import pygame

GREEN_BRICK = 'images/green_brick.png'
RED_BRICK = 'images/red_brick.png'
CYAN_BRICK = 'images/cyan_brick.png'
BLACK_BRICK = 'images/black_brick.png'


class BrickError(Exception):
    """brick shouldn't exist anymore"""
    pass


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super(Brick, self).__init__()

    def set_surface(self, my_image, x, y):
        self.image = pygame.image.load(my_image).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_pos(self):
        return self.rect.x, self.rect.y


class BasicBrick(Brick):
    def __init__(self):
        super(BasicBrick, self).__init__()
        self.required = True

    def hit_action(self):
        raise BrickError("brick was hit")


class GreenBrick(BasicBrick):
    def __init__(self, x, y):
        super(GreenBrick, self).__init__()
        super().set_surface(GREEN_BRICK, x, y)


class RedBrick(BasicBrick):
    def __init__(self, x, y):
        super(RedBrick, self).__init__()
        super().set_surface(RED_BRICK, x, y)


class CyanBrick(BasicBrick):
    def __init__(self, x, y):
        super(CyanBrick, self).__init__()
        super().set_surface(CYAN_BRICK, x, y)


class PermanentBrick(Brick):
    def __init__(self, x, y):
        super(PermanentBrick, self).__init__()
        super().set_surface(BLACK_BRICK, x, y)
        self.required = False

    def hit_action(self):  # brick should remain after getting hit
        pass
