import random

import pygame
import math
from shots import *
from targets import *
from paddles import Paddle

# screen params
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LAV = (200, 191, 231)  # lavender
BLUE = (0, 0, 128)
GREEN = (42, 249, 7)
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
            brick = BasicBrick(10 + i * DISTANCE, 10 + j * DISTANCE)
            brick_list.add(brick)

    for i in range(3):
        for j in range(2):
            brick = PermanentBrick(50 + i * 200, 50 + j * DISTANCE)
            brick_list.add(brick)


def shoot(paddle, balls_list):
    x, y = paddle.rect.center
    ball = Ball(x, y - 10)
    vx = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
    vy = random.randint(-MAX_VELOCITY, -1)
    # ball.update_v(vx, vy)
    balls_list.add(ball)
    return True


def ball_hit_brick(ball, brick):
    horizontal_hit = vertical_hit = False
    if ball.rect.centerx <= brick.rect.left or ball.rect.centerx >= brick.rect.right:
        vertical_hit = True
    if ball.rect.centery <= brick.rect.top or ball.rect.centery >= brick.rect.bottom:
        horizontal_hit = True
    ball.hit_brick(vertical_hit, horizontal_hit)


def game_over(screen):
    font = pygame.font.SysFont('ComicSansMS', 80)
    text = font.render('Game Over', True, RED, BLUE)
    screen.blit(text, (screen.get_rect().centerx - text.get_rect().width / 2, 100))
    pygame.display.flip()
    # TODO add "loose" sound


def winning(screen):
    font = pygame.font.SysFont('ComicSansMS', 80)
    text = font.render('You Won', True, RED, BLUE)
    screen.blit(text, (screen.get_rect().centerx - text.get_rect().width / 2, 100))
    pygame.display.flip()
    # TODO add "win" sound


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


    start_ball = Ball(paddle.rect.centerx, paddle.rect.centery - 10)
    screen.blit(start_ball.image, start_ball.get_pos())

    balls_list = pygame.sprite.Group()

    pygame.display.flip()

    clock = pygame.time.Clock()

    LEFT = 1


    prev_mouse_point = (0, 0)
    quit_game = False  # quit button was clicked
    while not quit_game:
        fill_bricks(brick_list)
        brick_list.draw(screen)
        balls_list.empty()

        ball_clicked = False
        win_or_loose = False
        while not quit_game and not win_or_loose:

            # enables position to move continuously with the keyboard
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                paddle.move_right()
            if keys[pygame.K_LEFT]:
                paddle.move_left()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    break
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
                    ball.hit_side_border()
                if ball.rect.y + 10 < 0:
                    ball.hit_top_border()
                if ball.rect.y - 20 > WINDOW_HEIGHT:
                    try:
                        ball.hit_bottom_border()
                    except BallError:
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
                    try:
                        brick.hit_action()
                    except BrickError:
                        brick_list.remove(brick)

            ball_paddle_hit_list = pygame.sprite.spritecollide(paddle, balls_list, False)
            for ball in ball_paddle_hit_list:
                ball.point_up()

            balls_list.draw(screen)
            brick_list.draw(screen)

            pygame.display.flip()

            if ball_clicked and not balls_list:
                game_over(screen)
                win_or_loose = True

            if not list(filter(lambda x: x.required, brick_list)):
                winning(screen)
                win_or_loose = True

            clock.tick(REFRESH_RATE)

        if quit_game:
            break
        font = pygame.font.SysFont('ComicSansMS', 80)
        text = font.render('Play Again', True, BLACK, GREEN)
        text_location=(screen.get_rect().centerx - text.get_rect().width / 2, 400)
        screen.blit(text, text_location)
        pygame.display.flip()

        again = False
        while not again and not quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        quit_game = True
                        break
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    pos = pygame.mouse.get_pos()
                    if text.get_rect().left <= pos[0]-text_location[0] <= text.get_rect().right \
                            and text.get_rect().top <= pos[1]-text_location[1] <= text.get_rect().bottom:
                        again = True

    pygame.quit()


if __name__ == '__main__':
    main()
