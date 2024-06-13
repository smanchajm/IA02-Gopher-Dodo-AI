import random
import time
from typing import Dict, List, Set, Tuple

from Dodo.grid import INIT_GRID4
import Game_playing.hexagonal_board as hexa
from Game_playing.hexagonal_board import Grid
from Game_playing.structures_classes import DOWN_DIRECTIONS, EMPTY, UP_DIRECTIONS, Action, ActionDodo, Player, Score, Strategy

# Quelques constantes
PLAYER1: Player = 1  # Player bleu
PLAYER2: Player = 2  # Player rouge

minimax_cache: Dict[Tuple[Grid, int, bool, Player], Tuple[int, ActionDodo]] = {}


# Fonction retournant les actions possibles d'un joueur pour un état donné (voir optimisation)
def legals_dodo(grid: Grid, player: Player, directions: List[Tuple[int, int]]) -> List[ActionDodo]:
    actions: Set[ActionDodo] = set()
    # On parcourt l'ensemble des cases de la grille
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            # Si la case est occupée par un jeton du player
            if cell == player:
                for ni, nj in hexa.hex_neighbor(i, j, directions):
                    if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] == EMPTY:
                        actions.add(((i, j), (ni, nj)))
    return list(actions)


# Fonction retournant Vrai si nous sommes dans un état final (fin de partie)
def final_dodo(grid: Grid) -> int:
    if not legals_dodo(grid, PLAYER1, DOWN_DIRECTIONS):
        return 1
    if not legals_dodo(grid, PLAYER2, UP_DIRECTIONS):
        return -1

    return 0


def play_dodo(grid: Grid, player: Player, action: ActionDodo) -> Grid:
    temp_grid: list[list[int]] = hexa.grid_tuple_to_grid_list(grid)
    temp_grid[action[0][0]][action[0][1]] = 0
    temp_grid[action[1][0]][action[1][1]] = player
    return hexa.grid_list_to_grid_tuple(temp_grid)


# Strategies
def strategy_first_legal_dodo(grid: Grid, player: Player) -> Action:
    if player == PLAYER1:
        return legals_dodo(grid, player, DOWN_DIRECTIONS)[0]
    return legals_dodo(grid, player, UP_DIRECTIONS)[0]


def strategy_random_dodo(grid: Grid, player: Player) -> Action:
    if player == PLAYER1:
        return random.choice(legals_dodo(grid, player, DOWN_DIRECTIONS))
    return random.choice(legals_dodo(grid, player, UP_DIRECTIONS))


# Minimax Strategy (sans cache)
def minmax_action(grid: Grid, player: Player, depth: int = 0) -> tuple[float, Action]:
    player1: Player = PLAYER1
    player2: Player = PLAYER2

    if depth == 0 or final_dodo(grid) != 0:
        return final_dodo(grid), (-1, -1) # On retourne le score de la grille

    if player == 1: # maximazing player
        best = (float("-inf"), (-1, -1))
        for item in legals_dodo(grid, player, DOWN_DIRECTIONS):
            tmp = play_dodo(grid, player, item)
            returned_values = minmax_action(tmp, player2, depth - 1)
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best

    if player == 2:  # minimizing player
        best = (float("inf"), (-1, -1))
        for item in legals_dodo(grid, player, UP_DIRECTIONS):
            tmp = play_dodo(grid, player, item)
            returned_values = minmax_action(tmp, player1, depth - 1)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best


def strategy_minmax(grid: Grid, player: Player) -> Action:
    return minmax_action(grid, player, 5)[1]


# Boucle de jeu Dodo
def dodo(
        strategy_1: Strategy, strategy_2: Strategy, init_grid: Grid
) -> Score:
    actual_grid: Grid = init_grid
    current_player: Player = 1
    current_action: Action
    nb_iterations: int = 0
    total_time_start = time.time()  # Chronomètre

    while not (final_dodo(actual_grid) == 1 or final_dodo(actual_grid) == -1):
        nb_iterations += 1
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        print(f"Iteration \033[36m {nb_iterations}\033[0m.")
        hexa.display_grid(actual_grid)
        if current_player == 1:
            current_action = strategy_1(actual_grid, current_player)
        else:
            current_action = strategy_2(actual_grid, current_player)
        actual_grid = play_dodo(actual_grid, current_player, current_action)
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1

        iteration_time_end = time.time()  # Fin du chronomètre pour la durée de cette itération
        print(f"Temps écoulé pour cette itération: {iteration_time_end - iteration_time_start} secondes")

    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie
    print(f"Temps total écoulé: {total_time_end - total_time_start} secondes")

    return final_dodo(actual_grid)


def main():
    print(dodo(strategy_minmax, strategy_random_dodo, INIT_GRID4, False))


if __name__ == "__main__":
    main()
