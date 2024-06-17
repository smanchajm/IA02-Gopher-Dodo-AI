""" Module concernant l'environnement du jeu Gopher-Dodo """

import os
import time
from typing import Any, List

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from Game_playing.grid import GRID4, INIT_GRID4
from Dodo.strategies_dodo import (
    StrategyLocal,
    strategy_minmax,
    strategy_random,
)

import Game_playing.hexagonal_board as hexa
from Game_playing.hexagonal_board import Grid
from Game_playing.structures_classes import ALL_DIRECTIONS, DOWN_DIRECTIONS, \
    UP_DIRECTIONS, Action, GameDodo, GameGopher, GridDict, \
        PlayerLocal, Time, convert_grid, new_gopher, print_dodo

matplotlib.use("TkAgg")


# Boucle de jeu Dodo
def dodo(
    env: GameDodo,
    strategy_1: StrategyLocal,
    strategy_2: StrategyLocal,
    debug: bool = False,
    graphics: bool = False,
) -> dict[str, int | float | Any]:
    """
    Fonction représentant la boucle de jeu de Dodo
    """
    time_history: List[float] = []
    current_action: Action
    tour: int = 0
    total_time_start = time.time()  # Chronomètre
    res = env.final()
    while res not in (1, -1):
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        if debug and env.current_player.id == 1:
            print(f"Tour \033[36m {tour}\033[0m.")
        if env.current_player.id == 1:
            tour += 1
            current_action = strategy_1(
                env, env.current_player
            )
        else:
            current_action = strategy_2(
                env, env.current_player
            )
        env.play(current_action)

        iteration_time_end = (
            time.time()
        )  # Fin du chronomètre pour la durée de cette itération

        if debug:
            print_dodo(env, GRID4)

        if debug:
            print(
                f"Temps écoulé pour cette itération: {iteration_time_end - iteration_time_start}"
                f" secondes"
            )

        res = env.final()

    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie
    if graphics:
        print(f"Temps total écoulé: {total_time_end - total_time_start} secondes")
        plt.plot(time_history)
        plt.ylabel("Temps d'itération (s)")
        plt.xlabel("Itération")
        plt.title("Temps d'itération en fonction de l'itération")
        plt.show()

    # Retourne un dictionnaire contenant les informations de la partie (benchmarking)
    return {
        "average_iteration_time": (
            sum(time_history) / len(time_history) if time_history else 0
        ),
        "total_turns": tour,
        "total_time": total_time_end - total_time_start,
        "winner": env.final(),
    }


# Boucle de jeu Gopher
def gopher(
    env: GameGopher,
    strategy_1: StrategyLocal,
    strategy_2: StrategyLocal,
    debug: bool = False,
    graphics: bool = False,
) -> dict[str, int | float | Any]:
    """
    Fonction représentant la boucle de jeu de Gopher
    """
    time_history: List[float] = []
    current_action: Action
    tour: int = 0
    total_time_start = time.time()  # Chronomètre

    res = env.final()

    while res not in (1, -1):
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        if debug and env.current_player.id == 1:
            print(f"Tour \033[36m {tour}\033[0m.")
        if env.current_player.id == env.max_player.id:
            tour += 1
            current_action = strategy_1(
                env, env.current_player
            )
            env.play(current_action)
        else:
            current_action = strategy_2(
                env, env.current_player
            )
            env.play(current_action)

        iteration_time_end = (
            time.time()
        )  # Fin du chronomètre pour la durée de cette itération
        if env.current_player == env.max_player:
            time_history.append(iteration_time_end - iteration_time_start)

        if debug:
            print_gopher(env, GRID4)
            print(
                f"Temps écoulé pour cette itération: {iteration_time_end - iteration_time_start}"
                f" secondes"
            )

        if tour > 1:
            res = env.final()
            print(f"Winner: {res}")
        print(f"max {env.legals(env.max_player)}")
        print(f"min {env.legals(env.min_player)}")

    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie
    if graphics:
        print(f"Temps total écoulé: {total_time_end - total_time_start} secondes")
        plt.plot(time_history)
        plt.ylabel("Temps d'itération (s)")
        plt.xlabel("Itération")
        plt.title("Temps d'itération en fonction de l'itération")
        plt.show()

    # Retourne un dictionnaire contenant les informations de la partie (benchmarking)
    return {
        "average_iteration_time": (
            sum(time_history) / len(time_history) if time_history else 0
        ),
        "total_turns": tour,
        "total_time": total_time_end - total_time_start,
        "winner": env.final(),
    }


