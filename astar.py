"""Première tentative d'implémenter A* pour le projet ASD1-Labyrinthes.

On part d'une grille rectangulaire. Chaque case est un "noeud". Les
déplacements permis sont verticaux et horizontaux par pas de 1, représentant
des "arêtes" avec un coût de 1.

Author: Dalker (daniel.kessler@dalker.org)
Date: 2021.04.06

"""

import logging as log

import architecte


class Grid():
    """
    Grille à résoudre par l'algorithme (vrai labyrinthe ou autre).

    Attributs:
    - n_rows: nombre de lignes
    - n_cols: nombre de colonnes
    - content: liste de listes de booléens
               (True: on peut passer, False: obstacle)
    - in_: tuple (row, col) de l'entrée [NB: in est interdit comme identifiant]
    - out: tuple (row, col) de la sortie
    """

    def __init__(self, ascii_grid):
        """
        Construire grille à partir de représentation en str.

        La grille d'entrée doit utiliser les symboles:
          '#' pour obstacle
          'I' pour l'entrée
          'O' pour la sortie
        Tout autre caractère est interprété comme "on peut passer"
        """
        rows = ascii_grid.strip().split("\n")
        self.n_rows = len(rows)
        self.n_cols = len(rows[0])
        assert all((len(row) == self.n_cols) for row in rows),\
            "la grille devrait être rectangulaire"
        log.debug("created grid with %d rows and %d cols",
                  self.n_rows, self.n_cols)
        self.content = [[char != "#" for char in row] for row in rows]
        for n_row, row in enumerate(rows):
            for n_col, char in enumerate(row):
                if char == "I":
                    self.in_ = (n_row, n_col)
                elif char == "O":
                    self.out = (n_row, n_col)


class Node():
    """
    Noeud lors de l'exploration de la grille.

    Attributs:
    - coords: coordonnées de ce noeud dans la grille (tuple (row, col))
    - in_cost: coût réel pour accéder à ce noeud depuis l'entrée
    - total_cost: coût estimé pour cheminer de l'entrée jusqu'à la sortie via
                  ce noeud
    - predecessor: noeud précédent dans le chemin optimal arrivant à ce noeud
    """

    def __init__(self, coords, in_cost=0, total_cost=None, predecessor=None):
        """Initialiser un node."""
        self.coords = coords
        self.in_cost = 0
        self.total_cost = self.in_cost if total_cost is None else total_cost
        self.predecessor = predecessor

    def __lt__(self, other):
        """Comparaison pour utiliser les nodes dans une PriorityQueue."""
        return self.total_cost < other.total_cost

    def __str__(self):
        """Retourner une représentation en str."""
        return f"Node({self.coords}, cost={self.total_cost})"


class Fringe():
    """Ensemble de nodes en attente de traitement.

    On doit pouvoir extraire efficacement un node de priorité minimale, mais
    aussi chercher un node et modifier la priorité d'un node.

    D'après nos recherches, un "Fibonacci Heap" est optimal pour ce cas, mais
    pour l'instant nous utilisons un "Heap" beaucoup plus basique et facile à
    manipuler, à savoir un dict. L'implémentation de cette classe peut être
    modifiée par la suite sans en modifier l'interface.
    """

    def __init__(self, first_node):
        """Initialiser le fringe."""
        self._contents = {first_node.coords: first_node}

    def pop(self):
        """Extraire un noeud de bas coût."""
        least = min(self._contents,
                    key=lambda coords: self._contents[coords].total_cost)
        least_node = self._contents[least]
        del self._contents[least]
        return least_node


def astar(grid):
    """Trouver un chemin optimal dans une grille par algorithme A*."""
    grid = Grid(grid)
    fringe = Fringe(Node(grid.in_))
    print(fringe.pop())


def test(grid):
    """Effectuer un test avec la grille donnée."""
    astar(grid)


if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    log.info("starting test")
    test(architecte.GRILLE1)
