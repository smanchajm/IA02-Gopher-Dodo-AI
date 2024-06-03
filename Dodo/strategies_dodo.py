""" Module contenant les différentes stratégies pour le jeu Dodo """

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
    starting_library: dict = Dict[Any, Any],
) -> Action:
    """
    Stratégie qui retourne la première action légale calculée
    """
    return env.legals_gopher(grid, player)[0]


def strategy_random_gopher(
    env: Environment,
    player: Player,
    grid: GridDict,
    starting_library: dict = Dict[Any, Any],
) -> Action:
    """
    Stratégie qui retourne une action légale aléatoire
    """
    return random.choice(env.legals_gopher(grid, player))


def strategy_random_dodo(
    env: Environment,
    player: Player,
    grid: Grid,
    starting_library: dict = Dict[Any, Any],
) -> Action:
    """
    Stratégie qui retourne une action légale aléatoire
    """
    return random.choice(env.legals_dodo(grid, player))


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


def evaluate(env: Environment, grid: Grid, player: Player) -> int:
    """
    Première fonction d'évaluation pour le jeu Dodo
    """
    if player == env.max_player:
        opponent = env.min_player
    else:
        opponent = env.max_player

    player_score = 0
    opponent_score = 0

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == player:
                player_score -= (
                    10  # Penalty for having a piece, to encourage blocking oneself
                )
                player_score -= 5 * len(
                    env.legals_dodo(grid, player)
                )  # Penalty for mobility
                if is_near_edge((i, j), len(grid), len(grid)):
                    player_score += (
                        5  # Reward for being near edge (easier to block oneself)
                    )
            elif cell == opponent:
                opponent_score += 10  # Reward for having a piece
                opponent_score += 5 * len(
                    env.legals_dodo(grid, opponent)
                )  # Reward for mobility
                if is_near_edge((i, j), len(grid), len(grid)):
                    opponent_score -= 5  # Penalty for opponent being near edge

    return player_score - opponent_score


# nombre de coups pour gagner ?
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
            if cell == player:
                player_score -= 400  # Pénalité pour avoir une pièce
                player_score -= 800 * player_moves  # Pénalité ajustée pour la mobilité
                if is_near_edge((i, j), grid_height, grid_width):
                    player_score += 400 - distance_to_edge(
                        (i, j), grid_height, grid_width
                    )  # Récompense dynamique pour la proximité du bord
            elif cell == opponent:
                opponent_score += 400  # Récompense pour avoir une pièce
                opponent_score += (
                    800 * opponent_moves
                )  # Récompense ajustée pour la mobilité
                if is_near_edge((i, j), grid_height, grid_width):
                    # Pénalité dynamique pour l'adversaire près du bord
                    opponent_score -= 400 - distance_to_edge(
                        (i, j), grid_height, grid_width
                    )

    return player_score - opponent_score


def distance_to_edge(cell: Cell, grid_height: int, grid_width: int) -> int:
    """
    Calculer la distance minimale d'une cellule aux bords de la grille
    """
    return min(cell[0], grid_height - 1 - cell[0], cell[1], grid_width - 1 - cell[1])


# Minimax Strategy (sans cache)
def minmax_action(
    env: Environment, player: Player, grid: Grid, depth: int = 0
) -> tuple[int, Action]:
    """
    Stratégie qui retourne le résultat de l'algorithme Minimax pour le jeu Dodo
    """
    if depth == 0 or env.final_dodo(grid) != 0:
        return env.final_dodo(grid), (-1, -1)  # On retourne le score de la grille

    if player == env.max_player:  # maximizing player
        best = (int("-inf"), ((-1, -1), (-1, -1)))
        for item in env.legals_dodo(grid, player):
            tmp = env.play_dodo(player, grid, item)
            returned_values: tuple[int, Action] = minmax_action(
                env, env.min_player, tmp, depth - 1
            )
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best

    if player == env.min_player:  # minimizing player
        best = (int("inf"), (-1, -1))
        for item in env.legals_dodo(grid, player):
            tmp = env.play_dodo(player, grid, item)
            returned_values = minmax_action(env, env.max_player, tmp, depth - 1)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best: tuple[int, Action] = (returned_values[0], item)
        return best
    return 0, (-1, -1)


# Define a type alias for the memoization key
MemoKey = tuple[Grid, int]


def minmax_action_alpha_beta_pruning(
    env: Environment, player: Player, grid: Grid, depth: int = 0
) -> tuple[float, Action]:
    """
    Stratégie qui retourne le résultat de l'algorithme Minimax avec élagage Alpha-Beta
    et memoization pour le jeu Dodo
    """
    memo: Dict[MemoKey, Tuple[float, Action]] = (
        {}
    )  # Dictionary to store the memoized results

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
                score = 10000000
            else:
                score = -10000000
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
    env: Environment, player: Player, grid: Grid, starting_library: dict = None
) -> Action:
    """
    Stratégie qui retourne l'action calculée par l'algorithme Minimax
    """
    # return minmax_action(env, player, grid, 4)[1]
    # return minmax_action_alpha_beta_pruning(env, player, grid, 4)[1]
    depth_factor = 13 / len(env.legals_dodo(grid, player))
    depth = min(5 * max(1, round(depth_factor)), 5)
    # depth = 5

    if starting_library is None:
        # print("No library provided")
        return minmax_action_alpha_beta_pruning(env, player, grid, depth)[1]
    # max_depth_in_library = min(100, len(starting_library))  # library covers first 100 iterations
    action = None

    # find is the hash key is in the library
    if hash(grid) in list(starting_library.keys()):
        # write in green
        print("\033[32mHash found in library\033[0m")
        action = starting_library[hash(grid)]["action"]
        # test if the action is in the legal actions
        if action not in env.legals_dodo(grid, player):
            action = None

    if action is None:
        # If no action is found in the library, perform the minimax search as usual
        action = minmax_action_alpha_beta_pruning(env, player, grid, depth)[1]

    return action


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
    if env.nb_moves < 200:
        action = env.precedent_action
        action = ((len(grid) - 1 - action[0][0], len(grid[0]) - 1 - action[0][1]), (len(grid) - 1 - action[1][0], len(grid[0]) - 1 - action[1][1]))
        return action
    return strategy_minmax(env, player, grid)
