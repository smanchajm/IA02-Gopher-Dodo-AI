""" Minimax with NegaScout algorithm """
import time
from cmath import inf
from copy import deepcopy

from Game_playing.structures_classes import (
    Action,
    Environment, PlayerLocal, ALL_DIRECTIONS, GameGopher, new_gopher
)

from strategies import evaluate_dynamic, strategy_minmax


class NegaScoutEngine:
    """ NegaScout Engine """
    def __init__(self, board: Environment, depth: int):
        self.board = board
        self.depth = depth

    def negascout(self, alpha, beta, depth, player):
        """ NegaScout algorithm """
        best = -float('inf')
        b = beta

        if depth == 0:
            return evaluate_dynamic(self.board, self.board.grid, player)

        opponent = self.board.min_player if player == self.board.max_player \
                                            else self.board.max_player

        legal_moves = self.board.legals(player)
        if not legal_moves:  # Pas de coups légaux possibles
            # Ou retournez une valeur appropriée
            return evaluate_dynamic(self.board, self.board.grid, player)

        first_move = True

        for move in legal_moves:
            self.board.play(move)
            score = -self.negascout(-b, -alpha, depth - 1, opponent)

            if score > best:
                if alpha < score < beta and not first_move:  # Principal Variation
                    best = max(score, best)
                else:
                    best = -self.negascout(-beta, -score, depth - 1, opponent)

            self.board.reverse_action(move)
            alpha = max(score, alpha)
            if alpha >= beta:
                return alpha

            b = alpha + 1
            first_move = False

        return best

    def get_move(self, player: PlayerLocal) -> Action:
        """
        Gets the best move for the player for given current grid.
        """

        self.board.grid = deepcopy(self.board.grid)
        legals = self.board.legals(player)
        opponent = self.board.min_player if player == self.board.max_player \
                                            else self.board.max_player
        best = -inf
        best_move = legals[0]

        for move in legals:
            self.board.play(move)
            score = -self.negascout(-inf, inf, self.depth, opponent)

            if score > best:
                best = score
                best_move = move

            self.board.reverse_action(move)

        return best_move



def main():
    """
    Main function
    """
    init_grid = new_gopher(4)


    # Creation of the board
    player_param: PlayerLocal = PlayerLocal(1, ALL_DIRECTIONS)
    player_opponent: PlayerLocal = PlayerLocal(2, ALL_DIRECTIONS)
    game = GameGopher(
        init_grid,
        player_param,
        player_opponent,
        player_param,
        4,
        300,
        0,
        init_grid,
        "Gopher",
    )

    # best move with NegaScout
    start = time.time()
    best_move = strategy_minmax(game, player_param)
    print(f"Best move alpha: {best_move}")
    print(f"Time: {time.time() - start}")


    engine = NegaScoutEngine(game, 7)
    start = time.time()
    best_move = engine.get_move(player_param)
    print(f"Best move nega: {best_move}")
    print(f"Time: {time.time() - start}")




if __name__ == '__main__':
    main()
