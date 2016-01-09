import unittest
import game_logic as gl

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_game_invalid_input(self):
        """It should throw an error if the number of players is < 2 or > 6."""
        test_nums = (0, 1, 7)
        for num in test_nums:
            self.assertRaises(ValueError, gl.ConnectMore, num)

    def test_create_game(self):
        """It should create a game with a board size appropriate for the number of players specified."""

        num_players = [2, 3, 4, 5, 6]
        widths = [6, 9, 9, 10, 12]
        heights = [6, 6, 8, 9, 9]

        for i in list(range(len(num_players))):
            game = gl.ConnectMore(num_players[i])
            self.assertEqual(num_players[i], game.num_players)
            self.assertEqual(widths[i], game.width)
            self.assertEqual(heights[i], game.height)
            self.assertEqual(num_players[i] * game.TURNS_PER_PLAYER, game.empty_squares)
            self.assertEqual(1, game.current_player)
            self.assertEqual(num_players[i], len(game.scores))
            self.assertEqual(0, sum(game.scores))

            #don't test 'private' variables like _squares
            #but do check there's the right number of columns
            self.assertRaises(ValueError, game.play, game.width + 1)
            self.assertEqual(None, game.play(game.width))

    def test_play(self):
        """It should update the game state as follows:

        1. place the current player's token in the first empty row of the column
        2. update the number of empty squares remaining
        3. update the current player to the next player
        4. update the game score
        """
        game = gl.ConnectMore(2)

        game.play(4)
        self.assertEqual(1, game._squares[0][3])
        self.assertEqual(35, game.empty_squares)
        self.assertEqual(2, game.current_player)

        game.play(4)
        self.assertEqual(2, game._squares[1][3])
        self.assertEqual(34, game.empty_squares)
        self.assertEqual(1, game.current_player)

        #score updated?
        game.play(5)
        game.play(5)
        self.assertEqual([0, 0], game.scores)
        game.play(6)
        self.assertEqual([1, 0], game.scores)
        game.play(6)
        self.assertEqual([1, 1], game.scores)

    def test_play_full_column(self):
        """It should throw an error if playing in a column that's already full."""
        game = gl.ConnectMore(2)
        game.play(1)
        game.play(1)
        game.play(1)
        game.play(1)
        game.play(1)
        game.play(1)

        self.assertRaises(gl.FullColumnError, game.play, 1)

    def test_play_update_scores(self):
        """It should update the score of a game based on the length of token chain
        created by the last token.

        NOTE: any token can create a chain by either extending an existing chain
        (which can be as short as 1), or joining two previous chains. In either
        case, the score should be updated to include the value for the resulting
        chain length, but removing the value of the previous chain lengths.
        This can be fundamentally tested for all possible combinations by
        joining two chains of 3 (smallest scoring chain) to form 1 chain of 7
        for any direction (sideways, updown, diagonal)... well, at least enough
        for my confidence level that it's working ;)
        """
        game = gl.ConnectMore(2)
        # fudge the game state to test the update logic
        game.width = 8
        game.height = 8
        game._squares = [
            [1, 2, 2, 2, 0, 2, 2, 2], #this is actually the bottom row
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        game.scores = [game.CHAIN_LENGTH_SCORE[6], game.CHAIN_LENGTH_SCORE[3] *2]
        self.assertEqual([5, 2], game.scores)

        game.play(1)
        self.assertEqual([8, 2], game.scores)

        game.play(5)
        self.assertEqual([8, 8], game.scores)

        game.play(1)
        self.assertEqual([13, 8], game.scores)

    def test_game_over(self):
        """It should throw a GameOverError when all squares are full."""
        game = gl.ConnectMore(4)

        for row in list(range(game.height)):
            for col in list(range(1, game.width + 1)):
                game.play(col)

        self.assertEqual(0, game.empty_squares)
        self.assertRaises(gl.GameOverError, game.play, 4)

        #may as well check diagonal scores while I'm here...
        points = game.CHAIN_LENGTH_SCORE
        expected_scores = [
            points[5] + points[8] + points[4],
            points[6] + points[7] + points[3],
            points[3] + points[7] + points[6],
            points[4] + points[8] + points[5]
        ]
        self.assertEqual(expected_scores, game.scores)

    def test_get_leaders(self):
        """It should return a list of the player(s) with the top score."""
        game = gl.ConnectMore(6)
        test_scores = [
            [5, 3],
            [4, 6, 5, 6]
        ]
        expected_leaders = [
            [1],
            [2, 4]
        ]

        for index, test in enumerate(test_scores):
            game.scores = test
            result = game.get_leaders()
            self.assertEqual(expected_leaders[index], result)

    def test_eq(self):
        """It should return true if all the state values of 2 games is equal."""
        game1 = gl.ConnectMore(2)
        game2 = gl.ConnectMore(2)
        self.assertEqual(game1, game2)
        game1.play(1)
        self.assertNotEqual(game1, game2)
        game2.play(1)
        self.assertEqual(game1, game2)

    def test_clone(self):
        """It should create a deep copy of the entire game."""
        game1 = gl.ConnectMore(2)
        game1.play(1)
        game2 = game1.clone()
        game2.play(2)
        self.assertNotEqual(game1, game2)
        game1.play(2)
        self.assertEqual(game1, game2)

    def test_undo_nothing(self):
        """It should do nothing if there's nothing to undo."""
        game = gl.ConnectMore(2)
        game.undo()
        self.assertTrue(True)

    def test_undo(self):
        """It should restore the game to the state it was in before the last play."""

        # Create a game board with an interesting mix of chains to test undos.
        plays = [1, 1,
                1, 1,
                1, 2,
                2, 2,
                2, 2,
                1, 2,
                3, 3,
                5, 4,
                5, 6,
                4, 4,
                4, 4,
                4, 6,
                5, 6,
                6, 5,
                5, 6,
                6, 5,
                3, 3,
                3, 3
                ]

        previous_states = []
        game = gl.ConnectMore(2)

        for i, col in enumerate(plays):
            previous_states.append(game.clone())
            game.play(col)
            self.assertNotEqual(previous_states[i], game)


        for i, col in enumerate(plays):
            game.undo()
            self.assertEqual(previous_states[-1], game)
            previous_states.pop()

if __name__ == '__main__':
    unittest.main()
