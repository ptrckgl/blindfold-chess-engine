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
    print("Type 'Start' to begin the game. Type in your move using modern")
    print("chess notation, and the engine's move will be printed back out.")
    print("Good luck!\n")


def print_interface(help=False):
    """Prints the interactive interface, and receives a command from user"""
    if help:
        print("> start: Starts the game")
        print("> playback: Prints all moves which have been played so far")
        return

    print("Input a command. Type 'help' for all commands.")
    command = input(">> ")
    while command not in ['start', 'playback']:
        print("Error: Please input a valid command.")
        command = input(">> ")

    return command


def main():
    colour, mode, difficulty = get_input()
    board = engine.create_board()
    game_over = False
    game_started = False

    print_welcome(colour, mode, difficulty)
    session, board, games, gid = None, None, None, None
    print(colour, mode, difficulty)

    while not game_over:
        command = print_interface()

        if command == 'start':
            if game_started:
                print("Oops... You have already started the game!")
            else:
                session, board, games, gid = engine.start_game(colour, mode, difficulty)
                if gid is not None:
                    game_started = True

        elif not game_started:
            print("This command cannot be used until the game has started!")

        elif command == 'playback':
            info = games.export(gid)
            print(engine.print_moves(info['moves']))


if __name__ == '__main__':
    main()
