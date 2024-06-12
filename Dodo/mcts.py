""" Module contenant les différentes stratégies pour le jeu Dodo """
import random
from typing import Any, Callable, Dict, Tuple
import numpy as np
from collections import defaultdict
from dataclasses import dataclass

from Game_playing.structures_classes import (
    Action,
    Cell,
    Environment,
    Grid,
    GridDict,
    Player,
)

Strategy = Callable[[Environment, Player, Grid], Action]


class MonteCarloTreeSearchNode:
    def __init__(self, env: Environment, parent=None, parent_action=None):
        self.env = env
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.env.legals(self.env.current_player)
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.env.play(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.env.final()

    def rollout(self):
        current_rollout_state = self.env

        while not current_rollout_state.final():
            possible_moves = current_rollout_state.legals(self.env.current_player)

            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.play(action)
        return current_rollout_state.final()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):

        current_node = self
        while not (current_node.is_terminal_node() == (1, -1)):

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)
