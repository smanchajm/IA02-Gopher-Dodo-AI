""" Module contenant les fonctions de jeu pour une partie en réseau """
import sys
import ast
import argparse

from Dodo.mcts import MCTS
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

    if game == "dodo":
        game_param = "Dodo"
    else:
        game_param = "Gopher"
    # Initialize the game here
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
    """ Final result of the game """
    print(f"Ending: {player} wins with a score of {score}")


def strategy_min_max_network(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    The minmax strategy with alpha-beta pruning for a network game
    """
    env.total_time = time_left
    param_player = env.max_player if player == env.max_player.id else env.min_player
    grid: GridDict = {}
    for cell in state:
        grid[cell[0]] = cell[1]
    env.grid = grid
    env.max_positions.positions.clear()
    env.min_positions.positions.clear()

    for cell in env.grid:
        if env.grid[cell] == env.max_player.id:
            env.max_positions.positions[cell] = env.max_player.id
        elif env.grid[cell] == env.min_player.id:
            env.min_positions.positions[cell] = env.min_player.id
    env.current_player = param_player
    action = strategy_minmax(env, env.max_player)
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
    return env, action


def strategy_random_network(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    The random strategy for a network game
    """
    env.total_time = time_left
    param_player = env.max_player if player == env.max_player.id else env.min_player
    grid: GridDict = {}
    for cell in state:
        grid[cell[0]] = cell[1]
    env.grid = grid
    env.max_positions.positions.clear()
    env.min_positions.positions.clear()

    for cell in env.grid:
        if env.grid[cell] == env.max_player.id:
            env.max_positions.positions[cell] = env.max_player.id
        elif env.grid[cell] == env.min_player.id:
            env.min_positions.positions[cell] = env.min_player.id
    env.current_player = param_player

    action = strategy_random(env, env.max_player)
    return env, action


def strategy_mcts_network(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    """
    The mcts strategy for a network game
    """
    env.total_time = time_left
    param_player = env.max_player if player == env.max_player.id else env.min_player
    grid: GridDict = {}
    for cell in state:
        grid[cell[0]] = cell[1]
    env.grid = grid
    env.max_positions.positions.clear()
    env.min_positions.positions.clear()

    for cell in env.grid:
        if env.grid[cell] == env.max_player.id:
            env.max_positions.positions[cell] = env.max_player.id
        elif env.grid[cell] == env.min_player.id:
            env.min_positions.positions[cell] = env.min_player.id
    env.current_player = param_player
    mcts = MCTS()
    action = mcts.search(env)
    return env, action


if __name__ == "__main__":
    sys.path.append('')
    sys.path.append('Game_playing')
    sys.path.append('Gopher')

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
        strategy_mcts_network,
        # strategy_min_max_network,
        # strategy_random_network,
        #strategy_brain,
        #strategy_first_legal_network,
        final_result,
        gui=True
    )
