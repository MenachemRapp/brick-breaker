import random

import pygame
import math
from shots import Ball
from targets import Brick
from paddles import Paddle

# screen params
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LAV = (200, 191, 231)  # lavender
IMAGE = 'tiles.png'  # background image
REFRESH_RATE = 60
SOUND_FILE = "guitar.mp3"  # sound file
MAX_VELOCITY = 7


def fill_bricks():
    pass


def shoot(paddle, balls_list):
    x, y = paddle.rect.center
    ball = Ball(x, y - 10)
    vx = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
    vy = random.randint(-MAX_VELOCITY, -1)
    ball.update_v(vx, vy)
    balls_list.add(ball)
    return True


def main():
    # init class
    pygame.init()

    # sound init
    pygame.mixer.init()
    pygame.mixer.music.load(SOUND_FILE)

    # set screen
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("My Game")

    # image background
    img = pygame.image.load(IMAGE)
    screen.blit(img, (0, 0))

    pygame.display.flip()

    paddle = Paddle(250, 500)
    screen.blit(paddle.image, paddle.get_pos())
    pygame.display.flip()

    NUMBER_OF_BRICKS_X = 7
    NUMBER_OF_BRICKS_Y = 3
    DISTANCE = 80
    brick_list = pygame.sprite.Group()
    new_balls_list = pygame.sprite.Group()
    for i in range(NUMBER_OF_BRICKS_X):
        for j in range(NUMBER_OF_BRICKS_Y):
            brick = Brick(10 + i * DISTANCE, 10 + j * DISTANCE)
            brick_list.add(brick)
    brick_list.draw(screen)

    pygame.display.flip()

    balls_list = pygame.sprite.Group()
    # input()
    clock = pygame.time.Clock()
    ball_x_pos = 0
    ball_y_pos = 0

    LEFT = 1
    SCROLL = 2
    RIGHT = 3

    ball_clicked = False
    mouse_pos_list = []
    prev_mouse_point = (0, 0)
    showing_mouse_point = [0, 0]
    finish = False
    while not finish:

        # enables position to move continuously with the keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            showing_mouse_point[1] -= 2
        if keys[pygame.K_DOWN]:
            showing_mouse_point[1] += 2
        if keys[pygame.K_RIGHT]:
            # showing_mouse_point[0] += 2
            paddle.move_right()
        if keys[pygame.K_LEFT]:
            paddle.move_left()
            # showing_mouse_point[0] -= 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    ball_clicked = shoot(paddle, balls_list)
                elif event.button == RIGHT:
                    pygame.mixer.music.play()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball_clicked = shoot(paddle, balls_list)
                if event.key == pygame.K_a:
                    brick_list.empty()
                    for i in range(NUMBER_OF_BRICKS_X):
                        for j in range(NUMBER_OF_BRICKS_Y):
                            brick = Brick(i * DISTANCE, j * DISTANCE)
                            brick_list.add(brick)
                    brick_list.draw(screen)

        # reset background image
        screen.blit(img, (0, 0))

        # screen.blit(player_image, [220, 300])

        # ball moves automatically
        ball_x_pos += 1
        ball_y_pos += 1
        pygame.draw.circle(screen, WHITE, [ball_x_pos, ball_y_pos], 32)

        # show mouse's current location
        mouse_point = pygame.mouse.get_pos()

        if mouse_point != prev_mouse_point:
            prev_mouse_point = mouse_point
            showing_mouse_point = list(mouse_point)
            paddle.update_loc(mouse_point[0] - 50)

        for brick in brick_list:
            brick_hit_list = pygame.sprite.spritecollide(brick, balls_list, False)
            if len(brick_hit_list) != 0:
                brick_list.remove(brick)

        screen.blit(paddle.image, paddle.get_pos())

        for ball in balls_list:
            if paddle.rect.center[1] - 5 <= ball.rect.bottom <= paddle.rect.center[1] + 5 \
                    and paddle.rect.left <= ball.rect.center[0] <= paddle.rect.right:
                ball.point_up()

        for ball in balls_list:
            ball.update_loc()
            if ball.rect.x + 80 > WINDOW_WIDTH or ball.rect.x + 10 < 0:
                ball.flip_x_dir()
            if ball.rect.y + 10 < 0:
                ball.flip_y_dir()
            if ball.rect.y - 20 > WINDOW_HEIGHT:
                balls_list.remove(ball)

        balls_list.draw(screen)
        brick_list.draw(screen)

        pygame.display.flip()

        if ball_clicked and not balls_list:
            print("Game Over")
            break

        if not brick_list:
            print("victory")
            break

        clock.tick(REFRESH_RATE)

    pygame.quit()


if __name__ == '__main__':
    main()
