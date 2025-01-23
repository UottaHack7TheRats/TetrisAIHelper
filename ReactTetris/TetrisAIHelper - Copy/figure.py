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
    pieceS = [[0, 1, 5, 6], [2, 6, 5, 9]]
    pieceZ = [[1, 2, 4, 5], [1, 5, 6, 10]]
    pieceT = [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]]
    pieceJ = [[0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8]]
    pieceL = [[2, 4, 5, 6], [1, 5, 9, 10], [4, 5, 6, 8], [0, 1, 5, 9]]

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

    # The following is values used for finding possible positions with each piece
    # Outer list defines rotations, while inner lists define other traits:
    # Traits in order are: 
    # width, 
    # height, 
    # possible x positions, 
    # empty columns on left

    # Constants for indexing
    info_width = 0
    info_height = 1
    info_possibilities = 2
    info_empty_space = 3

    pieceO_info = [[2, 2, 9, 1]]
    pieceI_info = [[1, 4, 10, 1], [4, 1, 7, 0]]
    pieceS_info = [[3, 2, 8, 0], [2, 3, 9, 1]]
    pieceZ_info = [[3, 2, 8, 0], [2, 3, 9, 1]]
    pieceT_info = [[3, 2, 8, 0], [2, 3, 9, 1], [3, 2, 8, 0], [2, 3, 9, 0]]
    pieceJ_info = [[3, 2, 8, 0], [2, 3, 9, 1], [3, 2, 8, 0], [2, 3, 9, 0]]
    pieceL_info = [[3, 2, 8, 0], [2, 3, 9, 1], [3, 2, 8, 0], [2, 3, 9, 0]]

    figures_info = [
        pieceO_info,
        pieceI_info,
        pieceS_info,
        pieceZ_info,
        pieceT_info,
        pieceJ_info,
        pieceL_info
    ]


    def __init__(self, x, y, typeOfPiece=None):
        self.x = x
        self.y = y
        if (typeOfPiece == None):
            self.type = random.randint(0, len(self.figures) - 1)
        else:
            self.type = typeOfPiece
        self.color = random.randint(1, len(Color.all_colors) - 1)
        self.rotation = 0
        self.piece = self.figures[self.type]
        self.piece_info = self.figures_info[self.type]

    def copy(self):

        ret = Figure(self.x, self.y)
        ret.type = self.type
        ret.color = self.color
        ret.rotation = self.rotation
        ret.piece = self.piece
        ret.piece_info = self.piece_info

        return ret

    def image(self):
        return self.piece[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
        