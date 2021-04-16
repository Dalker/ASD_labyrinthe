"""
Solveur A* pour labyrinthe sur grille rectangulaire.

Cette version utilise heapq pour la queue prioritaire.

Author: Dalker (daniel.kessler@dalker.org)
Date: 2021-04-16
"""

import heapq

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def astar(grid):
    """
    Trouver le plus court chemin vers la sortie.

    Entrée: grid est une grille rectangulaire sous forme d'objet
    contenant les attributs start et out et implémentant l'opération
    (row, col) in grid, retournant vrai si la cellule peut être traversée.

    Structures de donnée de travail:
    - closed: association des cellules déjà traversées à leurs parents
    - fringe: heapq des cellules à traiter, priorisées par coût heuristique
      cellule = tuple (heuristique, n_entree, cost, current, parent)
      - heuristique est le coût estimé d'un chemin passant par la cellule
        depuis le parent indiqué
      - n_entree est un numéro unique croissant qui, combiné à l'heuristique,
        assure une priorité unique sans lire le reste du tuple.
      - cost est le coût réel pour arriver à current depuis start via parent
      - current et parent sont des tuples (ligne, colonne)
    """

    outrow, outcol = grid.out
    n_fringe = 0
    fringe = [(0, 0, 0, grid.start, None)]
    heapq.heapify(fringe)
    closed = {grid.start: None}

    while fringe != []:
        _, _,  cost, cell, parent = heapq.heappop(fringe)
        if cell == grid.out:
            backtrack = [cell]
            cell = parent
            while cell is not None:
                backtrack.append(cell)
                cell = closed[cell]
            return reversed(backtrack)
        row, col = cell
        for prow, pcol in DIRECTIONS:
            newrow, newcol = row + prow, col + pcol
            if (newrow, newcol) not in grid:
                continue
            if (newrow, newcol) in closed:
                continue
            n_fringe += 1
            heuristic = abs(outrow - newrow) + abs(outcol - newcol)
            newcell = (newrow, newcol)
            heapq.heappush(fringe,
                           (heuristic, n_fringe, cost+1, newcell, cell))
        closed[cell] = parent

    print("Astar: Failed to find a solution.")
    return None


if __name__ == "__main__":
    # test minimal
    from generateur_ascii import MAZE10
    print(list(astar(MAZE10)))
