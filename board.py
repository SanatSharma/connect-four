from copy import copy, deepcopy
import random
import os 
import defs

random.seed()

class Board(object):
    """docstring for Board"""
    def __init__(self):
        super(Board, self).__init__()
        self.reset()
        self.states = [[0 for i in xrange(0, defs.NUM_FEATURES)]]
        self.num_states = 1

    def reset(self):
        b = ['.' for c in xrange(0,6)]
        self.cols = [copy(b) for c in xrange(0,7)]
        self.current_player = "X"
        self.fours = {"X": [], "O": []}
        self.init_fours()

    def init_fours(self):
        full_list = []
        # Add the verticals
        for row in xrange(0, 3):
            for col in xrange(0,7):
                full_list.append([(row, col), (row + 1, col), (row + 2, col), (row + 3, col)])
        # Add the horizontals
        for row in xrange(0, 6):
            for col in xrange(0, 4):
                full_list.append([(row, col), (row, col + 1), (row, col + 2), (row, col + 3)])
        # Add the up-rights
        for row in xrange(0, 3):
            for col in xrange(0, 4):
                full_list.append([(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)])
        # Add the up-lefts
        for row in xrange(3, 6):
            for col in xrange(0, 4):
                full_list.append([(row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)])
        self.fours["X"] = full_list
        self.fours["O"] = deepcopy(full_list)

    def cannot_play_in(self, col):
        return not ('.' in self.cols[col])

    def get_player(self):
        return self.current_player

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def other_player(self):
        if self.current_player == "X":
            return "O"
        else:
            return "X"

    def lowest_available(self, col):
        for i, sq in enumerate(self.cols[col]):
            if sq == '.':
                return i

    def directly_playable(self, row, col):
        return self.lowest_available(col) == row

    def filled(self, row, col):
        return self.cols[col][row] != "."

    def open(self, row, col):
        return not self.filled(row, col)

    def open_in_four(self, four):
        return [sq for sq in four if self.open(*sq)]

    # 1-indexed cols
    def play(self, col):
        assert 0 <= col < 7
        if (not self.cannot_play_in(col)):
            row = self.lowest_available(col)
            self.cols[col][row] = self.current_player
            #print len(self.fours["O"])
            self.remove_fours(col, row)
            #print len(self.fours["O"])
            self.switch_player()
            self.num_states += 1
        else:
            raise ValueError("ColumnFull")

    def remove_fours(self, col, row):
        iterlist = copy(self.fours[self.other_player()])
        for four in iterlist:
            # print ((row, col) in four)
            if (row, col) in four:
                # print "remove " + str(four)
                self.fours[self.other_player()].remove(four)
        # print self.fours[other_player]

    def transpose(self, l):
        # http://stackoverflow.com/a/11387441/2228485
        return [list(i) for i in zip(*l)]

    def display_board(self):
        # mutability makes this more difficult than it probably should be
        # Copy self.cols. Reverse every column
        col_copy = deepcopy(self.cols)
        for c in col_copy:
            c.reverse()
        for r in self.transpose(col_copy):
            print "{} {} {} {} {} {} {}".format(*r)

    def copy_board(self):
        return deepcopy(self.cols)

    def play_random(self):
        x = random.randint(0,6)
        while (self.cannot_play_in(x)):
            x = random.randint(0,6)
        self.play(x)

    # Heuristics/Features
    # Normalized such that best case for X => 1, best case for 0 => -1
    def fours_left(self):
        return 2 * len(self.fours["X"])/69. - 1

    def fours_left_opponent(self):
        return 2 * (1 - len(self.fours["O"])/69.) - 1

    # This should be normalized to something better I think...
    def fours_difference(self):
        return 2 * (len(self.fours["X"]) - len(self.fours["O"]))/69. - 1

    # A helper function.
    def how_many_in(self, four, player):
        tally = 0
        for (row, col) in four:
            if self.cols[col][row] == player:
                tally += 1
        return tally

    # A helper function.
    def some_in_a_row(self, n, player):
        ns = 0
        for f in self.fours[player]:
            if self.how_many_in(f, player) >= n:
                ns += 1
        if player == "X":
            return 2 * ns/69. - 1
        else: # player == "O"
            return 2 * (1 - ns/69.) - 1

    # More heuristics/features.
    def important_threes(self):
        return self.some_in_a_row(3, "X")

    def important_threes_opponent(self):
        return self.some_in_a_row(3, "O")

    def important_threes_difference(self):
        return self.important_threes() - self.important_threes_opponent()

    def important_twos(self):
        return self.some_in_a_row(2, "X")

    def important_twos_opponent(self):
        return self.some_in_a_row(2, "X")

    def important_twos_difference(self):
        return self.important_twos() - self.important_twos_opponent()

    def present_in(self):
        return self.some_in_a_row(1, "X")

    def opponent_present_in(self):
        return self.some_in_a_row(1, "O")

    def presence_difference(self):
        return self.present_in() - self.opponent_present_in()

    def x_odd_threats(self):
        odd_threat = False
        for f in self.fours["X"]:
            if self.how_many_in(f, "X") == 3:
                for (row, col) in f:
                    if (self.cols[col][row] == ".") and row % 2 == 0:
                        return 1
        return 0

    def zugzwang(self):
        if self.x_odd_threats():
            "X"
        else:
            "O"


