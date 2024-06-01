""" Module concernant l'environnement du jeu Gopher-Dodo """

import os
import time
import pickle

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd  # type: ignore

matplotlib.use("TkAgg")
from structures_classes import *
from Dodo.grid import *
from Dodo.strategies_dodo import (
    strategy_random_dodo,
    strategy_minmax,
)


# Function to save the library to a file
def save_library(library, filename):
    with open(filename, "wb") as file:
        pickle.dump(library, file)


# Function to load the library from a file
def load_library(filename):
    with open(filename, "rb") as file:
        library = pickle.load(file)
    return library


def read_plk(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


# Boucle de jeu Dodo
def dodo(
        env: GameDodo,
        strategy_1: Strategy,
        strategy_2: Strategy,
        init_grid: Grid,
        debug: bool = False,
        starting_library: Dict = None,
        building_library: bool = False,
        graphics: bool = False,
        library: bool = False,
) -> dict[str, int | float | Any]:
    """
    Fonction représentant la boucle de jeu de Dodo
    """
    time_history: List[float] = []
    actual_grid: Grid = init_grid
    current_player: Player = env.max_player
    current_action: Action
    tour: int = 0
    total_time_start = time.time()  # Chronomètre

    # Permet d'éviter d'avoir une valeur par défaut mutable
    if starting_library is None:
        starting_library = {}

    # Permet de tester nos stratégies sans la librairie
    if library:
        if starting_library == {}:
            try:  # On essaie de charger la librairie de coups de départ
                starting_library = load_library("starting_library.pkl")
            except FileNotFoundError:
                starting_library = {}
    else:
        starting_library = None

    res = env.final_dodo(actual_grid)
    while not (res == 1 or res == -1):
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        if debug and current_player.id == 1:
            print(f"Tour \033[36m {tour}\033[0m.")
        if current_player.id == 1:
            tour += 1
            current_action = strategy_1(
                env, current_player, actual_grid, starting_library
            )
            if building_library:
                if hash(actual_grid) not in starting_library.keys() and tour < 100:
                    # print(f"Adding {hash(actual_grid)} to the library")
                    starting_library[hash(actual_grid)] = {"action": current_action[0]}
        else:
            current_action = strategy_2(
                env, current_player, actual_grid, starting_library
            )

        actual_grid = env.play_dodo(current_player, actual_grid, current_action)

        iteration_time_end = (
            time.time()
        )  # Fin du chronomètre pour la durée de cette itération
        if current_player.id == 1:
            time_history.append(iteration_time_end - iteration_time_start)

        if current_player.id == 1:
            current_player = env.min_player
        else:
            current_player = env.max_player

        if debug:
            hexa.display_grid(actual_grid)

        if debug:
            print(
                f"Temps écoulé pour cette itération: {iteration_time_end - iteration_time_start}"
                f" secondes"
            )

        res = env.final_dodo(actual_grid)

    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie
    if graphics:
        print(f"Temps total écoulé: {total_time_end - total_time_start} secondes")
        plt.plot(time_history)
        plt.ylabel("Temps d'itération (s)")
        plt.xlabel("Itération")
        plt.title("Temps d'itération en fonction de l'itération")
        plt.show()
    if building_library:
        save_library(starting_library, "starting_library.pkl")

    # Retourne un dictionnaire contenant les informations de la partie (benchmarking)
    return {
        "average_iteration_time": (
            sum(time_history) / len(time_history) if time_history else 0
        ),
        "total_turns": tour,
        "total_time": total_time_end - total_time_start,
        "winner": env.final_dodo(actual_grid),
    }


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
            state, player, Player(2, UP_DIRECTIONS), hex_size, total_time, [], []
        )


def append_to_csv(dataframe: pd.DataFrame, filename: str):
    """
    Fonction permettant d'ajouter une ligne à un fichier CSV
    """
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    path_file = os.path.join(parent_dir, "Benchmarks", filename)

    # Vérifier si le fichier existe
    file_exists = os.path.isfile(path_file)

    # Créer le dossier Benchmarks s'il n'existe pas déjà
    os.makedirs(os.path.dirname(path_file), exist_ok=True)

    # Écrire dans le fichier
    with open(path_file, "a", newline="", encoding="utf-8") as f:
        if not file_exists:
            dataframe.to_csv(f, header=True, index=False)
        else:
            dataframe.to_csv(f, header=False, index=False)


def add_to_benchmark(
        list_results,
        filename: str,
        game_number: int,
        strategy_1: str,
        strategy_2: str,
        grid: int,
        depth: int,
        starting_library: bool,
):
    """
    Fonction permettant d'ajouter les statistiques d'une partie à un fichier CSV
    """
    win_number = sum(res['winner'] == 1 for res in list_results)
    loss_number = game_number - win_number
    new_benchmark = {
        "strategy_1": strategy_1,
        "strategy_2": strategy_2,
        "Grid": grid,
        "depth": depth,
        "game_number": game_number,
        "starting_library": starting_library,
        "win_rate": sum(res["winner"] == 1 for res in list_results) / game_number,
        "average_turns": sum(res["total_turns"] for res in list_results)
                         / game_number,
        "min_turns": min(res["total_turns"] for res in list_results),
        "max_turns": max(res["total_turns"] for res in list_results),
        "average_iteration_time": sum(
            res["average_iteration_time"] for res in list_results)
                                  / game_number,
        "average_total_time": sum(res["total_time"] for res in list_results)
                              / game_number,
        "average_turns_win": (
            (sum(res["total_turns"] for res in list_results if res["winner"] == 1)
             / win_number)
            if win_number > 0
            else 0
        ),
        "average_turns_loss": (
            (
                    sum(res["total_turns"] for res in list_results if res["winner"] == -1)
                    / loss_number
            )
            if loss_number > 0
            else 0
        ),
    }

    # Créer un DataFrame avec une seule ligne
    df_results = pd.DataFrame([new_benchmark])
    print(df_results)
    append_to_csv(df_results, f"{filename}.csv")


def launch_multi_game(game_number: int = 1):
    """
    Fonction permettant de lancer plusieurs parties de jeu
    """
    # Liste pour stocker les résultats des parties
    list_results = []
    player1: Player = Player(1, DOWN_DIRECTIONS)
    size_init_grid = 4
    init_grid = INIT_GRID4
    for i in range(game_number):
        game = initialize("Dodo", init_grid, player1, 4, 5)
        print(len(game.legals_dodo(init_grid, player1)))
        res = dodo(
            game,
            strategy_minmax,
            strategy_random_dodo,
            init_grid,
            debug=True,
            building_library=False,
            graphics=False,
            library=False,
        )
        list_results.append(res)
        print(f"Partie {i + 1}: {res}")

    # Ajout des stat à un fichier CSV
    add_to_benchmark(
        list_results,
        "benchmark",
        game_number,
        "strategy_minmax",
        "strategy_random_dodo",
        size_init_grid,
        5,
        False,
    )


# Fonction principale de jeu Dodo
def main():
    """
    Fonction principale de jeu Dodo
    """

    launch_multi_game(100)


if __name__ == "__main__":
    main()