# Initialisation de l'environnement
def initialize(
    game: str, grid: GridDict, player: int, hex_size: int, total_time: Time
) -> GameDodo | GameGopher:
    """
    Fonction permettant d'initialiser l'environnement de jeu
    """
    # Initialisation de l'environnement du jeu Dodo
    if game == "Dodo":
        if player == 1:
            player_selected: PlayerLocal = PlayerLocal(1, UP_DIRECTIONS)
            return GameDodo(
                grid, player_selected, PlayerLocal(2, DOWN_DIRECTIONS), \
                    player_selected, hex_size, total_time
            )

        player_selected: PlayerLocal = PlayerLocal(2, DOWN_DIRECTIONS)
        player_opponent: PlayerLocal = PlayerLocal(1, UP_DIRECTIONS)
        return GameDodo(
            grid, player_selected, player_opponent, player_opponent, hex_size, total_time
        )

    # Initialisation de l'environnement du jeu Gopher
    grid = new_gopher(hex_size)
    if player == 1:
        player_param: PlayerLocal = PlayerLocal(1, ALL_DIRECTIONS)
        return GameGopher(
            grid,
            player_param,
            PlayerLocal(2, ALL_DIRECTIONS),
            player_param,
            hex_size,
            total_time,
        )
    player_param: PlayerLocal = PlayerLocal(2, ALL_DIRECTIONS)
    player_opponent: PlayerLocal = PlayerLocal(1, ALL_DIRECTIONS)
    return GameGopher(
        grid,
        player_param,
        player_opponent,
        player_opponent,
        hex_size,
        total_time,
    )


def append_to_csv(dataframe: pd.DataFrame, filename: str):
    """
    Fonction permettant d'ajouter une ligne à un fichier CSV
    """
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    path_file = os.path.join(parent_dir, "../Benchmarks", filename)

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
    grid: int
):
    """
    Fonction permettant d'ajouter les statistiques d'une partie à un fichier CSV
    """
    win_number = sum(res["winner"] == 1 for res in list_results)
    loss_number = game_number - win_number
    new_benchmark = {
        "strategy_1": strategy_1,
        "strategy_2": strategy_2,
        "Grid": grid,
        "game_number": game_number,
        "win_rate": sum(res["winner"] == 1 for res in list_results) / game_number,
        "average_turns": sum(res["total_turns"] for res in list_results) / game_number,
        "min_turns": min(res["total_turns"] for res in list_results),
        "max_turns": max(res["total_turns"] for res in list_results),
        "average_iteration_time": sum(
            res["average_iteration_time"] for res in list_results
        )
        / game_number,
        "average_total_time": sum(res["total_time"] for res in list_results)
        / game_number,
        "average_turns_win": (
            (
                sum(res["total_turns"] for res in list_results if res["winner"] == 1)
                / win_number
            )
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


def print_gopher(env: GameGopher, empty_grid: Grid):
    """
    Fonction permettant d'afficher une grille de jeu Gopher
    """
    temp_grid = hexa.grid_tuple_to_grid_list(empty_grid)
    for position, _ in env.max_positions.positions.items():
        conv_pos = hexa.reverse_convert(position[0], position[1], env.hex_size)
        temp_grid[conv_pos[0]][conv_pos[1]] = 1
    for position, _ in env.min_positions.positions.items():
        conv_pos = hexa.reverse_convert(position[0], position[1], env.hex_size)
        temp_grid[conv_pos[0]][conv_pos[1]] = 2

    hexa.display_grid(hexa.grid_list_to_grid_tuple(temp_grid))


def launch_multi_game(game_number: int = 1, name: str = "Dodo"):
    """
    Fonction permettant de lancer plusieurs parties de jeu
    """
    debug = True
    if game_number > 1:
        debug = False
    # Liste pour stocker les résultats des parties
    list_results = []
    size_init_grid = 4
    if name == "Dodo":
        for i in range(game_number):
            init_grid = convert_grid(INIT_GRID4, size_init_grid)
            game = initialize("Dodo", init_grid, 1, size_init_grid, 5)
            res = dodo(
                game,
                strategy_minmax,
                strategy_random,
                debug=debug,
                graphics=False,
            )
            list_results.append(res)
            print(f"Partie {i + 1}: {res}")

    else:
        init_grid = new_gopher(7)
        for i in range(game_number):
            game = initialize("Gopher", init_grid, 1, 7, 5)
            res = gopher(
                game,
                strategy_minmax,
                strategy_random,
                debug=debug,
                graphics=False,
            )
            list_results.append(res)
            print(f"Partie {i + 1}: {res}")

    # Ajout des stat à un fichier CSV
    add_to_benchmark(
        list_results,
        "benchmark",
        game_number,
        "strategy_alpha_beta",
        "strategy_random",
        size_init_grid,
    )


# Fonction principale de jeu Dodo
def main():
    """
    Fonction principale de jeu Dodo
    """

    launch_multi_game(1, "Dodo")


if __name__ == "__main__":
    main()
