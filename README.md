# Blindfold Chess Engine

### Introduction

The aim of this project is to allow you to play chess on the Lichess website... Through the command line. The purpose of this project was for myself to practice reading online documentation (boring), and to help improve blindfold visualisation ability whilst playing chess (fun). You can also play entirely through the command line without needing to log into Lichess, by entering chess moves in modern algebraic notation. Enjoy!

### Complete Before Using

- Run 'pip install berserk', 'pip install chess' and 'pip install interruptingcow' on your command line.
- You must create a Lichess account before using this program.
- You must create an API token for your Lichess account, which can be achieved by selecting your account name (top right) -> 'Preferences' -> 'API access tokens' -> Large Blue '+'. Name your access token, and select the two options 1. 'Send, accept and reject challenges' and 2. 'Play games with the board API'. After clicking 'submit', you will see a personal access token which will only be shown ONCE. Complete the next step before exiting this page.
- Create an environment variable on your linux terminal named 'LICHESS_TOKEN' which is equal to the personal access token you have previously created. I would recommend putting this inside of your ~/.bashrc file.

### Important Notes

- At this moment in time, all games created have no time limit, and are always against the Lichess Bot (From level 1 to 8)
- On occasion, after making a move it seems like there was no response from the server. In this case, press enter to give the terminal a 'nudge' and it should return the computer's move as normal.

### Usage/Commands

- Usage: 'python3 main.py [default]'. Including the 'default' argument automatically assigns game parameters, being {'colour': 'white', 'mode': 'standard', 'difficulty': 1}. If the 'default' argument is left out, the user will be able to choose these values.
- Available commands can be seen using by typing 'help' once the program has been envoked, and game parameters have been assigned.
- The 'move' command is how you play the game - by first typing 'move' into the command line, followed by your move in algebraic notation. Note, if you insert a move which is not legal, you will be asked to insert another move. Typing 'back' will cancel your move, where you can insert any command and continue as usual.
