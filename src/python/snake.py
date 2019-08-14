import pygame as pg
import random
import os

pg.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
food_img_loc = '../resources/images/food/'
snake_head_img = pg.image.load('../resources/images/snake_head.png')
food_img_file = random.choice(os.listdir(food_img_loc))
food = pg.image.load(food_img_loc + food_img_file)


display_width = 800
display_height = 600
# define surface as gameDisplay
gameDisplay = pg.display.set_mode((display_width, display_height))
# set title of the game window
pg.display.set_caption("Snake Game")

# set icon
icon = pg.image.load('../resources/images/snake_head.png')
pg.display.set_icon(icon)  # size is 32x32

# intialize frames per second
clock = pg.time.Clock()

block_size = 20
FPS = 15
food_thickness = 30
direction = "right"

small_font = pg.font.SysFont("comicsansms", 25)
med_font = pg.font.SysFont("comicsansms", 50)
large_font = pg.font.SysFont("comicsansms", 75)


def pause():
    """
    Pause the game
    """
    paused = True
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press C to continue or Q to quit", black, 25)

    pg.display.update()

    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    paused = False
                if event.key == pg.K_q:
                    pg.quit()
                    quit()
        clock.tick(5)


def score(score_gained):
    """
    Set the score gained
    """
    text = small_font.render("Score: " + str(score_gained), True, black)
    gameDisplay.blit(text, [0, 0])


def rand_food_gen():
    """
    Generate food at random location
    """
    rand_food_x = round(random.randrange(0, display_width - food_thickness))
    rand_food_y = round(random.randrange(0, display_height - food_thickness))
    return rand_food_x, rand_food_y


def game_intro():
    """
    Welcome Window or entry to the game
    """
    intro = True

    while intro:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    intro = False
                if event.key == pg.K_q:
                    pg.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake", green, -100, "large")
        message_to_screen("Eat! Grow! Die! Repeat!", black, -20)
        message_to_screen("Press C to play again or Q to quit", black, 100)
        pg.display.update()
        clock.tick(5)


def snake(snake_list):
    """
    Define snake and snake head rotation logic
    """
    head = snake_head_img

    if direction == "up":
        head = snake_head_img

    if direction == "right":
        head = pg.transform.rotate(snake_head_img, 270)

    if direction == "left":
        head = pg.transform.rotate(snake_head_img, 90)

    if direction == "down":
        head = pg.transform.rotate(snake_head_img, 180)

    gameDisplay.blit(head, (snake_list[-1][0], snake_list[-1][1]))

    for pos in snake_list[:-1]:
        # Create a rectangle for snake
        pg.draw.rect(gameDisplay, green, [pos[0], pos[1], block_size, block_size])


def text_objects(text, color, size):
    """
    Define properties of text
    """
    text_surface = small_font.render(text, True, color)
    if size == "small":
        text_surface = small_font.render(text, True, color)
    elif size == "med":
        text_surface = med_font.render(text, True, color)
    elif size == "large":
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    """
    Adding text to screen
    """
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(text_surf, text_rect)


def game_loop():
    """
    Main game loop
    """
    global direction
    global food
    game_exit = False
    game_over = False
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 0
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    rand_food_x, rand_food_y = rand_food_gen()

    # game loop
    while not game_exit:
        # game over loop
        while game_over:
            message_to_screen("Game Over", red, -50, "large")
            message_to_screen("Press C to play again or Q to quit", black, 50, "med")
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pg.K_c:
                        game_loop()

        # event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pg.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pg.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pg.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pg.K_p:
                    pause()

        # boundary logic
        if lead_x >= display_width or lead_x < 0 or lead_y > display_height or lead_y <= 0:
            game_over = True

        # snake movement logic
        lead_x += lead_x_change
        lead_y += lead_y_change

        # fill background color
        gameDisplay.fill(white)

        # create food
        gameDisplay.blit(food, (rand_food_x, rand_food_y))

        # snake length logic
        snake_head = list()
        snake_head.append(lead_x)
        snake_head.append(lead_y)

        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # snake collision logic
        for eachSegment in snake_list[:-1]:
            if eachSegment == snake_head:
                game_over = True

        # create snake
        snake(snake_list)

        # set score
        score(snake_length-1)

        # render the display with new updates
        pg.display.update()

        # eating logic
        food_x_thickness = rand_food_x + food_thickness
        food_y_thickness = rand_food_y + food_thickness
        lead_x_block_size = lead_x + block_size
        lead_y_block_size = lead_y + block_size
        if rand_food_x < lead_x < food_x_thickness or rand_food_x < lead_x_block_size < food_x_thickness:
            if rand_food_y < lead_y < food_y_thickness or rand_food_y < lead_y_block_size < food_y_thickness:
                rand_food_x, rand_food_y = rand_food_gen()
                snake_length += 1
                food_img_file = random.choice(os.listdir(food_img_loc))
                food = pg.image.load(food_img_loc + food_img_file)

        # frames per second
        clock.tick(FPS)

    pg.quit()
    quit()


game_intro()
game_loop()
