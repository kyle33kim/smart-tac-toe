import unittest
from backend.game import TicTacToe

class TestGame(unittest.TestCase):
    def test_board_starts_empty(self):
        game = TicTacToe()
        self.assertTrue(all(cell == " " for cell in game.board))

    def test_make_valid_move(self):
        game = TicTacToe()
        result = game.make_move(0, 'X')
        self.assertTrue(result)
        self.assertEqual(game.board[0], 'X')

    def test_make_invalid_move(self):
        game = TicTacToe()
        game.make_move(0, 'X')
        result = game.make_move(0, 'O')  # Try to move in same spot
        self.assertFalse(result)
        self.assertEqual(game.board[0], 'X')  # Should still be 'X'

    def test_winner_horizontal(self):
        game = TicTacToe()
        game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        game.current_winner = None
        self.assertTrue(game.check_winner(0, 'X'))

    def test_winner_diagonal(self):
        game = TicTacToe()
        game.board = ['O', ' ', ' ', ' ', 'O', ' ', ' ', ' ', 'O']
        game.current_winner = None
        self.assertTrue(game.check_winner(0, 'O'))

if __name__ == '__main__':
    unittest.main()
