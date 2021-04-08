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

import matplotlib.pyplot as plt

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
    - passable: liste de listes de booléens
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
        self.passable = [[char != "#" for char in row] for row in rows]
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
        """La cellule est-elle dans la grille et traversable?"""
        row, col, *_ = cell  # décomposer le tuple de coordonnées
        if (0 <= row < self.n_rows and
                0 <= col < self.n_cols and
                self.passable[row][col]):
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
        self.fringe = fringe
        self.closed = closed
        _, self._axes = plt.subplots()
        self.max_color = 2*sum(abs(grid.in_[j] - grid.out[j]) for j in (0, 1))
        self._matrix = [[0 if self.grid.passable[row][col]
                         else 2*self.max_color
                         for col in range(grid.n_cols)]
                        for row in range(grid.n_rows)]
        self._image = self._axes.matshow(self._matrix)
        self._axes.set_axis_off()
        self.update()

    def update(self):
        """Update and display the view of the Maze."""
        for cell in self.fringe.heuristic:
            row, col = cell
            heuristic = self.fringe.heuristic[cell]
            self._matrix[row][col] = heuristic
            self._image.set_data(self._matrix)
        plt.pause(0.001)

    def showpath(self, path):
        """Montrer le chemin trouvé et laisser l'image visible."""
        for row, col in path:
            self._matrix[row][col] = self.max_color
            self._image.set_data(self._matrix)
            plt.pause(0.1)
        plt.show()


def astar(grid, view=False):
    """
    Trouver un chemin optimal dans une grille par algorithme A*.

    Entrée: un objet Grid.
    Sortie: une liste de cellules successives constituant un chemin
    """
    closed = dict()  # associations cellule_traitée -> prédecesseur
    fringe = Fringe(grid.in_)  # file d'attente de cellules à traiter
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


def test(asciimaze, view=False):
    """Effectuer un test avec la grille donnée."""
    grid = Grid(asciimaze)
    print("Trying to find an A* path in grid:")
    print(grid)
    path = astar(grid, view)
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
    test(architecte.GRILLE2, view=True)
