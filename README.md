# Board Game AI Challenge : Dodo and Gopher AI

The aim of this project is to create artificial Gopher and Dodo players capable of playing in an AI competition.
This project was carried out as part of the IA02 (Problem-Solving and Logic Programming) course at the Compiegne University of Technology (UTC).

These two games were created by Mark Steere.

## Rules

Both games are played on a hexagonal board. The implementation is freely inspired by Red Blob Games [Implementation of hex Grid](https://www.redblobgames.com/grids/hexagons/).

* **[Dodo Rules](https://www.marksteeregames.com/Gopher_hex_rules.pdf)**.
* **[Gopher Rules](https://www.marksteeregames.com/Dodo_rules.pdf)**.

## Features

* Run simulations for "Gopher" and "Dodo" games.
* Apply different strategies for each player (MCTS, minmax (alpha-beta), random).
* Benchmark and visualize game performance.
* Debugging and graphical output options.

## Requirements

* Python 3.6 or higher
* Required Python packages: `matplotlib`
* Add the path of the project to the PYTHONPATH environment variable.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/smanchajm/gopher-dodo.git
```

2. Install the required Python packages:

```sh
pip install matplotlib
```

3. Add the project path to the PYTHONPATH environment variable

## Normal usage

You can run the simulations from the command line by specifying the game type and various options:

```sh
python3 main.py <game> [options]
```

### Arguments

* `<game>`: The game to launch, either `dodo` or `gopher`.

### Options

* `--games`: Number of games to play (default: 1).
* `--strategy1`: Strategy for player 1 (`minmax`, `random`, `mcts`; default: `minmax`).
* `--strategy2`: Strategy for player 2 (`minmax`, `random`, `mcts`; default: `minmax`).
* `--size`: Size of the board (default: 4).
* `--time`: Time limit for one player (default: 360 seconds).

### Examples

1. Launch a single game of "Dodo" with random strategy for player 1 and minmax strategy for player 2:

   ```sh
   python3 main.py dodo --strategy1 random --strategy2 minmax
   ```

2. Launch five games of "Gopher" with MCTS for both players:

   ```sh
   python3 main.py gopher --games 5 --strategy1 mcts --strategy2 mcts
   ```

## Server usage

The server runs on the command line (terminal under Linux and macOS, powershell under Windows)

1. Go in the directory `Server`
2. Add execution rights (if necessary under Linux and MaxOS): `chmod a+x <gndserver-1.0.2-...>`
3. Check operation and see the options: `./gndserver-1.0.2-...`

```bash
# all options
./gndserver -h
```

```bash
# launch a dodo server against a random player
./gndserver -game dodo -random
```

```bash
# run a gopher server against a random player
./gndserver -game gopher -random
```

```bash
# launch a gopher server against a random gopher player who will be the blue player
./gndserver -game gopher -rcolor blue -random
```

```bash
# reset all
rm config.json server.json
```

## Client usage

You could use the client to connect to the server and play the game.
The format of the command is as follows:

```bash
python test_client.py <id_group> <player_name> <player_key>
```

```bash
# launch the client
python test_client.py 12 toto totovelo
```

## Code Structure

* `view_graphic`: Displays iteration time as a graph.
* `dodo`: Game loop for "Dodo" with timing and debugging features.
* `gopher`: Game loop for "Gopher" with specific initialization for the first move.
* `initialize`: Initializes the game environment.
* `grid_state_color`: Converts the game state into a colored grid representation.
* `print_gopher`: Prints the current state of the "Gopher" game board.
* `launch_multi_game`: Runs multiple game sessions consecutively and stores the results.
* `main`: Main script to run the simulations.

## Implementation

### Game Representation

Afin de représenter les deux jeux, nous avons utilisé une grille hexagonale. Chaque case de la grille est représentée par un tuple (x, y) qui correspond à ses coordonnées. Les cases sont stockées dans un dictionnaire où la clé est le tuple (x, y) et la valeur est l'état de la case (0, 1, 2) en fonction du joueur. L'accès aux cases et donc en O(1).
De plus, deux autres dictionnaires sont utilisés pour stocker les positions des joueurs et les cases adjacentes à chaque case, afin de réduire la complexité.

### Game Environment

* **Environment** : Afin que les deux jeux puissent utiliser les mêmes stratégies et structures de données une classe abstraite `Environment` a été créée. Cette classe contient les méthodes nécessaires pour initialiser le jeu, effectuer un mouvement, vérifier la fin du jeu, obtenir les mouvements possibles, etc.
* **Dodo** : La classe `Dodo` hérite de la classe `Environment` et implémente les règles spécifiques au jeu Dodo.
* **Gopher** : La classe `Gopher` hérite de la classe `Environment` et implémente les règles spécifiques au jeu Gopher.

&rarr; Cette implémentation permet de facilement ajouter de nouveaux jeux en héritant de la classe `Environment`. De plus, chaque stratégie peut être utilisée pour n'importe quel jeu (GGP MCTS).

### Optimisations

* **Cache des scores** : Pour éviter de recalculer les scores des cases à chaque itération, un cache a été mis en place. Ainsi, les scores des cases sont calculés une seule fois et stockés dans un dictionnaire.
* **Calcul des mouvements possibles** : Pour chaque joueur, les mouvements possibles sont calculés une seule fois et stockés dans un dictionnaire.
* **Gestion des symétries** : Pour réduire le nombre de calculs, les symétries de la grille ont voulu être prises en compte. Néanmoins, après implémentation, il s'est avéré que le calcul des symétries prenait plus de temps que le calcul des mouvements possibles. Cette optimisation n'a donc pas été retenue.
* **numpy** : L'utilisation de la bibliothèque `numpy` a été envisagée pour optimiser les calculs. Cependant, l'implémentation n'a pas pu être réalisée par manque de temps.

## Minimax variant

### Classic Minimax

Un minimax classique a été implémenté pour les deux jeux. Cependant, même avec la mémoïsation le temps de calcul est très long pour le jeu Gopher. Pour le jeu Dodo, le temps de calcul est acceptable pour une profondeur de 5.

### Alpha-Beta Pruning

* Implémentation de l'élagage alpha-bêta pour réduire le nombre de nœuds explorés.
* Ajout d'un cache pour stocker les valeurs des nœuds explorés.
* Implémentation d'un stop time afin de breaker la recherche en profondeur si le temps restant est trop faible.

### Evaluation function

Pour le jeu **Dodo**

* Nombre de coups légaux
* Distance entre les deux joueurs
* Distance entre les joueurs et les bords
* Nombre de pions définitivement bloqués

### adaptive depth

Une profondeur adaptative a été implémentée. L'idée est de calculer la profondeur en fonction du nombre de coups légaux possibles. Plus il y a de coups possibles, plus la profondeur est grande.
En effet, la profondeur a besoin d'être différente en fonction de l'avancement de la partie.

Fonction de calcul de la profondeur adaptative :

* **depth_factor** = 1 / (log(len(env.legals(player)), 2) / 5) * 1.2

&rarr; Ceci donne de bons résultats. Néanmoins, il est compliqué de trouver un bon facteur car l'explosion combinatoire est très rapide et ne dépend pas que du nombre de coups possibles.

## Monte Carlo Tree Search (MCTS) UCB 1

### Structure

L'implémentation de ce MCTS a fortement été inspirée de l'article de l'article de [Monte Carlo Tree Search (MCTS) algorithm for dummies!](https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa) et de * [MCTS python](https://ai-boson.github.io/mcts/)

L'implémentation est donc composée de 2 classes :

* **Node** : Représente un noeud de l'arbre de recherche. Contient les informations suivantes :
  * `state` : L'état du jeu à ce noeud.
  * `parent` : Le noeud parent.
  * `children` : Les noeuds enfants.
  * `untried_moves` : Les mouvements non explorés.
  * `player_just_moved` : Le joueur qui vient de jouer.
  * `wins` : Le nombre de victoires.
  * `visits` : Le nombre de visites.

* **MCTS** : Représente l'algorithme MCTS. Contient les méthodes suivantes :
  * `selection` : Sélection du noeud à explorer.
  * `expansion` : Expansion du noeud sélectionné.
  * `simulation` : Simulation d'une partie aléatoire.
  * `backpropagation` : Mise à jour des statistiques des noeuds explorés.
  * `get_best_move` : Récupération du meilleur mouvement.

Pour optimiser la complexité spatiale, seules les actions possibles sont stockées dans les noeuds. Les états du jeu ne sont pas stockés. Néanmoins pour mieux coller à notre structure de jeu, nous avons stocké les noeuds joués afin de pouvoir reverse les coups.

### Time Management

Un des gros avantages de MCTS est qu'il est possible de le stopper à tout moment pour récupérer le meilleur coup trouvé. Cependant, il est important de gérer le temps de calcul pour ne pas dépasser le temps imparti. Pour cela, nous avons implémenté un système de time management basé sur le nombre de simulations effectuées.

* **Iteration time** : Pour calculer le temps alloué à chaque appel de MCTS nous nous sommes appuyés sur l'article de [Remi Coulom](https://www.remi-coulom.fr/Publications/TimeManagement.pdf). L'idée est de calculer le temps moyen d'une itération et de le multiplier par un facteur pour obtenir le temps alloué à chaque itération.
* **Stop time** : Pour éviter de dépasser le temps imparti, nous avons implémenté un système de stop time inspiré de l'article de [Maastricht University](https://dke.maastrichtuniversity.nl/m.winands/documents/time_management_for_monte_carlo_tree_search.pdf). Après chaque simulation, nous vérifions la différence de visite entre l'enfant le plus visité et le second. Si cette différence est trop grande pour être rattrapée, nous stoppons la recherche.

## Optimisations MCTS

Optimisations non implémentées par manque de temps :

* **Parallelisations** : Il est possible de paralléliser les simulations pour accélérer le temps de calcul
  * **Root parallelisation** : Chaque simulation est lancée dans un thread différent. Se pose la question de la concaténation des résultats.
  * **Leaf parallelisation** : Implémentation d'une virtual loss [Parallel Monte-Carlo Tree Search - Maastricht University](https://dke.maastrichtuniversity.nl/m.winands/documents/multithreadedMCTS2.pdf)

* **Heuristique** : Il est possible d'ajouter une heuristique pour guider l'exploration de l'arbre. Néanmoins, nous avons décidé de ne pas l'implémenter pour garder un MCTS sans biais.

## Other Strategies

* **Random** : Un joueur qui joue aléatoirement.
* **First legal move** : Un joueur qui joue le premier coup légal trouvé.

## Résultats

* **Dodo MCTS vs random** : Le MCTS gagne 100% des parties.
* **Gopher alpha-beta vs random** : L'alpha-beta gagne 100% des parties.
* **Gopher MCTS vs alpha-beta** : Les deux algorithmes sont équivalents, même si l'alpha-beta a un léger avantage si on lui laisse plus de temps. Néanmoins, MCTS est bien plus flexible.

## Conclusion

* **MCTS** : L'algorithme MCTS est très puissant et flexible. Il est capable de s'adapter à n'importe quel jeu et de rivaliser avec des algorithmes plus classiques comme l'alpha-beta. Néanmoins, il est très gourmand en temps de calcul et nécessite une bonne gestion du temps.
* **Alpha-beta** : L'algorithme alpha-beta est très efficace pour les jeux avec une profondeur de recherche limitée. Il est capable de rivaliser avec MCTS. Néamoins, il est très peu flexible et nécessite une bonne évaluation heuristique.

## Ressources

* [Hexagonal Grids](https://www.redblobgames.com/grids/hexagons/)
* [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
* [MCTS python](https://ai-boson.github.io/mcts/)
* [Monte Carlo Tree Search (MCTS) algorithm for dummies!](https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa)
* [Tictactoe-mtcs](https://github.com/maksimKorzh/tictactoe-mtcs/tree/master)
* [Time Management for Monte-Carlo Tree Search Applied to the Game of Go (INRIA)](https://www.remi-coulom.fr/Publications/TimeManagement.pdf)
* [Time Management for Monte Carlo Tree Search (Maastricht University)](https://dke.maastrichtuniversity.nl/m.winands/documents/time_management_for_monte_carlo_tree_search.pdf)

## Contributors

* Paul Clément
* Samuel Manchajm

## License

[GNU GPL v3.0](https://choosealicense.com/licenses/gpl-3.0/)
