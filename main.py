from shots import *
from targets import *
from paddles import Paddle
from levels import *

# screen params
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
INSTRUCTIONS_RECT = (80, 200, 450, 150)

# colors
RED = (255, 0, 0)
BLUE = (0, 0, 128)
GREEN = (42, 249, 7)
BLACK = (0, 0, 0)
LAV = (200, 191, 231)  # lavender
OFF_WHITE = (245, 240, 220)

# files
BACKGROUND = "images/tiles.png"  # background image
ICON = "images/icon.png"
INSTRUCTIONS = "text/instructions.txt"

# mouse buttons
LEFT = 1
RIGHT = 3

REFRESH_RATE = 60
LEVEL = level1


def shoot(paddle, balls_list):
    """
    add a new ball
    :param paddle: sprite of the paddle
    :param balls_list: list of all balls
    :return: true
    """
    x, y = paddle.rect.center
    ball = Ball(x, y - 10)
    balls_list.add(ball)
    return True


def ball_hit_brick(ball, brick):
    """
    determine how did the ball hit the brick
    :param ball:
    :param brick:
    """
    horizontal_hit = vertical_hit = False
    if ball.rect.centerx <= brick.rect.left:
        horizontal_hit = "left"
    elif brick.rect.right <= ball.rect.centerx:
        horizontal_hit = "right"

    if ball.rect.centery <= brick.rect.top:
        vertical_hit = "top"
    elif brick.rect.bottom <= ball.rect.centery:
        vertical_hit = "bottom"
    ball.hit_brick(vertical_hit, horizontal_hit, brick)


def game_over(screen):
    """
    generate a "game over" screen
    :param screen: game screen
    """
    font = pygame.font.SysFont('ComicSansMS', 80)
    text = font.render('Game Over', True, RED, BLUE)
    screen.blit(text, (screen.get_rect().centerx - text.get_rect().width / 2, 100))
    pygame.display.flip()
    # TODO add "loose" sound


def winning(screen):
    """
    generate a "winning" screen
    :param screen: game screen
    """
    font = pygame.font.SysFont('ComicSansMS', 80)
    text = font.render('You Won', True, RED, BLUE)
    screen.blit(text, (screen.get_rect().centerx - text.get_rect().width / 2, 100))
    pygame.display.flip()
    # TODO add "win" sound


def play_again_banner(screen):
    """
    generate a "play again" screen
    :param screen: game screen
    :return: whether the "quit" button was clicked
    """
    font = pygame.font.SysFont('ComicSansMS', 80)
    text = font.render('Play Again', True, BLACK, GREEN)
    text_location = (screen.get_rect().centerx - text.get_rect().width / 2, 400)
    screen.blit(text, text_location)
    pygame.display.flip()

    again = False
    while not again:  # and not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                pos = pygame.mouse.get_pos()
                if text.get_rect().left <= pos[0] - text_location[0] <= text.get_rect().right \
                        and text.get_rect().top <= pos[1] - text_location[1] <= text.get_rect().bottom:
                    again = True
    return False


def pause(screen):
    """
    generate a "pause screen" with instructions
    :param screen: game screen
    :return: return from function when any button was clicked.
    Return "true" if the "quit" button was clicked
    """

    # draw a rectangle with the instructions
    pygame.draw.rect(screen, OFF_WHITE, INSTRUCTIONS_RECT)
    with open(INSTRUCTIONS, 'r') as input_file:
        instructions = input_file.read().splitlines()
        for index, line in enumerate(instructions[:-1]):
            line_list = line.split('\t')
            font = pygame.font.SysFont('Times', 20)

            if index == 0:  # underline title
                font.set_underline(True)
            else:  # the rest of the lines should have dashes from the key to the action
                dashes = font.render("-" * 45, True, BLACK, OFF_WHITE)
                screen.blit(dashes, (INSTRUCTIONS_RECT[0] + 20, INSTRUCTIONS_RECT[1] + index * key.get_rect().height))

            # draw key
            key = font.render(line_list[0], True, BLACK, OFF_WHITE)
            screen.blit(key, (INSTRUCTIONS_RECT[0] + 20, INSTRUCTIONS_RECT[1] + index * key.get_rect().height))

            # draw action
            action = font.render(line_list[1], True, BLACK, OFF_WHITE)
            screen.blit(action, (INSTRUCTIONS_RECT[0] + 320, INSTRUCTIONS_RECT[1] + index * key.get_rect().height))

        # draw "click any ket to continue"
        any_key = font.render(instructions[-1], True, BLACK, OFF_WHITE)
        screen.blit(any_key, (INSTRUCTIONS_RECT[0] + 100, INSTRUCTIONS_RECT[1] + (index + 1.5) * key.get_rect().height))

    # draw "Pause" banner
    font = pygame.font.SysFont('ComicSansMS', 80)
    text = font.render("Pause", True, BLACK, GREEN)
    screen.blit(text, (screen.get_rect().centerx - text.get_rect().width / 2, 60))

    pygame.display.flip()
    while True:
        event = pygame.event.get()
        if [x for x in event if x.type == pygame.QUIT]:
            return True
        if [x for x in event if x.type == pygame.MOUSEBUTTONDOWN or x.type == pygame.KEYDOWN]:
            return False


