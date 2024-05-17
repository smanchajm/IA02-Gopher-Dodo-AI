""" Module concernant l'environnement du jeu Gopher-Dodo """
from dataclasses import dataclass

from Dodo.dodo_implementation import EMPTY, UP_DIRECTIONS
from structures import *
import random
import time
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


Environment = GameDodo


# Boucle de jeu Dodo
def dodo(
        env: GameDodo, strategy_1: Strategy, strategy_2: Strategy, init_grid: Grid, debug: bool = False
) -> Score:
    actual_grid: Grid = init_grid
    current_player: Player = 1
    current_action: Action
    nb_iterations: int = 0
    total_time_start = time.time()  # Chronomètre

    while not (env.final_dodo(actual_grid) == 1 or env.final_dodo(actual_grid) == -1):
        nb_iterations += 1
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        print(f"Iteration \033[36m {nb_iterations}\033[0m.")
        hexa.display_grid(actual_grid)
        if current_player == 1:
            current_action = strategy_1(actual_grid, current_player)
        else:
            current_action = strategy_2(actual_grid, current_player)
        actual_grid = env.play_dodo(current_player, actual_grid, current_action)
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1

        iteration_time_end = time.time()  # Fin du chronomètre pour la durée de cette itération
        print(f"Temps écoulé pour cette itération: {iteration_time_end - iteration_time_start} secondes")

    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie
    print(f"Temps total écoulé: {total_time_end - total_time_start} secondes")

    return env.final_dodo(actual_grid)


# Initialisation de l'environnement
def initialize(game: str, state: State, player: Player, hex_size: int, total_time: Time) -> Environment:
    if game == "Dodo":
        max_positions: State = []
        min_positions: State = []
        for cell, sel_player in state:
            if sel_player == player.id:
                max_positions.append((cell, player.id))
            else:
                min_positions.append((cell, player.id))
        return GameDodo(state, player, Player(2, UP_DIRECTIONS), hex_size, total_time, max_positions, min_positions)
    if game == "Gopher":
        pass
        # return GameGopher(state, player, Player(2, UP_DIRECTIONS), hex_size, total_time)
    else:
        raise ValueError("Jeu non reconnu")

