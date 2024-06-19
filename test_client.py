""" Module contenant les fonctions de jeu pour une partie en réseau """

import argparse
import ast

from Dodo.mcts import MCTS
from Dodo.strategies_dodo import (strategy_first_legal, strategy_minmax,
                                  strategy_random)
from Game_playing.main import initialize
from Game_playing.structures_classes import (Action, Environment, GridDict,
                                             Score, State, Time)
from Serveur.gndclient import DODO_STR, GOPHER_STR, Player, start


def reinit(env: Environment, time_left: Time, state: State, player: int):
    """
    MAJ des positions du temps et du joueur
    """
    # Reinitialisation des deonnées de l'environnement
    env.total_time = time_left
    param_player = env.max_player if player == env.max_player.id else env.min_player

    grid: GridDict = {}
    for cell in state:
        grid[cell[0]] = cell[1]
    env.grid = grid

    # Sauvegarde de l'état précédent
    env.precedent_state = env.grid.copy()

    # Réinitialisation des positions des joueurs
    env.max_positions.positions.clear()
    env.min_positions.positions.clear()

    for cell in env.grid:
        if env.grid[cell] == env.max_player.id:
            env.max_positions.positions[cell] = env.max_player.id
        elif env.grid[cell] == env.min_player.id:
            env.min_positions.positions[cell] = env.min_player.id

    env.current_player = param_player
    env.current_round += 1
    print("Round ", env.current_round)

    return env


def copie_action(env: Environment) -> Action:
    """
    Fonction permettant de copier l'action de l'adversaire
    """
    actions = []
    for cell in env.grid:
        if env.precedent_state[cell] != env.grid[cell]:
            actions.append(cell)
    print("Action copiée ", actions)

    action = (actions[0], actions[1])
    res = (
        (env.hex_size - 1 - action[0][0], env.hex_size - 1 - action[0][1]),
        (env.hex_size - 1 - action[1][0], env.hex_size - 1 - action[1][1]),
    )

    return res


def initialize_for_network(
    game: str, state: State, player: int, hex_size: int, total_time: Time
) -> Environment:
    """
    Fonction d'initialisation de l'environnement de jeu pour une partie en réseau (Gopher ou Dodo)
    """

    print(
        f"{game} playing {player} on a grid of size {hex_size}. Time remaining: {total_time}"
    )

    # Conversion de l'état en grille de type GridDict
    grid: GridDict = {}
    for cell in state:
        grid[cell[0]] = cell[1]

    if game == "dodo":
        game_param = "Dodo"
    else:
        game_param = "Gopher"

    # Appel de la fonction d'initialisation du jeu
    return initialize(game_param, grid, player, hex_size, total_time)


def strategy_brain(
    env: Environment, state: State, _: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    The strategy of the player
    """
    print("New state ", state)
    print("Time remaining ", time_left)
    print("What's your play ? ", end="")
    s = input()
    print()
    t = ast.literal_eval(s)
    print(t)
    return env, t


def final_result(_: State, score: Score, player: Player):
    """Final result of the game"""
    print(f"Ending: {player} wins with a score of {score}")


def strategy_min_max_network(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    Fonction permettant de lancer l'algorithme alpha-beta pour un état donné
    """
    # Réinitialisation de l'environnement
    env = reinit(env, time_left, state, player)

    # Appel de la stratégie alpha-beta
    action = strategy_minmax(env, env.max_player)
    return env, action


def strategy_first_legal_network(
    env: Environment, _: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    Fonction permettant de jouer le premier coup légal
    """
    env.total_time = time_left
    param_player = env.max_player if player == env.max_player.id else env.min_player
    action = strategy_first_legal(env, param_player)
    return env, action


def strategy_random_network(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    Fonction permettant de jouer un coup aléatoire
    """

    env = reinit(env, time_left, state, player)
    action = strategy_random(env, env.max_player)
    return env, action


def strategy_mcts_network(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    Fonction permettant de jouer un coup avec l'algorithme MCTS (Monte Carlo Tree Search)
    """
    env = reinit(env, time_left, state, player)
    mcts = MCTS()
    action = mcts.search(env, 300)
    return env, action


ouverture = [((), ())]


def strategy_dodo(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    Stratégie complète pour le jeu Dodo
    """
    # Réinitialisation de l'environnement
    env = reinit(env, time_left, state, player)

    # Calcul du temps de jeu en fonction du nombre de tours restants (voir article ReadMe)
    play_time = time_left / (30 + max(60 - env.current_round, 0))
    print("play_time", play_time)
    print(f"time left {time_left}")

    # Appel de l'algorithme MCTS
    mcts = MCTS()
    action = mcts.search(env, round_time=play_time)

    return env, action


def strategy_gopher(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    Stratégie complète pour le jeu Gopher
    """

    # Réinitialisation de l'environnement
    env = reinit(env, time_left, state, player)

    # Ouverture déterministe dans un coin
    if env.max_player.id == 1 and env.current_round == 0 or env.current_round == 1:
        return env, (0, env.hex_size - 1)

    # Stratégie de survie si le temps restant est inférieur à 5 secondes
    if time_left < 5:
        print("strategy_first_legal")
        return env, strategy_first_legal(env, env.max_player)

    # Appel de l'algorithme alpha-beta
    action = strategy_minmax(env, env.max_player)
    print("time left", env.total_time)

    return env, action


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://localhost:8080/")
    parser.add_argument("-d", "--disable-dodo", action="store_true")
    parser.add_argument("-g", "--disable-gopher", action="store_true")
    args = parser.parse_args()

    available_games = [DODO_STR, GOPHER_STR]
    if args.disable_dodo:
        available_games.remove(DODO_STR)
    if args.disable_gopher:
        available_games.remove(GOPHER_STR)

    start(
        args.server_url,
        args.group_id,
        args.members,
        args.password,
        available_games,
        initialize_for_network,
        strategy_dodo,
        # strategy_gopher,
        # strategy_mcts_network,
        # strategy_min_max_network,
        # strategy_random_network,
        # strategy_brain,
        # strategy_first_legal_network,
        final_result,
        gui=True,
    )
