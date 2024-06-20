# Board Game AI Challenge : Dodo and Gopher AI

The aim of this project is to create artificial Gopher and Dodo players capable of playing in an AI competition.
This project was carried out as part of the IA02 (Problem-Solving and Logic Programming) course at the Compiegne University of Technology (UTC).

These two games were created by Mark Steere.

## Rules

Both games are played on a hexagonal board. The implementation is freely inspired by Red Blob Games [Implementation of hex Grid](https://www.redblobgames.com/grids/hexagons/).

* **[Dodo Rules](https://www.redblobgames.com/grids/hexagons/)**.
* **[Gopher Rules](https://www.marksteeregames.com/Dodo_rules.pdf)**.

## Features

* Run simulations for "Gopher" and "Dodo" games.
* Apply different strategies for each player (minmax, random, MCTS).
* Benchmark and visualize game performance.
* Debugging and graphical output options.

## Requirements

* Python 3.6 or higher
* Required Python packages: `matplotlib`
* Add the path of the project to the PYTHONPATH environment variable.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/gopher-dodo.git
cd Game_playing
```

2. Install the required Python packages:

```sh
pip install matplotlib
```

## Usage

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

### Examples

1. Launch a single game of "Dodo" with random strategy for player 1 and minmax strategy for player 2:

   ```sh
   python3 main.py dodo --strategy1 random --strategy2 minmax
   ```

2. Launch five games of "Gopher" with MCTS for both players:

   ```sh
   python3 main.py gopher --games 5 --strategy1 mcts --strategy2 mcts
   ```

## Code Structure

* `view_graphic`: Displays iteration time as a graph.
* `dodo`: Game loop for "Dodo" with timing and debugging features.
* `gopher`: Game loop for "Gopher" with specific initialization for the first move.
* `initialize`: Initializes the game environment.
* `grid_state_color`: Converts the game state into a colored grid representation.
* `print_gopher`: Prints the current state of the "Gopher" game board.
* `launch_multi_game`: Runs multiple game sessions consecutively and stores the results.
* `main`: Entry point for the module to launch games based on command-line arguments.

## Contributors

* Paul Clément
* Samuel Manchajm

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

For questions or suggestions, please open an issue on GitHub or contact the repository owner.

---

This README provides an overview of the project, installation instructions, usage examples, and a brief description of the code structure. Adjust the `git clone` URL and other specific details as needed for your project.
