from figure import Figure

class Tetris:

    # Score amounts for each amount of lines cleared

    scoring = [
        40,         # 1 line cleared
        100,        # 2 lines cleared
        300,        # 3 lines cleared
        1200        # 4 lines cleared
    ]

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

    def copy(self):

        ret = Tetris(self.height, self.width)

        ret.level = self.level
        ret.score = self.score
        ret.lines_cleared = self.lines_cleared
        ret.state = self.state
        ret.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        ret.height = self.height
        ret.width = self.width
        ret.x = self.x
        ret.y = self.y
        ret.zoom = self.zoom

        if self.figure is not None:
            ret.figure = self.figure.copy()
        else:
            ret.figure = None

        if self.next_figure is not None:
            ret.next_figure = self.next_figure.copy()
        else:
            ret.next_figure = None

        for i in range (self.height):
            for j in range(self.width):
                ret.field[i][j] = self.field[i][j]

        return ret

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):

        if self.figure is None:
            return False

        # Loop through all coordinates in the pieces image
        try:
            for i in self.figure.image():

                x_coord = self.figure.x + (i % 4)
                y_coord = self.figure.y + (i // 4)

                below_floor = y_coord >= self.height
                outside_left = x_coord < 0
                outside_right = x_coord >= self.width
                inside_piece = self.field[y_coord][x_coord] > 0

                # Invalid position
                if below_floor or outside_left or outside_right or inside_piece:
                    return True

        # IndexError means the piece lies outside the game field
        except IndexError:
            return True

        # If the loop finished without returning, theres no intersection
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
        self.score += self.scoring[lines - 1] * (self.level + 1)

    def update_level(self):
        if self.lines_cleared >= self.level * 10:
            self.level += 1

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.place_piece()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.place_piece()

    def place_piece(self):
        try:
            for i in self.figure.image():
                    
                x_coord = self.figure.x + (i % 4)
                y_coord = self.figure.y + (i // 4)

                self.field[y_coord][x_coord] = self.figure.color

        except IndexError:
            print("place_piece failed")
        
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def place_piece_no_update(self):
        try:
            for i in self.figure.image():
                    
                x_coord = self.figure.x + (i % 4)
                y_coord = self.figure.y + (i // 4)

                self.field[y_coord][x_coord] = self.figure.color

        except IndexError:
            print("place_piece_no_update failed")

    def go_side(self, dx):
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx

    def rotate(self):
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = (self.figure.rotation - 1) % len(self.figure.figures[self.figure.type])
