# Module concernant la grille hexagonale de jeu
from typing import List

# Structures de données

# Types de base utilisés par l'arbitre
# que votre IA puisse jouer (objet, dictionnaire, autre...)
Cell = tuple[int, int]
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu

# Exemples de Grid
GRID1 = (
    (-1, -1, -1, -1, -1, -1, 0, 0, 1, 0, 0, 0, 0),
    (-1, -1, -1, -1, -1, 0, 0, 1, 0, 0, 0, 0, 0),
    (-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, -1, -1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0),
    (-1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 0, 0, -1),
    (0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1),
    (0, 0, 0, 2, 0, 0, 0, 0, 0, -1, -1, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1),
)

GRID2 = (
    ((-1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0), (-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0),
     (-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0), (-1, -1, -1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
     (-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1), (0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1),
     (0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1))

)


# Generation de l'état de départ avec la nouvelle structure de données
def grid_generation_test(n: int) -> State:
    res: State = []
    m = n - 1

    # Remplissage d'une grille vide
    # Remplissage de la première moitié de la grille
    for r in range(n - 1, -1, -1):
        for q in range(r - m, n):
            res.append(((q, r), 0))
    # Remplissage de la seconde moitié de la grille
    for r in range(-1, -n, -1):
        for q in range(-m, n + r):
            res.append(((q, r), 0))

    return res


def display_grid_test(grid: State):
    displayed_lines: List[int] = []
    for coord, player in grid:
        if coord[1] not in displayed_lines:
            print()
            displayed_lines.append(coord[1])
            for i in range(coord[1]):
                print("\033[30m", end="")
                print("".rjust(2), end=" ")
            print("\033[0m", end="")

        if player == 1:
            print("\033[34m", end="")
        # Coloration en rouge si == 2
        if player == 2:
            print("\033[31m", end="")
        print(str(player).rjust(2), end=" ")
        print("\033[0m", end="")


directions_case_neighbors: List[tuple[int, int]] = [
    (1, 0),
    (1, 1),
    (0, -1),
    (-1, 0),
    (-1, -1),
    (0, 1),
]


# Voisins d'une case selon certaines directions
def hex_neighbor(q, r, directions) -> List[tuple[int, int]]:
    return [(q + dq, r + dr) for dq, dr in directions]


def main():
    n = 7
    print(grid_generation_test(n))
    print(len(grid_generation_test(n)))
    display_grid_test(grid_generation_test(n))

    pass


if __name__ == "__main__":
    main()

""""
# Fonctions avec l'ancienne structure de données
def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    return [list(i) for i in grid]


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return tuple(tuple(i) for i in grid)
    

def display_neighbors(grid: Grid, q: int, r: int, directions: List[tuple[int, int]], n):
    neighbors: List[tuple[int, int]] = hex_neighbor(q, r, directions)

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            # Coloration en noir si == -1
            if cell == -1:
                print("\033[30m", end="")
            # Coloration en vert si c'est un voisin
            if convert(i, j, n) in neighbors:
                print("\033[92m", end="")
            # Coloration en rose element sélectionné
            if convert(i, j, n) == (q, r):
                print("\033[95m", end="")
            # Coloration en bleu si == 1
            elif cell == 1:
                print("\033[34m", end="")
            # Coloration en rouge si == 2
            elif cell == 2:
                print("\033[31m", end="")
            print(str(cell).rjust(2), end=" ")
            print("\033[0m", end="")
        print()


def grid_generation(n: int) -> Grid:
    # Création d'un tableau 2(n-1) * 2(n-1)
    m = n - 1
    grid = [[-1] * (2 * m) for _ in range(2 * m)]

    # Remplissage d'une grille vide
    # Remplissage de la première moitié de la grille
    for r in range(m):
        for q in range(m - r, 2 * m):
            grid[r][q] = 0
    # Remplissage de la seconde moitié de la grille
    for r in range(m):
        for q in range(2 * m - r - 1):
            grid[r + m][q] = 0
    # Ajout d'une colonne et d'une ligne de 0 au milieu de la grille
    grid.insert(m, [-0] * (2 * m))
    for ligne in grid:
        ligne.insert(m, 0)

    return grid_list_to_grid_tuple(grid)


def display_grid(grid: Grid):
    for row in grid:
        for cell in row:
            # Coloration en noir si == -1
            if cell == -1:
                print("\033[30m", end="")
            # Coloration en bleu si == 1
            if cell == 1:
                print("\033[34m", end="")
            # Coloration en rouge si == 2
            if cell == 2:
                print("\033[31m", end="")
            print(str(cell).rjust(2), end=" ")
            print("\033[0m", end="")
        print()


# Conversion de coordonnées allant de 0 à 2n à des coordonnées allant de -n à n
def convert(q: int, r: int, n) -> (int, int):
    return -q + n - 1, -n + r + 1
    
    
"""""
