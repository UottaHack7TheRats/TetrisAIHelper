import pygame
import random

import color as Color
from figure import Figure
from tetris import Tetris
from gameStateEvalution import TetrisStateRanker
from moves import get_next_states


# def get_ghost_position(figure, field):
#     # Check where the figure will land by moving it down until it collides
#     ghost_position = figure.y
#     while not game.intersects(piece):
#         ghost_position += 1
#     return ghost_position
def intersects(piece):
    for i in range(4):
        for j in range(4):
            if i * 4 + j in piece.image():
                if i + piece.y >= game.height or \
                        j + piece.x >= game.width or \
                        j + piece.x < 0 or \
                        game.field[i + piece.y][j + piece.x] > 0:
                    return True
    return False
def moveGhostDown(figure):
    piece = figure.copy()
    while not intersects(piece):
        piece.y += 1
    piece.y -= 1
    return piece
# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Tetris")

# Loop until the user closes the window
done = False
clock = pygame.time.Clock()
fps = 25

game = Tetris(20, 10)
counter = 0
pressing_down = False

decision_tree_best = None

tile_size = 19      # This is the default value for game.zoom - 2 for padding

# Load image textures for tiles
tile_blue_temp = pygame.image.load("textures/blueTile.png")
tile_green_temp = pygame.image.load("textures/greenTile.png")
tile_light_blue_temp = pygame.image.load("textures/lightBlueTile.png")
tile_orange_temp = pygame.image.load("textures/orangeTile.png")
tile_purple_temp = pygame.image.load("textures/purpleTile.png")
tile_red_temp = pygame.image.load("textures/redTile.png")
tile_yellow_temp = pygame.image.load("textures/yellowTile.png")

