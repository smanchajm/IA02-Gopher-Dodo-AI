""" Module concernant l'environnement du jeu Gopher-Dodo """
from archives.dodo_implementation import UP_DIRECTIONS
from structures_classes import *
import time
from Game_playing.grid import *
from Dodo.strategies_dodo import strategy_random_dodo, strategy_minmax


# Boucle de jeu Dodo
def dodo(
        env: GameDodo, strategy_1: Strategy, strategy_2: Strategy, init_grid: Grid, debug: bool = False
) -> Score:
    actual_grid: Grid = init_grid
    current_player: Player = env.max_player
    current_action: Action
    nb_iterations: int = 0
    total_time_start = time.time()  # Chronomètre

    while not (env.final_dodo(actual_grid) == 1 or env.final_dodo(actual_grid) == -1):
        nb_iterations += 1
        iteration_time_start = time.time()  # Chronomètre une itération de jeu
        print(f"Iteration \033[36m {nb_iterations}\033[0m.")
        if current_player.id == 1:
            current_action = strategy_1(env, current_player, actual_grid)
        else:
            current_action = strategy_2(env, current_player, actual_grid)
        actual_grid = env.play_dodo(current_player, actual_grid, current_action)
        if current_player.id == 1:
            current_player = env.min_player
        else:
            current_player = env.max_player
        hexa.display_grid(actual_grid)

        iteration_time_end = time.time()  # Fin du chronomètre pour la durée de cette itération
        print(f"Temps écoulé pour cette itération: {iteration_time_end - iteration_time_start} secondes")

    total_time_end = time.time()  # Fin du chronomètre pour la durée totale de la partie
    print(f"Temps total écoulé: {total_time_end - total_time_start} secondes")
    return env.final_dodo(actual_grid)


# Initialisation de l'environnement
def initialize(game: str, state: State, player: Player, hex_size: int, total_time: Time) -> Environment:
    if game == "Dodo":
        max_positions: State = []
        min_positions: State = []
        for cell in state:
            if cell[1] == player.id:
                max_positions.append((cell[0], player.id))
            else:
                min_positions.append((cell[0], player.id))
        return GameDodo(state, player, Player(2, UP_DIRECTIONS), hex_size, total_time, max_positions, min_positions)
    if game == "Gopher":
        pass
        # return GameGopher(state, player, Player(2, UP_DIRECTIONS), hex_size, total_time)
    else:
        raise ValueError("Jeu non reconnu")


def main():
    player1 = Player(1, DOWN_DIRECTIONS)
    game = initialize("Dodo", INIT_GRID4, player1, 7, 5)
    print(dodo(game, strategy_minmax, strategy_random_dodo, INIT_GRID4, False))


if __name__ == "__main__":
    main()
