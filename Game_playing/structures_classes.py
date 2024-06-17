""" Module regroupant l'ensemble des structures de données utilisées """

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union
from collections import namedtuple
from abc import ABC, abstractmethod

import Game_playing.hexagonal_board as hexa

# Types de base utilisés par l'arbitre

Cell = tuple[int, int]
ActionDodo = tuple[Cell, Cell]  # case de départ → case d'arrivée
ActionGopher = Cell
Action = Union[ActionGopher, ActionDodo]
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

DOWN_DIRECTIONS: List[tuple[int, int]] = [(-1, 0), (-1, -1), (0, -1)]

ALL_DIRECTIONS: List[tuple[int, int]] = [
    (0, -1),
    (-1, -1),
    (-1, 0),
    (1, 0),
    (1, 1),
    (0, 1),
]


# DataClass PlayerLocal
@dataclass
class PlayerLocal:
    """
    Classe représentant un joueur
    """
    id: int
    directions: Directions


# Initialisation des struct de données
GridDict = dict[Cell, int]
MaxPositionsCr = namedtuple("max_position", ["player", "positions"])
MinPositionsCr = namedtuple("min_position", ["player", "positions"])


@dataclass
class Environment(ABC):
    """Classe représentant un jeu"""

    grid: GridDict
    max_player: PlayerLocal
    min_player: PlayerLocal
    current_player: PlayerLocal
    hex_size: int
    total_time: Time

    @abstractmethod
    def legals(self, player: PlayerLocal) -> list[Action]:
        """
        Fonction retournant les actions possibles d'un joueur pour un état donné
        """

    @abstractmethod
    def final(self, debug: bool = False) -> int:
        """
        Fonction retournant le score si nous sommes dans un état final (fin de partie)
        """

    @abstractmethod
    def play(self, action: Action):
        """
        Fonction jouant un coup pour un joueur donné
        """

    @abstractmethod
    def reverse_action(self, action: Action):
        """
        Fonction annulant un coup pour un joueur donné
        """


# DataClass Game Dodo

@dataclass
class GameDodo(Environment):
    """Classe représentant le jeu Dodo"""

    # Initialisation des positions des joueurs
    def __post_init__(self):
        super().__init__(
            self.grid,
            self.max_player,
            self.min_player,
            self.current_player,
            self.hex_size,
            self.total_time,
        )

        self.max_positions = MaxPositionsCr(player=self.max_player, positions={})
        self.min_positions = MinPositionsCr(player=self.min_player, positions={})

        self.max_positions.positions.clear()
        self.min_positions.positions.clear()
        for cell in self.grid:
            if self.grid[cell] == self.max_player.id:
                self.max_positions.positions[cell] = self.max_player.id
            elif self.grid[cell] == self.min_player.id:
                self.min_positions.positions[cell] = self.min_player.id

    # Fonction retournant les actions possibles d'un joueur pour un état donné (voir optimisation)
    def legals(self, player: PlayerLocal) -> list[ActionDodo]:
        """
        Fonction retournant les actions possibles d'un joueur pour un état donné
        """
        actions: Dict[ActionDodo, Any] = {}

        if player.id == self.max_positions.player.id:
            positions = self.max_positions.positions
        else:
            positions = self.min_positions.positions

        # Recherche des coups légaux
        for position in positions:
            neighbors = hexa.neighbor_gopher(
                position[0], position[1], player.directions
            )
            for neighbor in neighbors:
                r = neighbor[0]
                q = neighbor[1]
                if (r, q) in self.grid:
                    if self.grid[neighbor] == EMPTY:  # problème ici
                        if (position, neighbor) not in actions:
                            actions[(position, neighbor)] = None
        return list(actions.keys())

    # Fonction retournant le score si nous sommes dans un état final (fin de partie)
    def final(self) -> int:
        """
        Fonction retournant le score si nous sommes dans un état final (fin de partie)
        """
        if not self.legals(self.max_positions.player):
            return 1
        if not self.legals(self.min_positions.player):
            return -1
        return 0

    def play(self, action: ActionDodo) -> None:
        """
        Fonction jouant un coup pour un joueur donné
        """

        # Mise à jour de la grille
        self.grid[action[1]] = self.current_player.id
        self.grid[action[0]] = 0

        # Debug

        # if (
        #     action[0] not in self.max_positions.positions
        #     and self.current_player.id == self.max_positions.player.id
        # ):
        #     print(f"action :{action}")
        #     print(f" error action[0]:{action[0]}")
        #     print(f" error action[1]:{action[1]}")
        #     print(f" error pos:{self.max_positions.positions}")

        # Mise à jour des positions des joueurs
        if self.current_player.id == self.max_positions.player.id:
            del self.max_positions.positions[action[0]]
            self.max_positions.positions[action[1]] = self.current_player.id
        else:
            del self.min_positions.positions[action[0]]
            self.min_positions.positions[action[1]] = self.current_player.id

        # Changement de joueur
        self.current_player = (
            self.min_player
            if self.current_player == self.max_player
            else self.max_player
        )

    def reverse_action(self, action: ActionDodo):
        """
        Fonction annulant un coup pour un joueur donné
        """
        # Changement de joueur
        self.current_player = (
            self.min_player
            if self.current_player == self.max_player
            else self.max_player
        )

        # Mise à jour de la grille
        self.grid[action[0]] = self.current_player.id
        self.grid[action[1]] = EMPTY

        # Mise à jour des positions des joueurs
        if self.current_player.id == self.min_positions.player.id:
            self.min_positions.positions.pop(action[1])
            self.min_positions.positions[action[0]] = self.min_positions.player.id
        else:
            self.max_positions.positions.pop(action[1])
            self.max_positions.positions[action[0]] = self.max_positions.player.id

    def reverse_action_player(self, action: ActionDodo, _: PlayerLocal):
        """
        Fonction annulant un coup pour un joueur donné
        """

        # Mise à jour de la grille
        self.grid[action[0]] = self.current_player.id
        self.grid[action[1]] = EMPTY

        # Mise à jour des positions des joueurs
        if self.current_player.id == self.max_positions.player.id:
            self.min_positions.positions.pop(action[1])
            self.min_positions.positions[action[0]] = self.min_positions.player.id
        else:
            self.max_positions.positions.pop(action[1])
            self.max_positions.positions[action[0]] = self.max_positions.player.id

        # Changement de joueur
        self.current_player = (
            self.min_player
            if self.current_player == self.max_player
            else self.max_player
        )


