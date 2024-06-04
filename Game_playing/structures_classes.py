""" Module regroupant l'ensemble des structures de données utilisées """

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union, NamedTuple
from collections import namedtuple

import Game_playing.hexagonal_board as hexa
from Dodo.grid import GRID2, INIT_GRID, INIT_GRID4

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
    (-1, 0),
    (-1, -1),
    (0, -1)
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


GridDict = dict[Cell, int]
max_positions_cr = namedtuple("max_position", ["player", "positions"])
min_positions_cr = namedtuple("min_position", ["player", "positions"])


# DataClass Game Dodo
@dataclass
class GameDodo:
    """Classe représentant le jeu Dodo"""

    # state: State
    grid: GridDict
    max_player: Player
    min_player: Player
    current_player: Player
    hex_size: int
    total_time: Time
    max_positions = max_positions_cr(
        player=Player(1, DOWN_DIRECTIONS),
        positions={}
    )
    min_positions = min_positions_cr(
        player=Player(2, UP_DIRECTIONS),
        positions={}
    )

    # Initialisation des positions des joueurs
    def __post_init__(self):
        for cell in self.grid:
            if self.grid[cell] == self.max_player.id:
                self.max_positions.positions[cell] = self.max_player.id
            elif self.grid[cell] == self.min_player.id:
                self.min_positions.positions[cell] = self.min_player.id
        #self.max_positions.player = self.max_player
        #self.min_positions.player = self.min_player

    # Fonction retournant les actions possibles d'un joueur pour un état donné (voir optimisation)
    def legals_dodo(self, player: Player) -> list[ActionDodo]:
        """
        Fonction retournant les actions possibles d'un joueur pour un état donné
        """
        actions: Dict[ActionDodo, Any] = (
            {}
        )

        if player.id == self.max_positions.player.id:
            positions = self.max_positions.positions
        else:
            positions = self.min_positions.positions

        for position in positions:
            neighbors = hexa.neighbor_gopher(position[0], position[1], player.directions)
            for neighbor in neighbors:
                r = neighbor[0]
                q = neighbor[1]
                if -self.hex_size <= r <= self.hex_size and -self.hex_size <= q <= self.hex_size:
                    if self.grid[neighbor] == EMPTY:  # problème ici
                        if (position, neighbor) not in actions:
                            actions[(position, neighbor)] = None
        return list(actions.keys())

    # Fonction retournant le score si nous sommes dans un état final (fin de partie)
    def final_dodo(self, debug: bool = False) -> int:
        """
        Fonction retournant le score si nous sommes dans un état final (fin de partie)
        """
        if not self.legals_dodo(self.max_positions.player):
            if debug:
                print(self.legals_dodo(self.max_positions.player))
            return 1
        if not self.legals_dodo(self.min_positions.player):
            if debug:
                print(self.legals_dodo(self.min_positions.player))
            return -1
        return 0

    def play_dodo(self, action: ActionDodo) -> None:
        """
        Fonction jouant un coup pour un joueur donné
        """
        self.grid[action[1]] = self.current_player.id
        self.grid[action[0]] = 0

        # Mise à jour des positions des joueurs
        if self.current_player.id == self.max_positions.player.id:
            self.max_positions.positions.pop(action[0])
            self.max_positions.positions[action[1]] = self.current_player.id
        else:
            self.min_positions.positions.pop(action[0])
            self.min_positions.positions[action[1]] = self.current_player.id



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
        self.grid[action] = self.current_player.id

        # Mise à jour des positions des joueurs
        if self.current_player.id == self.max_player.id:
            self.max_positions[action] = self.current_player.id
        else:
            self.min_positions[action] = self.current_player.id


Environment = GameDodo | GameGopher
Strategy = Callable[[Environment, Player, GridDict, dict], Action]

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


def print_dodo(env: GameDodo, empty_grid: Grid):
    """
    Fonction permettant d'afficher une grille de jeu Dodo
    """
    temp_grid = hexa.grid_tuple_to_grid_list(empty_grid)
    for position in env.max_positions.positions:
        print(position)
        conv_pos = hexa.reverse_convert(position[0], position[1], env.hex_size)
        temp_grid[conv_pos[0]][conv_pos[1]] = 1
    for position, _ in env.max_positions.positions.items():
        conv_pos = hexa.reverse_convert(position[0], position[1], env.hex_size)
        temp_grid[conv_pos[0]][conv_pos[1]] = 2

    hexa.display_grid(hexa.grid_list_to_grid_tuple(temp_grid))


def convert_grid(grid: Grid, hex_size: int) -> GridDict:
    new_gopher(hex_size)
    res: GridDict = {}
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i][j] != -1:
                coord = hexa.convert(i, j, hex_size)
                res[coord] = grid[i][j]
    return res

