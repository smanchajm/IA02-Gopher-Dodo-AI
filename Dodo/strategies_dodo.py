""" Module contenant les différentes stratégies pour le jeu Dodo """
import random
from typing import Callable, Dict, Tuple
from Game_playing.structures_classes import Environment, Player, Grid, Action, Cell

Strategy = Callable[[Environment, Player, Grid], Action]


def strategy_first_legal_dodo(env: Environment, player: Player, grid: Grid) -> Action:
    """
    Stratégie qui retourne la première action légale calculée
    """
    return env.legals_dodo(grid, player)[0]


def strategy_random_dodo(env: Environment, player: Player, grid: Grid, starting_library: dict = None) -> Action:
    """
    Stratégie qui retourne une action légale aléatoire
    """
    return random.choice(env.legals_dodo(grid, player))


# Fonctions d'évaluation
def is_near_edge(cell: Cell, grid_height: int, grid_width: int) -> bool:
    return cell[0] == 0 or cell[0] == grid_height - 1 or cell[1] == 0 or cell[1] == grid_width - 1


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


def evaluate_dynamic(env: Environment, grid: Grid, player: Player) -> int:
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
                    player_score += 400 - distance_to_edge((i, j), grid_height,
                                                           grid_width)  # Récompense dynamique pour la proximité du bord
            elif cell == opponent:
                opponent_score += 400  # Récompense pour avoir une pièce
                opponent_score += 800 * opponent_moves  # Récompense ajustée pour la mobilité
                if is_near_edge((i, j), grid_height, grid_width):
                    opponent_score -= 400 - distance_to_edge((i, j), grid_height,
                                                             grid_width)  # Pénalité dynamique pour l'adversaire près du bord

    return player_score - opponent_score


def distance_to_edge(cell: Cell, grid_height: int, grid_width: int) -> int:
    # Calculer la distance minimale d'une cellule aux bords de la grille
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
        best = (int("-inf"), (-1, -1))
        for item in env.legals_dodo(grid, player):
            tmp = env.play_dodo(player, grid, item)
            returned_values: tuple[int, Action] = minmax_action(env, env.min_player, tmp, depth - 1)
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
    et memoïsation pour le jeu Dodo
    """
    memo: Dict[MemoKey, Tuple[int, Action]] = {}  # Dictionary to store the memoized results

    def minmax_alpha_beta_pruning(
            env: Environment,
            player: Player,
            grid: Grid,
            depth: int,
            alpha: float,
            beta: float,
    ) -> tuple[float, Action]:
        # Convert grid to a tuple so it can be used as a key in the dictionary
        grid_key = grid
        player_id = player.id  # Use a unique identifier for the player

        if (grid_key, player_id) in memo:
            return memo[(grid_key, player_id)]

        if env.final_dodo(grid) != 0:
            score = env.final_dodo(grid)
            memo[(grid_key, player_id)] = (score, (-1, -1))
            return score, (-1, -1)
        if depth == 0:
            score = evaluate_dynamic(env, grid, player)
            # score = evaluate(env, grid, player)
            memo[(grid_key, player_id)] = (score, (-1, -1))
            return score, (-1, -1)

        if player == env.max_player:  # Maximizing player
            best = (float("-inf"), (-1, -1))
            for item in env.legals_dodo(grid, player):
                tmp = env.play_dodo(player, grid, item)
                returned_values = minmax_alpha_beta_pruning(
                    env, env.min_player, tmp, depth - 1, alpha, beta
                )
                if max(best[0], returned_values[0]) == returned_values[0]:
                    best: tuple[float, Action] = (returned_values[0], item)
                alpha = max(alpha, best[0])
                if beta <= alpha:
                    break
            memo[(grid_key, player_id)] = best
            return best

        if player == env.min_player:  # Minimizing player
            best = (float("inf"), (-1, -1))
            for item in env.legals_dodo(grid, player):
                tmp = env.play_dodo(player, grid, item)
                returned_values = minmax_alpha_beta_pruning(
                    env, env.max_player, tmp, depth - 1, alpha, beta
                )
                if min(best[0], returned_values[0]) == returned_values[0]:
                    best: tuple[float, Action] = (returned_values[0], item)
                beta = min(beta, best[0])
                if beta <= alpha:
                    break
            memo[(grid_key, player_id)] = best
            return best
        return 0, (-1, -1)

    return minmax_alpha_beta_pruning(
        env, player, grid, depth, float("-inf"), float("inf")
    )


def strategy_minmax(env: Environment, player: Player, grid: Grid, starting_library: dict = None) -> Action:
    """
    Stratégie qui retourne l'action calculée par l'algorithme Minimax
    """
    # return minmax_action(env, player, grid, 4)[1]
    # return minmax_action_alpha_beta_pruning(env, player, grid, 4)[1]

    if starting_library is None:
        # print("No library provided")
        return minmax_action_alpha_beta_pruning(env, player, grid, 6)[1]
    # max_depth_in_library = min(100, len(starting_library))  # Assuming library covers first 100 iterations
    action = None

    # find is the hash key is in the library
    if hash(grid) in list(starting_library.keys()):
        # write in green
        print("\033[32mHash found in library\033[0m")
        action = starting_library[hash(grid)]['action']
        # test if the action is in the legal actions
        if action not in env.legals_dodo(grid, player):
            action = None

    if action is None:
        # If no action is found in the library, perform the minimax search as usual
        action = minmax_action_alpha_beta_pruning(env, player, grid, 6)[1]

    return action
