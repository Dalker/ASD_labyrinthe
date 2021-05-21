"""
Solveur A* 3ème version après d'autres lectures.

Ce module fournit un solveur qui s'attend à travailler sur une
grille rectangulaire fournie comme un objet avec des attributs
start et out (tuples de coordonnée de départ et arrivée du
labyrinthe) et une métode __contains__ permettant de vérifier
si un tuple de coordonnées est accessible dans la grille.

Author: Dalker
Date: 2021-05-14
"""

import heapq

from viewer import AstarView


def null_distance(node1, node2):
    """Retourner distance nulle entre noeuds pour émule Dijkstra."""
    return 0


def manhattan_distance(node1, node2):
    """Retourner la "Manhattan distance" (distance L1) entre 2 noeuds."""
    return abs(node2[0] - node1[0]) + abs(node2[1] - node1[1])


class QueuePrioritaire():
    """
    Queue prioritaire pour gérer la marge de A*.

    Attribut:
    - queue: heapq
    """

    def __init__(self, start):
        """Initialiser la queue à partir du noeud de départ."""
        self.queue = [(0, start)]
        heapq.heapify(self.queue)

    def __str__(self):
        """Retourner la file d'attente sous forme ascii."""
        return str(self.queue)

    def insert(self, priority, node):
        """Insérer un noeud dans la queue."""
        heapq.heappush(self.queue, (priority, node))

    def pop(self):
        """Obtenir le prochain noeud."""
        try:
            return heapq.heappop(self.queue)[1]
        except IndexError:  # la queue est vide
            return None


def astar(grid, distance=manhattan_distance, view=None):
    """
    Exécuter l'Algorithme A* et retourner le chemin optimal.

    L'objet grid fournit un départ grid.start, une arrivée grid.out et un moyen
    de vérifier si des coordonnées (x, y) sont accessibles: (x, y) in grid.

    En cours d'évolution, l'algorithme classe les noeuds connus en:
    - marge: ensemble des noeuds connectés pas encore évalués (initialisée avec
             le noeud de départ)
    - noeuds déjà évalués, avec leur cout_reel (coût pour y arriver par le
      meilleur chemin trouvé jusqu'à présent) et predecesseur (noeuds précédent
      dans le meilleur chemin chemin trouvé pour y arriver jusqu'à présent)

    La marge est une queue prioritaire avec comme priorité le coût réel pour
    arriver au noeud + le coût heuristique pour poursuivre jusqu'à la sortie.

    Quand la sortie est prioritaire dans la marge, on a trouvé un chemin de
    distance minimale. En effet, si ce n'était pas le cas, un autre noeud de
    la marge aurait une distance réelle inférieure et serait prioritaire, vu
    qu'une heuristique admissible n'a pas le droit de sur-estimer les
    distances.
    """

    marge = QueuePrioritaire(grid.start)
    cout_reel = {grid.start: 0}
    parent = {grid.start: None}

    if view is not None:
        viewer = AstarView(grid, marge.queue, cout_reel, view)

    while True:
        if view is not None:
            viewer.update()
        noeud_courant = marge.pop()
        if noeud_courant is None:
            raise ValueError("A*: la grille fournie n'a pas de solution")
        if noeud_courant == grid.out:
            break  # on a trouvé un chemin optimal vers la sortie
        for direction in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            # calculer coordonnées d'un voisin potentiel
            voisin = tuple([noeud_courant[i] + direction[i] for i in (0, 1)])
            if voisin not in grid:
                continue  # on ne peut pas accéder à ces coordonnées
            cout_voisin = cout_reel[noeud_courant] + 1
            if voisin in cout_reel and cout_voisin >= cout_reel[voisin]:
                continue  # on a un meilleur chemin pour arriver à ce voisin
            # on est arrivé jusqu'ici: ajouter le voisin à la marge
            cout_reel[voisin] = cout_voisin
            parent[voisin] = noeud_courant
            marge.insert(cout_voisin + distance(voisin, grid.out), voisin)

    # on est arrivé jusqu'ici: le chemin optimal a été trouvé
    etape = grid.out
    chemin = []
    while etape is not None:
        chemin.append(etape)
        etape = parent[etape]
    if view is not None:
        viewer.showpath(chemin)
    return reversed(chemin)


if __name__ == "__main__":
    # test minimal
    import cProfile
    from pstats import SortKey
    from generateur_ascii import MAZE10 as maze
    # from generateur_ab import Maze
    # maze = Maze(50, 60, 0.01)
    print(maze)
    print(list(astar(maze, distance=manhattan_distance)))
    # cProfile.run("astar(maze, distance=distance0)", sort=SortKey.TIME)
    # cProfile.run("astar(maze, distance=distance1)", sort=SortKey.TIME)
