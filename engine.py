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


def generate_game(moves):
    """Generates a game node which has all moves inserted into it"""
    game, first, node = chess.pgn.Game(), True, None

    # Insert the moves into the 'game' object
    for move in moves.split(' '):
        if move == '':
            return None
        if first:
            node = game.add_variation(chess.Move.from_uci(move))
            first = False
        else:
            node = node.add_variation(chess.Move.from_uci(move))

    return game


def generate_game_board(moves):
    """Generates a board position based on all moves made"""
    return generate_game(moves).end().board()


def print_moves(moves, return_first=False, return_last=False):
    """Prints the moves in a nice/standard format"""
    game = generate_game(moves)

    # Occurs when no moves of the game have been played
    if game is None:
        return

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
    challenges = berserk.clients.Challenges(session)
    berserk_board = berserk.clients.Board(session)
    gid = None  # Game id

    # Todo: Add checking to see if there is already a game in progress
    # Assume: There are no games in progress

    challenges.create_ai(level=difficulty, color=colour)
    for event in berserk_board.stream_incoming_events():
        if event['type'] == 'gameStart':
            gid = event['game']['id']
        break

    print("Game successfully started.")
    return (berserk_board, gid)


def make_move(move, made_moves, gid, berserk_board):
    """Makes a move on the board after checking it is a legal move."""
    if len(made_moves) != 0:
        game_board = generate_game_board(made_moves)
    else:
        game_board = chess.Board()

    # Check if the move is legal, make it and return true!
    legal_moves = [game_board.san(x) for x in game_board.legal_moves]
    syntax_dict = dict(zip(legal_moves, [str(x) for x in game_board.legal_moves]))
    if move in legal_moves:
        berserk_board.make_move(gid, syntax_dict[move])
        print("Move successfully made.")
        return True

    return False


def resign(gid, berserk_board, print_output=True):
    """Resigns the game"""
    try:
        berserk_board.resign_game(gid)
        if print_output:
            print("Game successfully resigned.")
    except berserk.exceptions.ResponseError:
        if print_output:
            print("Error: Game is already over.")


def game_is_over(moves):
    """Checks if the game is over"""
    game_board = generate_game_board(moves)
    outcome = game_board.outcome()

    if game_board.is_game_over():
        print(f"{outcome.termination.name.capitalize()}!")
        return True

    return False
