from figure import Figure
from tetris import Tetris


def get_next_states(tetris: Tetris, figure: Figure):

    '''
        Returns a big list of all possible board states using the current board state and the next piece
    '''

    state = [[0 for _ in range(tetris.width)] for _ in range(tetris.height)]

    # Colors are stored in tetris.field, so I just swap all non zero values with 1 for ease of use
    for i in range(len(state)):
        for j in range(len(state[0])):
            if tetris.field[i][j] == 0:
                state[i][j] = 0
            else:
                state[i][j] = 1

    # Stores output values
    next_states = []

    rotation_count = len(figure.piece)

    for i in range(rotation_count):

        for j in range(figure.piece_info[i][Figure.info_possibilities]):
            
            figure_copy = figure.copy()
            figure_copy.x = j

            # Rotate copy based on outer loop
            for k in range(i):
                figure_copy.rotate()

            offset = figure_copy.piece_info[i][Figure.info_empty_space]
            figure_copy.x -= offset

            next_tetris = tetris.copy()
            next_tetris.figure = figure_copy

            while (True):

                figure_copy.y += 1

                if next_tetris.intersects():
                    figure_copy.y -= 1
                    break

            next_tetris.freeze()

            next_states.append(next_tetris.field)

    return next_states



if __name__ == "__main__":
    tetris = Tetris(20, 10)  # Initialize a game with 20 rows and 10 columns
    figure = Figure(3, 0)    # Initialize the figure (you can modify this to set up a specific piece)

    tetris.field[19][0] = 1

    next_states = get_next_states(tetris, figure)
    for idx, state in enumerate(next_states):
        print(f"Next State {idx+1}:")
        for row in state:
            print(row)