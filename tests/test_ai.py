import unittest
from backend.game import TicTacToe
from backend.ai import minimax

class TestAI(unittest.TestCase):
    def test_ai_blocks_win(self):
        game = TicTacToe()
        game.board = ['X', 'X', ' ', ' ', 'O', ' ', ' ', ' ', 'O']
        game.current_winner = None
        move = minimax(game, 'O')['position']
        self.assertEqual(move, 2)  # Block X from winning

    def test_ai_takes_win(self):
        game = TicTacToe()
        game.board = ['O', 'O', ' ', 'X', 'X', ' ', ' ', ' ', ' ']
        game.current_winner = None
        move = minimax(game, 'O')['position']
        self.assertEqual(move, 2)  # Win move

if __name__ == '__main__':
    unittest.main()