# THINGS I ADDED/CHANGED

    def update_features(self):
        self.states.append([self.important_threes(), 
                       self.important_threes_opponent(), 
                       self.important_threes_difference(), 
                       self.important_twos(), 
                       self.important_twos_opponent(), 
                       self.present_in(), 
                       self.opponent_present_in(), 
                       self.presence_difference(), 
                       self.x_odd_threats()])

    def get_features(self):
        return self.states

    def get_numstates(self):
        return self.num_states

    def get_score(self, machine_weights):
        for four in self.fours["O"]:
            if (self.cols[(four[0])[1]][(four[0])[0]] == 
                self.cols[(four[1])[1]][(four[1])[0]] == 
                self.cols[(four[2])[1]][(four[2])[0]] == 
                self.cols[(four[3])[1]][(four[3])[0]] == 
                "O"):
                return - defs.INFINITY

        for four in self.fours["X"]:
            if (self.cols[(four[0])[1]][(four[0])[0]] == 
                self.cols[(four[1])[1]][(four[1])[0]] == 
                self.cols[(four[2])[1]][(four[2])[0]] == 
                self.cols[(four[3])[1]][(four[3])[0]] == 
                "X"):
                return defs.INFINITY

        output = 0.0
        curr_state = [self.important_threes(), 
                       self.important_threes_opponent(), 
                       self.important_threes_difference(), 
                       self.important_twos(), 
                       self.important_twos_opponent(), 
                       self.present_in(), 
                       self.opponent_present_in(), 
                       self.presence_difference(), 
                       self.x_odd_threats()]

        if machine_weights:
            coeffso = 0.0
            for i in xrange(defs.NUM_HIDDEN):
                aux = 0.0
                coeffsh = 0.0
                for j in xrange(defs.NUM_FEATURES):
                    aux += curr_state[j] * defs.init_hweights[i][j]
                    coeffsh += defs.init_hweights[i][j]
                output += defs.sigmoid(aux/coeffsh) * defs.init_oweight[i]
                coeffso += defs.init_oweight[i]
            return output / coeffso
        
        else:
            coeffs = 0.0
            for i in xrange(defs.NUM_FEATURES):
                output += curr_state[i] * defs.human_weights[i]
                coeffs += defs.human_weights[i]
            return output / coeffs

    def winning(self):
        if (self.cannot_play_in(0) and \
            self.cannot_play_in(1) and \
            self.cannot_play_in(2) and \
            self.cannot_play_in(3) and \
            self.cannot_play_in(4) and \
            self.cannot_play_in(5) and \
            self.cannot_play_in(6)):
            return 0
        for four in self.fours["O"]:
            if (self.cols[(four[0])[1]][(four[0])[0]] == 
                self.cols[(four[1])[1]][(four[1])[0]] == 
                self.cols[(four[2])[1]][(four[2])[0]] == 
                self.cols[(four[3])[1]][(four[3])[0]] == 
                "O"):
                return -1

        for four in self.fours["X"]:
            if (self.cols[(four[0])[1]][(four[0])[0]] == 
                self.cols[(four[1])[1]][(four[1])[0]] == 
                self.cols[(four[2])[1]][(four[2])[0]] == 
                self.cols[(four[3])[1]][(four[3])[0]] == 
                "X"):
                return 1
        return defs.INFINITY

    def playable(self):
        lst = []
        for i in xrange(0,7):
            if not self.cannot_play_in(i):
                lst.append(i)
        return lst
