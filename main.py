import random

import pygame
import math
from shots import Ball
from targets import Brick

# screen params
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LAV = (200, 191, 231)  # lavender
IMAGE = 'tiles.png'  # background image
REFRESH_RATE = 60
SOUND_FILE = "guitar.mp3"  # sound file
MAX_VELOCITY = 10


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

    # color background
    screen.fill(WHITE)

    # image background
    img = pygame.image.load(IMAGE)
    screen.blit(img, (0, 0))

    pygame.display.flip()

    # set mouse image - later will be set to mouse location
    # pygame.mouse.set_visible(False)
    player_image = pygame.image.load('player.png').convert()
    player_image.set_colorkey(LAV)

    # draw red circle -not used
    for i in range(0, 359, 4):
        pygame.draw.line(screen, RED, [300, 300],
                         [300 + 270 * math.sin(math.radians(i)), 300 + 270 * math.cos(math.radians(i))], 1)
    """
    ball1 = Ball(100, 100)
    ball2 = Ball(200, 200)
    screen.blit(ball1.image, ball1.get_pos())
    screen.blit(ball2.image, ball2.get_pos())
    """

    NUMBER_OF_BALLS_X = 7
    NUMBER_OF_BALLS_Y = 3
    DISTANCE = 80
    brick_list = pygame.sprite.Group()
    new_balls_list = pygame.sprite.Group()
    for i in range(NUMBER_OF_BALLS_X):
        for j in range(NUMBER_OF_BALLS_Y):
            brick = Brick(i * DISTANCE, j * DISTANCE)
            brick_list.add(brick)
    brick_list.draw(screen)

    pygame.display.flip()

    balls_list = pygame.sprite.Group()
    #input()
    clock = pygame.time.Clock()
    ball_x_pos = 0
    ball_y_pos = 0

    LEFT = 1
    SCROLL = 2
    RIGHT = 3

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
            showing_mouse_point[0] += 2
        if keys[pygame.K_LEFT]:
            showing_mouse_point[0] -= 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    x, y = showing_mouse_point
                    ball = Ball(x - 50, y - 50)
                    vx = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
                    vy = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
                    ball.update_v(vx, vy)
                    balls_list.add(ball)
                    # mouse_pos_list.append(pygame.mouse.get_pos())
                elif event.button == RIGHT:
                    pygame.mixer.music.play()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x, y = showing_mouse_point
                    ball = Ball(x - 50, y - 50)
                    vx = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
                    vy = random.randint(-MAX_VELOCITY, MAX_VELOCITY)
                    ball.update_v(vx, vy)
                    balls_list.add(ball)
                    #balls_list.empty()
                    mouse_pos_list = []
                if event.key == pygame.K_a:
                    brick_list.empty()
                    for i in range(NUMBER_OF_BALLS_X):
                        for j in range(NUMBER_OF_BALLS_Y):
                            brick = Brick(i * DISTANCE, j * DISTANCE)
                            brick_list.add(brick)
                    brick_list.draw(screen)


                # discrete version
                """if event.key == pygame.K_RIGHT:
                    showing_mouse_point[0] += 4
                if event.key == pygame.K_LEFT:
                    showing_mouse_point[0] -= 4
                if event.key == pygame.K_UP:
                    showing_mouse_point[1] -= 4
                if event.key == pygame.K_DOWN:
                    showing_mouse_point[1] += 4"""

        # reset background image
        screen.blit(img, (0, 0))

        # screen.blit(player_image, [220, 300])

        # ball moves automatically
        ball_x_pos += 1
        ball_y_pos += 1
        pygame.draw.circle(screen, WHITE, [ball_x_pos, ball_y_pos], 32)

        # show mouse's current location
        mouse_point = pygame.mouse.get_pos()
        # print(mouse_point)

        # if 0 >= mouse_point[0] >= WINDOW_WIDTH and 0 >= mouse_point[1] >= WINDOW_HEIGHT and mouse_point != prev_mouse_point:
        if mouse_point != prev_mouse_point:
            prev_mouse_point = mouse_point
            showing_mouse_point = list(mouse_point)

        screen.blit(player_image, (showing_mouse_point[0] - 50, showing_mouse_point[1] - 50))

        """
        for i in mouse_pos_list:
            screen.blit(player_image, (i[0] - 50, i[1] - 50))
        
        new_balls_list.empty()
        for ball in balls_list:
            balls_hit_list = pygame.sprite.spritecollide(ball, balls_list, False)
            if len(balls_hit_list) == 1:  # ball collides only with itself
             new_balls_list.add(ball)

        balls_list = new_balls_list.copy()
        """
        """
        balls_list.empty()
        for ball in new_balls_list:
            balls_list.add(ball)
        """
        for brick in brick_list:
            balls_hit_list = pygame.sprite.spritecollide(brick, balls_list, False)
            if len(balls_hit_list) != 0:
                brick_list.remove(brick)





        for ball in balls_list:
            ball.update_loc()
            if ball.rect.x+80 > WINDOW_WIDTH or ball.rect.x+10 < 0:
                ball.flip_x_dir()
            if ball.rect.y+10 < 0:
                ball.flip_y_dir()
            if ball.rect.y - 20 > WINDOW_HEIGHT:
                balls_list.remove(ball)

        balls_list.draw(screen)
        brick_list.draw(screen)

        pygame.display.flip()
        clock.tick(REFRESH_RATE)

    pygame.quit()


if __name__ == '__main__':
    main()
