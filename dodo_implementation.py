# Module concernant la réalisation du jeu DoDo

from typing import List, NamedTuple, Set
from collections import namedtuple
import hexagonal_board as hex

# Structures de données
State = hex.Grid

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


# Initialisation Grille DoDo
def init_grid_dodo(n: int) -> hex.Grid:
    grid: hex.Grid = hex.grid_generation(n)


# Règles du DoDo

# Fonction retournant les actions possibles d'un joueur pour un état donné
# À optimiser pour améliorer la complexité
def legals_dodo(grid: State, player: Player, directions) -> list[ActionDodo]:
    actions: Set[ActionDodo] = set()  # On utilise un ensemble pour garantir l'unicité

    # On parcourt l'ensemble des cases de la grille
    for i, ligne in enumerate(grid):
        for j, element in enumerate(ligne):
            # Si la case est occupée par un jeton du player
            if element == player:
                neighbors = hex.hex_neighbor(i, j, directions)
                for neighbor in neighbors:
                    # Ajouter un voisin si
                    if grid[neighbor[0]][neighbor[1]] == 0:
                        actions.add(((i, j), neighbor))

    return list(actions)


def main():
    n = 7
    res = hex.grid_generation(n)
    hex.display_neighbors(hex.GRID2, 3, 3, UP_DIRECTIONS, n)
    print(legals_dodo(hex.GRID2, player1, UP_DIRECTIONS))

    pass


if __name__ == "__main__":
    main()
