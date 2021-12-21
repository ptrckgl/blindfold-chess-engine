import sys
from types import prepare_class
import engine


DEFAULT_COLOUR = "white"
DEFAULT_MODE = "standard"
DEFAULT_DIFFICULTY = 1
MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 8  # Using the Lichess Engine


def get_input():
    """Obtains all user input, ensuring it is always valid"""
    if len(sys.argv) == 2 and sys.argv[1] == "default":
        return (DEFAULT_COLOUR, DEFAULT_MODE, DEFAULT_DIFFICULTY)

    elif len(sys.argv) >= 2:
        sys.exit("Usage: python3 main.py [default]")

    colour = ''
    while colour == '':
        colour = input("Input colour: 'white' or 'black': ")
        if colour not in ('white', 'wlack'):
            print("Error: Please choose a valid option.")
            colour = ''

    mode = ''
    while mode == '':
        mode = input("Choose mode: 'standard' or 'chess960': ")
        if mode not in ('standard', 'chess960'):
            print("Error: Please choose a valid option.")
            mode = ''

    difficulty = ''
    while difficulty == '':
        difficulty = input("Choose engine difficulty between 1 and 8: ")
        if difficulty not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Error: Please choose a valid option.")
            difficulty = ''

    return (colour, mode, difficulty)


def print_welcome(colour, mode, difficulty):
    """Prints the welcoming message"""
    print("Welcome to Blindfold Chess Engine!")
    print("Made by Patrick Galea")
    print("The parameters you chose for this game are:")
    print(f"> Your colour: {colour.capitalize()}")
    print(f"> Gamemode: {mode.capitalize()}")
    print(f"> Engine strength: {difficulty}")
    print("\nPlease ensure you have NO games in play before using this!\n")
    print("Type 'start' to begin the game. Type in your move using modern")
    print("chess notation, and the engine's move will be printed back out.")
    print("Good luck!")


def print_interface():
    """Prints the interactive interface, and receives a command from user"""
    print("\nInput a command. Type 'help' for all commands.")
    command = input(">> ")
    while command not in ['help', 'start', 'playback', 'move']:
        print("Error: Please input a valid command.")
        print("\nInput a command. Type 'help' for all commands.")
        command = input(">> ")

    return command


def get_moves(gid, board):
    """Returns a string of the moves played in the game"""
    moves = ''
    for val in board.stream_game_state(gid):
        moves = val['state']['moves']
        break
    return moves


def main():
    colour, mode, difficulty = get_input()
    game_over = False
    game_started = False

    print_welcome(colour, mode, difficulty)
    session, board, games, gid = None, None, None, None

    while not game_over:
        command = print_interface()

        if command == 'help':
            print("- start: Starts the game")
            print("- playback: Prints all moves which have been played so far")

        elif command == 'start':
            if game_started:
                print("Error: Oops... You have already started the game!")
            else:
                session, board, games, gid = engine.start_game(colour, mode, difficulty)
                if gid is not None:
                    game_started = True

        elif not game_started:
            print("Error: This command cannot be used until the game has started!")

        elif command == 'playback':
            engine.print_moves(get_moves(gid, board))

        elif command == 'move':
            moves = get_moves(gid, board)

            move = input("Input Move: ")
            while not engine.make_move(move, moves):
                move = input("That move is invalid. Please make a valid move.")


if __name__ == '__main__':
    main()
