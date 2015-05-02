import random
import board
import engine
import defs
from copy import copy, deepcopy

# This function starts a Multiplayer game of Connect 4.
def multiplayer():
    defs.cls()
    b = board.Board()
    b.display_board()

    while(b.winning() == defs.INFINITY):
        defs.human_play(b)
        print ""
        b.display_board()
        
    defs.print_winner(b.winning())

# This function starts a Singleplayer game of Connect 4.
def singleplayer(play_as, code):
    defs.cls()
    b = board.Board()
    eng = engine.Engine()
    b.display_board()

    if play_as == "X":
        AI_color = 1
    else:
        AI_color = -1

    while(b.winning() == defs.INFINITY):
        while(play_as == b.get_player()):
            defs.human_play(b)
            print ""
            b.display_board()

        if (b.winning() == defs.INFINITY):
            defs.AI_play(b, eng, AI_color)
            print ""
            b.display_board()

    defs.print_winner(b.winning())

# This function plays itself as a way of training the Neural Network.
def play_itself():
    defs.cls()
    b = board.Board()
    eng = engine.Engine()
    b.display_board()

    while(b.winning() == defs.INFINITY):
        defs.AI_play(b, eng, 1)
        print ""
        b.display_board()

        if (b.winning() == defs.INFINITY):
            defs.AI_play(b, eng, -1)
            print ""
            b.display_board()
    
    defs.print_winner(b.winning())
    defs.train(b)

def main():
    defs.cls()
    mode = ""
    while not("s" in mode or "m" in mode):
        try:
            mode = raw_input("Singleplayer, Multiplayer or Trainer? (s/m/t): ")
            assert (mode in ["s","m","t"])
        except AssertionError:
            print "Please type in (s/m/t).\n"

        if "s" in mode:
            code = -1
            defs.cls()
            while not (code in [1,2,3]):
                try:
                    code = int(raw_input(\
                        "There are three different AI's:\n" + \
                        "1 - Random Moves except for Immediate Threats \n" + \
                        "2 - Minimax with heuristically defined Scoring Weights \n" + \
                        "3 - Minimax with Machine Learning Scoring Weights \n\n" + \
                        "Pick one: "))

                    assert (code in [1,2,3])
                except AssertionError:
                    print "Please play an integer from 1 to 3!\n"
                except ValueError:
                    print "Please play an integer from 1 to 3!\n"
                except UnboundLocalError:
                    print "Please play an integer from 1 to 3!\n"

            player = ""
            defs.cls()
            while not("y" in player or "n" in player):
                try:
                    player = raw_input("Do you want to start playing? (y/n): ")
                    assert (player in ["y","n"])
                except AssertionError:
                    print "Please type in (y/n).\n"

            if player == "y":
                singleplayer("X", code)
            else:
                singleplayer("O", code)

        elif "m" in mode:
            multiplayer()

        elif "t" in mode:
            play_itself()

if __name__ == "__main__":
    main ()
