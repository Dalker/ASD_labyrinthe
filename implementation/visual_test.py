"""
Test visuel d'un générateur et solveur de labyrinthe.

Author: Dalker (daniel.kessler@dalker.org)
Date: 2021-04-10
"""

import logging as log

import matplotlib.pyplot as plt

import generateur_ab as ab
import solveur_astar_naif as astar


def test(maze, solver):
    """Effectuer un test avec la grille et le solveur donnés."""
    print("Trying to find an A* path in grid:")
    log.debug("initial maze:\n%s", maze)
    path = solver(maze)
    if path is not None:
        print("A* solution found:")
        print("\n".join([
            "".join(["*" if (nrow, ncol) in path else val
                     for ncol, val in enumerate(row)])
            for nrow, row in enumerate(str(maze).split("\n"))]))
    else:
        print("No A* solution found.")


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    print("* starting basic test *")
    # test(gen.MAZE10, view=True)
    maze = ab.Maze(30, 40, 0.1)
    d1 = astar.distance1
    d2 = astar.distance2
    dj = astar.distance0
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_title("A* with Manhattan distance")
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_title("A* with euclidean distance")
    axj = fig.add_subplot(2, 2, 3)
    axj.set_title("A* with 0 distance (= Dijkstra)")
    test(maze,
         lambda mz: astar.astar(mz, distance=d1, view=ax1))
    test(maze,
         lambda mz: astar.astar(mz, distance=d2, view=ax2))
    test(maze,
         lambda mz: astar.astar(mz, distance=dj, view=axj))
    plt.show()
