""" Module contenant les fonctions de jeu pour une partie en réseau """
import sys

import ast
import argparse
from Dodo.strategies_dodo import strategy_first_legal, strategy_minmax, strategy_random
from Game_playing.main import initialize
from Game_playing.structures_classes import Action, Environment, Score, State, Time, GridDict
from gndclient import DODO_STR, GOPHER_STR, start, Player


def initialize_for_network(
    game: str, state: State, player: int, hex_size: int, total_time: Time
) -> Environment:
    """
    Initialize the game for a network game
    """
    print("Init")
    print(
        f"{game} playing {player} on a grid of size {hex_size}. Time remaining: {total_time}"
    )

    grid: GridDict = {}
    for cell in state:
        grid[cell[0]] = cell[1]


    # Initialize the game here
    return initialize(game, grid, player, hex_size, total_time)


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
    """ Final result of the game """
    print(f"Ending: {player} wins with a score of {score}")


def strategy_min_max_network(
    env: Environment, _: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    The minmax strategy with alpha-beta pruning for a network game
    """
    env.total_time = time_left
    param_player = env.max_player if player == env.max_player.id else env.min_player
    action = strategy_minmax(env, param_player)
    print(action)
    return env, action


def strategy_first_legal_network(
    env: Environment, _: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    The first legal strategy for a network game
    """
    env.total_time = time_left
    param_player = env.max_player if player == env.max_player.id else env.min_player
    action = strategy_first_legal(env, param_player)
    print(action)
    return env, action


def strategy_random_network(
    env: Environment, _: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    The random strategy for a network game
    """
    env.total_time = time_left
    param_player = env.max_player if player == env.max_player.id else env.min_player
    action = strategy_random(env, param_player)
    print(action)
    return env, action


if __name__ == "__main__":
    sys.path.append('C:/Users/samma/Documents/Programmation/IA02/IA02-Gopher-Dodo-AI/Dodo')
    sys.path.append('C:/Users/samma/Documents/Programmation/IA02/IA02-Gopher-Dodo-AI/Game_playing')
    sys.path.append('C:/Users/samma/Documents/Programmation/IA02/IA02-Gopher-Dodo-AI/Gopher')

    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://localhost:8080/")
    parser.add_argument("-d", "--disable-dodo", action="store_false")
    parser.add_argument("-g", "--disable-gopher", action="store_false")
    args = parser.parse_args()

    available_games = []
    if not args.disable_dodo:
        available_games.append(DODO_STR)
    if not args.disable_gopher:
        available_games.append(GOPHER_STR)

    start(
        args.server_url,
        args.group_id,
        args.members,
        args.password,
        available_games,
        initialize_for_network,
        # strategy_min_max_network,
        # strategy_random_network,
        strategy_brain,
        # strategy_first_legal_network,
        final_result,
        gui=True,
    )
