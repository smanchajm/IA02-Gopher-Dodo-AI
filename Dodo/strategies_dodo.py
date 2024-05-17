""" Module contenant les différentes stratégies pour le jeu Dodo """
import random
from Game_playing.structures_classes import *

Strategy = Callable[[Environment, Player, Grid], Action]


def strategy_first_legal_dodo(env: Environment, player: Player, grid: Grid) -> Action:
    return env.legals_dodo(grid, player)[0]


def strategy_random_dodo(env: Environment, player: Player, grid: Grid) -> Action:
    return random.choice(env.legals_dodo(grid, player))


# Minimax Strategy (sans cache)
def minmax_action(env: Environment, player: Player, grid: Grid, depth: int = 0) -> tuple[float, Action]:
    if depth == 0 or env.final_dodo(grid) != 0:
        return env.final_dodo(grid), (-1, -1)  # On retourne le score de la grille

    if player == env.max_player:  # maximazing player
        best = (float("-inf"), (-1, -1))
        for item in env.legals_dodo(grid, player):
            tmp = env.play_dodo(player, grid, item)
            returned_values = minmax_action(env, env.min_player, tmp, depth - 1)
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best

    if player == env.min_player:  # minimizing player
        best = (float("inf"), (-1, -1))
        for item in env.legals_dodo(grid, player):
            tmp = env.play_dodo(player, grid, item)
            returned_values = minmax_action(env, env.max_player, tmp, depth - 1)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best

def minmax_action_with_alpha_beta_pruning(env: Environment, player: Player, grid: Grid, depth: int = 0) -> tuple[float, Action]:
    def minmax_alpha_beta(env: Environment, player: Player, grid: Grid, depth: int, alpha: float, beta: float) -> tuple[float, Action]:
        if depth == 0 or env.final_dodo(grid) != 0:
            return env.final_dodo(grid), (-1, -1)  # On retourne le score de la grille

        if player == env.max_player:  # maximazing player
            best = (float("-inf"), (-1, -1))
            for item in env.legals_dodo(grid, player):
                tmp = env.play_dodo(player, grid, item)
                returned_values = minmax_alpha_beta(env, env.min_player, tmp, depth - 1, alpha, beta)
                if max(best[0], returned_values[0]) == returned_values[0]:
                    best = (returned_values[0], item)
                alpha = max(alpha, best[0])
                if beta <= alpha:
                    break
            return best

        if player == env.min_player:  # minimizing player
            best = (float("inf"), (-1, -1))
            for item in env.legals_dodo(grid, player):
                tmp = env.play_dodo(player, grid, item)
                returned_values = minmax_alpha_beta(env, env.max_player, tmp, depth - 1, alpha, beta)
                if min(best[0], returned_values[0]) == returned_values[0]:
                    best = (returned_values[0], item)
                beta = min(beta, best[0])
                if beta <= alpha:
                    break
            return best

    return minmax_alpha_beta(env, player, grid, depth, float("-inf"), float("inf"))

def strategy_minmax(env: Environment, player: Player, grid: Grid, ) -> Action:
    # return minmax_action(env, player, grid, 4)[1]
    return minmax_action_with_alpha_beta_pruning(env, player, grid, 6)[1]
