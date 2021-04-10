"""
Test visuel d'un générateur et solveur de labyrinthe.

Author: Dalker (daniel.kessler@dalker.org)
Date: 2021-04-10
"""

import logging as log

import generateur_ab as ab
import solveur_astar_naif as astar_naif


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
    maze = ab.Maze(10, 10, .2)
    d1 = astar_naif.distance1
    d2 = astar_naif.distance2
    test(maze,
         lambda mz: astar_naif.astar(mz, distance=d1, view=True))
