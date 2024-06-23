# Board Game AI Challenge: Dodo and Gopher AI

The aim of this project is to create artificial Gopher and Dodo players capable of competing in an AI challenge. This project was carried out as part of the IA02 (Problem-Solving and Logic Programming) course at the Compiegne University of Technology (UTC). These two games were created by Mark Steere.

## Table of Contents

- [Board Game AI Challenge: Dodo and Gopher AI](#board-game-ai-challenge-dodo-and-gopher-ai)
  - [Table of Contents](#table-of-contents)
  - [Rules](#rules)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Normal Usage](#normal-usage)
    - [Arguments](#arguments)
    - [Options](#options)
    - [Examples](#examples)
  - [Server Usage](#server-usage)
  - [Client Usage](#client-usage)
  - [Code Structure](#code-structure)
  - [Implementation](#implementation)
    - [Game Representation](#game-representation)
    - [Game Environment](#game-environment)
    - [Optimizations](#optimizations)
  - [Minimax Variant](#minimax-variant)
    - [Classic Minimax](#classic-minimax)
    - [Alpha-Beta Pruning](#alpha-beta-pruning)
    - [Evaluation Function](#evaluation-function)
    - [Adaptive Depth](#adaptive-depth)
  - [Monte Carlo Tree Search (MCTS) UCB 1](#monte-carlo-tree-search-mcts-ucb-1)
    - [Structure](#structure)
    - [Time Management](#time-management)
    - [MCTS Optimizations](#mcts-optimizations)
  - [Other Strategies](#other-strategies)
  - [Results](#results)
  - [Conclusion](#conclusion)
  - [Resources](#resources)
  - [Contributors](#contributors)
  - [License](#license)

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

## Normal Usage

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

## Server Usage

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

## Client Usage

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
* `print_grid`: Prints the current state of a Gopher or Dodo game board.
* `launch_multi_game`: Runs multiple game sessions consecutively and stores the results.
* `main`: Main script to run the simulations.

## Implementation

### Game Representation

To represent the two games, we used a hexagonal grid. Each cell in the grid is represented by a tuple (x, y) corresponding to its coordinates. The cells are stored in a dictionary where the key is the tuple (x, y) and the value is the state of the cell (0, 1, 2) depending on the player. Access to the cells is O(1). Additionally, two other dictionaries are used to store the players' positions and the cells adjacent to each cell to reduce complexity.

### Game Environment

* **Environment**: To allow both games to use the same strategies and data structures, an abstract class `Environment` was created. This class contains the necessary methods to initialize the game, make a move, check the end of the game, get possible moves, etc.
* **Dodo**: The `Dodo` class inherits from the `Environment` class and implements the specific rules of the Dodo game.
* **Gopher**: The `Gopher` class inherits from the `Environment` class and implements the specific rules of the Gopher game.

&rarr; This implementation makes it easy to add new games by inheriting from the `Environment` class. Moreover, each strategy can be used for any game (GGP MCTS).

### Optimizations

* **Score Cache**: To avoid recalculating cell scores at each iteration, a cache has been implemented. Thus, cell scores are calculated once and stored in a dictionary.
* **Calculation of Possible Moves**: For each player, the possible moves are calculated once and stored in a dictionary.
* **Handling Symmetries**: To reduce the number of calculations, grid symmetries were considered. However, after implementation, it turned out that symmetry calculations took more time than calculating possible moves, so this optimization was discarded.
* **numpy**: The use of the `numpy` library was considered to optimize calculations. However, the implementation was not completed due to a lack of time.

## Minimax Variant

### Classic Minimax

A classic minimax was implemented for both games. However, even with memoization, the calculation time is very long for the Gopher game. For the Dodo game, the calculation time is acceptable for a depth of 5.

### Alpha-Beta Pruning

* Implementation of alpha-beta pruning to reduce the number of nodes explored.
* Adding a cache to store the values of explored nodes.
* Implementation of a stop time to break the depth search if the remaining time is too short.

### Evaluation Function

For the **Dodo** game

* Number of legal moves
* Distance between the two players
* Distance between the players and the edges
* Number of permanently blocked pieces

### Adaptive Depth

An adaptive depth was implemented. The idea is to calculate the depth based on the number of possible legal moves. The more possible moves, the greater the depth. The depth needs to vary depending on the progress of the game.

Adaptive depth calculation function:

* **depth_factor** = 1 / (log(len(env.legals(player)), 2) / 5) * 1.2

&rarr; This gives good results. However, finding a good factor is complicated because the combinatorial explosion is very rapid and depends not only on the number of possible moves.

## Monte Carlo Tree Search (MCTS) UCB 1

### Structure

The implementation of this MCTS was heavily inspired by the article [Monte Carlo Tree Search (MCTS) algorithm for dummies!](https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2

bae53bfa) and [MCTS python](https://ai-boson.github.io/mcts/)

The implementation consists of two classes:

* **Node**: Represents a node in the search tree. Contains the following information:
  * `state`: The game state at this node.
  * `parent`: The parent node.
  * `children`: The child nodes.
  * `untried_moves`: The unexplored moves.
  * `player_just_moved`: The player who just moved.
  * `wins`: The number of wins.
  * `visits`: The number of visits.

* **MCTS**: Represents the MCTS algorithm. Contains the following methods:
  * `selection`: Selection of the node to explore.
  * `expansion`: Expansion of the selected node.
  * `simulation`: Simulation of a random game.
  * `backpropagation`: Update of the statistics of the explored nodes.
  * `get_best_move`: Retrieval of the best move.

To optimize spatial complexity, only possible actions are stored in the nodes. Game states are not stored. However, to better fit our game structure, we stored the played nodes to be able to reverse the moves.

### Time Management

One of the major advantages of MCTS is that it can be stopped at any time to retrieve the best found move. However, it is important to manage the calculation time to not exceed the allotted time. For this, we implemented a time management system based on the number of simulations performed.

* **Iteration time**: To calculate the time allocated to each MCTS call, we relied on the article by [Remi Coulom](https://www.remi-coulom.fr/Publications/TimeManagement.pdf). The idea is to calculate the average time of an iteration and multiply it by a factor to get the time allocated to each iteration.
* **Stop time**: To avoid exceeding the allotted time, we implemented a stop time system inspired by the article by [Maastricht University](https://dke.maastrichtuniversity.nl/m.winands/documents/time_management_for_monte_carlo_tree_search.pdf). After each simulation, we check the visit difference between the most visited child and the second. If this difference is too large to be caught up, we stop the search.

### MCTS Optimizations

Optimizations not implemented due to lack of time:

* **Parallelizations**: It is possible to parallelize simulations to speed up calculation time.
  * **Root parallelization**: Each simulation is launched in a different thread. The question of concatenating the results arises.
  * **Leaf parallelization**: Implementation of a virtual loss [Parallel Monte-Carlo Tree Search - Maastricht University](https://dke.maastrichtuniversity.nl/m.winands/documents/multithreadedMCTS2.pdf)

* **Heuristic**: It is possible to add a heuristic to guide the tree exploration. However, we decided not to implement it to keep an unbiased MCTS.

## Other Strategies

* **Random**: A player who plays randomly.
* **First legal move**: A player who plays the first legal move found.
* **Ngascout**: We also tried to implement a Negascout based on [Beat my chess ai](https://github.com/danthurston/BeatMyChessAI/tree/main) implementation. However, alpha-beta was already working well, so we decided not to use it to focus on MCTS.

## Results

* **Dodo MCTS vs random**: The MCTS wins 100% of the games.
* **Gopher alpha-beta vs random**: The alpha-beta wins 100% of the games.
* **Gopher MCTS vs alpha-beta**: The two algorithms are equivalent, although alpha-beta has a slight advantage if given more time. However, MCTS is much more flexible.

## Conclusion

* **DODO**: For playing the DODO game, we decided to use the MCTS algorithm which is very powerful and flexible. It is capable of adapting to any grid size with its adaptive time and long games. However, it can still be greatly improved to increase the number of simulations.
* **GOPHER**: Conversely, for GOPHER we used the alpha-beta algorithm which is very effective for games with limited search depth like Gopher. Indeed, GOPHER is a game with a bounded number of moves, making it more predictable than DODO. In this game, alpha-beta can compete with MCTS. However, it is very inflexible and requires significant improvement in heuristic evaluation.

## Resources

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