@dataclass
class GameGopher(Environment):
    """Classe représentant le jeu Gopher"""

    # Initialisation des positions des joueurs
    def __post_init__(self):
        super().__init__(
            self.grid,
            self.max_player,
            self.min_player,
            self.current_player,
            self.hex_size,
            self.total_time,
        )

        self.neighbor_dict = {}
        for cell in self.grid:
            neighbors = hexa.neighbor_gopher(cell[0], cell[1], ALL_DIRECTIONS)
            l = []
            for neighbor in neighbors:
                if neighbor in self.grid:
                    l.append(neighbor)
            self.neighbor_dict[cell] = l

        self.max_positions = MaxPositionsCr(player=self.max_player, positions={})
        self.min_positions = MinPositionsCr(player=self.min_player, positions={})
        self.max_positions.positions.clear()
        self.min_positions.positions.clear()

        for cell in self.grid:
            if self.grid[cell] == self.max_player.id:
                self.max_positions.positions[cell] = self.max_player.id
            elif self.grid[cell] == self.min_player.id:
                self.min_positions.positions[cell] = self.min_player.id

    def legals(self, player: PlayerLocal) -> list[ActionGopher]:
        result: list[ActionGopher] = []

        if (
                len(self.max_positions.positions) == 0
                and len(self.min_positions.positions) == 0
        ):
            for position in self.grid:
                result.append(position)
            return result

        opponent_positions = (
            self.min_positions.positions
            if player == self.max_player
            else self.max_positions.positions
        )

        oponnent_player = self.min_player if player == self.max_player else self.max_player

        for position in opponent_positions.keys():
            moves = []
            for neighbor in self.neighbor_dict[position]:
                # print(f"neighbor: {neighbor}")
                if self.grid[neighbor] == 0:
                    moves.append(neighbor)

            for move in moves:
                enemy: int = 0
                friendly: int = 0
                for neighbor in self.neighbor_dict[move]:
                    if self.grid[neighbor] == player.id:
                        friendly += 1
                    elif self.grid[neighbor] == oponnent_player.id:
                        enemy += 1
                if friendly == 0 and enemy == 1:
                    result.append(move)

        return result

    def final(self, debug: bool = False) -> int:
        """
        Fonction retournant le score si nous sommes dans un état final (fin de partie)
        """
        if not self.legals(self.max_positions.player) and self.max_positions.player.id == self.current_player.id:
            return -1
        if not self.legals(self.min_positions.player) and self.min_positions.player.id == self.current_player.id:
            return 1
        return 0

    def play(self, action: ActionGopher):
        """
        Fonction jouant un coup pour un joueur donné
        :param action:
        :return:
        """

        self.grid[action] = self.current_player.id

        # Mise à jour des positions des joueurs
        if self.current_player.id == self.max_player.id:
            self.max_positions.positions[action] = self.current_player.id
        else:
            self.min_positions.positions[action] = self.current_player.id

        # Changement de joueur
        self.current_player = (
            self.min_player
            if self.current_player == self.max_player
            else self.max_player
        )

    def reverse_action(self, action: ActionGopher):
        """
        Fonction annulant un coup pour un joueur donné
        """

        # Changement de joueur
        self.current_player = (
            self.min_player
            if self.current_player == self.max_player
            else self.max_player
        )

        # Mise à jour de la grille
        self.grid[action] = 0

        # Mise à jour des positions des joueurs
        if self.current_player.id == self.min_positions.player.id:
            self.min_positions.positions.pop(action)
        else:
            self.max_positions.positions.pop(action)


Strategy = Callable[[Environment, PlayerLocal, GridDict, dict], Action]


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
        conv_pos = hexa.reverse_convert(position[0], position[1], env.hex_size)
        temp_grid[conv_pos[0]][conv_pos[1]] = 1
    for position in env.min_positions.positions:
        conv_pos = hexa.reverse_convert(position[0], position[1], env.hex_size)
        temp_grid[conv_pos[0]][conv_pos[1]] = 2
    hexa.display_grid(hexa.grid_list_to_grid_tuple(temp_grid))


def convert_grid(grid: Grid, hex_size: int) -> GridDict:
    """
    Fonction permettant de convertir une grille de jeu (tuple) en dictionnaire

    """

    new_gopher(hex_size)
    res: GridDict = {}
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i][j] != -1:
                coord = hexa.convert(i, j, hex_size)
                res[coord] = grid[i][j]
    return res
