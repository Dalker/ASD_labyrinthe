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
import time

import logging as log

import matplotlib.pyplot as plt

# import generateur_ascii as gen

import generateur_ab as ab


class Foo:
    def add_path(self, path):
        """Ajouter un chemin à la représentation ASCII de la grille."""


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


class AstarView():
    """
    Visualisation de l'avancée de l'algorithme A*.

    Attributs:
    - grid: Grid
    - fringe: Fringe
    - closed: list
    Tous trois sont des références aux objects manipulés en cours d'algorithme.
    Les modifications sont donc visibles automatiquement.
    """

    def __init__(self, grid, fringe, closed):
        """Initialiser la vue."""
        self.grid = grid
        lignes = str(grid).split("\n")
        n_rows = len(lignes)
        n_cols = max(len(ligne) for ligne in lignes)
        self.fringe = fringe
        self.closed = closed
        _, self._axes = plt.subplots()
        self.max_color = 2 * sum(abs(grid.start[j] - grid.out[j]) for j in (0, 1))
        self._matrix = [[16 if (row, col) in self.grid
                         else 0
                         for col in range(n_cols)]
                        for row in range(n_rows)]
        self._image = self._axes.matshow(self._matrix,
                                         cmap=plt.get_cmap("plasma"))
        self._axes.set_axis_off()
        self.update()

    def update(self):
        """Update and display the view of the Maze."""
        maxdistance = max(self.fringe.cost[cell]
                          for cell in self.fringe.heuristic) + 1
        for cell in self.fringe.heuristic:
            row, col = cell
            heuristic = self.fringe.cost[cell]
            self._matrix[row][col] = 16 - (8*heuristic) // maxdistance
            self._image.set_data(self._matrix)
        plt.pause(0.000001)

    def showpath(self, path):
        """Montrer le chemin trouvé et laisser l'image visible."""
        for row, col in path:
            self._matrix[row][col] = 2
            self._image.set_data(self._matrix)
            plt.pause(0.00001)
        plt.show()


def astar(grid, view=False):
    """
    Trouver un chemin optimal dans une grille par algorithme A*.

    Entrée: un objet Grid.
    Sortie: une liste de cellules successives constituant un chemin
    """
    closed = dict()  # associations cellule_traitée -> prédecesseur
    fringe = Fringe(grid.start)  # file d'attente de cellules à traiter
    if view:
        astar_view = AstarView(grid, fringe, closed)
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
            if view:
                astar_view.showpath(path)
            return path
        cost += 1
        for direction in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            neighbour = tuple(current[j] + direction[j] for j in (0, 1))
            if neighbour not in grid or neighbour in closed:
                continue
            distance = sum(abs(neighbour[j] - grid.out[j]) for j in (0, 1))
            fringe.append(neighbour, cost, cost+distance, predecessor=current)
            if view:
                astar_view.update()
        closed[current] = predecessor
        if view:
            astar_view.update()


def test(maze, view=False):
    """Effectuer un test avec la grille donnée."""
    # print("Trying to find an A* path in grid:")
    # print(maze)
    start_time = time.time()
    path = astar(maze, view)
    if path is not None:
        # grid.add_path(path)
        print("A* solution found for Maze ", maze.rows, " x ", maze.cols)
        path_str = "\n".join([
            "".join(["*" if (nrow, ncol) in path else val
                     for ncol, val in enumerate(row)])
            for nrow, row in enumerate(str(maze).split("\n"))])
        # print (path_str)
    else:
        print("No A* solution found.")
    elapsed = time.time() - start_time
    # print("time elapsed : ", elapsed, "s")
    return elapsed


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    
    time_ab = []
    rows_cols = []
    time_astar = []
    for i in range(1, 11):
        start_time = time.time()
        maze = ab.Maze(10*i, 10*i)
        time_ab.append(time.time() - start_time)
        rows_cols.append(maze.rows)
        time_astar.append(test(maze, view=False))
    for rows, ab_time, astar_time in zip(rows_cols, time_ab, time_astar):
        print(f"\nFor {rows}x{rows}: {ab_time}s for generate, {astar_time}s for solve")
        
