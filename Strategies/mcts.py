""" Module concernant l'implémentation de l'algorithme Monte Carlo Tree Search """

import math
import random
import time
from collections import deque

from Game_playing.structures_classes import Action, Environment


# tree node class definition
class TreeNode:
    """
    Classe représentant un nœud de l'arbre de recherche
    """

    def __init__(self, env: Environment, parent=None, p_action=None):
        # initialisation de l'environnement
        self.env = env

        # initialisation de l'état terminal ou non
        if not self.env.legals(self.env.current_player):
            self.is_terminal = True
        else:
            self.is_terminal = False

        # initialisation du flag indiquant si le nœud est complètement développé
        self.is_fully_expanded = self.is_terminal
        # initialisation du parent du nœud
        self.parent: TreeNode = parent
        self.parent_action: Action = p_action
        # initialisation du nombre de visites du nœud
        self.visits = 0
        # initialisation du score du nœud
        self.score = 0
        # initialisation des enfants du nœud
        self.children: list[TreeNode] = []
        self.unexplored_actions = self.env.legals(self.env.current_player)


class MCTS:
    """
    Classe représentant l'algorithme Monte Carlo Tree Search (MCTS)

    Ajouter les sources :
    """

    def __init__(self):
        self.root = None

    # reinitialisation des positions des joueurs
    def reinit_pos(self, env: Environment):
        """
        Méthode permettant de réinitialiser les positions des joueurs
        """

        env.max_positions.positions.clear()
        env.min_positions.positions.clear()
        for cell in env.grid:
            if env.grid[cell] == env.max_player.id:
                env.max_positions.positions[cell] = env.max_player.id
            elif env.grid[cell] == env.min_player.id:
                env.min_positions.positions[cell] = env.min_player.id

    def expand(self, node: TreeNode):
        """
        Méthode d'expansion qui permet d'ajouter un enfant à un nœud donné
        """
        self.reinit_pos(node.env)

        action: Action = (
            node.unexplored_actions.pop()
        )  # on récupère une action enfant non explorée
        node.env.play(action)  # on joue l'action
        child = TreeNode(
            env=node.env, parent=node, p_action=action
        )  # on crée un nouveau nœud enfant
        node.env.reverse_action(action)  # on annule l'action

        # reinitialisation des positions des joueurs
        self.reinit_pos(child.env)
        self.reinit_pos(node.env)

        if child not in node.children:
            node.children.append(child)

        return child

    def rollout(self, param_env: Environment):
        """
        Méthode de simulation qui permet de simuler une partie
        en faisant des coups aléatoires à partir du nœud actuel
        """

        i = 0
        self.reinit_pos(param_env)

        # Création d'une pile pour stocker les actions effectuées
        stack: deque = deque()

        # Tant que la partie n'est pas terminée on joue des coups aléatoires
        while param_env.legals(param_env.max_player) and param_env.legals(
                param_env.min_player
        ):
            i += 1
            action: Action = random.choice(param_env.legals(param_env.current_player))
            stack.append(action)
            param_env.play(action)

        score: int = (
            param_env.final()
        )  # on récupère le score final de la partie (-1, 1)

        # on annule les actions effectuées pour revenir à l'état initial
        while len(stack) > 0:
            sel_action = stack.pop()
            param_env.reverse_action(sel_action)

        return score

    def backpropagate(self, node: TreeNode, score: int):
        """
        Méthode de backpropagation
        qui permet de remonter les visites et les scores jusqu'au nœud racine
        """

        # on remonte les visites et les scores jusqu'au nœud racine
        while node is not None:
            # update node's visits
            node.visits += 1
            # update node's score
            node.score += score
            # set node to parent
            node = node.parent

    def get_best_move(self, param_node: TreeNode, exploration_constant=math.sqrt(2)):
        """
        Méthode qui permet de sélectionner le meilleur enfant en fonction de la formule UCB1
        """

        # calcul des poids des enfants
        choices_weights = [
            (child.score / child.visits)
            + exploration_constant
            * math.sqrt((math.log(param_node.visits) / child.visits))
            for child in param_node.children
        ]

        # retourner l'enfant avec le poids le plus élevé
        return param_node.children[choices_weights.index(max(choices_weights))]

    def select(self, node: TreeNode):
        """
        Méthode de sélection
        qui permet de sélectionner l'enfant le plus prometteur des enfants du nœud actuel
        ou d'ajouter (expand) un enfant si le nœud actuel n'est pas terminal
        """

        stack: deque[Action] = (
            deque()
        )  # on crée une pile pour stocker les actions effectuées
        current_node: TreeNode = node  # on initialise le nœud actuel
        self.reinit_pos(current_node.env)

        # Tant que le nœud actuel n'est pas terminal on sélectionne le meilleur enfant
        while not current_node.is_terminal:

            # si le nœud actuel n'est pas complètement développé on ajoute un enfant
            if not len(current_node.unexplored_actions) == 0:
                return self.expand(current_node), stack

            # si le nœud actuel est complètement développé on sélectionne le meilleur enfant
            current_node = self.get_best_move(current_node, math.sqrt(2))
            stack.append(current_node.parent_action)
            node.env.play(current_node.parent_action)

            self.reinit_pos(current_node.env)

        return current_node, stack

    def get_most_winning(self, node: TreeNode):
        """
        Méthode qui permet de retourner le nœud enfant avec le meilleur ratio de victoires
        """

        # initialisation des variables
        max_score = -float("inf")
        best_node = None

        # on parcourt les enfants du nœud actuel et on retourne le meilleur enfant
        for child in node.children:
            score = child.score / child.visits
            if score > max_score:
                max_score = score
                best_node = child

        return best_node

    def stop(self, n, time_left, time_spent, visits_best, visits_second_best):
        """
        Implémentation de la stratégie STOP pour déterminer si la recherche peut s'arrêter
        """

        return (n * (time_left / time_spent) * 1.1) < (visits_best - visits_second_best)

    def search(self, initial_state: Environment, nb_simulations=800, round_time=None):
        """
        Méthode principale de l'algorithme MCTS qui permet de rechercher la meilleure action 
        à jouer en fonction de l'état initial select -> expand -> rollout -> backpropagate
        """

        self.root = TreeNode(initial_state, None)  # création du nœud racine
        node: TreeNode
        stack: deque[
            Action
        ]  # initialisation de la pile pour stocker les actions effectuées
        start_time = time.time()
        n: int = 0

        # si le temps de simulation est None on effectue un nombre de simulations donné
        if round_time is None:
            for _ in range(nb_simulations):
                n += 1
                node, stack = self.select(self.root)  # selection d'un nœud (sélection)

                score = self.rollout(node.env)  # simulation d'une partie (simulation)

                # on annule les actions effectuées pour revenir à l'état initial
                while len(stack) > 0:
                    self.root.env.reverse_action(stack.pop())

                self.backpropagate(node, score)  # backpropagation des résultats

                self.reinit_pos(self.root.env)

        # si le temps de simulation est donné
        # on effectue des simulations jusqu'à ce que le temps soit écoulé
        else:
            while (time.time() - start_time) < round_time:
                n += 1

                node, stack = self.select(self.root)  # Séléction d'un nœud (sélection)

                # score current node (simulation phase)
                score = self.rollout(node.env)  # Simulation d'une partie (simulation)

                # On annule les actions effectuées pour revenir à l'état initial
                while len(stack) > 0:
                    self.root.env.reverse_action(stack.pop())

                self.backpropagate(node, score)  # Backpropagation des résultats

                self.reinit_pos(self.root.env)

                # Mise à jour des variables pour la stratégie STOP
                visits_best = max(self.root.children, key=lambda child: child.visits).visits
                visits_second_best = max(
                    [child for child in self.root.children if child.visits != visits_best],
                    key=lambda child: child.visits,
                    default=self.root
                ).visits

                # On vérifie si on peut arrêter la recherche STOP
                time_spent = time.time() - start_time
                time_left = round_time - time_spent if round_time else 0
                if time_spent > 0 and \
                        self.stop(n, time_left, time_spent, visits_best, visits_second_best):
                    print(f"temps économisé: {time_left}")
                    break

            print(f"nombre de simulations: {n}")

        # On retourne le nœud enfant avec le meilleur ratio de victoires
        return self.get_most_winning(self.root).parent_action
