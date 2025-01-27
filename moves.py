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
            state[i][j] = tetris.field[i][j]

    # Stores output values
    next_states = []

    rotation_count = len(figure.piece)

    for i in range(rotation_count):

        for j in range(figure.piece_info[i][Figure.info_possibilities]):
            
            figure_copy = figure.copy()
            figure_copy.x = j
            figure_copy.y = 0

            # Rotate copy based on outer loop
            while figure_copy.rotation != i:
                figure_copy.rotate()

            offset = figure_copy.piece_info[i][Figure.info_empty_space]
            figure_copy.x -= offset

            next_tetris = tetris.copy()
            next_tetris.figure = figure_copy

            while not next_tetris.intersects():
                figure_copy.y += 1

            figure_copy.y -= 1

            next_tetris.place_piece_no_update()

            next_states.append((next_tetris.field,next_tetris.figure))

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