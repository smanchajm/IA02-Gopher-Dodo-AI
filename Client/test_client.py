#!/usr/bin/python3

import ast
import argparse
from typing import Dict, Any
from strategies_dodo import strategy_first_legal
from main import initialize
from structures_classes import Player
from gndclient import start, Action, Score, State, Time, DODO_STR, GOPHER_STR

Environment = Dict[str, Any]

def strategy_brain(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    print("New state ", state)
    print("Time remaining ", time_left)
    print("What's your play ? ", end="")
    s = input()
    print()
    t = ast.literal_eval(s)
    return (env, t)


def final_result(state: State, score: Score, player: Player):
    print(f"Ending: {player} wins with a score of {score}")


if __name__ == "__main__":
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
        initialize,
        strategy_first_legal,
        final_result,
        gui=True,
    )
