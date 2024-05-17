""" Module regroupant l'ensemble des structures de données utilisées """
from typing import Union, Callable

# Types de base utilisés par l'arbitre
# Environment = ...  # type de l'environnement (objet, dictionnaire, autre...)
Cell = tuple[int, int]
ActionDodo = tuple[Cell, Cell]  # case de départ → case d'arrivée
ActionGopher = Cell
Action = Union[ActionGopher, ActionDodo]
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu
Grid = tuple[tuple[int, ...], ...]  # Array de Array en diagonal
Score = int
Time = int
Strategy = Callable[[Grid, Player], Action]