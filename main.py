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
BACKGROUND = 'tiles.png'  # background image
REFRESH_RATE = 60
SOUND_FILE = "guitar.mp3"  # sound file
MAX_VELOCITY = 7

NUMBER_OF_BRICKS_X = 7
NUMBER_OF_BRICKS_Y = 3
DISTANCE = 80


def fill_bricks(brick_list):
    brick_list.empty()
    for i in range(NUMBER_OF_BRICKS_X):
        for j in range(NUMBER_OF_BRICKS_Y):
            brick = Brick(i * DISTANCE, j * DISTANCE)
            brick_list.add(brick)


def shoot(paddle, balls_list):
    x, y = paddle.rect.center
    ball = Ball(x, y - 10)
    vx = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
    vy = random.randint(-MAX_VELOCITY, -1)
    ball.update_v(vx, vy)
    balls_list.add(ball)
    return True


def ball_hit_brick(ball, brick):
    horizontal_hit = vertical_hit = False
    if ball.rect.centerx <= brick.rect.left or ball.rect.centerx >= brick.rect.right:
        vertical_hit = True
    if ball.rect.centery <= brick.rect.top or ball.rect.centery >= brick.rect.bottom:
        horizontal_hit = True
    ball.hit_brick(vertical_hit, horizontal_hit)


def main():
    # init class
    pygame.init()

    """
    # sound init
    pygame.mixer.init()
    pygame.mixer.music.load(SOUND_FILE)
    """

    # set screen
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Breaker")

    # image background
    img = pygame.image.load(BACKGROUND)
    screen.blit(img, (0, 0))

    paddle = Paddle(250, 500)
    screen.blit(paddle.image, paddle.get_pos())

    brick_list = pygame.sprite.Group()
    fill_bricks(brick_list)
    brick_list.draw(screen)

    start_ball = Ball(paddle.rect.centerx, paddle.rect.centery - 10)
    screen.blit(start_ball.image, start_ball.get_pos())

    balls_list = pygame.sprite.Group()

    pygame.display.flip()

    clock = pygame.time.Clock()

    LEFT = 1

    ball_clicked = False
    prev_mouse_point = (0, 0)

    finish = False  # quit button was clicked
    while not finish:

        # enables position to move continuously with the keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            paddle.move_right()
        if keys[pygame.K_LEFT]:
            paddle.move_left()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    ball_clicked = shoot(paddle, balls_list)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball_clicked = shoot(paddle, balls_list)
                if event.key == pygame.K_a:
                    fill_bricks(brick_list)
                    brick_list.draw(screen)

        # reset background image
        screen.blit(img, (0, 0))

        # show mouse's current location
        mouse_point = pygame.mouse.get_pos()

        if mouse_point != prev_mouse_point:
            prev_mouse_point = mouse_point
            paddle.update_loc(mouse_point[0] - 50)

        screen.blit(paddle.image, paddle.get_pos())

        # display the starting position of the ball
        if not ball_clicked:
            screen.blit(start_ball.image, (paddle.rect.centerx - 10, paddle.rect.centery - 20))

        for ball in balls_list:
            ball.update_loc()
            if ball.rect.center[0] > WINDOW_WIDTH or ball.rect.center[0] < 0:
                ball.flip_x_dir()
            if ball.rect.y + 10 < 0:
                ball.flip_y_dir()
            if ball.rect.y - 20 > WINDOW_HEIGHT:
                balls_list.remove(ball)

        # balls hit bricks
        for ball in balls_list:
            ball_brick_hit_list = pygame.sprite.spritecollide(ball, brick_list, False)
            if ball_brick_hit_list:
                ball_hit_brick(ball, ball_brick_hit_list[0])

        # brick hit by ball
        for brick in brick_list:
            brick_hit_list = pygame.sprite.spritecollide(brick, balls_list, False)
            if brick_hit_list:
                brick_list.remove(brick)

        ball_paddle_hit_list = pygame.sprite.spritecollide(paddle, balls_list, False)
        for ball in ball_paddle_hit_list:
            ball.point_up()

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
