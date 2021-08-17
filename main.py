
import pygame
import math

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
pygame.init()

size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")

WHITE = (255, 255, 255)
screen.fill(WHITE)

IMAGE = 'tiles.png'


RED = (255, 0, 0)
for i in range(0, 359, 4):
    pygame.draw.line(screen, RED, [300, 300], [300+270*math.sin(math.radians(i)), 300+270*math.cos(math.radians(i))], 1)

LAV = (200, 191, 231)

REFRESH_RATE = 60
clock = pygame.time.Clock()
ball_x_pos = 0
ball_y_pos = 0

pygame .mouse.set_visible(False)
LEFT = 1
SCROLL = 2
RIGHT = 3

mouse_pos_list = []
prev_mouse_point=[]
finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.MOUSEBUTTONDOWN \
                and event.button == LEFT:
            mouse_pos_list.append(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                ball_x_pos = 0
                ball_y_pos = 0
             if event.key == pygame.K_right:
                ball_x_pos += 4
             if event.key == pygame.K_left:
                ball_x_pos -= 4
            if event.key == pygame.K_up:
                ball_y_pos += 4
            if event.key == pygame.K_down:
                ball_y_pos -= 4




    img = pygame.image.load(IMAGE)
    screen.blit(img, (0, 0))
    player_image = pygame.image.load('player.png').convert()
    player_image.set_colorkey(LAV)
    screen.blit(player_image, [220, 300])

    ball_x_pos += 1
    ball_y_pos += 1



    pygame.draw.circle(screen, WHITE, [ball_x_pos, ball_y_pos], 32)
    mouse_point = pygame.mouse.get_pos()
    if 0>mouse_point[0]>END_X and 0>mouse_point[1]>END_Y and mouse_point!=prev_mouse_point:
        prev_mouse_point=mouse_point
    screen.blit(player_image, (mouse_point[0] - 50, mouse_point[1] - 50))
    for i in mouse_pos_list:
        screen.blit(player_image, (i[0]-50,i[1]-50))

    pygame.display.flip()
    clock.tick(REFRESH_RATE)


pygame.quit()
