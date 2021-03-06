"""
Solveur A* pour labyrinthe sur grille rectangulaire.

Cette version utilise heapq pour la queue prioritaire.

Author: Dalker
Date: 2021.04.16
"""

import heapq

from viewer import AstarView

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def distance1(x1, y1, x2, y2):
    """Retourner la "Manhattan distance" entre (x1, y1) et (x2, y2)."""
    return abs(x1 - x2) + abs(y1 - y2)


def distance2(x1, y1, x2, y2):
    """Retourner la distance euclidienne entre (x1, y1) et (x2, y2)."""
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


def distance0(x1, y1, x2, y2):
    """Retourner 0 (transforme A* en Dijkstra)."""
    return 0


def astar(grid, distance=distance1, view=None):
    """
    Trouver le plus court chemin vers la sortie.

    Entrée: grid est une grille rectangulaire sous forme d'objet
    contenant les attributs start et out et implémentant l'opération
    (row, col) in grid, retournant vrai si la cellule peut être traversée.

    Structures de donnée de travail:
    - closed: association des cellules déjà traversées à leur meilleur parent
    - fringe: heapq des cellules à traiter, priorisées par coût total heuristique
      cellule = tuple (heuristique, n_entree, cost, current, parent)
      - heuristique est le coût estimé d'un chemin passant par la cellule
        depuis le parent indiqué
      - n_entree est un numéro unique croissant qui, combiné à l'heuristique,
        assure une priorité unique sans lire le reste du tuple.
      - cost est le coût réel pour arriver à current depuis start via parent
      - current et parent sont des tuples (ligne, colonne)
    - distance: distance function to use for heuristics
    - view: Viewer to initialize with access to fringe and closed and call for updates
    """

    outrow, outcol = grid.out
    n_fringe = 0
    fringe = [(0, 0, 0, grid.start, None)]
    heapq.heapify(fringe)
    closed = {grid.start: None}

    if view is not None:
        astar_view = AstarView(grid, fringe, closed, view)

    while fringe != []:
        _, _,  cost, cell, parent = heapq.heappop(fringe)
        if view is not None:
            astar_view.update()
        if cell == grid.out:
            backtrack = [cell]
            cell = parent
            while cell is not None:
                backtrack.append(cell)
                cell = closed[cell]
            if view is not None:
                astar_view.showpath(backtrack)
            return reversed(backtrack)
        row, col = cell
        for prow, pcol in DIRECTIONS:
            newrow, newcol = row + prow, col + pcol
            if (newrow, newcol) not in grid:
                continue  # mouvement pas possible: passer au suivant
            if (newrow, newcol) in closed:
                continue  # cellule déjà traitée: passer au suivant
            n_fringe += 1
            # heuristic = abs(outrow - newrow) + abs(outcol - newcol)
            heuristic = distance(outrow, outcol, newrow, newcol)
            newcell = (newrow, newcol)
            heapq.heappush(fringe,
                           (cost+heuristic, n_fringe, cost+1, newcell, cell))
        closed[cell] = parent

    print("Astar: Failed to find a solution.")
    return None


def dijkstra(grid):
    """A* réduit à Dijkstra's algorithm en prenant heuristique nulle."""
    return astar(grid, distance=distance0)


if __name__ == "__main__":
    # test minimal
    import cProfile
    # from generateur_ascii import MAZE30 as maze
    from generateur_ab import Maze
    from pstats import SortKey
    maze = Maze(50, 60, 0.01)
    print(maze)
    # print(list(astar(MAZE10, distance=distance1)))
    cProfile.run("astar(maze, distance=distance0)", sort=SortKey.TIME)
    cProfile.run("astar(maze, distance=distance1)", sort=SortKey.TIME)
    cProfile.run("astar(maze, distance=distance2)", sort=SortKey.TIME)
