"""
Test visuel d'un générateur et solveur de labyrinthe.

Author: Dalker
Date: 2021-04-10
"""

import logging as log
# import concurrent.futures as cf

import matplotlib.pyplot as plt

import generateur_ab as ab
# import solveur_astar_naif as astar
import solveur_astar_heapq as astar_v2
import solveur_astar_v3 as astar_v3


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


def triple_test():
    """Comparer 3 choix de distances: Manhattan, Euclidean, 0 (pour v2)."""
    maze = ab.Maze(20, 30, 0.1)
    d1 = astar_v2.distance1
    d2 = astar_v2.distance2
    dj = astar_v2.distance0
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_title("A* with Manhattan distance")
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_title("A* with euclidean distance")
    axj = fig.add_subplot(2, 2, 3)
    axj.set_title("A* with 0 distance (= Dijkstra)")
    test(maze, astar_v2.astar, d1, ax1)
    test(maze, astar_v2.astar, d2, ax2)
    test(maze, astar_v2.astar, dj, axj)


def astar_vs_dijkstra():
    """Comparer 2 choix de distances: heuristique Manhattan vs. 0 (pour v3)."""
    maze = ab.Maze(25, 25, 0)
    fig = plt.figure()
    ax0 = fig.add_subplot(1, 2, 1)
    ax0.set_title("A* with null heuristic")
    ax1 = fig.add_subplot(1, 2, 2)
    ax1.set_title("A* with Manhattan heuristic")
    # tentative de concurrence ci-dessous: ne marche pas à cause du GUI
    # with cf.ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.submit(test, maze, astar.astar, d0, ax0)
    #     executor.submit(test, maze, astar.astar, d1, ax1)
    test(maze, astar_v3.astar, astar_v3.null_distance, ax0)
    test(maze, astar_v3.astar, astar_v3.manhattan_distance, ax1)


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    astar_vs_dijkstra()
    plt.show()
