import berserk  # Using the Lichess API
import chess
import chess.pgn
import os

'''
Notes:
- By default, games have no time limit
- Must set an environment variable 'LICHESS_TOKEN' which is the API token for your lichess account
- Must tick two options when creating this api token (eventually make a list of steps)
- pip install berserk/chess libraries
'''


def print_moves(moves):
    """Prints the moves in a nice/standard format"""
    new_moves = moves
    game = chess.pgn.Game()
    first = True
    node = None

    # Insert the moves into the 'game'
    for move in new_moves.split(' '):
        if first:
            node = game.add_variation(chess.Move.from_uci(move))
            first = False
        else:
            node = node.add_variation(chess.Move.from_uci(move))

    # Print all the moves in modern algebraic notation
    index = 1
    for move in str(game[0]).split(' '):
        if index == 1:
            print(move, end="")
        elif index == 2:
            print(f" {move:<8}", end="")
        else:  # Index == 3
            print(move)
            index = 0
        index += 1


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
