""" Module concernant l'environnement du jeu Gopher-Dodo """
from dataclasses import dataclass

from structures import *
from typing import Dict, List, Set, Tuple
from Game_playing import hexagonal_board as hexa
from Game_playing.grid import *
from Game_playing.structures import *



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
    def legals_dodo(self, player: Player, grid: Grid) -> List[ActionDodo]:
        actions: Set[ActionDodo] = set()
        # On parcourt l'ensemble des cases de la grille
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                # Si la case est occupée par un jeton du player
                if cell == player.id:
                    for ni, nj in hexa.hex_neighbor(i, j, player.directions):
                        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] == EMPTY:
                            actions.add(((i, j), (ni, nj)))
        return list(actions)

    # Fonction retournant le score si nous sommes dans un état final (fin de partie)
    def final_dodo(self, grid: Grid) -> int:
        if not self.legals_dodo(self.max_player, grid):
            return 1
        elif not self.legals_dodo(self.min_player, grid):
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


