import pygame

LAV = (200, 191, 231)  # lavender
PINK = (255, 20, 147)
MOVING_IMAGE = 'player.png'
HORIZONTAL_VELOCITY = 3
VERTICAL_VELOCITY = 5


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Brick, self).__init__()
        self.image = pygame.image.load(MOVING_IMAGE).convert()
        self.image.set_colorkey(LAV)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_pos(self):
        return self.rect.x, self.rect.y

