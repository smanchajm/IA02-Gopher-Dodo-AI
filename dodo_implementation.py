# Module concernant la réalisation du jeu DoDo
import random
from typing import List, Set, Callable, Union
import hexagonal_board as hexa
from grid import *


# Structures de données
Grid = hexa.Grid

# Types de base utilisés par l'arbitre
Environment = ...  # Ensemble des données utiles (cache, état de jeu...) pour
# que votre IA puisse jouer (objet, dictionnaire, autre...)
Cell = tuple[int, int]
ActionDodo = tuple[Cell, Cell]  # case de départ -> case d'arrivée
ActionGopher = Cell
Action = Union[ActionGopher, ActionDodo]
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu
Score = int
Time = int
Strategy = Callable[[Grid, Player], Action]

# Quelques constantes
DRAW = 0
EMPTY = 0

UP_DIRECTIONS: List[tuple[int, int]] = [
    (1, 0),
    (1, 1),
    (0, 1),
]

DOWN_DIRECTIONS: List[tuple[int, int]] = [
    (0, -1),
    (-1, 0),
    (-1, -1),
]

player1 = 1  # Player bleu
player2 = 2  # Player rouge


# Règles du DoDo


# Fonction retournant les actions possibles d'un joueur pour un état donné (voir optimisation)
def legals_dodo(grid: Grid, player: Player, directions) -> list[ActionDodo]:
    actions: Set[ActionDodo] = set()  # On utilise un ensemble pour garantir l'unicité

    # On parcourt l'ensemble des cases de la grille
    for i, ligne in enumerate(grid):
        for j, element in enumerate(ligne):
            # Si la case est occupée par un jeton du player
            if element == player:
                neighbors = hexa.hex_neighbor(i, j, directions)
                for neighbor in neighbors:
                    # Ajouter un voisin si
                    r = neighbor[0]
                    q = neighbor[1]
                    if 0 <= r < len(grid) and 0 <= q < len(grid[0]):
                        if grid[neighbor[0]][neighbor[1]] == 0:
                            actions.add(((i, j), neighbor))

    return list(actions)


# Fonction retournant Vrai si nous sommes dans un état final (fin de partie)
def final_dodo(grid: Grid) -> int:
    if not legals_dodo(grid, player1, DOWN_DIRECTIONS):
        return 1
    elif not legals_dodo(grid, player2, UP_DIRECTIONS):
        return -1
    else:
        return 0


def play_dodo(grid: Grid, player: Player, action: ActionDodo) -> Grid:
    temp_grid: list[list[int, ...], ...] = hexa.grid_tuple_to_grid_list(grid)
    temp_grid[action[0][0]][action[0][1]] = 0
    temp_grid[action[1][0]][action[1][1]] = player
    return hexa.grid_list_to_grid_tuple(temp_grid)


# Strategies
def strategy_first_legal_dodo(grid: Grid, player: Player) -> Action:
    if player == player1:
        return legals_dodo(grid, player, DOWN_DIRECTIONS)[0]
    else:
        return legals_dodo(grid, player, UP_DIRECTIONS)[0]


def strategy_random_dodo(grid: Grid, player: Player) -> Action:
    if player == player1:
        return random.choice(legals_dodo(grid, player, DOWN_DIRECTIONS))
    else:
        return random.choice(legals_dodo(grid, player, UP_DIRECTIONS))


# Boucle de jeu Dodo
def dodo(strategy_1: Strategy, strategy_2: Strategy, init_grid: Grid, debug: bool = False) -> Score:
    actual_grid: Grid = init_grid
    current_player: Player = 1
    current_action: Action
    nb_iterations: int = 0

    while not (final_dodo(actual_grid) == 1 or final_dodo(actual_grid) == -1):
        nb_iterations += 1
        if current_player == 1:
            current_action = strategy_1(actual_grid, current_player)
        else:
            current_action = strategy_2(actual_grid, current_player)
        actual_grid = play_dodo(actual_grid, current_player, current_action)
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1

    print(f"Iteration \033[36m {nb_iterations}\033[0m.")
    hexa.display_grid(actual_grid)

    return final_dodo(actual_grid)


def main():
    init_grid = INIT_GRID
    print(dodo(strategy_random_dodo, strategy_random_dodo, init_grid, False))
    pass


if __name__ == "__main__":
    main()