# Resize images so they all match
tile_blue = pygame.transform.scale(tile_blue_temp, (tile_size, tile_size))
tile_green = pygame.transform.scale(tile_green_temp, (tile_size, tile_size))
tile_light_blue = pygame.transform.scale(tile_light_blue_temp, (tile_size, tile_size))
tile_orange = pygame.transform.scale(tile_orange_temp, (tile_size, tile_size))
tile_purple = pygame.transform.scale(tile_purple_temp, (tile_size, tile_size))
tile_red = pygame.transform.scale(tile_red_temp, (tile_size, tile_size))
tile_yellow = pygame.transform.scale(tile_yellow_temp, (tile_size, tile_size))

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    # Get best next move
    next_states = get_next_states(game, game.figure)
    next_states_scored = []

    for state in next_states:
        ranker = TetrisStateRanker(state)
        score = ranker.rank_state()
        next_states_scored.append([score, state])

    next_states_scored.sort()
    decision_tree_best = next_states_scored[0][1]

    # Move all down
    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

            # print("Score: ", next_states_scored[0][0])
            # for row in next_states_scored[0][1]:
            #     print(row)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
            if event.key == pygame.K_RETURN:
                if decision_tree_best != None:
                    
                    for i in range(len(game.field)):
                        for j in range(len(game.field[0])):
                            game.field[i][j] = decision_tree_best[i][j]

                    game.new_figure()
                    game.break_lines()

                    decision_tree_best = None


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill((0, 0, 0))

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, (72, 72, 72), [
                game.x + game.zoom * j,
                game.y + game.zoom * i,
                game.zoom,
                game.zoom
            ], 1)

            if game.field[i][j] > 0:

                tile_pos_x = game.x + game.zoom * j
                tile_pos_y = game.y + game.zoom * i

                match Color.all_colors[game.field[i][j]]:

                    case Color.blue:
                        screen.blit(tile_blue, (tile_pos_x, tile_pos_y))

                    case Color.green:
                        screen.blit(tile_green, (tile_pos_x, tile_pos_y))

                    case Color.light_blue:
                        screen.blit(tile_light_blue, (tile_pos_x, tile_pos_y))

                    case Color.purple:
                        screen.blit(tile_purple, (tile_pos_x, tile_pos_y))

                    case Color.red:
                        screen.blit(tile_red, (tile_pos_x, tile_pos_y))

                    case Color.orange:
                        screen.blit(tile_orange, (tile_pos_x, tile_pos_y))

                    case Color.yellow:
                        screen.blit(tile_yellow, (tile_pos_x, tile_pos_y))


            elif decision_tree_best is not None:
                if decision_tree_best[i][j] > 0:
                    pygame.draw.rect(screen, Color.yellow, [
                        game.x + game.zoom * j + 6,
                        game.y + game.zoom * i + 6,
                        game.zoom - 12,
                        game.zoom - 12
                    ])



    # Inside your main loop, just before drawing the current figure, add:
    if game.figure is not None:
        piece = moveGhostDown(game.figure)

        # Draw the ghost piece in a lighter color (for example, a semi-transparent color)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.figure.image():

                    piece_color = Color.all_colors[game.figure.color]

                    pygame.draw.rect(
                        screen, 
                        piece_color, 
                        [  # Lighter color for ghost piece
                            game.x + game.zoom * (j + piece.x) + 1,
                            game.y + game.zoom * (i + piece.y) + 1,
                            game.zoom - 2,
                            game.zoom - 2,
                        ],
                        2  # Border width of unfilled rect
                    )


    #display game
    tile_size = game.zoom

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.figure.image():

                    tile_pos_x = game.x + game.zoom * (j + game.figure.x)
                    tile_pos_y = game.y + game.zoom * (i + game.figure.y)

                    match Color.all_colors[game.figure.color]:

                        case Color.blue:
                            screen.blit(tile_blue, (tile_pos_x, tile_pos_y))

                        case Color.green:
                            screen.blit(tile_green, (tile_pos_x, tile_pos_y))

                        case Color.light_blue:
                            screen.blit(tile_light_blue, (tile_pos_x, tile_pos_y))

                        case Color.purple:
                            screen.blit(tile_purple, (tile_pos_x, tile_pos_y))

                        case Color.red:
                            screen.blit(tile_red, (tile_pos_x, tile_pos_y))

                        case Color.orange:
                            screen.blit(tile_orange, (tile_pos_x, tile_pos_y))

                        case Color.yellow:
                            screen.blit(tile_yellow, (tile_pos_x, tile_pos_y))

    # Display next piece
    if game.next_figure is not None:
        font_next = pygame.font.SysFont('Calibri', 20, True, False)
        text_next = font_next.render("Next Piece:", True, (255, 255, 255))
        screen.blit(text_next, [300, 50])

        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.next_figure.image():

                    tile_pos_x = 300 + game.zoom * j + 1
                    tile_pos_y = 80 + game.zoom * i + 1

                    match Color.all_colors[game.next_figure.color]:

                        case Color.blue:
                            screen.blit(tile_blue, (tile_pos_x, tile_pos_y))

                        case Color.green:
                            screen.blit(tile_green, (tile_pos_x, tile_pos_y))

                        case Color.light_blue:
                            screen.blit(tile_light_blue, (tile_pos_x, tile_pos_y))

                        case Color.purple:
                            screen.blit(tile_purple, (tile_pos_x, tile_pos_y))

                        case Color.red:
                            screen.blit(tile_red, (tile_pos_x, tile_pos_y))

                        case Color.orange:
                            screen.blit(tile_orange, (tile_pos_x, tile_pos_y))

                        case Color.yellow:
                            screen.blit(tile_yellow, (tile_pos_x, tile_pos_y))

    font = pygame.font.SysFont('Calibri', 25, True, False)
    text_score = font.render(f"Score: {game.score}", True, (255, 255, 255))
    text_level = font.render(f"Level: {game.level}", True, (255, 255, 255))
    screen.blit(text_score, [0, 0])
    screen.blit(text_level, [0, 30])

    if game.state == "gameover":
        font_game_over = pygame.font.SysFont('Calibri', 65, True, False)
        text_game_over = font_game_over.render("Game Over", True, (255, 0, 0))
        text_restart = font_game_over.render("Press ESC", True, (0, 0, 255))
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_restart, [25, 300])

    pygame.display.flip()
    clock.tick(fps)



pygame.quit()


