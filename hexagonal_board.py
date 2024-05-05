# Generated code -- CC0 -- No Rights Reserved -- http://www.redblobgames.com/grids/hexagons/
from __future__ import division
from __future__ import print_function
import collections
import math
from typing import List

# 0 représente une case vide, 1 représente une case marquée par rouge et 2 une case marquée par bleu
Grid = tuple[tuple[int, ...], ...]


def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    return [list(i) for i in grid]


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    return tuple(tuple(i) for i in grid)


def grid_generation(n: int):
    # Création d'un tableau 2n * 2n
    grid = [[-1] * (2 * n) for _ in range(2 * n)]

    # Remplissage d'une grille vide
    for r in range(n):
        for q in range(n - r, 2*n):
            grid[r][q] = 0
    for r in range(n):
        for q in range(2*n-r-1):
            grid[r+n][q] = 0

    grid.insert(n, [-0] * (2 * n))
    for ligne in grid:
        ligne.insert(n, 0)

    return grid


def display_grid(grid):
    for row in grid:
        for cell in row:
            # Coloration en rouge si == -1
            if cell == -1:
                print("\033[91m", end="")
            print(str(cell).rjust(2), end=" ")
            print("\033[0m", end="")
        print()


def main():
    n = 6
    resultat = grid_generation(n)
    display_grid(resultat)
    pass


if __name__ == "__main__":
    main()

