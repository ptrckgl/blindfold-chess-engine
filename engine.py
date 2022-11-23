import berserk  # Using the Lichess API
import chess
import chess.pgn
import os
import interruptingcow


def get_moves(gid, board):
    """Returns a string of the moves played in the game"""
    moves = ''
    for val in board.stream_game_state(gid):
        moves = val['state']['moves']
        break
    return moves


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
    gid = None

    print("Terminating all games in progress...")
    try:
        # Execute it for 3 seconds (should be plenty of time to resign games in progress)
        with interruptingcow.timeout(3, exception=RuntimeError):
            for event in berserk_board.stream_incoming_events():
                if event['type'] == 'gameStart':
                    command_resign(event['game']['id'], berserk_board, print_output=False)
    except RuntimeError:
        pass

    # Not sure why this change is required...
    try:
        challenges.create_ai(level=difficulty, color=colour)
    except:
        pass
    
    for event in berserk_board.stream_incoming_events():
        if event['type'] == 'gameStart':
            gid = event['game']['id']
        break

    print("Game successfully started.")
    print(f"The link to the game is: lichess.org/{gid}")
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
        try:
            berserk_board.make_move(gid, syntax_dict[move])
        except:
            pass
        print("Move successfully made.")
        return True

    return False


def game_is_over(moves):
    """Checks if the game is over"""
    game_board = generate_game_board(moves)
    outcome = game_board.outcome()

    if game_board.is_game_over():
        print(f"{outcome.termination.name.capitalize()}!")
        return True

    return False


def command_help():
    """The help command"""
    print("- start: Starts the game and resigns all current games in progress.")
    print("- playback: Prints all moves which have been played so far.")
    print("- move: Allows you to input a move to play. Type 'back' to cancel making a move.")
    print("- resign: Resign the game.")
    print("- exit: Terminates the program.")
    print("- clear: Clears the screen.")


def command_exit(gid, berserk_board, game_started):
    """The exit command"""
    if game_started:
        try:
            command_resign(gid, berserk_board, print_output=False)
        except:
            pass


def command_start(colour, mode, difficulty):
    """The start command"""
    berserk_board, gid = start_game(colour, mode, difficulty)

    # Upon starting the game, if playing black, display the opponents first move
    if colour == 'black':
        # While no move has been played yet
        while '' in get_moves(gid, berserk_board).split(' '):
            pass

        print("Computer Move:", print_moves(get_moves(gid, berserk_board), return_first=True))

    return berserk_board, gid


def command_playback(gid, berserk_board):
    """The playback command"""
    print(f"The link to the game is: lichess.org/{gid}")
    print_moves(get_moves(gid, berserk_board))


def command_move(gid, berserk_board, colour):
    """The (make) move command. Returns True if the game is over, False if not."""
    moves = get_moves(gid, berserk_board)
    move = input("Input Move: ")
    while move != 'back' and not make_move(move, moves, gid, berserk_board):
        print("That move is invalid. Please make a valid move.")
        move = input("Input Move: ")

    if move == 'back':
        return False

    # Check if the game is over and display to user if so
    if game_is_over(get_moves(gid, berserk_board)):
        return True

    # Wait until the computer has made a move, then print it back out to the user
    mod_val = {'white': 1, 'black': 0}
    while len(get_moves(gid, berserk_board).split(' ')) % 2 == mod_val[colour]:
        pass
    print("Computer Move:", print_moves(get_moves(gid, berserk_board), return_last=True))

    # Check if the game is over and display to user if so
    if game_is_over(get_moves(gid, berserk_board)):
        return True


def command_resign(gid, berserk_board, print_output=True):
    """The resign command"""
    try:
        try:
            berserk_board.resign_game(gid)
        except:
            pass
        if print_output:
            print("Game successfully resigned.")
    except berserk.exceptions.ResponseError:
        if print_output:
            print("Error: Game is already over.")
