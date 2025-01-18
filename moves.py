from figure import Figure
from tetris import Tetris

def get_next_states(tetris: Tetris, figure: Figure):

    state = [[0 for _ in range(tetris.width)] for _ in range(tetris.height)]

    # Colors are stored in tetris.field, so I just swap all non zero values with 1 for ease of use
    for i in range(len(state)):
        for j in range(len(state[0])):
            if tetris.field[i][j] == 0:
                state[i][j] = 0
            else:
                state[i][j] = 1

    next_states = []
    rotation_count = len(figure.piece)
    for i in figure.piece_info:
        next_states.append()
    

    # find all possible moves
    match figure.piece:

        case Figure.pieceO:
            pass

        case Figure.pieceI:
            pass

        case Figure.pieceS:
            pass

        case Figure.pieceZ:
            pass

        case Figure.pieceT:
            pass

        case Figure.pieceJ:
            pass

        case Figure.pieceL:
            pass


    # store the board state after each move



if __name__ == "__main__":
    tetris = Tetris(20, 10)
    figure = Figure(3, 0)

    get_next_states(tetris, figure)