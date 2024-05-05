from typing import List

# Structures de données

# 0 représente une case vide, 1 représente une case marquée par rouge et 2 une case marquée par bleu
Grid = tuple[tuple[int, ...], ...]


# Conversion


def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    return [list(i) for i in grid]


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return tuple(tuple(i) for i in grid)


def grid_generation(n: int) -> Grid:
    # Création d'un tableau 2n * 2n
    m = n - 1
    grid = [[-1] * (2 * m) for _ in range(2 * m)]

    # Remplissage d'une grille vide
    for r in range(m):
        for q in range(m - r, 2 * m):
            grid[r][q] = 0
    for r in range(m):
        for q in range(2 * m - r - 1):
            grid[r + m][q] = 0
    grid.insert(m, [-0] * (2 * m))
    for ligne in grid:
        ligne.insert(m, 0)

    return grid_list_to_grid_tuple(grid)


# Attention les coordonnées sont inversées : Dans l'exemple on a colonne puis ligne alors que dans tableau on a ligne
# puis colonne
def display_grid(grid: Grid):
    for row in grid:
        for cell in row:
            # Coloration en rouge si == -1
            if cell == -1:
                print("\033[91m", end="")
            print(str(cell).rjust(2), end=" ")
            print("\033[0m", end="")
        print()


# Conversion de coordonnées allant de 0 à 2n à des coordonnées allant de -n à n
def convert(q: int, r: int, n) -> (int, int):
    return -q + n - 1, - n + r + 1


hex_directions: List[tuple[int, int]] = [(1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (0, 1)]


# Voisins d'une case selon certaines directions
def hex_neighbor(q, r, directions) -> List[tuple[int, int]]:
    return [(q + dq, r + dr) for dq, dr in directions]


def display_neighbors(grid: Grid, q: int, r: int, directions: List[tuple[int, int]], n):
    neighbors: List[tuple[int, int]] = hex_neighbor(q, r, directions)
    res_grid: list[list[int]] = grid_tuple_to_grid_list(grid)

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            # Coloration en rouge si == -1
            if cell == -1:
                print("\033[91m", end="")
            if convert(i, j, n) in neighbors:
                print("\033[92m", end="")
            if convert(i, j, n) == (q, r):
                print("\033[95m", end="")
            print(str(cell).rjust(2), end=" ")
            print("\033[0m", end="")
        print()


def main():
    n = 7
    res = grid_generation(n)
    display_neighbors(res, -4, -5, hex_directions, n)


    pass


if __name__ == "__main__":
    main()
