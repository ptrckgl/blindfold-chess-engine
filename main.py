import sys


DEFAULT_COLOUR = "w"
DEFAULT_MODE = "standard"


def get_input():
    """Obtains all user input, ensuring it is always valid"""
    if len(sys.argv) == 2 and sys.argv[1] == "default":
        return (DEFAULT_COLOUR, DEFAULT_MODE)
    
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

    return (colour, mode)


def main():
    colour, mode = get_input()
    print(colour, mode)


if __name__ == '__main__':
    main()
