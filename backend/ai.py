import math
from .game import TicTacToe

MAX_DEPTH = 9  # enough to explore all meaningful lines

def minimax(state: TicTacToe,
            player: str,
            depth: int = 0,
            alpha: float = -math.inf,
            beta: float = math.inf):
    max_player = 'O'
    other = 'X' if player == 'O' else 'O'

    # 1) terminal win
    if state.current_winner == other:
        # quicker wins are better
        score = (MAX_DEPTH - depth + 1)
        return {
            'position': None,
            'score': score if other == max_player else -score
        }

    # 2) reached depth cap => draw
    if depth >= MAX_DEPTH:
        return {'position': None, 'score': 0}

    # 3) no moves => draw
    moves = state.available_moves()
    if not moves:
        return {'position': None, 'score': 0}

    # initialize best
    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}

    for move in moves:
        # simulate move (no auto-clear in simulation)
        state.make_move(move, player, simulate=True)
        sim = minimax(state, other, depth + 1, alpha, beta)

        # undo simulation
        state.board[move] = " "
        state.current_winner = None
        if state.history[player]:
            state.history[player].pop()

        sim['position'] = move

        # alpha-beta pruning
        if player == max_player:
            if sim['score'] > best['score']:
                best = sim
            alpha = max(alpha, sim['score'])
        else:
            if sim['score'] < best['score']:
                best = sim
            beta = min(beta, sim['score'])

        if beta <= alpha:
            break

    return best
