# Module concernant la réalisation du jeu DoDo
from typing import List, Set
import hexagonal_board as hexa

# Structures de données
Grid = hexa.Grid

# Types de base utilisés par l'arbitre
Environment = ...  # Ensemble des données utiles (cache, état de jeu...) pour
# que votre IA puisse jouer (objet, dictionnaire, autre...)
Cell = tuple[int, int]
ActionDodo = tuple[Cell, Cell]  # case de départ -> case d'arrivée
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu
Score = int
Time = int


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
            if r < m-1 and q >= m:
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
    hexa.display_grid(hexa.grid_list_to_grid_tuple(temp_grid))

    return list(actions)


def main():
    n = 7
    init_grid = hexa.INIT_GRID
    hexa.display_neighbors(init_grid, 6, 0, UP_DIRECTIONS, n)
    print(legals_dodo(init_grid, player2, UP_DIRECTIONS))
    pass


if __name__ == "__main__":
    main()
