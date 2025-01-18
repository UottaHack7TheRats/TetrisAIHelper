from figure import Figure

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
        self.next_figure = Figure(0, 0)

    def new_figure(self):
        self.figure = Figure(3, 0)

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