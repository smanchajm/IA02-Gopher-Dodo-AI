""" Module concernant l'environnement du jeu Gopher-Dodo """

import os
import time
from typing import Any, List

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd  # type: ignore
from Dodo.mcts import MCTS
from Dodo.strategies_dodo import (StrategyLocal, strategy_minmax,
                                  strategy_random)

import Game_playing.hexagonal_board as hexa
from Game_playing.grid import GRID2, GRID4, INIT_GRID4
from Game_playing.hexagonal_board import Grid
from Game_playing.structures_classes import (ALL_DIRECTIONS, DOWN_DIRECTIONS,
                                             UP_DIRECTIONS, Action, GameDodo,
                                             GameGopher, GridDict, PlayerLocal,
                                             Time, convert_grid, new_gopher,
                                             print_dodo)

matplotlib.use("TkAgg")


def view_graphic(
    time_history: List[float], total_time_start: float, total_time_end: float
):
    """
    Affiche les graphiques concernant le temps d'itération en fonction de l'itération
    """
    print(f"Temps total écoulé: {total_time_end - total_time_start} secondes")
    plt.plot(time_history)
    plt.ylabel("Temps d'itération (s)")
    plt.xlabel("Itération")
    plt.title("Temps d'itération en fonction de l'itération")
    plt.show()


