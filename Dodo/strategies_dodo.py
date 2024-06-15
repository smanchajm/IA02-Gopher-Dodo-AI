""" Module contenant les différentes stratégies pour le jeu Dodo """
from cmath import log
import random
from typing import Callable

from Game_playing.structures_classes import (
    Action,
    Cell,
    Environment,
    Grid,
    GridDict,
    PlayerLocal,
)

StrategyLocal = Callable[[Environment, PlayerLocal], Action]

# Define a type alias for the memoization key
MemoKey = tuple[GridDict, int]


def strategy_first_legal(
    env: Environment,
    player: PlayerLocal,
) -> Action:
    """
    Stratégie qui retourne la première action légale calculée
    """
    return env.legals(player)[0]


def strategy_random(
    env: Environment,
    player: PlayerLocal,
) -> Action:
    """
    Stratégie qui retourne une action légale aléatoire
    """
    return random.choice(env.legals(player))


# Fonctions d'évaluation
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


# nombre de coups pour gagner ?
def evaluate_dynamic(env: Environment, grid: GridDict, player: PlayerLocal) -> int:
    """
    Fonction d'évaluation pour le jeu Dodo avec une récompense dynamique pour la proximité du bord
    """
    opponent = env.min_player if player == env.max_player else env.max_player

    player_moves = len(env.legals(player))
    opponent_moves = len(env.legals(opponent))

    player_score = 0
    opponent_score = 0

    grid_height = env.hex_size
    grid_width = env.hex_size

    for cell in grid:
        if grid[cell] == player:
            player_score -= 40  # Pénalité pour avoir une pièce
            player_score -= 80 * player_moves  # Pénalité ajustée pour la mobilité

            if is_near_edge(cell, grid_height, grid_width):
                player_score += 40 - distance_to_edge(
                    cell, grid_height, grid_width
                )  # Récompense dynamique pour la proximité du bord
        elif cell == opponent:
            opponent_score += 40  # Récompense pour avoir une pièce
            opponent_score += (
                80 * opponent_moves
            )  # Récompense ajustée pour la mobilité

            if is_near_edge(cell, grid_height, grid_width):
                # Pénalité dynamique pour l'adversaire près du bord
                opponent_score -= 40 - distance_to_edge(
                    cell, grid_height, grid_width
                )

    return player_score - opponent_score


def distance_to_edge(cell: Cell, grid_height: int, grid_width: int) -> int:
    """
    Calculer la distance minimale d'une cellule aux bords de la grille
    """
    return min(cell[0], grid_height - 1 - cell[0], cell[1], grid_width - 1 - cell[1])


# Minimax Strategy (sans cache)
def minmax_action(
    env: Environment, player: PlayerLocal, depth: int = 0
) -> tuple[int, Action]:
    """
    Stratégie qui retourne le résultat de l'algorithme Minimax pour le jeu Dodo
    """
    if depth == 0 or env.final() != 0:
        return env.final(), (-1, -1)  # On retourne le score de la grille

    if player == env.max_player:  # maximizing player
        best = (int("-inf"), ((-1, -1), (-1, -1)))
        for item in env.legals(player):
            env.play(item)
            returned_values: tuple[int, Action] = minmax_action(
                env, env.min_player, depth - 1
            )
            env.reverse_action(item)
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best

    if player == env.min_player:  # minimizing player
        best = (int("inf"), (-1, -1))
        for item in env.legals(player):
            env.play(item)
            returned_values = minmax_action(env, env.max_player, depth - 1)
            env.reverse_action(item)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best: tuple[int, Action] = (returned_values[0], item)
        return best
    return 0, (-1, -1)


def minmax_action_alpha_beta_pruning(
    env: Environment, player: PlayerLocal, depth: int = 0
) -> tuple[float, Action]:
    """
    Stratégie qui retourne le résultat de l'algorithme Minimax avec élagage Alpha-Beta
    """

    def minmax_alpha_beta_pruning(
        env: Environment,
        player: PlayerLocal,
        depth: int,
        alpha: float,
        beta: float,
    ) -> tuple[float, Action]:

        # Si la profondeur est nulle ou si la partie est terminée
        res = env.final()
        if res != 0:
            if res == 1:
                score = 10000
            else:
                score = -10000
            return score, (-1, -1)
        if depth == 0:
            score = evaluate_dynamic(env, env.grid, player)
            return score, (-1, -1)

        if player == env.max_player.id:  # Maximizing player
            best_max: tuple[float, Action] = (float("-inf"), (-1, -1))
            for action in env.legals(player):
                env.play(action)
                returned_values = minmax_alpha_beta_pruning(
                    env, env.min_player, depth - 1, alpha, beta
                )
                env.reverse_action(action)
                if returned_values[0] > best_max[0]:
                    best_max = (returned_values[0], action)
                alpha = max(alpha, best_max[0])
                if beta <= alpha:
                    break
            return best_max

        if player == env.min_player.id:  # Minimizing player
            best_min: tuple[float, Action] = (float("inf"), (-1, -1))
            for item in env.legals(player):
                env.play(item)
                returned_values = minmax_alpha_beta_pruning(
                    env, env.max_player, depth - 1, alpha, beta
                )
                env.reverse_action(item)
                if returned_values[0] < best_min[0]:
                    best_min = (returned_values[0], item)
                beta = min(beta, best_min[0])

                if beta <= alpha:
                    break
            return best_min
        return 0, (-3, -3)

    return minmax_alpha_beta_pruning(env, player, depth, float("-inf"), float("inf"))


def strategy_minmax(
    env: Environment, player: PlayerLocal
) -> Action:
    """
    Stratégie qui retourne l'action calculée par l'algorithme Minimax
    """

    try:
        depth_factor = 1/(log(len(env.legals(player)), 2) / 5) * 1.2
    except ZeroDivisionError:
        depth_factor = 1
    depth_factor = depth_factor.real # convert depth factor to a float

    depth = min(6 + round(depth_factor), 15)

    return minmax_action_alpha_beta_pruning(env, player, depth)[1]
