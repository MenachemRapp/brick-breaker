from targets import *

NUMBER_OF_BRICKS_X = 12
NUMBER_OF_BRICKS_Y = 8
DISTANCE_X = 50
DISTANCE_Y = 20


def level1():
    brick_options = [GreenBrick, RedBrick, CyanBrick]

    brick_list = pygame.sprite.Group()

    # fill all regular bricks
    for i in range(NUMBER_OF_BRICKS_X):
        for j in range(NUMBER_OF_BRICKS_Y):
            brick = brick_options[(i + j) % len(brick_options)](i * DISTANCE_X, j * DISTANCE_Y)
            brick_list.add(brick)

    # add permanent bricks
    for i in range(4):
        brick = PermanentBrick(DISTANCE_X + i * DISTANCE_X * 3, DISTANCE_Y * NUMBER_OF_BRICKS_Y)
        brick_list.add(brick)

    return brick_list
