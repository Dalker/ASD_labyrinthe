"""
Test visuel d'un générateur et solveur de labyrinthe.

Author: Dalker (daniel.kessler@dalker.org)
Date: 2021-04-10
"""

import logging as log

import matplotlib.pyplot as plt

import generateur_ab as ab
# import solveur_astar_naif as astar
import solveur_astar_heapq as astar


def test(maze, solver, distance, axes):
    """Tester le solver sur le maze donné et visualiser dans les axes."""
    log.debug("initial maze:\n%s", maze)
    path = solver(maze, distance=distance, view=axes)
    # if path is not None:
    #     print("A* solution found:")
    #     print("\n".join([
    #         "".join(["*" if (nrow, ncol) in path else val
    #                  for ncol, val in enumerate(row)])
    #         for nrow, row in enumerate(str(maze).split("\n"))]))
    if path is None:
        print("No A* solution found.")


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    print("* starting basic test *")
    # test(gen.MAZE10, view=True)
    maze = ab.Maze(20, 30, 0.1)
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
    test(maze, astar.astar, d1, ax1)
    test(maze, astar.astar, d2, ax2)
    test(maze, astar.astar, dj, axj)
    plt.show()
