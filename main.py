import pygame
import math

# screen params
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LAV = (200, 191, 231)  # lavender
IMAGE = 'tiles.png'  # background image
REFRESH_RATE = 60

# init class
pygame.init()

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
pygame.mouse.set_visible(False)
player_image = pygame.image.load('player.png').convert()
player_image.set_colorkey(LAV)

# draw red circle -not used
for i in range(0, 359, 4):
    pygame.draw.line(screen, RED, [300, 300],
                     [300 + 270 * math.sin(math.radians(i)), 300 + 270 * math.cos(math.radians(i))], 1)
pygame.display.flip()

clock = pygame.time.Clock()
ball_x_pos = 0
ball_y_pos = 0

LEFT = 1
SCROLL = 2
RIGHT = 3

mouse_pos_list = []
prev_mouse_point = (0, 0)
showing_mouse_point=[0,0]
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
        elif event.type == pygame.MOUSEBUTTONDOWN \
                and event.button == LEFT:
            mouse_pos_list.append(pygame.mouse.get_pos())

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mouse_pos_list=[]
            if event.key == pygame.K_a:
                ball_x_pos = 0
                ball_y_pos = 0
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

    #screen.blit(player_image, [220, 300])

    # ball moves automatically
    ball_x_pos += 1
    ball_y_pos += 1
    pygame.draw.circle(screen, WHITE, [ball_x_pos, ball_y_pos], 32)

    # show mouse's current location
    mouse_point = pygame.mouse.get_pos()
    #print(mouse_point)

    #if 0 >= mouse_point[0] >= WINDOW_WIDTH and 0 >= mouse_point[1] >= WINDOW_HEIGHT and mouse_point != prev_mouse_point:
    if mouse_point != prev_mouse_point:
        prev_mouse_point = mouse_point
        showing_mouse_point= list(mouse_point)


    screen.blit(player_image, (showing_mouse_point[0] - 50, showing_mouse_point[1] - 50))

    for i in mouse_pos_list:
        screen.blit(player_image, (i[0] - 50, i[1] - 50))

    pygame.display.flip()
    clock.tick(REFRESH_RATE)

pygame.quit()
