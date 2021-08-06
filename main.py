
import pygame

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
pygame.init()

size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")

WHITE = (255, 255, 255)
screen.fill(WHITE)

IMAGE='tiles.png'
img = pygame.image.load(IMAGE)
screen.blit(img, (0,0))
pygame.display.flip()



finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
pygame.quit()

