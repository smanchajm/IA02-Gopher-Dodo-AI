"""" Exemples de Grid """

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
    (-1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0),
    (-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1),
    (0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1),
)


# Exemple de grille initiale de taille 7 pour Dodo
INIT_GRID = (
    (-1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1),
    (-1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 1, 1),
    (-1, -1, -1, -1, 0, 0, 0, 1, 1, 1, 1, 1, 1),
    (-1, -1, -1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1),
    (-1, -1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1),
    (-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    (2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1),
    (2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1),
    (2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, -1, -1),
    (2, 2, 2, 2, 2, 0, 0, 0, 0, 0, -1, -1, -1),
    (2, 2, 2, 2, 2, 2, 0, 0, 0, -1, -1, -1, -1),
    (2, 2, 2, 2, 2, 2, 2, 0, -1, -1, -1, -1, -1),
    (2, 2, 2, 2, 2, 2, 2, -1, -1, -1, -1, -1, -1),
)

INIT_GRID4 = (
    (-1, -1, -1, 1, 1, 1, 1),
    (-1, -1, 0, 1, 1, 1, 1),
    (-1, 0, 0, 0, 1, 1, 1),
    (2, 2, 0, 0, 0, 1, 1),
    (2, 2, 2, 0, 0, 0, -1),
    (2, 2, 2, 2, 0, -1, -1),
    (2, 2, 2, 2, -1, -1, -1),
)

INIT_GRID3 = (
    (-1, -1, 1, 1, 1),
    (-1, 0, 1, 1, 1),
    (2, 2, 0, 1, 1),
    (2, 2, 2, 0, -1),
    (2, 2, 2, -1, -1),
)


taille = 0
for i in range(0, len(INIT_GRID)):
    for j in range(0, len(INIT_GRID[i])):
        if INIT_GRID[i][j] != -1:
            taille += 1
print(taille)