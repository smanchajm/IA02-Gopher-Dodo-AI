# Module concernant la réalisation du jeu DoDo

from typing import List, NamedTuple, Set
from collections import namedtuple
import hexagonal_board as hex


# Structures de données
Action = namedtuple('Action', ['player', 'coord'])
Player = namedtuple('Player', ['number', 'directions'])
State = hex.Grid


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


player1 = Player(1, DOWN_DIRECTIONS)  # Player bleu
player2 = Player(2, UP_DIRECTIONS)  # Player rouge


# Règles du DoDo

# À optimiser pour améliorer la complexité
def legals(grid: State, player: Player) -> list[Action]:
    actions: Set[tuple[int, int]] = set()  # On utilise un ensemble pour garantir l'unicité
    res: List[Action] = []

    # On parcourt l'ensemble des cases de la grille
    for i, ligne in enumerate(grid):
        for j, element in enumerate(ligne):
            # Si la case est occupée par un jeton du player
            if element == player.number:
                neighbors = hex.hex_neighbor(i, j, player.directions)
                for neighbor in neighbors:
                    # Ajouter un voisin si
                    if grid[neighbor[0]][neighbor[1]] == 0:
                        actions.add(neighbor)
    for action in actions:
        res.append(Action(player.number, action))

    return res


def main():
    n = 7
    res = hex.grid_generation(n)
    hex.display_neighbors(hex.GRID2, 3, 3, UP_DIRECTIONS, n)
    print(legals(hex.GRID2, player1))

    pass


if __name__ == "__main__":
    main()
