import berserk  # Using the Lichess API
import os

'''
Notes:
- By default, games have no time limit
- Must set an environment variable 'LICHESS_TOKEN' which is the API token for your lichess account
- Must tick two options when creating this api token (eventually make a list of steps)
'''


def create_board():
    """Creates and returns the board as a 2d array"""
    # Find a way to convert these to unicode characters
    return [
        ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
        ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
        ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
    ]


def start_game(colour, mode, difficulty):
    """Starts the game using the Lichess API"""
    # opp_colour = 'white' if colour == 'black' else 'black'
    len_moves = {'white': 0, 'black': 1}
    session = berserk.TokenSession(os.environ['LICHESS_TOKEN'])
    # client = berserk.clients.Client(session)
    challenges = berserk.clients.Challenges(session)
    board = berserk.clients.Board(session)
    games = berserk.clients.Games(session)

    challenges.create_ai(level=difficulty, color=colour)
    for event in board.stream_incoming_events():
        if event['type'] == 'gameStart':
            gid = event['game']['id']
            info = games.export(gid)
            if len(info['moves']) != len_moves[colour]:
                print("You already have a game in progress. Please finish it!")
            break

    print("Game successfully started.")
    return (session, board, games)
