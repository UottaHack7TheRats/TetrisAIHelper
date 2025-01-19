from tetris import Tetris


class TetrisStateRanker:
    def __init__(self, field):
        self.field = field
        self.width = len(field[0])
        self.height = len(field)


    def calculate_bumpiness(self):
        heights = [0] * self.width
        bumpiness = 0

        # Calculate the height of each column
        for j in range(self.width):
            for i in range(self.height):
                if self.field[i][j] > 0:
                    heights[j] = self.height - i
                    break
        
        # Calculate bumpiness (difference between adjacent column heights)
        for i in range(1, len(heights)):
            bumpiness += abs(heights[i] - heights[i-1])

        return bumpiness

    def calculate_holes(self):
        holes = 0
        for j in range(self.width):
            block_found = False
            for i in range(self.height):
                if self.field[i][j] > 0:
                    block_found = True
                elif block_found and self.field[i][j] == 0:
                    holes += 1
        return holes

    def calculate_aggregate_height(self):
        heights = [0] * self.width
        for j in range(self.width):
            for i in range(self.height):
                if self.field[i][j] > 0:
                    heights[j] = self.height - i
                    break
        return sum(heights)

    def calculate_completed_lines(self):
        completed_lines = 0
        for i in range(self.height):
            if all(self.field[i][j] > 0 for j in range(self.width)):
                completed_lines += 1
        return completed_lines

    def rank_state(self):
        bumpiness = self.calculate_bumpiness()
        holes = self.calculate_holes()
        aggregate_height = self.calculate_aggregate_height()
        completed_lines = self.calculate_completed_lines()

        # A simple ranking score where lower is better (more favorable)
        rank_score = bumpiness * 1.2 + holes * 10 + aggregate_height * 0.8 - completed_lines * 2

        return rank_score

# Usage
# tetris_game = Tetris(20, 10)  # Example game
# ranker = TetrisStateRanker(tetris_game)
# state_rank = ranker.rank_state()
# print(f"Current game state rank: {state_rank}")