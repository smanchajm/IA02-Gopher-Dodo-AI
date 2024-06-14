""" Module concernant l'implémentation de l'algorithme Monte Carlo Tree Search """
from Dodo.grid import GRID1, GRID2, INIT_GRID, INIT_GRID4, GRID4
from copy import deepcopy
from Game_playing.structures_classes import *

" erreur avec (2, 0)"

# On a toujours des  KeyError: (2, 0) que cette case au bout de bcp d'itérations pk ???


#
# MCTS algorithm implementation
#

# packages
import math
import random


# tree node class definition
class TreeNode:
    # class constructor (create tree node class instance)
    def __init__(self, env: Environment, parent):
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
        self.parent = parent

        # init the number of node visits
        self.visits = 0

        # init the total score of the node
        self.score = 0

        # init current node's children
        self.children = {}


# MCTS class definition
class MCTS:
    # search for the best move in the current position
    def __init__(self):
        self.root = None

    def search(self, initial_state: Environment):
        # create root node
        self.root = TreeNode(initial_state, None)

        #print(f"initial state: {initial_state.grid}")

        # walk through 1000 iterations
        for iteration in range(50):
            #self.root = TreeNode(deepcopy(initial_state), None)

            #print(f"iteration: {iteration}")
            # select a node (selection phase)
            node = self.select(self.root)

            # score current node (simulation phase)
            score = self.rollout(node.env)

            # backpropagate results
            self.backpropagate(node, score)

            self.root.env.max_positions.positions.clear()
            self.root.env.min_positions.positions.clear()
            for cell in self.root.env.grid:
                if self.root.env.grid[cell] == self.root.env.max_player.id:
                    self.root.env.max_positions.positions[cell] = self.root.env.max_player.id
                elif self.root.env.grid[cell] == self.root.env.min_player.id:
                    self.root.env.min_positions.positions[cell] = self.root.env.min_player.id
        """
        print(f"nb children: {len(self.root.children)}")
        for node in self.root.children.values():
            print(f"score_node: {node.score}")
            print(f"visits: {node.visits}")"""

        # pick up the best move in the current position
        try:
            best = self.get_best_move(self.root, 0)
            """
            for k in best.env.grid:
                if k in self.root.env.grid and best.env.grid[k] != self.root.env.grid[k]:"""


            action = [k for k in best.env.grid if k in self.root.env.grid and best.env.grid[k] != self.root.env.grid[k]]
            return action
        except Exception as e:
            #print(f"Exception in getting best move: {e}")
            return None

    # select most promising node
    def select(self, node: TreeNode):
        # make sure that we're dealing with non-terminal nodes
        while not node.is_terminal:
            # case where the node is fully expanded
            if node.is_fully_expanded:
                #print(f"mooove")
                node = self.get_best_move(node, 2)

            # case where the node is not fully expanded
            else:
                #print(f" best positions: {node.env.max_positions.positions}")
                # otherwise expand the
                node.env.max_positions.positions.clear()
                node.env.min_positions.positions.clear()
                for cell in node.env.grid:
                    if node.env.grid[cell] == node.env.max_player.id:
                        node.env.max_positions.positions[cell] = node.env.max_player.id
                    elif node.env.grid[cell] == node.env.min_player.id:
                        node.env.min_positions.positions[cell] = node.env.min_player.id
                return self.expand(node)

        # return node
        return node

    # expand node
    def expand(self, node: TreeNode):
        #print(f"positions: {node.env.max_positions.positions}")
        #print(f"grid: {node.env.grid}")

        actions = node.env.legals(node.env.current_player)
        for action in actions:
            state = deepcopy(node.env)
            game = GameDodo(state.grid, state.max_player, state.min_player, state.current_player, state.hex_size,
                                state.total_time)
            """
            if action[0] == (2, 0):
                print("\033[34m", end="")
                print(f"action: {action}")
                print("\033[0m", end="")"""
            #print(f"posafte: {game.max_positions.positions}")
            game.play(action)
            # Update the positions dictionary
            node.env.max_positions.positions.clear()
            node.env.min_positions.positions.clear()
            for cell in node.env.grid:
                if node.env.grid[cell] == node.env.max_player.id:
                    node.env.max_positions.positions[cell] = node.env.max_player.id
                elif node.env.grid[cell] == node.env.min_player.id:
                    node.env.min_positions.positions[cell] = node.env.min_player.id
            #print(f"posafterrrrr: {game.max_positions.positions}")

            if str(game) not in node.children:
                new_node = TreeNode(game, node)
                node.children[str(game)] = new_node
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                # Update the positions dictionary of the original environment

                return new_node



    # simulate the game via making random moves until reach end of the game --> ça marche
    def rollout(self, param_env: Environment):
        # make random moves for both sides until terminal state of the game is reached
        i = 0
        param_env.max_positions.positions.clear()
        param_env.min_positions.positions.clear()
        for cell in param_env.grid:
            if param_env.grid[cell] == param_env.max_player.id:
                param_env.max_positions.positions[cell] = param_env.max_player.id
            elif param_env.grid[cell] == param_env.min_player.id:
                param_env.min_positions.positions[cell] = param_env.min_player.id
        while param_env.legals(param_env.current_player):
            i += 1
            #print(f"prof + {i}")
            # try to make a move
            try:
                # make the on board
                # generate legal states (moves) for the given node
                actions = param_env.legals(param_env.current_player)

                states = []
                for action in actions:
                    # Make a deep copy of the environment for each action
                    env_copy = deepcopy(param_env)

                    # Create a new GameDodo object with the copied environment
                    game = GameDodo(env_copy.grid, env_copy.max_player, env_copy.min_player, env_copy.current_player,
                                    env_copy.hex_size, env_copy.total_time)
                    game.play(action)  # type: ignore
                    # Apply the action to the new game object and append the result to states
                    states.append(game)
                param_env = random.choice(states)

            # no moves available
            except:
                # return a draw score
                return 0

        # return score from the player "x" perspective
        return param_env.final()

    # backpropagate the number of visits and score up to the root node
    def backpropagate(self, node: TreeNode, score: int):
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
        for child_node in param_node.children.values():
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
        #print(f"best : {best.env.grid}")
        #print(f"best pos: {best.env.max_positions.positions}")
        return best


def main():
    player1: Player = Player(1, DOWN_DIRECTIONS)
    init_grid = convert_grid(INIT_GRID4, 4)
    game = GameDodo(init_grid, player1, Player(2, UP_DIRECTIONS), player1, 4, 2)
    mcts = MCTS()
    selected_node = mcts.search(game)

    print(selected_node)
    return

if __name__ == "__main__":
    main()