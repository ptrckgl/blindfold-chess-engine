import berserk  # Using the Lichess API
import chess
import os

'''
Notes:
- By default, games have no time limit
- Must set an environment variable 'LICHESS_TOKEN' which is the API token for your lichess account
- Must tick two options when creating this api token (eventually make a list of steps)
- pip install berserk/chess libraries
'''


def create_board():
    """Creates and returns the board as a 2d array"""
    # Note, the colours don't matter which is why there is no differentiation
    return [
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]


def translate_moves(moves):
    """Translates moves from square-to-square notation to modern notation"""
    # Todo: COMPLETE THIS FUNCTION
    # For example, from e2e4 to e4, b1c3 to Nc3
    # Some situations to consider: (Combinations of?) En-passant, Promotion, Castling, Check
    board = create_board()
    new_moves = []
    for move in moves.split(' '):
        sq1, sq2 = move[0:2], move[2:4]

    return new_moves


def print_moves(moves):
    """Prints the moves in a nice/standard format"""
    # Todo: new_moves = translate_moves(moves)
    # TODO: Use 'chess' library instead of re-invent the wheel
    new_moves = moves
    white_move = True
    turn = 1
    for move in new_moves.split(' '):
        if white_move:
            print(f"{turn}. {move:<8}", end="")
            turn += 1
        else:
            print(move)
        white_move = not white_move
    print()


def start_game(colour, mode, difficulty):
    """Starts the game using the Lichess API"""
    session = berserk.TokenSession(os.environ['LICHESS_TOKEN'])
    # client = berserk.clients.Client(session)
    challenges = berserk.clients.Challenges(session)
    board = berserk.clients.Board(session)
    games = berserk.clients.Games(session)
    gid = None  # Game id

    # Todo: Add checking to see if there is already a game in progress
    # Assume: There are no games in progress

    challenges.create_ai(level=difficulty, color=colour)
    for event in board.stream_incoming_events():
        if event['type'] == 'gameStart':
            gid = event['game']['id']
        break

    print("Game successfully started.")
    return (session, board, games, gid)
