""" Module contenant les différentes stratégies pour le jeu Dodo """

from cmath import log
import random
from typing import Any, Callable, Dict, Tuple

from Dodo.grid import INIT_GRID
from Game_playing.structures_classes import (Action, Cell, Environment, Grid,
                                             GridDict, Player)

Strategy = Callable[[Environment, Player, Grid], Action]

def strategy_first_legal_dodo(env: Environment, player: Player, grid: Grid) -> Action:
    """
    Stratégie qui retourne la première action légale calculée
    """
    return env.legals_dodo(grid, player)[0]


def strategy_first_legal_gopher(
    env: Environment,
    player: Player,
    grid: GridDict,
) -> Action:
    """
    Stratégie qui retourne la première action légale calculée
    """
    return env.legals_gopher(grid, player)[0]


def strategy_random_gopher(
    env: Environment,
    player: Player,
    grid: GridDict,
) -> Action:
    """
    Stratégie qui retourne une action légale aléatoire
    """
    return random.choice(env.legals_gopher(grid, player))


def strategy_random_dodo(
    env: Environment,
    player: Player,
    grid: Grid,
) -> Action:
    """
    Stratégie qui retourne une action légale aléatoire
    """
    return random.choice(env.legals_dodo(grid, player))


def is_near_edge(cell: Cell, grid_height: int, grid_width: int) -> bool:
    """
    Déterminer si une cellule est proche du bord de la grille
    """
    return (
        cell[0] == 0
        or cell[0] == grid_height - 1
        or cell[1] == 0
        or cell[1] == grid_width - 1
    )


def evaluate_dynamic(env: Environment, grid: Grid, player: Player) -> int:
    """
    Fonction d'évaluation pour le jeu Dodo avec une récompense dynamique pour la proximité du bord
    """
    opponent = env.min_player if player == env.max_player else env.max_player

    player_moves = len(env.legals_dodo(grid, player))
    opponent_moves = len(env.legals_dodo(grid, opponent))

    player_score = 0
    opponent_score = 0

    grid_height = len(grid)
    grid_width = len(grid[0])

    for i in range(grid_height):
        for j in range(grid_width):
            cell = grid[i][j]
            if cell == player.id:
                player_score -= 40  # Pénalité pour avoir une pièce
                player_score -= 80 * player_moves  # Pénalité ajustée pour la mobilité
                if is_near_edge((i, j), grid_height, grid_width):
                    player_score += 40 - distance_to_edge(
                        (i, j), grid_height, grid_width
                    )  # Récompense dynamique pour la proximité du bord
            elif cell == opponent.id:
                opponent_score += 40  # Récompense pour avoir une pièce
                opponent_score += (
                    80 * opponent_moves
                )  # Récompense ajustée pour la mobilité
                if is_near_edge((i, j), grid_height, grid_width):
                    # Pénalité dynamique pour l'adversaire près du bord
                    opponent_score -= 40 - distance_to_edge(
                        (i, j), grid_height, grid_width
                    )
    
    return player_score - opponent_score


def distance_to_edge(cell: Cell, grid_height: int, grid_width: int) -> int:
    """
    Calculer la distance minimale d'une cellule aux bords de la grille
    """
    return min(cell[0], grid_height - 1 - cell[0], cell[1], grid_width - 1 - cell[1])


def minmax_action_alpha_beta_pruning(
    env: Environment, player: Player, grid: Grid, depth: int = 0
) -> tuple[float, Action]:
    """
    Stratégie qui retourne le résultat de l'algorithme Minimax avec élagage Alpha-Beta
    et memoization pour le jeu Dodo
    """
    memo = {}  # Closure

    def minmax_alpha_beta_pruning(
        env: Environment,
        player: Player,
        grid: Grid,
        depth: int,
        alpha: float,
        beta: float,
    ) -> tuple[float, Action]:
        
        # Convert grid to a tuple, so it can be used as a key in the dictionary
        grid_key = grid
        player_id = player.id  # Use a unique identifier for the player

        if (grid_key, player_id) in memo:
            return memo[(grid_key, player_id)]

        # Si la profondeur est nulle ou si la partie est terminée
        res = env.final_dodo(grid)

        if res != 0:
            if res == 1:
                score = 10000
            else:
                score = -10000
            # score = env.final_dodo(grid)
            memo[(grid_key, player_id)] = (score, (-1, -1))
            return score, (-1, -1)
        if depth == 0:
            score = evaluate_dynamic(env, grid, player)
            memo[(grid_key, player_id)] = (score, (-1, -1))
            return score, (-1, -1)

        if player == env.max_player:  # Maximizing player
            best_max: tuple[float, Action] = (float("-inf"), (-1, -1))
            for action in env.legals_dodo(grid, player):
                tmp = env.play_dodo(player, grid, action)
                returned_values = minmax_alpha_beta_pruning(
                    env, env.min_player, tmp, depth - 1, alpha, beta
                )
                if returned_values[0] > best_max[0]:
                    best_max = (returned_values[0], action)
                alpha = max(alpha, best_max[0])
                if beta <= alpha:
                    break
            memo[(grid_key, player_id)] = best_max
            return best_max

        if player == env.min_player:  # Minimizing player
            best_min: tuple[float, Action] = (float("inf"), (-1, -1))
            for item in env.legals_dodo(grid, player):
                tmp = env.play_dodo(player, grid, item)
                returned_values = minmax_alpha_beta_pruning(
                    env, env.max_player, tmp, depth - 1, alpha, beta
                )
                if returned_values[0] < best_min[0]:
                    best_min = (returned_values[0], item)
                beta = min(beta, best_min[0])
                if beta <= alpha:
                    break
            memo[(grid_key, player_id)] = best_min
            return best_min
        return 0, (-1, -1)

    return minmax_alpha_beta_pruning(
        env, player, grid, depth, float("-inf"), float("inf")
    )


def strategy_minmax(
    env: Environment, player: Player, grid: Grid
) -> Action:
    """
    Stratégie qui retourne l'action calculée par l'algorithme Minimax
    """
    try:
        depth_factor = 1/(log(len(env.legals_dodo(grid, player)), 2) / 5) * 1.2
    except ZeroDivisionError:
        depth_factor = 1
    depth_factor = depth_factor.real # convert depth factor to a float
    # print(f"Depth factor: {depth_factor}")

    depth = min(2 + round(depth_factor), 9)
    # print(f"Depth: {depth}")

    return minmax_action_alpha_beta_pruning(env, player, grid, depth)[1]


def is_first_move(env: Environment, grid: Grid) -> bool:
    """
    Déterminer si le premier coup a été joué
    """
    return env.nb_moves == 0


def strategy_botte_secrete(
   env: Environment, player: Player, grid: Grid, starting_library: dict = None) -> Action:
    """
    Stratégie qui copie les mouvements de l'adversaire pour les 100 premiers coups et joue ensuite avec l'algorithme Minmax
    """
    if is_first_move(env, grid):
        return strategy_minmax(env, player, grid)
    if env.nb_moves < 100:
        action = env.precedent_action
        action = ((len(grid) - 1 - action[0][0], len(grid[0]) - 1 - action[0][1]), (len(grid) - 1 - action[1][0], len(grid[0]) - 1 - action[1][1]))
        return action
    return strategy_minmax(env, player, grid)
