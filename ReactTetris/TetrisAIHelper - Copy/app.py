from flask import Flask, request, jsonify
from flask_cors import CORS

from main import moveGhostDown
from figure import Figure
from gameStateEvalution import TetrisStateRanker
from moves import get_next_states
from tetris import Tetris  # Import CORS from flask_cors

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # This will allow requests from any origin by default

@app.route('/get-move', methods=['POST'])
def get_move():
    data = request.json
    board = data.get('board')
    upcoming_blocks = data.get('upcomingBlocks')
    
    # Your AI logic here
    move = calculate_best_move(board, upcoming_blocks)

    return jsonify({"move": move})

def calculate_best_move(board, upcoming_block):
    # Example: Simple logic (replace with AI logic)
    # Return an example move like "left", "right", "rotate", or "drop"

    game = Tetris(20, 10)
    game.field = board

    currentPieceNumber = None
    match(upcoming_block):
        case 'O': currentPieceNumber = 0
        case 'I': currentPieceNumber = 1
        case 'S': currentPieceNumber = 2
        case 'Z': currentPieceNumber = 3
        case 'T': currentPieceNumber = 4
        case 'J': currentPieceNumber = 5
        case 'L': currentPieceNumber = 6

    currentPiece = Figure(3, 0, currentPieceNumber)
    game.figure = currentPiece

    next_states = get_next_states(game, game.figure)
    next_states_scored = []

    for state in next_states:
        ranker = TetrisStateRanker(state[0])
        score = ranker.rank_state()
        next_states_scored.append([score, state])

    next_states_scored.sort()
    decision_tree_best = next_states_scored[0][1]

    #recomended = moveGhostDown(decision_tree_best[1])
    recomended = decision_tree_best[1]
    # match(recomended.type):
    #     case 0: currentPiece = 'O'
    #     case 1: currentPiece = 'I'
    #     case 2: currentPiece = 'S'
    #     case 3: currentPiece = 'Z'
    #     case 4: currentPiece = 'T'
    #     case 5: currentPiece = 'J'
    #     case 6: currentPiece = 'L'
    print(recomended.image())
    return (recomended.x,recomended.y,recomended.type,recomended.image())

if __name__ == '__main__':
    app.run(debug=True)
