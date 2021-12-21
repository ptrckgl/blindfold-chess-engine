from typing import Iterator
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


def print_moves(moves, return_first=False, return_last=False):
    """Prints the moves in a nice/standard format"""
    game, first, node = chess.pgn.Game(), True, None

    # Insert the moves into the 'game' object
    for move in moves.split(' '):
        if first:
            node = game.add_variation(chess.Move.from_uci(move))
            first = False
        else:
            node = node.add_variation(chess.Move.from_uci(move))

    # Return the first move of the game (this is called when player is black)
    if return_first:
        return str(game[0]).split(' ')[1]

    # Return the last move of the game (this is called for displaying computer's move)
    if return_last:
        return str(game[0]).split(' ')[-1]

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
    return (board, gid)


def make_move(move, made_moves, gid, game_board):
    """Makes a move on the board after checking it is a legal move."""
    board = chess.Board()

    # Check that there has actually been a made move
    if len(made_moves) != 0:
        for m in made_moves.split(' '):
            board.push(chess.Move.from_uci(m))

    # Check if the move is legal, make it and return true!
    legal_moves = [board.san(x) for x in board.legal_moves]
    syntax_dict = dict(zip(legal_moves, [str(x) for x in board.legal_moves]))
    if move in legal_moves:
        game_board.make_move(gid, syntax_dict[move])
        print("Move successfully made.")
        return True

    return False
