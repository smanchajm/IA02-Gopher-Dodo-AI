# Module concernant la réalisation du jeu DoDo
import random
from typing import List, Set, Callable, Union
import hexagonal_board as hexa

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


# Fonction de génération de grille pour le jeu DoDo --> en cours de réalisation
def grid_generation_dodo(n: int) -> Grid:
    # Création d'un tableau 2(n-1) * 2(n-1)
    m = n - 1
    grid = [[-1] * (2 * m) for _ in range(2 * m)]

    # Remplissage d'une grille vide
    # Remplissage de la première moitié de la grille
    for r in range(m):
        for q in range(m - r, 2 * m):
            if r < m - 1 and q >= m:
                grid[r][q] = 1
            else:
                grid[r][q] = 0
    # Remplissage de la seconde moitié de la grille
    for r in range(m):
        for q in range(2 * m - r - 1):
            if r >= 1 and q < m:
                grid[r + m][q] = 2
            else:
                grid[r + m][q] = 0
    # Ajout d'une colonne et d'une ligne de 0 au milieu de la grille
    grid.insert(m, [-0] * (2 * m))
    for ligne in grid:
        ligne.insert(m, 0)

    return hexa.grid_list_to_grid_tuple(grid)


# Règles du DoDo


# Fonction retournant les actions possibles d'un joueur pour un état donné (voir optimisation)
def legals_dodo(grid: Grid, player: Player, directions) -> list[ActionDodo]:
    actions: Set[ActionDodo] = set()  # On utilise un ensemble pour garantir l'unicité
    temp_grid: list[list[int, ...], ...] = hexa.grid_tuple_to_grid_list(grid)

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
                            temp_grid[r][q] = 4
    #hexa.display_grid(hexa.grid_list_to_grid_tuple(temp_grid))

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
def dodo(strategy_1: Strategy, strategy_2: Strategy, debug: bool = False) -> Score:
    actual_grid: Grid = hexa.INIT_GRID
    current_player: Player = 1
    current_action: Action
    nb_iterations: int = 0

    while not (final_dodo(actual_grid) == 1 or final_dodo(actual_grid) == -1):
        nb_iterations += 1
        print(f"Iteration \033[36m {nb_iterations}\033[0m.")
        if current_player == 1:
            current_action = strategy_1(actual_grid, current_player)
        else:
            current_action = strategy_2(actual_grid, current_player)
        actual_grid = play_dodo(actual_grid, current_player, current_action)
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1
        hexa.display_grid(actual_grid)

    return final_dodo(actual_grid)


def main():
    n = 7
    init_grid = hexa.INIT_GRID
    # hexa.display_neighbors(init_grid, 6, 0, UP_DIRECTIONS, n)
    # print(legals_dodo(init_grid, player2, UP_DIRECTIONS))
    # print(final_dodo(init_grid))
    # print(legals_dodo(play_dodo(init_grid, player2, ((6, 0), (5, 1))), player2, UP_DIRECTIONS))

    print(dodo(strategy_random_dodo, strategy_random_dodo, False))

    pass


if __name__ == "__main__":
    main()
