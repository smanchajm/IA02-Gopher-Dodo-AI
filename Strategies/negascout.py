""" Minimax with NegaScout algorithm """
from cmath import inf
from copy import deepcopy

from Game_playing.structures_classes import (
    Action,
    Environment, PlayerLocal
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



