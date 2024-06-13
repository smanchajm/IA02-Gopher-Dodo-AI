""" Module concernant l'implémentation de l'algorithme Monte Carlo Tree Search """
from typing import Callable
from collections import defaultdict
import numpy as np


from Game_playing.structures_classes import (
    Action,
    Environment,
    Grid,
    Player,
)

Strategy = Callable[[Environment, Player, Grid], Action]

""" La base du code de l'algorithme MCTS est inspirée 
de l'article suivant: https://ai-boson.github.io/mcts/"""

# voir si on change de player quand on va plus loin dans l'arbre
class MonteCarloTreeSearchNode:
    """ Classe qui représente un noeud de l'arbre de recherche de l'algorithme MCTS"""
    def __init__(self, env: Environment, parent=None, parent_action=None):
        self.env = env
        self.player = env.current_player
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()

    def untried_actions(self):
        self._untried_actions = self.env.legals(self.player)
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
        self.env.reverse_action(action)
        return child_node

    def is_terminal_node(self):
        return self.env.final()

    def rollout(self):
        current_rollout_state = self.env
        cache = []
        while not current_rollout_state.final():
            possible_moves = current_rollout_state.legals(self.player)

            action = self.rollout_policy(possible_moves)
            cache.append(action)
            current_rollout_state = current_rollout_state.play(action)
        return current_rollout_state.final()

    # a modif
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

    # a modif pour ajouter un cache
    def _tree_policy(self):

        current_node = self
        while current_node.is_terminal_node() != (1, -1):

            if not current_node.is_fully_expanded():
                return current_node.expand()
            current_node = current_node.best_child()
        return current_node

    # a modif pour ajouter un cache
    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)
