""" Module regroupant l'ensemble des structures de données utilisées """

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union

import Game_playing.hexagonal_board as hexa

# Types de base utilisés par l'arbitre

Cell = tuple[int, int]
ActionDodo = tuple[Cell, Cell]  # case de départ → case d'arrivée
ActionGopher = Cell
Action = Union[ActionGopher, ActionDodo]
Player2 = int  # 1 ou 2
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

ALL_DIRECTIONS: List[tuple[int, int]] = [
    (0, -1),
    (-1, -1),
    (-1, 0),
    (1, 0),
    (1, 1),
    (0, 1),
]

""" Module concernant l'environnement du jeu Gopher-Dodo """


# DataClass Player
@dataclass
class Player:
    """Classe représentant un joueur"""

    id: int
    directions: Directions


GridDict = dict[Cell, Player]


# DataClass Game Dodo
@dataclass
class GameDodo:
    """Classe représentant le jeu Dodo"""

    # state: State
    grid: Grid
    max_player: Player
    min_player: Player
    hex_size: int
    total_time: Time
    max_positions: State
    min_positions: State

    # Fonction retournant les actions possibles d'un joueur pour un état donné (voir optimisation)
    def legals_dodo(self, grid: Grid, player: Player) -> list[ActionDodo]:
        """
        Fonction retournant les actions possibles d'un joueur pour un état donné
        """
        actions: Dict[ActionDodo, Any] = (
            {}
        )  # On utilise un ensemble pour garantir l'unicité

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
                                if ((i, j), neighbor) not in actions:
                                    actions[((i, j), neighbor)] = None

        return list(actions.keys())

    # Fonction retournant le score si nous sommes dans un état final (fin de partie)
    def final_dodo(self, grid: Grid, debug: bool = False) -> int:
        """
        Fonction retournant le score si nous sommes dans un état final (fin de partie)
        """
        if not self.legals_dodo(grid, self.max_player):
            if debug:
                print(self.legals_dodo(grid, self.max_player))
            return 1
        if not self.legals_dodo(grid, self.min_player):
            if debug:
                print(self.legals_dodo(grid, self.min_player))
            return -1
        return 0

    def play_dodo(self, player: Player, grid: Grid, action: ActionDodo) -> Grid:
        """
        Fonction jouant un coup pour un joueur donné
        """
        temp_grid: List[list[int]] = hexa.grid_tuple_to_grid_list(grid)
        temp_grid[action[0][0]][action[0][1]] = 0
        temp_grid[action[1][0]][(action[1][1])] = player.id
        return hexa.grid_list_to_grid_tuple(temp_grid)


@dataclass
class GameGopher:
    """Classe représentant le jeu Gopher"""

    grid: GridDict
    max_player: Player
    min_player: Player
    current_player: Player
    hex_size: int
    total_time: Time
    max_positions: GridDict
    min_positions: GridDict

    def legals_gopher(self, grid: GridDict, player: Player) -> list[ActionGopher]:
        """
        Fonction retournant les actions possibles d'un joueur pour un état donné
        """
        result: List[ActionGopher] = []

        # Premier coup
        if len(self.max_positions) == 0 and len(self.min_positions) == 0:
            for position in grid:
                result.append(position)
            return result

        player_positions = (
            self.max_positions if player == self.max_player else self.min_positions
        )
        opponent_positions = (
            self.min_positions if player == self.max_player else self.max_positions
        )

        for position in opponent_positions.keys():
            neighbors = hexa.neighbor_gopher(
                position[0], position[1], player.directions
            )
            for neighbor in neighbors:
                if neighbor in grid:
                    if grid[neighbor] == 0:
                        if neighbor in result:
                            result.remove(neighbor)
                        else:
                            result.append(neighbor)

        for position in player_positions.keys():
            neighbors = hexa.neighbor_gopher(
                position[0], position[1], player.directions
            )
            for neighbor in neighbors:
                if neighbor in grid:
                    if neighbor in result:
                        result.remove(neighbor)

        return result

    def final_gopher(self, grid: GridDict, debug: bool = False) -> int:
        """
        Fonction retournant le score si nous sommes dans un état final (fin de partie)
        """
        if self.current_player == self.max_player and not self.legals_gopher(
            grid, self.current_player
        ):
            if debug:
                print(self.legals_gopher(grid, self.max_player))
            return 1
        if self.current_player == self.min_player and not self.legals_gopher(
            grid, self.current_player
        ):
            if debug:
                print(self.legals_gopher(grid, self.min_player))
            return -1
        return 0

    def play_gopher(self, action: ActionGopher):
        """
        Fonction jouant un coup pour un joueur donné
        :param action:
        :return:
        """
        self.grid[action] = self.current_player

        # Mise à jour des positions des joueurs
        if self.current_player.id == self.max_player.id:
            self.max_positions[action] = self.current_player
        else:
            self.min_positions[action] = self.current_player


Environment = GameDodo | GameGopher
Strategy = Callable[[Environment, Player, Grid, dict], Action]

StrategyGopher = Callable[[Environment, Player, GridDict, dict], Action]


def new_gopher(h: int) -> GridDict:
    """
    Fonction permettant de créer une nouvelle grille de jeu pour Gopher
    """
    h = h - 1  # pour avoir un plateau de taille h
    res: GridDict = {}
    for r in range(h, -h - 1, -1):
        qmin = max(-h, r - h)
        qmax = min(h, r + h)
        for q in range(qmin, qmax + 1):
            res[(q, r)] = EMPTY
    return res
