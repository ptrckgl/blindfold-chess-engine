import sys
import os
from types import prepare_class
import engine


DEFAULT_COLOUR = "white"
DEFAULT_MODE = "standard"
DEFAULT_DIFFICULTY = 1


def cls_function():
    """Clears the screen in the command prompt."""
    # os.name == 'nt' is checking for a microsoft OS
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input():
    """Obtains all user input, ensuring it is always valid"""
    if len(sys.argv) == 2 and sys.argv[1] == "default":
        return (DEFAULT_COLOUR, DEFAULT_MODE, DEFAULT_DIFFICULTY)

    elif len(sys.argv) >= 2:
        sys.exit("Usage: python3 main.py [default]")

    colour = ''
    while colour == '':
        colour = input("Input colour: 'white' or 'black': ")
        if colour not in ('white', 'black'):
            print("Error: Please choose a valid option.")
            colour = ''

    mode = ''
    while mode == '':
        mode = input("Choose mode: 'standard': ")
        if mode not in ('standard'):
            print("Error: Please choose a valid option.")
            mode = ''

    difficulty = ''
    while difficulty == '':
        difficulty = input("Choose engine difficulty between 1 and 8: ")
        if int(difficulty) not in [1, 2, 3, 4, 5, 6, 7, 8]:
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
    while command not in ['help', 'start', 'playback', 'move', 'resign', 'exit']:
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
    playing = True

    while playing:
        colour, mode, difficulty = get_input()
        game_over = False
        game_started = False
        print_welcome(colour, mode, difficulty)
        berserk_board, gid = None, None

        while not game_over:
            command = print_interface()

            if command == 'help':
                print("- start: Starts the game")
                print("- playback: Prints all moves which have been played so far")
                print("- move: Allows you to insert a move to play")
                print("- resign: Resign the game")
                print("- exit: Terminates the program")

            elif command == 'exit':
                if game_started:
                    engine.resign(gid, berserk_board, print_output=False)
                game_over = True
                playing = False

            elif command == 'start':
                if game_started:
                    print("Error: Oops... You have already started the game!")
                else:
                    berserk_board, gid = engine.start_game(colour, mode, difficulty)
                    if gid is not None:
                        game_started = True

                # Upon starting the game, if playing black, display the opponents first move
                if colour == 'black':
                    # While no move has been played yet
                    while '' in get_moves(gid, berserk_board).split(' '):
                        pass

                    print("Computer Move:",
                          engine.print_moves(get_moves(gid, berserk_board), return_first=True))

            elif not game_started:
                print("Error: This command cannot be used until the game has started!")

            elif command == 'playback':
                engine.print_moves(get_moves(gid, berserk_board))

            elif command == 'move':
                moves = get_moves(gid, berserk_board)
                move = input("Input Move: ")
                while not engine.make_move(move, moves, gid, berserk_board):
                    print("That move is invalid. Please make a valid move.")
                    move = input("Input Move: ")

                # Check if the game is over and display to user if so
                if engine.game_is_over(get_moves(gid, berserk_board)):
                    game_over = True
                    break

                # Wait until the computer has made a move, then print it back out to the user
                mod_val = {'white': 1, 'black': 0}
                while len(get_moves(gid, berserk_board).split(' ')) % 2 == mod_val[colour]:
                    pass
                print("Computer Move:",
                      engine.print_moves(get_moves(gid, berserk_board), return_last=True))

                # Check if the game is over and display to user if so
                if engine.game_is_over(get_moves(gid, berserk_board)):
                    game_over = True

            elif command == 'resign':
                engine.resign(gid, berserk_board)
                game_over = True

        if not playing:
            break

        print("\nThe game is over. Thanks for playing!")
        if len(input("Press enter to exit, or input any character to play again: ")) == 0:
            sys.exit()
        cls_function()


if __name__ == '__main__':
    main()
