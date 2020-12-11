Hi, and welcome to my chess engine!
Here is a guide on how to run the chess program through the command line/terminal:

In order to run the chess.py module, you'll need to first install python3 and pygame from the terminal
install python3: from the internet, from PowerShell in Windows, from the terminal.
install pygame: from any terminal, type "pip install pygame".

Running chess.py through the terminal:
--> python3 chess.py <(~optional) choice> <(~optional) board_state> <--

The choice determines whether or not you will play against the AI or another player.
The current implementation of the AI class only makes random moves each turn; to be updated.
choice default: "0" (sets the black player as a human)
choice other: Anything other than "0" currently sets the black player to the AI.

The board_state determines the starting state of the board when the game is loaded.
All of the available states can be viewed in the "States" folder. 
The state parameter will default to the regular chess opening if given no input.
Besides the default chess board state, ten of the most common chess openings have been provided.
In the current implementation, 
you must give a choice parameter in order to manually set the starting state.

*You may save the current state of the board at any time by pressing (CTRL + S).
*Currently only one state can be saved manually under the name "new_state.txt".
*If you wish to save several states at once, 
*you'll have to manually change the name of the new_state file before saving another state.

In addition to the state file, a log file will be saved after each game, showing the order of moves
that was played and on what turns.
The log file is not overwritten, only added to, so it isn't necessary to change the log file's name
after each game unless you'd like to save a certain game under a particular name.

Enjoy and have fun!