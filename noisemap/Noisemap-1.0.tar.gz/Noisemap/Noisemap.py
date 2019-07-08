import random
import numpy as np
import sys

print("Noise Map Experiment 1")
print("(c) Proximas 2019")
print()


def mapGen(size, smoothness):

    print("Creating map...", end="", flush=True)

    global grid
    grid = [[random.random() for x in range(size)] for y in range(size)] #Create the array
    print("done")

    print("Smoothing map...", end="", flush=True)

    for i in range(smoothness):
        for x in range(len(grid)): #Average out the points to make the noise more smooth
            for y in range(len(grid)):
                try:
                    chunksum = grid[x][y - 1] + grid[x - 1][y] + grid[x + 1][y] + grid[x][y + 1] + grid[x][y]

                except IndexError:
                    a = 0
    print("done")
                

    global grid2
    grid2 = np.array(grid)

    return grid2
