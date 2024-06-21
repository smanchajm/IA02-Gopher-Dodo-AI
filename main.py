""" Module concernant l'environnement du jeu Gopher-Dodo """

import argparse
import time
from typing import Any, List

import matplotlib
import matplotlib.pyplot as plt
from Server.gndclient import BLUE, RED, State, cell_to_grid, empty_grid
from Strategies.mcts import MCTS
from Strategies.strategies import (StrategyLocal, strategy_minmax, strategy_random, strategy_mcts)
from Game_playing.benchmark import add_to_benchmark
import Game_playing.hexagonal_board as hexa
from Game_playing.grid import INIT_GRID, INIT_GRID4
from Game_playing.structures_classes import (ALL_DIRECTIONS, DOWN_DIRECTIONS,
                                             UP_DIRECTIONS, Action, Environment, GameDodo,
                                             GameGopher, GridDict, PlayerLocal,
                                             Time, convert_grid, new_gopher)

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
            # if env.hex_size == 4:
                # print_dodo(env, INIT_GRID4)
            # else:
                # print_dodo(env, INIT_GRID)
            print_grid(env)
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
                current_action = strategy_1(env, env.current_player)

            time_history_max.append(
                time.time() - iteration_time_start
            )  # Stockage du temps d'itération

        # Lancement de la stratégie 2
        else:
            current_action = strategy_2(env, env.current_player)

            time_history_min.append(time.time() - iteration_time_start)

        # Jouer l'action courante
        env.play(current_action)

        if env.current_player == env.max_player:
            time_history.append(time.time() - iteration_time_start)

        res = env.final()

        # Affichage de la grille de jeu et du temps d'itération
        if debug:
            print_grid(env)
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
                "Dodo"
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
            "Dodo"
        )

    # Initialisation de l'environnement du jeu Gopher
    grid = new_gopher(hex_size) # Création de la grille de jeu Gopher

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
            "Gopher"
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
        "Gopher"
    )


def grid_state_color(state: State, hex_size: int) -> str:
    """ Convert the state to a grid with colors """
    # Initialize an empty grid with the specified hex size
    grid = empty_grid(hex_size)

    # ANSI escape codes for red and blue
    RED_COLOR = "\033[91m"
    BLUE_COLOR = "\033[94m"
    RESET_COLOR = "\033[0m"

    for cell, player in state:
        x, y = cell_to_grid(cell, hex_size)
        if player == RED:
            grid[x][y] = f"{RED_COLOR}R{RESET_COLOR}"
        elif player == BLUE:
            grid[x][y] = f"{BLUE_COLOR}B{RESET_COLOR}"
        else:
            grid[x][y] = " "

    # Convert the grid to a string
    return "\n".join("".join(c for c in line) for line in grid)


def print_grid(env: Environment):
    """
    Fonction permettant d'afficher une grille de jeu Gopher
    """

    # convert env.grid which is a dict into a state
    state = []
    for cell, player in env.grid.items():
        if player == 1:
            state.append((cell, RED))
        elif player == 2:
            state.append((cell, BLUE))
        else:
            state.append((cell, player))

    print(grid_state_color(state, env.hex_size))


def launch_multi_game(
    game_number: int = 1,
    name: str = "Dodo",
    strategy_1: Any = strategy_minmax,
    strategy_2: Any = strategy_minmax,
    timer: Time = 720,
    size_init_grid: int = 4,
):
    """
    Fonction permettant de lancer plusieurs parties de jeu à la suite
    """
    if game_number <= 1:
        debug = True
        graphics = True
    else:
        debug = False
        graphics = False

    list_results = []  # Liste pour stocker les résultats des parties

    if name == "Dodo":
        print("Lancement de Dodo")
        print(f"Stratégie 1: {strategy_1.__name__} pour le joueur R")
        print(f"Stratégie 2: {strategy_2.__name__} pour le joueur B")
        # Lancement de n parties de jeu Dodo
        for i in range(game_number):
            if size_init_grid == 4:
                init_grid = convert_grid(INIT_GRID4, size_init_grid)
            else:
                init_grid = convert_grid(INIT_GRID, size_init_grid)
            game = initialize("Dodo", init_grid, 1, size_init_grid, timer)
            res = dodo(
                game,
                strategy_1,
                strategy_2,
                debug=debug,
                graphics=graphics,
            )
            list_results.append(res)
            print(f"Partie {i + 1}: {res}")

    # Lancement de n parties de jeu Gopher
    else:
        name = "Gopher"
        print("Lancement de Gopher")
        print(f"Stratégie 1: {strategy_1.__name__} pour le joueur R")
        print(f"Stratégie 2: {strategy_2.__name__} pour le joueur B")
        init_grid = new_gopher(size_init_grid)
        for i in range(game_number):
            game = initialize("Gopher", init_grid, 1, size_init_grid, 720)
            res = gopher(
                game,
                strategy_1,
                strategy_2,
                debug=debug,
                graphics=graphics,
            )
            # print_gopher(game)
            print_grid(game)
            list_results.append(res)
            print(f"Partie {i + 1} : winner is {res['winner']}")

    # Ajout des stat à un fichier CSV
    add_to_benchmark(
        list_results,
        "benchmark",
        name,
        game_number,
        str(strategy_1.__name__),
        str(strategy_2.__name__),
        size_init_grid,
    )


def main():
    """Main function to launch the game based on command-line arguments."""
    parser = argparse.ArgumentParser(description="Launch Gopher or Dodo game")
    parser.add_argument("game", choices=["dodo", "gopher"], help="Specify the game to launch")
    parser.add_argument(
        "--games", type=int, default=1, help="Number of games to play (default: 1)"
    )
    parser.add_argument(
        "--strategy1", choices=["minmax", "random", "mcts"], default="random",
        help="Strategy for player 1 (default: random)"
    )
    parser.add_argument(
        "--strategy2", choices=["minmax", "random", "mcts"], default="mcts",
        help="Strategy for player 2 (default: mcts)"
    )
    parser.add_argument(
        "--time", type=int, default=360, 
        help="Time for the mcts strategy (default: 720)"
    )
    parser.add_argument(
        "--size", type=int, default=4,
        help="Size of the initial grid (default: 4)"
    )

    args = parser.parse_args()

    strategies = {
        "minmax": strategy_minmax,
        "random": strategy_random,
        "mcts": strategy_mcts,
    }

    strategy_1 = strategies[args.strategy1]
    strategy_2 = strategies[args.strategy2]

    if args.game == "dodo":
        launch_multi_game(
            game_number=args.games,
            name="Dodo",
            strategy_1=strategy_1,
            strategy_2=strategy_2,
            timer=Time(args.time*2),
            size_init_grid=args.size,
        )
    else:
        launch_multi_game(
            game_number=args.games,
            name="Gopher",
            strategy_1=strategy_1,
            strategy_2=strategy_2,
            timer=Time(args.time*2),
            size_init_grid=args.size,
        )


if __name__ == "__main__":
    main()
