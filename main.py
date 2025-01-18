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

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

            next_states = get_next_states(game, game.figure)
            next_states_scored = []

            for state in next_states:
                ranker = TetrisStateRanker(state)
                score = ranker.rank_state()
                next_states_scored.append([score, state])

            next_states_scored.sort()
            decision_tree_best = next_states_scored[0][1]

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
                pygame.draw.rect(screen, Color.all_colors[game.field[i][j]], [
                    game.x + game.zoom * j + 1,
                    game.y + game.zoom * i + 1,
                    game.zoom - 2,
                    game.zoom - 2
                ])
            elif decision_tree_best is not None:
                if decision_tree_best[i][j] > 0:
                    pygame.draw.rect(screen, Color.yellow, [
                        game.x + game.zoom * j + 1,
                        game.y + game.zoom * i + 1,
                        game.zoom - 2,
                        game.zoom - 2
                    ])



    # Inside your main loop, just before drawing the current figure, add:
    if game.figure is not None:
        piece = moveGhostDown(game.figure)

        # Draw the ghost piece in a lighter color (for example, a semi-transparent color)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.figure.image():
                    pygame.draw.rect(screen, (128, 128, 128), [  # Lighter color for ghost piece
                        game.x + game.zoom * (j + piece.x) + 1,
                        game.y + game.zoom * (i + piece.y) + 1,
                        game.zoom - 2,
                        game.zoom - 2
                    ])


    #display game
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.figure.image():
                    pygame.draw.rect(screen, Color.all_colors[game.figure.color], [
                        game.x + game.zoom * (j + game.figure.x) + 1,
                        game.y + game.zoom * (i + game.figure.y) + 1,
                        game.zoom - 2,
                        game.zoom - 2
                    ])

    # Display next piece
    if game.next_figure is not None:
        font_next = pygame.font.SysFont('Calibri', 20, True, False)
        text_next = font_next.render("Next Piece:", True, (255, 255, 255))
        screen.blit(text_next, [300, 50])

        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.next_figure.image():
                    pygame.draw.rect(screen, Color.all_colors[game.next_figure.color], [
                        300 + game.zoom * j + 1,
                        80 + game.zoom * i + 1,
                        game.zoom - 2,
                        game.zoom - 2
                    ])

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


