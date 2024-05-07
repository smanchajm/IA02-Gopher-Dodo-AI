import numpy as np

Cell = tuple[int, int]
Player = int  # 1 ou 2
State = list[tuple[Cell, Player]]  # État du jeu pour la boucle de jeu

# Create a hexagonal grid
def grid_generation(n: int) -> np.ndarray:

    grid = np.zeros((2*n - 1), dtype=np.ndarray) # Permet de définir le nombre de lignes de la grille

    # Chaque ligne possède un tableau de taille n + i
    for i in range(0, n): # On créé les n premières lignes (triangle supérieur)
        grid[i] = np.zeros((n+i), dtype=object)
    for i in range(n, 2*n - 1): # On créé les n-1 dernières lignes (triangle inférieur)
        grid[i] = np.zeros((2*n+n-2-i), dtype=object)

    for r in range(0, 2*n - 1):
        if r < n:
            for q in range(0, n+r):
                grid[r][q] = Cell([n-r+q-1, r])
        else:
            # reverse pyramid
            for q in range(0, 2*n+n-2-r):
                grid[r][q] = Cell([q, r])

    return grid

def grid_to_state(grid: np.ndarray) -> State:
    state = []
    for r in range(0, len(grid)):
        for q in range(0, len(grid[r])):
            state.append((grid[r][q], 0))
    return state

def init_grid_dodo(n: int) -> State:
    grid = grid_generation(n)
    state = grid_to_state(grid)

    compteur = 0
    
    # Remplissage des cases de départ pour le joueur 1 (triangle supérieur)
    for j in range(0, n):
        state[compteur] = (state[compteur][0], 1)
        compteur += 1

    for i in range(1, n):
        for j in range(0, n+i):
            if (state[compteur][0][0]+state[compteur][0][1]) < 2*n-i:
                state[compteur] = (state[compteur][0], 1)
            compteur += 1

    return state

def display_state(state: State, n: int):
    # on parcourt toute la grille
    # si le player est 0, on affiche 0 en blanc
    # si le player est 1, on affiche 1 en bleu
    # si le player est 2, on affiche 2 en rouge
    compteur = 0
    for i in range(0, n): # On affiche les n premières lignes (triangle supérieur)
        for j in range(0, n+i):
            if state[compteur][1] == 0:
                print("\033[37m0", end=" ")
            elif state[compteur][1] == 1:
                print("\033[34m1", end=" ")
            else:
                print("\033[31m2", end=" ")
            compteur += 1
        print("")

    for i in range(n, 2*n - 1): # On affiche les n-1 dernières lignes (triangle inférieur)
        for j in range(0, 2*n+n-2-i):
            if state[compteur][1] == 0:
                print("\033[37m0", end=" ")
            elif state[compteur][1] == 1:
                print("\033[34m1", end=" ")
            else:
                print("\033[31m2", end=" ")
            compteur += 1
        print("")

def main():
    n = 4
    state = init_grid_dodo(n)
    # display_state(state, n)
    print(state)
    display_state(state,n)

if __name__ == "__main__":
    main()