def init_screen():
    """
    first screen setup
    :return: screen , background image, paddle, ball on paddle
    """
    # set screen
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Breaker")
    icon = pygame.image.load(ICON)
    icon.set_colorkey(LAV)
    pygame.display.set_icon(icon)

    # image background
    img = pygame.image.load(BACKGROUND)
    screen.blit(img, (0, 0))

    # init paddle
    paddle = Paddle(250, 500)
    screen.blit(paddle.image, paddle.get_pos())

    # set ball on paddle
    start_ball = Ball(paddle.rect.centerx, paddle.rect.centery - paddle.rect.height)
    screen.blit(start_ball.image, start_ball.get_pos())

    # display screen
    pygame.display.flip()

    return screen, img, paddle, start_ball


def end_game(ball_list, brick_list, screen):
    """
    set ending screen
    :param ball_list: group of balls
    :param brick_list: group of bricks
    :param screen: game screen
    :return: True if game is over
    """
    if not ball_list:
        game_over(screen)
        return True

    if not list(filter(lambda x: x.required, brick_list)):
        winning(screen)
        return True

    return False


def clicked_button_action(screen, brick_list, balls_list, paddle):
    """
    do action when any button is clicked
    :param screen: game screen
    :param brick_list: group of bricks
    :param balls_list: group of balls
    :param paddle: game paddle
    :return: quit game, new ball was shot now
    """
    # init variables
    quit_game, ball_clicked = False, False

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
            elif event.button == RIGHT:
                quit_game = pause(screen)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_clicked = shoot(paddle, balls_list)
            elif event.key == pygame.K_a:
                brick_list.empty()
                brick_list.add(LEVEL())
                brick_list.draw(screen)
            elif event.key == pygame.K_PAUSE:
                quit_game = pause(screen)

    return quit_game, ball_clicked


def main():
    # init objects
    pygame.init()
    brick_list = pygame.sprite.Group()
    balls_list = pygame.sprite.Group()
    screen, img, paddle, start_ball = init_screen()
    clock = pygame.time.Clock()

    prev_mouse_point = (0, 0)
    quit_game = False  # quit button was clicked
    while not quit_game:
        brick_list = LEVEL()
        brick_list.draw(screen)
        balls_list.empty()

        ball_clicked = False
        win_or_loose = False
        while not quit_game and not win_or_loose:

            # act according to the clicked button
            quit_game, ball_clicked_now = clicked_button_action(screen, brick_list, balls_list, paddle)
            if ball_clicked_now:
                ball_clicked = True

            # reset background image
            screen.blit(img, (0, 0))

            # show mouse's current location
            mouse_point = pygame.mouse.get_pos()

            # display paddle
            if mouse_point != prev_mouse_point:
                prev_mouse_point = mouse_point
                paddle.update_loc(mouse_point[0] - paddle.rect.width / 2)

            screen.blit(paddle.image, paddle.get_pos())

            # display the starting position of the ball
            if not ball_clicked:
                screen.blit(start_ball.image, (paddle.rect.centerx - 10, paddle.rect.centery - 20))

            # set ball location and test if the ball is within the screen borders
            for ball in balls_list:
                ball.update_loc()
                if ball.rect.center[0] > WINDOW_WIDTH:
                    ball.hit_side_border("right")
                if ball.rect.center[0] < 0:
                    ball.hit_side_border("left")
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

            # ball hit paddle
            ball_paddle_hit_list = pygame.sprite.spritecollide(paddle, balls_list, False)
            for ball in ball_paddle_hit_list:
                ball.point_up()

            # draw balls and bricks on the screen
            balls_list.draw(screen)
            brick_list.draw(screen)
            pygame.display.flip()

            # end game
            if ball_clicked:
                win_or_loose = end_game(balls_list, brick_list, screen)

            clock.tick(REFRESH_RATE)

        if quit_game:
            break

        quit_game = play_again_banner(screen)

    pygame.quit()


if __name__ == '__main__':
    main()
