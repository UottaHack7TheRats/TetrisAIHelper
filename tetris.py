import pygame
import random

# Define colors
class Color:
    black = (0, 0, 0)
    purple = (120, 37, 179)
    cyan = (100, 179, 179)
    darkred = (80, 34, 22)
    green = (80, 134, 22)
    red = (180, 34, 22)
    pink = (180, 34, 122)

colors = [
    Color.black, 
    Color.purple, 
    Color.cyan, 
    Color.darkred, 
    Color.green, 
    Color.red, 
    Color.pink
]

class Figure:


    # The following is how the pieces are defined, as well as their rotations
    # The numbers in the inner lists represent positions in a 4x4 matrix. as follows:

    #   0    1    2    3
    #   4    5    6    7
    #   8    9    10   11
    #   12   13   14   15

    pieceO = [[1, 2, 5, 6]]
    pieceI = [[1, 5, 9, 13], [4, 5, 6, 7]]
    pieceS = [[4, 5, 9, 10], [2, 6, 5, 9]]
    pieceZ = [[6, 7, 9, 10], [1, 5, 6, 10]]
    pieceT = [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]
    pieceJ = [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]]
    pieceL = [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]]

    # This list just hold the pieces for easier access (via index)

    figures = [
        pieceO,
        pieceI,
        pieceS,
        pieceZ,
        pieceT,
        pieceJ,
        pieceL
    ]


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

class Tetris:
    def __init__(self, height, width):
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.state = "start"
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.height = height
        self.width = width
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.next_figure = Figure(0, 0)  # Initialize the next figure

    def new_figure(self):
        self.figure = self.next_figure  # Set the current figure to the next figure
        self.next_figure = Figure(0, 0)  # Generate a new next figure

    def intersects(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y >= self.height or \
                            j + self.figure.x >= self.width or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        return True
        return False

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            if all(self.field[i][j] > 0 for j in range(self.width)):
                lines += 1
                for k in range(i, 0, -1):
                    self.field[k] = self.field[k - 1][:]
                self.field[0] = [0 for _ in range(self.width)]
        self.update_score(lines)
        self.lines_cleared += lines
        self.update_level()

    def update_score(self, lines):
        scoring = {1: 40, 2: 100, 3: 300, 4: 1200}
        self.score += scoring.get(lines, 0) * (self.level + 1)

    def update_level(self):
        if self.lines_cleared >= self.level * 10:
            self.level += 1

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx

    def rotate(self):
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = (self.figure.rotation - 1) % len(self.figure.figures[self.figure.type])

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

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

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

    screen.fill((255, 255, 255))

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, (128, 128, 128), [
                game.x + game.zoom * j,
                game.y + game.zoom * i,
                game.zoom,
                game.zoom
            ], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]], [
                    game.x + game.zoom * j + 1,
                    game.y + game.zoom * i + 1,
                    game.zoom - 2,
                    game.zoom - 2
                ])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color], [
                        game.x + game.zoom * (j + game.figure.x) + 1,
                        game.y + game.zoom * (i + game.figure.y) + 1,
                        game.zoom - 2,
                        game.zoom - 2
                    ])

    # Display next piece
    if game.next_figure is not None:
        font_next = pygame.font.SysFont('Calibri', 20, True, False)
        text_next = font_next.render("Next Piece:", True, (0, 0, 0))
        screen.blit(text_next, [300, 50])

        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.next_figure.image():
                    pygame.draw.rect(screen, colors[game.next_figure.color], [
                        300 + game.zoom * j + 1,
                        80 + game.zoom * i + 1,
                        game.zoom - 2,
                        game.zoom - 2
                    ])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    text_score = font.render(f"Score: {game.score}", True, (0, 0, 0))
    text_level = font.render(f"Level: {game.level}", True, (0, 0, 0))
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
