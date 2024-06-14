""" Module concernant l'implémentation de l'algorithme Monte Carlo Tree Search """
from collections import deque

from grid import INIT_GRID4
from structures_classes import *

import math
import random


# tree node class definition
class TreeNode:
    # class constructor (create tree node class instance)
    def __init__(self, env: Environment, parent=None, p_action=None):
        # init associated board state
        self.env = env

        # init is node terminal flag
        if not self.env.legals(self.env.current_player):
            # we have a terminal node
            self.is_terminal = True
        # otherwise
        else:
            # we have a non-terminal node
            self.is_terminal = False

        # init is fully expanded flag
        self.is_fully_expanded = self.is_terminal
        # init parent node if available
        self.parent: TreeNode = parent
        self.parent_action: Action = p_action
        # init the number of node visits
        self.visits = 0
        # init the total score of the node
        self.score = 0
        # init current node's children
        self.children: list[TreeNode] = []
        self.unexplored_actions = self.env.legals(self.env.current_player)


# MCTS class definition
class MCTS:
    # search for the best move in the current position
    def __init__(self):
        self.root = None

    def reinit_pos(self, env: Environment):
        env.max_positions.positions.clear()
        env.min_positions.positions.clear()
        for cell in env.grid:
            if env.grid[cell] == env.max_player.id:
                env.max_positions.positions[cell] = env.max_player.id
            elif env.grid[cell] == env.min_player.id:
                env.min_positions.positions[cell] = env.min_player.id

    # expand node
    def expand(self, node: TreeNode):
        #print(f"grid before expand: {node.env.grid}")
        #print(f"pos before expand: {node.env.max_positions.positions}")
        self.reinit_pos(node.env)
        #print(f"actions unex: {node.unexplored_actions}")
        action: Action = node.unexplored_actions.pop()
        node.env.play(action)
        # leg: list[Action] = node.env.legals(node.env.current_player)
        child = TreeNode(env=node.env, parent=node, p_action=action)
        node.env.reverse_action(action)
        self.reinit_pos(child.env)
        self.reinit_pos(node.env)

        if child not in node.children:
            node.children.append(child)

        return child

    # simulate the game via making random moves until reach end of the game --> ça marche
    def rollout(self, param_env: Environment):
        #print(f"grid before rollout: {param_env.grid}")
        # make random moves for both sides until terminal state of the game is reached
        i = 0
        self.reinit_pos(param_env)

        stack: deque = deque()
        while param_env.legals(param_env.max_player) and param_env.legals(param_env.min_player):
            i += 1
            #print(f"prof {i}")
            action: Action = random.choice(param_env.legals(param_env.current_player))
            #print(f"action: {action}, player: {param_env.current_player.id}")
            stack.append(action)
            param_env.play(action)

        score: int = param_env.final()
        #print(f"score: {score}")
        #print(f"stack rollout: {stack}")
        #print(f"grid after rollout: {param_env.grid}")


        while len(stack) > 0:
            sel_action = stack.pop()
            #print(f"reverse action: {sel_action}, player: {param_env.current_player.id}")
            param_env.reverse_action(sel_action)

        #print(f"grid DEStck rollout: {param_env.grid}")
        return score

    # backpropagate the number of visits and score up to the root node
    def backpropagate(self, node: TreeNode, score: int):  # a voir si on le modif
        # update nodes's up to root node
        while node is not None:
            # update node's visits
            node.visits += 1
            # update node's score
            node.score += score
            # set node to parent
            node = node.parent

    # select the best node basing on UCB1 formula
    def get_best_move(self, param_node: TreeNode, exploration_constant):
        # define best score & best moves
        best_score = float('-inf')
        best_moves = []

        # loop over child nodes
        for child_node in param_node.children:
            # define current player

            if child_node.env.current_player == child_node.env.max_player:
                current_player = 1
            else:
                current_player = -1

            # get move score using UCT formula
            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(
                math.log(param_node.visits / child_node.visits))

            # better move has been found
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]

            # found as good move as already available
            elif move_score == best_score:
                best_moves.append(child_node)
        # return one of the best moves randomly
        best = random.choice(best_moves)

        return best

    # select most promising node
    def select(self, node: TreeNode):
        stack: deque[Action] = deque()
        current_node: TreeNode = node
        self.reinit_pos(current_node.env)

        # make sure that we're dealing with non-terminal nodes
        while not current_node.is_terminal:

            if not len(current_node.unexplored_actions) == 0:
                return self.expand(current_node), stack
            else:
                current_node = self.get_best_move(current_node, math.sqrt(2))
                stack.append(current_node.parent_action)
                node.env.play(current_node.parent_action)

                self.reinit_pos(current_node.env)

        return current_node, stack

    def search(self, initial_state: Environment):
        # create root node
        self.root = TreeNode(initial_state, None)
        node: TreeNode
        stack: deque[Action]

        # walk through 1000 iterations
        for iteration in range(2000):
            #print(f"iteration: {iteration}")
            # select a node (selection phase)
            node, stack = self.select(self.root)

            # score current node (simulation phase)
            score = self.rollout(node.env)

            #print(f"stack: {stack}")
            while len(stack) > 0:
                self.root.env.reverse_action(stack.pop())

            # backpropagate results
            self.backpropagate(node, score)

            self.reinit_pos(self.root.env)

        best = self.get_best_move(self.root, math.sqrt(2))

        return best.parent_action


def main():
    player1: Player = Player(1, DOWN_DIRECTIONS)
    init_grid = convert_grid(INIT_GRID4, 4)
    print(init_grid)
    game = GameDodo(init_grid, player1, Player(2, UP_DIRECTIONS), player1, 4, 2)
    mcts = MCTS()
    selected_node = mcts.search(game)

    print(selected_node)
    return


if __name__ == "__main__":
    main()
