import numpy as np

Cell = tuple[int, int]

# Create a hexagonal grid
def grid_generation(n: int) -> np.ndarray:
    grid = np.zeros((2*n-1, 2*n-1), dtype=object)

    for r in range(0, 2*n - 1):
        if r < n:
            for q in range(0, n+r):
                grid[r][q] = Cell([n-r+q-1, r])
        else:
            # reverse pyramid
            for q in range(0, 2*n+n-2-r):
                grid[r][q] = Cell([q, r])

    return grid


def main():
    n = 4
    print(grid_generation(n))

if __name__ == "__main__":
    main()