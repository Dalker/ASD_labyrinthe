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

import architecte


class Grid():
    """
    Grille à résoudre par l'algorithme (vrai labyrinthe ou autre).

    NB: la grille est fixe et ne connaît pas les coûts, donc ne gère que des
    cellules représentées par des tuples (row, col), tout en acceptant
    (row, col, _) comme entrée de ses méthodes.

    Attributs:
    - ascii: représentation ASCII de la grille
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
        self.ascii = ascii_grid.strip()
        rows = self.ascii.split("\n")
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

    def __str__(self):
        """Restituer une vue ASCII de la grille."""
        return self.ascii

    def __contains__(self, cell):
        """La cellule est-elle dans la grille?"""
        row, col, *_ = cell  # décomposer le tuple de coordonnées
        if (0 <= row < self.n_rows and
                0 <= col < self.n_cols and
                self.content[row][col]):
            return True
        return False

    def add_path(self, path):
        """Ajouter un chemin à la représentation ASCII de la grille."""
        asciirows = self.ascii.split("\n")
        self.ascii = "\n".join([
            "".join(["*" if (row, col) in path else asciirows[row][col]
                     for col in range(self.n_cols)])
            for row in range(self.n_rows)])


class Fringe():
    """
    Ensemble de cellules en attente de traitement.

    Une cellule est un tuple (row, col, cost). Le Fringe associe à chacune
    aussi un coût estimé, qui doit être fourni lorsque la cellule est ajoutée.

    On doit pouvoir extraire efficacement une cellule de priorité minimale,
    mais aussi chercher une cellule et modifier la priorité d'un node.

    D'après nos recherches, un "Fibonacci Heap" est optimal pour ce cas, mais
    pour l'instant nous utilisons un "Heap" beaucoup plus basique et facile à
    manipuler, à savoir un dict. L'implémentation de cette classe peut être
    modifiée par la suite sans en modifier l'interface.
    """

    def __init__(self, first_cell):
        """
        Initialiser le fringe.

        Entrée: un tuple (ligne, colonne) indiquant l'entrée du labyrinthe.
        """
        self._cost = {first_cell: 0}
        self._heuristic = {first_cell: 0}
        self._predecessor = {first_cell: None}

    def append(self, cell, real_cost, estimated_cost, predecessor=None):
        """
        Ajouter une cellule au fringe ou la mettre à jour.

        Si la cellule est déjà présente, on la met à jour si le nouveau coût
        estimé est plus bas que le précédent.

        Entrées:
        - cell: cellule sous forme (row, col, cout_reel_pour_arriver_a_cell)
        - estimated_cost: coût estimé d'un chemin complet passant par cell
        - predecessor: cellule précédente dans le chemin arrivant à cell
                       avec le coût réel indiqué
        """
        if cell not in self._heuristic:
            self._cost[cell] = real_cost
            self._heuristic[cell] = estimated_cost
            self._predecessor[cell] = predecessor

    def pop(self):
        """Extraire un noeud de bas coût ainsi que son prédecesseur."""
        if not self._heuristic:  # fringe is empty
            return None, None, None
        least = min(self._heuristic,
                    key=lambda cell: self._heuristic[cell])
        del self._heuristic[least]
        return least, self._predecessor[least], self._cost[least]


def astar(grid):
    """
    Trouver un chemin optimal dans une grille par algorithme A*.

    Entrée: un objet Grid.
    """
    closed = dict()  # associations cellule_traitée -> prédecesseur
    fringe = Fringe(grid.in_)  # file d'attente de cellules à traiter
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
            return list(reversed(path))
        cost += 1
        for direction in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            neighbour = tuple(current[j] + direction[j] for j in (0, 1))
            if neighbour not in grid or neighbour in closed:
                continue
            distance = sum(abs(neighbour[j] - grid.out[j]) for j in (0, 1))
            fringe.append(neighbour, cost, cost+distance, predecessor=current)
        closed[current] = predecessor


def test(asciimaze):
    """Effectuer un test avec la grille donnée."""
    grid = Grid(asciimaze)
    print("Trying to find an A* path in grid:")
    print(grid)
    path = astar(grid)
    if path is not None:
        grid.add_path(path)
        print("A* solution found:")
        print(grid)
    else:
        print("No A* solution found.")
    print()


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    print("* starting unsolvable test *")
    test("#I#O#")
    print("* starting basic test *")
    test(architecte.GRILLE1)
