"""
Première tentative d'implémenter A* pour le projet ASD1-Labyrinthes.

On part d'une grille rectangulaire. Chaque case est un "noeud". Les
déplacements permis sont verticaux et horizontaux par pas de 1, représentant
des "arêtes" avec un coût de 1.

Tout est basé sur une grille rectangulaire.

L'objet de base est une cellule, représentée par un tuple (row, col, cost), où
(row, col) sont des coordonnées dans la grille et cost le coût réel pour
arriver jusqu'à cette cellule depuis le départ, s'il est déjà connu, None
sinon.

Author: Dalker (daniel.kessler@dalker.org)
Start Date: 2021.04.06
"""

import logging as log
from viewer import AstarView


class Fringe():
    """
    Ensemble de cellules en attente de traitement avec informations de coût.

    Une cellule est un tuple (row, col, cost). Le Fringe associe à chacune
    aussi un coût estimé, qui doit être fourni lorsque la cellule est ajoutée.

    On doit pouvoir extraire efficacement une cellule de priorité minimale,
    mais aussi chercher une cellule et modifier la priorité d'un node.

    D'après nos recherches, un "Fibonacci Heap" est optimal pour ce cas, mais
    pour l'instant nous utilisons un "Heap" beaucoup plus basique et facile à
    manipuler, à savoir un (ou plusieurs) dict. L'implémentation de cette
    classe peut être modifiée par la suite sans en modifier l'interface.

    Attributs:
    - cost: coût réel pour accéder à cette cellule
    - heuristic: coût heuristique d'une cellule
    """

    def __init__(self, first_cell):
        """
        Initialiser le fringe.

        Entrée: un tuple (ligne, colonne) indiquant l'entrée du labyrinthe.
        """
        self.cost = {first_cell: 0}
        self.heuristic = {first_cell: 0}
        self._predecessor = {first_cell: None}

    def append(self, cell, real_cost, estimated_cost, predecessor=None):
        """
        Ajouter une cellule au fringe ou la mettre à jour.

        Si la cellule est déjà présente, on la met à jour si le nouveau coût
        est plus bas que le précédent (on a trouvé un meilleur chemin pour y
        arriver).

        Entrées:
        - cell: cellule sous forme (row, col)
        - real_cost: coût réel pour arriver jusqu'à cette cellule
        - estimated_cost: coût estimé d'un chemin complet passant par cell
        - predecessor: cellule précédente dans le chemin arrivant à cell
                       avec le coût réel indiqué
        """
        if cell not in self.cost or real_cost < self.cost[cell]:
            self.cost[cell] = real_cost
            self.heuristic[cell] = estimated_cost
            self._predecessor[cell] = predecessor

    def pop(self):
        """
        Extraire un noeud de bas coût ainsi que son prédecesseur.

        Sortie: tuple (cellule, prédecesseur, coût)
        """
        if not self.heuristic:  # fringe is empty
            return None, None, None
        least = min(self.heuristic,
                    key=lambda cell: self.heuristic[cell])
        del self.heuristic[least]
        return least, self._predecessor[least], self.cost[least]


def distance0(cell1, cell2):
    """Return 0 distance for A* to behave like Dijkstra's algorithm."""
    return 0


def distance1(cell1, cell2):
    """Return Manhattan distance between cells."""
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])


def distance2(cell1, cell2):
    """Return euclidean distance between cells."""
    return ((cell1[0] - cell2[0])**2 + (cell1[1] - cell2[1])**2)**0.5


def astar(grid, distance=distance1, view=None, diagonals=False):
    """
    Trouver un chemin optimal dans une grille par algorithme A*.

    Entrée: un objet Grid.
    Sortie: une liste de cellules successives constituant un chemin
    """
    directions = ((0, 1, 1), (0, -1, 1), (-1, 0, 1), (1, 0, 1))
    if diagonals:
        directions += ((1, 1, 1.4), (1, -1, 1.4), (-1, 1, 1.4), (-1, -1, 1.4))
    closed = dict()  # associations cellule_traitée -> prédecesseur
    fringe = Fringe(grid.start)  # file d'attente de cellules à traiter
    if view is not None:
        astar_view = AstarView(grid, fringe.heuristic, closed, view)
    while True:
        current, predecessor, cost = fringe.pop()
        if current is None:
            log.debug("Le labyrinthe ne peut pas être résolu.")
            return None
        if current == grid.out:
            log.debug("Found exit!")
            path = [current]
            current = predecessor
            while current in closed:
                path.append(current)
                current = closed[current]
            path = list(reversed(path))
            if view is not None:
                astar_view.showpath(path)
            return path
        for direction in directions:
            neighbour = tuple(current[j] + direction[j] for j in (0, 1))
            if neighbour not in grid or neighbour in closed:
                continue
            neighbour_cost = cost + direction[2]
            heuristic = neighbour_cost + distance(neighbour, grid.out)
            fringe.append(neighbour,
                          neighbour_cost,
                          heuristic,
                          predecessor=current)
        closed[current] = predecessor
        if view is not None:
            astar_view.update()


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
