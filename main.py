import sys
import engine


DEFAULT_COLOUR = "w"
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
        colour = input("Input colour: 'w' or 'b': ")
        if colour not in ('w', 'b'):
            colour = ''

    mode = ''
    while mode == '':
        mode = input("Choose mode: 'standard' or '960': ")
        if mode not in ('standard', '960'):
            mode = ''

    difficulty = ''
    while difficulty == '':
        difficulty = input("Choose engine difficulty between 1 and 8: ")
        if difficulty not in [1, 2, 3, 4, 5, 6, 7, 8]:
            difficulty = ''

    return (colour, mode, difficulty)


def print_welcome(colour, mode, difficulty):
    """Prints the welcoming message"""
    print("Welcome to Blindfold Chess Engine!")
    print("Made by Patrick Galea")
    print("The parameters you chose for this game are:")
    print(f"> Your colour: {'White' if colour == 'w' else 'Black'}")
    print(f"> Gamemode: {mode.capitalize()}")
    print(f"> Engine strength: {difficulty}")
    print("Type 'Start' to begin the game. Type in your move using modern")
    print("chess notation, and the engine's move will be printed back out.")
    print("Good luck!\n")


def print_interface(help=False):
    """Prints the interactive interface, and receives a command from user"""
    if help:
        print("start: Starts the game")
        return
    print("Input a command. Type 'help' for all commands.")
    command = input(">> ")


def main():
    colour, mode, difficulty = get_input()
    board = engine.create_board()
    game_over = False

    print_welcome(colour, mode, difficulty)

    while not game_over:
        command = print_interface()
        moves = engine.get_legal_moves(board, colour)
        break


if __name__ == '__main__':
    main()
