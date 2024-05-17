""" Module regroupant l'ensemble des structures de données utilisées """
from typing import Union, Callable, List, Set
from dataclasses import dataclass
from Game_playing import hexagonal_board as hexa

# Types de base utilisés par l'arbitre

Cell = tuple[int, int]
ActionDodo = tuple[Cell, Cell]  # case de départ → case d'arrivée
ActionGopher = Cell
Action = Union[ActionGopher, ActionDodo]
# Player = int  # 1 ou 2
State = list[tuple[Cell, int]]  # État du jeu pour la boucle de jeu
Grid = tuple[tuple[int, ...], ...]  # Array de Array en diagonal
Directions = list[tuple[int, int]]  # Liste de directions
Score = int
Time = int

# Quelques constantes
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


""" Module concernant l'environnement du jeu Gopher-Dodo """


# DataClass Player
@dataclass
class Player:
    """ Classe représentant un joueur """
    id: int
    directions: Directions


# DataClass Game Dodo
@dataclass
class GameDodo:
    """ Classe représentant le jeu Dodo """
    state: State
    # grid: Grid
    max_player: Player
    min_player: Player
    hex_size: int
    total_time: Time
    max_positions: State
    min_positions: State

    # Fonction retournant les actions possibles d'un joueur pour un état donné (voir optimisation)
    def legals_dodo(self, grid: Grid, player: Player) -> list[ActionDodo]:
        actions: Set[ActionDodo] = set()  # On utilise un ensemble pour garantir l'unicité

        # On parcourt l'ensemble des cases de la grille
        for i, ligne in enumerate(grid):
            for j, element in enumerate(ligne):
                # Si la case est occupée par un jeton du player
                if element == player.id:
                    neighbors = hexa.hex_neighbor(i, j, player.directions)
                    for neighbor in neighbors:
                        # Ajouter un voisin si
                        r = neighbor[0]
                        q = neighbor[1]
                        if 0 <= r < len(grid) and 0 <= q < len(grid[0]):
                            if grid[neighbor[0]][neighbor[1]] == 0:
                                actions.add(((i, j), neighbor))

        return list(actions)

    # Fonction retournant le score si nous sommes dans un état final (fin de partie)
    def final_dodo(self, grid: Grid, debug: bool = False) -> int:
        if not self.legals_dodo(grid, self.max_player):
            if debug:
                print(self.legals_dodo(grid, self.max_player))
            return 1
        elif not self.legals_dodo(grid, self.min_player):
            if debug:
                print(self.legals_dodo(grid, self.min_player))
            return -1
        else:
            return 0

    def play_dodo(self, player: Player, grid: Grid, action: ActionDodo) -> Grid:
        temp_grid: list[list[int, ...], ...] = hexa.grid_tuple_to_grid_list(grid)
        temp_grid[action[0][0]][action[0][1]] = 0
        temp_grid[action[1][0]][(action[1][1])] = player.id
        return hexa.grid_list_to_grid_tuple(temp_grid)


@dataclass
class GameGopher:
    pass


Environment = GameDodo
Strategy = Callable[[Environment, Player, Grid], Action]
