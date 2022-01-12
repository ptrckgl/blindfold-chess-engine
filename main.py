import sys
import os
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
    print(f"> Engine strength: {difficulty}\n")
    print("Type 'start' to begin the game. Note that this will resign all games in progress.")
    print("To move, use the command 'move' and type in your move using modern chess notation.")
    print("The computers move will be printed back out to you.")
    print("Good luck! :)")


def print_interface(cleared=False):
    """Prints the interactive interface, and receives a command from user"""
    # So after using 'clear', theres not an annoying blank line at the top of the command line!
    if not cleared:
        print("")

    print("Input a command. Type 'help' for a description of all available commands.")
    command = input(">> ").lower()
    while command not in ['help', 'start', 'playback', 'move', 'resign', 'exit', 'clear']:
        print("Error: Please input a valid command.")
        print("\nInput a command. Type 'help' for all commands.")
        command = input(">> ")

    return command


def main():
    playing = True

    while playing:
        colour, mode, difficulty = get_input()
        game_over = False
        game_started = False
        print_welcome(colour, mode, difficulty)
        berserk_board, gid = None, None
        command = ""

        while not game_over:
            command = print_interface(cleared=(command == 'clear'))

            if command == 'help':
                engine.command_help()

            elif command == 'clear':
                cls_function()

            elif command == 'exit':
                engine.command_exit(gid, berserk_board, game_started)
                game_over = True
                playing = False

            elif command == 'start':
                if game_started:
                    print("Error: Oops... You have already started the game!")
                    continue

                berserk_board, gid = engine.command_start(colour, mode, difficulty)
                game_started = True

            elif not game_started:
                print("Error: This command cannot be used until the game has started!")

            elif command == 'playback':
                engine.command_playback(gid, berserk_board)

            elif command == 'move':
                game_over = engine.command_move(gid, berserk_board, colour)

            elif command == 'resign':
                engine.command_resign(gid, berserk_board)
                game_over = True

        if not playing:
            break

        print("\nThe game is over. Thanks for playing!")
        print("The final playback of the game is as follows:\n")
        engine.command_playback(gid, berserk_board)
        if len(input("\nPress enter to exit, or input any character to play again: ")) == 0:
            sys.exit()
        cls_function()


if __name__ == '__main__':
    main()
