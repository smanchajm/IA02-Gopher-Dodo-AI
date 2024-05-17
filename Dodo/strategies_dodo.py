""" Module contenant les différentes stratégies pour le jeu Dodo """

import random
from Game_playing.classes import *
Strategy = Callable[[Environment, Player,Grid], Action]


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


def strategy_minmax(env: Environment, player: Player, grid: Grid,) -> Action:
    return minmax_action(env, player, grid, 3)[1]
