""" Module concernant l'environnement du jeu Gopher-Dodo """
import time
import matplotlib.pyplot as plt
from Game_playing.hexagonal_board import display_grid
from structures_classes import *
from Dodo.grid import *
from Dodo.strategies_dodo import (
    strategy_random_dodo,
    strategy_minmax,
)

import pickle

# Function to save the library to a file
def save_library(library, filename):
    with open(filename, 'wb') as file:
        pickle.dump(library, file)

# Function to load the library from a file
def load_library(filename):
    with open(filename, 'rb') as file:
        library = pickle.load(file)
    return library


# Boucle de jeu Dodo
def dodo(
    env: GameDodo,
    strategy_1: Strategy,
    strategy_2: Strategy,
    init_grid: Grid,
    debug: bool = False,
    starting_library: dict = {},
    building_library: bool = False
) -> Score:
    """
    Fonction représentant la boucle de jeu de Dodo
    """
    time_history: list[Time] = []
    actual_grid: Grid = init_grid
    current_player: Player = env.max_player
    current_action: Action
    nb_iterations: int = 0
    total_time_start = time.time()  # Chronomètre

    if starting_library == {}:
        try: # On essaie de charger la librairie de coups de départ
            starting_library = load_library('starting_library.pkl')
        except FileNotFoundError:
            starting_library = {}

    while not (env.final_dodo(actual_grid) == 1 or env.final_dodo(actual_grid) == -1):
        nb_iterations += 1
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        if debug:
            print(f"Iteration \033[36m {nb_iterations}\033[0m.")
        if current_player.id == 1:
            current_action = strategy_1(env, current_player, actual_grid, starting_library)
            if building_library:
                if hash(actual_grid) not in starting_library.keys():
                    # print(f"Adding {hash(actual_grid)} to the library")
                    starting_library[hash(actual_grid)] = {'action': current_action[0]}
        else:
            current_action = strategy_2(env, current_player, actual_grid)
        actual_grid = env.play_dodo(current_player, actual_grid, current_action)
        if current_player.id == 1:
            current_player = env.min_player
        else:
            current_player = env.max_player

        if debug:
            hexa.display_grid(actual_grid)

        iteration_time_end = (
            time.time()
        )  # Fin du chronomètre pour la durée de cette itération
        if debug:
            print(
                f"Temps écoulé pour cette itération: {iteration_time_end - iteration_time_start}"
                f" secondes")
        time_history.append(iteration_time_end - iteration_time_start)

    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie
    if debug:
        print(f"Temps total écoulé: {total_time_end - total_time_start} secondes")
        plt.plot(time_history)
        plt.ylabel("Temps d'itération (s)")
        plt.xlabel("Itération")
        plt.title("Temps d'itération en fonction de l'itération")
        plt.show()
    if building_library:
        save_library(starting_library, 'starting_library.pkl')
    return env.final_dodo(actual_grid)


def read_plk(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


# Initialisation de l'environnement
def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Environment:
    """
    Fonction permettant d'initialiser l'environnement de jeu
    """
    if game == "Dodo":
        max_positions: State = []
        min_positions: State = []
        for cell in state:
            if cell[1] == player.id:
                max_positions.append((cell[0], player.id))
            else:
                min_positions.append((cell[0], player.id))
        return GameDodo(
            state,
            player,
            Player(2, UP_DIRECTIONS),
            hex_size,
            total_time,
            max_positions,
            min_positions,
        )
    if game == "Gopher":
        return GameDodo(
            state,
            player,
            Player(2, UP_DIRECTIONS),
            hex_size,
            total_time,
            [],
            []
        )


# Fonction principale de jeu Dodo
def main():
    """
    Fonction principale de jeu Dodo
    """
    player1 = Player(1, DOWN_DIRECTIONS)
    game = initialize("Dodo", INIT_GRID, player1, 4, 5)
    print(dodo(game, strategy_minmax, strategy_random_dodo, INIT_GRID, False, building_library=True))
    starting_library = load_library('starting_library.pkl')
    print(len(starting_library))

if __name__ == "__main__":
    main()