# Boucle de jeu Dodo
def dodo(
    env: GameDodo,
    strategy_1: StrategyLocal,
    strategy_2: StrategyLocal,
    debug: bool = False,
    graphics: bool = False,
):
    """
    Fonction représentant la boucle de jeu de Dodo
    """

    # Initialisation du stockage de données pour le benchmark
    time_history: List[float] = []
    time_history_max: List[float] = []
    time_history_min: List[float] = []

    # Initialisation des variables de la boucle de jeu
    current_action: Action
    tour: int = 0
    total_time_start = time.time()  # Chronomètre

    # Boucle de jeu tant que la partie n'est pas dans un état final
    res = env.final()
    while res not in (1, -1):
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        if debug and env.current_player.id == 1:
            print(f"Tour \033[36m {tour}\033[0m.")

        # Lancement de la stratégie 1
        if env.current_player.id == 1:
            tour += 1
            current_action = strategy_1(env, env.current_player)
            time_history_max.append(time.time() - iteration_time_start)
        # Lancement de la stratégie 2
        else:
            current_action = strategy_2(env, env.current_player)
            time_history_min.append(time.time() - iteration_time_start)

        # Jouer l'action courante
        env.play(current_action)  # type: ignore

        iteration_time_end = (
            time.time()
        )  # Fin du chronomètre pour la durée de cette itération

        if debug:
            print_dodo(env, GRID4)
            print(
                f"Temps écoulé pour cette itération: {iteration_time_end - iteration_time_start}"
                f" secondes"
            )

        res = env.final()

    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie

    # Affichage des graphiques concernant le temps d'itération en fonction de l'itération
    if graphics:
        view_graphic(time_history, total_time_start, total_time_end)

    # Retourne un dictionnaire contenant les informations de la partie (benchmarking)
    return {
        "average_iteration_time": (
            sum(time_history) / len(time_history) if time_history else 0
        ),
        "average_iteration_time_max": (
            sum(time_history_max) / len(time_history_max) if time_history_max else 0
        ),
        "average_iteration_time_min": (
            sum(time_history_min) / len(time_history_min) if time_history_min else 0
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
):
    """
    Fonction représentant la boucle de jeu de Gopher
    """

    # Initialisation du stockage de données pour le benchmark
    time_history: List[float] = []
    time_history_max: List[float] = []
    time_history_min: List[float] = []

    # Initialisation des variables de la boucle de jeu
    current_action: Action
    tour: int = 0
    total_time_start = time.time()  # Chronomètre

    # Boucle de jeu tant que la partie n'est pas dans un état final
    res = env.final()
    while res not in (1, -1):
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        if debug and env.current_player.id == 1:
            print(f"Tour \033[36m {tour}\033[0m.")  # Affichage du tour

        # Lancement de la stratégie 1
        if env.current_player.id == env.max_player.id:
            tour += 1

            # Ouvrir le jeu avec une action spécifique pour le premier tour (coin supérieur)
            if tour == 1 and env.current_player == env.max_player:
                current_action = (0, env.hex_size - 1)
            else:
                if strategy_1 == strategy_minmax:
                    current_action = strategy_1(env, env.current_player)
                else:
                    print("MCTS")
                    print(f"current player: {env.current_player.id}")
                    mcts = MCTS()
                    current_action = mcts.search(env, round_time=13)
            time_history_max.append(
                time.time() - iteration_time_start
            )  # Stockage du temps d'itération
        # Lancement de la stratégie 2
        else:
            if strategy_2 == strategy_minmax:
                current_action = strategy_2(env, env.current_player)
            else:
                mcts = MCTS()
                current_action = mcts.search(env, round_time=13)
            time_history_min.append(time.time() - iteration_time_start)

        # Jouer l'action courante
        env.play(current_action)  # type: ignore

        if env.current_player == env.max_player:
            time_history.append(time.time() - iteration_time_start)

        # Affichage de la grille de jeu et du temps d'itération
        if debug:
            print_gopher(env, GRID2)
            print(
                f"Temps écoulé pour cette itération: {time.time() - iteration_time_start}"
                f" secondes"
            )

    # Fin de la boucle de jeu
    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie
    if graphics:
        view_graphic(time_history, total_time_start, total_time_end)

    # Retourne un dictionnaire contenant les informations de la partie (benchmarking)
    return {
        "average_iteration_time": (
            sum(time_history) / len(time_history) if time_history else 0
        ),
        "total_turns": tour,
        "total_time": total_time_end - total_time_start,
        "winner": env.final(),
        "average_iteration_time_max": (
            sum(time_history_max) / len(time_history_max) if time_history_max else 0
        ),
        "average_iteration_time_min": (
            sum(time_history_min) / len(time_history_min) if time_history_min else 0
        ),
    }


# Initialisation de l'environnement
def initialize(game: str, grid: GridDict, player: int, hex_size: int, total_time: Time):
    """
    Fonction permettant d'initialiser l'environnement de jeu
    """
    # Initialisation des joueurs
    player_selected: PlayerLocal
    player_opponent: PlayerLocal

    # Initialisation de l'environnement du jeu Dodo
    if game == "Dodo":
        # Initialisation de l'environnement du jeu Dodo si nous jouons en premier
        if player == 1:
            player_selected = PlayerLocal(1, UP_DIRECTIONS)
            player_opponent = PlayerLocal(2, DOWN_DIRECTIONS)
            # Retourne l'environnement du jeu Dodo initialisé
            return GameDodo(
                grid,
                player_selected,
                player_opponent,
                player_selected,
                hex_size,
                total_time,
                0,
                grid,
            )

        # Initialisation de l'environnement du jeu Dodo si nous jouons en second
        player_selected = PlayerLocal(2, DOWN_DIRECTIONS)
        player_opponent = PlayerLocal(1, UP_DIRECTIONS)

        # Retourne l'environnement du jeu Dodo initialisé
        return GameDodo(
            grid,
            player_selected,
            player_opponent,
            player_opponent,
            hex_size,
            total_time,
            0,
            grid,
        )

    # Initialisation de l'environnement du jeu Gopher
    grid = new_gopher(hex_size)  # Création de la grille de jeu Gopher
    # Initialisation de l'environnement du jeu Gopher si nous jouons en premier
    if player == 1:
        player_param = PlayerLocal(1, ALL_DIRECTIONS)
        player_opponent = PlayerLocal(2, ALL_DIRECTIONS)
        # Retourne l'environnement du jeu Gopher initialisé
        return GameGopher(
            grid,
            player_param,
            player_opponent,
            player_param,
            hex_size,
            total_time,
            0,
            grid,
        )

    # Initialisation de l'environnement du jeu Gopher si nous jouons en second
    player_param = PlayerLocal(2, ALL_DIRECTIONS)
    player_opponent = PlayerLocal(1, ALL_DIRECTIONS)
    # Retourne l'environnement du jeu Gopher initialisé
    return GameGopher(
        grid,
        player_param,
        player_opponent,
        player_opponent,
        hex_size,
        total_time,
        0,
        grid,
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
    with open("benchmark.csv", "a", newline="", encoding="utf-8") as f:
        if not file_exists:
            dataframe.to_csv(f, header=True, index=False)
        else:
            dataframe.to_csv(f, header=True, index=False)


def add_to_benchmark(
    list_results,
    filename: str,
    game_number: int,
    strategy_1: str,
    strategy_2: str,
    grid: int,
):
    """
    Fonction permettant d'ajouter les statistiques d'une partie à un fichier CSV
    """

    # Calcul des statistiques
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
        "average_iteration_time_max": sum(
            res["average_iteration_time_max"] for res in list_results
        )
        / game_number,
        "average_iteration_time_min": sum(
            res["average_iteration_time_min"] for res in list_results
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

    # Création d'un DataFrame avec une seule ligne
    df_results = pd.DataFrame([new_benchmark])
    print(f"Résultats : {df_results}")
    # Ajout des statistiques à un fichier CSV
    append_to_csv(df_results, f"{filename}.csv")


def print_gopher(env: GameGopher, empty_grid: Grid):
    """
    Fonction permettant d'afficher une grille de jeu Gopher
    """

    # Initialisation de la grille de jeu
    temp_grid = hexa.grid_tuple_to_grid_list(empty_grid)

    # Affichage des positions des joueurs en convertissant les coordonnées
    for position, _ in env.max_positions.positions.items():
        conv_pos = hexa.reverse_convert(position[0], position[1], env.hex_size)
        temp_grid[conv_pos[0]][conv_pos[1]] = 1
    for position, _ in env.min_positions.positions.items():
        conv_pos = hexa.reverse_convert(position[0], position[1], env.hex_size)
        temp_grid[conv_pos[0]][conv_pos[1]] = 2

    hexa.display_grid(hexa.grid_list_to_grid_tuple(temp_grid))


def launch_multi_game(
    game_number: int = 1,
    name: str = "Dodo",
    strategy_1: Any = strategy_minmax,
    strategy_2: Any = strategy_minmax,
):
    """
    Fonction permettant de lancer plusieurs parties de jeu à la suite
    """
    debug = True

    list_results = []  # Liste pour stocker les résultats des parties
    size_init_grid = 7  # Taille de la grille de jeu
    if name == "Dodo":
        # Lancement de n parties de jeu Dodo
        for i in range(game_number):
            init_grid = convert_grid(INIT_GRID4, size_init_grid)
            game = initialize("Dodo", init_grid, 1, size_init_grid, 5)
            res = dodo(
                game,
                strategy_1,
                strategy_2,
                debug=debug,
                graphics=False,
            )
            list_results.append(res)
            print(f"Partie {i + 1}: {res}")

    # Lancement de n parties de jeu Gopher
    else:
        init_grid = new_gopher(size_init_grid)
        for i in range(game_number):
            game = initialize("Gopher", init_grid, 1, size_init_grid, 500)
            print(f"max player: {game.max_player.id}")

            res = gopher(
                game,
                strategy_1,
                strategy_2,
                debug=False,
                graphics=False,
            )
            list_results.append(res)
            print(f"Partie {i + 1}: {res}")

    # Ajout des stat à un fichier CSV
    add_to_benchmark(
        list_results,
        "benchmark",
        game_number,
        "alpha-beta",
        "mcts",
        size_init_grid,
    )


# Fonction principale de jeu Dodo
def main():

    # mcts first player alpha-beta second player
    launch_multi_game(50, "Gopher", "mcts", strategy_minmax)
    # alpha-beta first player mcts second player
    launch_multi_game(10, "Gopher", strategy_minmax, "mcts")


if __name__ == "__main__":
    main()
