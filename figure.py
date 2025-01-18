import random

import color as Color

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
    pieceT = [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]]
    pieceJ = [[0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8]]
    pieceL = [[3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9], [1, 2, 6, 10]]

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
        self.color = random.randint(1, len(Color.all_colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
        