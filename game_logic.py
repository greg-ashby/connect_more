import json
import copy

# Use a global variable to store copies of the previous state after each play.
#
# Note that this isn't a good idea - you couldn't use this on a real server
# to host multiple games for instance. But I reverted to this because using
# an instance variable was equally bad (or worse). Each call to play does:
#   1. clone the current instance
#   2. store the clone in history (makes 'undo' really simple to implement)
#
# So if history is an instance variable, it gets included in the cloning each
# time and re-stored in history as the 'history' of that copy. This means that
# each instance in history has it's own complete copy of the entire game's
# history up to that point! Each subsequent call to play() recopies every
# instance with their entire copy of history again, so history grows at an n^2
# rate. After about 10 calls to play(), it starts getting VERY slow... about
# 1 second to execute the 10th call, and doubles every play after that.
#
# TODO: To fix this, clone() needs to be changed to not re-copy history each
# time, and then history can be made an instance variable again.
history = []

class ConnectMore:

    TURNS_PER_PLAYER = 18
    WIDTHS = [6, 9, 9, 10, 12]
    HEIGHTS = [6, 6, 8, 9, 9]

    #initiate the value of each chain length with length 3=1, 4=2,
    #and everything else upto max dimensions as a 'fibonacci-ish' sequence
    CHAIN_LENGTH_SCORE = [0, 0, 0, 1, 2]
    for chain_length in range(5, max(WIDTHS)+1):
        CHAIN_LENGTH_SCORE.append(
            CHAIN_LENGTH_SCORE[chain_length-1] +
            CHAIN_LENGTH_SCORE[chain_length-2])

    def __init__(self, num_players):
        if num_players < 2 or num_players > 6:
            raise ValueError("Number of players must be between 2 and 6")

        #players are 1-based indexed, '0' in a square means it's empty
        self.current_player = 1
        self.num_players = num_players
        self.scores = [0 for player in range(self.num_players)]
        self.empty_squares = num_players * ConnectMore.TURNS_PER_PLAYER
        self.width = ConnectMore.WIDTHS[num_players - 2]
        self.height = ConnectMore.HEIGHTS[num_players - 2]

        self._squares = [
            [0 for each_column in list(range(self.width))]
            for each_row in list(range(self.height))
        ]

        #adding as an instance attribute so UIs can display leaderboard
        self.leaders = self.get_leaders()


    def play(self, col_num):
        """Drops the current player's 'Token' in the corresponding column.

        Throws an error if the column or row is invalid/full, or if the game
        is already over, returns nothing otherwise.

        NOTE: columns are numbered 1 to width, not 0 to width-1 (assuming
        players will input the number 1, 2, 3, etc, not 0, 1, 2, etc).
        """
        if(self.empty_squares <= 0):
            raise GameOverError()

        col_num -= 1
        if col_num >= self.width:
            raise ValueError("Invalid Column Number")

        history.append(self.clone())

        for row_num, row in enumerate(self._squares):
            #go through each row until there's an empty square in the column
            if row[col_num] == 0:
                row[col_num] = self.current_player
                self._update_scores(row_num, col_num)
                break
            if row_num == self.height - 1:
                raise FullColumnError()

        self.current_player = self.current_player % self.num_players + 1
        self.empty_squares -= 1

    def undo(self):
        """Reverts the game back to its prior state before the last play."""
        self.__dict__.update(history[-1].__dict__)
        history.pop()

    def _update_scores(self, row, col):
        """Updates the current score based on the last token played (at row, col).

        NOTE: this should not be called from outside the expected order in
        play method as it assumes this is a newly played token and only updates
        the score from that. It makes no effort to compute the correct score
        from the rest of board state.
        """

        #directions to check for chains from the last token played
        # each pair has a forward [0] and backward [1]
        directions = [
            [[0, 1], [0, -1]], #right and left
            [[1, 1], [-1, -1]], #diagonal
            [[1, 0], [-1, 0]], #up and down
            [[1, -1], [-1, 1]] #other diagonal
        ]

        def is_match(row, col, token):
            """Checks is a square is inside the board and contains a token."""
            if 0 <= row < self.height and 0 <= col < self.width:
                return token == self._squares[row][col]
            return False

        def get_chain_length(row, col, direction, count):
            """Recursively checks how long a chain of matching tokens is."""
            token = self._squares[row][col]
            next_row = row + direction[0]
            next_col = col + direction[1]
            if is_match(next_row, next_col, token):
                return get_chain_length(next_row, next_col, direction, count + 1)
            else:
                return count

        #algorithm:
        #for each direction to search
        #  determine the chain length forward from row, col
        #  determine the chain length backward from row, col
        #  subtract score for the previous chain lengths
        #  add score for new total length

        for direction in directions:
            forward_length = 0
            back_length = 0

            forward_length = get_chain_length(row, col, direction[0], 0)
            back_length = get_chain_length(row, col, direction[1], 0)

            self.scores[self.current_player-1] -= \
                self.CHAIN_LENGTH_SCORE[forward_length]
            self.scores[self.current_player-1] -= \
                self.CHAIN_LENGTH_SCORE[back_length]
            self.scores[self.current_player-1] += \
                self.CHAIN_LENGTH_SCORE[forward_length + back_length + 1]

        #update leaders so web UI doesn't need another ajax call when game over
        self.leaders = self.get_leaders()

    def get_leaders(self):
        """Returns the human-displayable player numbers with the highest scores
        i.e. players 1-6, not players 0-5.
        """
        top_score = max(self.scores)
        leaders = [i+1 for i, x in enumerate(self.scores) if x == top_score]
        return leaders

    def __repr__(self):
        token = lambda x: " " if x == 0 else str(x)
        score = lambda p, n: "Player " + str(p+1) + ": " + str(n)

        result = "Cols: "
        result += ' | '.join([str(n+1) for n in range(self.width)])
        result += " |\n"
        result += ''.join(["----" for n in range(self.width + 1)])
        result += "\n"

        for row in reversed(self._squares):
            result += "    | "
            result += ' | '.join([token(n) for n in row])
            result += " |\n"

        result += ''.join(["----" for n in range(self.width + 1)])
        result += "\n"

        result += "SCORES: "
        result += '\n\t'.join([score(p, n) for p, n in enumerate(self.scores)])
        result += "\n"
        return result

    def to_json(self):
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def clone(self):
        return copy.deepcopy(self)

class FullColumnError(Exception):
    pass

class GameOverError(Exception):
    pass

if __name__ == '__main__':
    game1 = ConnectMore(2)
    print(game1)
