"""
Viewer for A* type solver.

Author: Dalker
Date: 2021.04-05
"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

EXPLORED = 2
FRINGE = 5
PATH = 8
UNKNOWN = 10
WALL = 0

UNKNOWN = 0
PATH = 1
FRINGE = 2
EXPLORED = 3  # start of Explored values (10 shades)
WALL = 14

COLORMAP = ListedColormap(['#222',  # unknown -> gris
                           '#a40',  # path -> orange
                           '#770',  # fringe -> jaune
                           # 10 tons pour "explored" selon coût
                           '#44f',
                           '#44e',
                           '#33d',
                           '#33c',
                           '#22b',
                           '#22a',
                           '#119',
                           '#118',
                           '#007',
                           '#006',
                           '#111',  # wall -> noir
                           ])


class AstarView():
    """
    Visualisation de l'avancée de l'algorithme A*.

    Attributs:
    - axes: matplotlib Axes
    - grid: Grid
    - fringe: access to object that can be tested with "cell in fringe"
    - explored: access to object that can be tested with "cell in explored"
    Tous trois sont des références aux objects manipulés en cours d'algorithme.
    Les modifications sont donc visibles automatiquement.
    """

    def __init__(self, grid, fringe, explored, axes=None):
        """Initialiser la vue."""
        if axes is None or axes is True:
            _, self.axes = plt.subplots()
        else:
            self.axes = axes
        self.grid = grid
        lignes = str(grid).split("\n")
        n_rows = len(lignes)
        n_cols = max(len(ligne) for ligne in lignes)
        self.max_cost = int(3 * (n_rows * n_cols)**.5)
        self.update_freq = int((n_rows * n_cols)**.5) // 2
        self.update_next = 1
        self.fringe = fringe
        self.explored = explored
        self._matrix = [[UNKNOWN if (row, col) in self.grid
                         else WALL
                         for col in range(n_cols)]
                        for row in range(n_rows)]
        self._image = self.axes.matshow(self._matrix,
                                        cmap=COLORMAP,
                                        # cmap=plt.get_cmap("twilight")
                                        )
        self.axes.set_axis_off()
        self.update()

    def colornum(self, row, col):
        """Translate a cost into a number between 0 and 9."""
        if self.explored[(row, col)]:
            cost = self.explored[(row, col)]
        else: cost = row * col // 2 + 1
        if cost > self.max_cost:
            print("cost overflow:", cost, "/", self.max_cost)
        return EXPLORED + min(10 * cost // self.max_cost, 9)

    def update(self):
        """Update and display the view of the Maze."""
        self.update_next -= 1
        if self.update_next == 0:
            self.update_next = self.update_freq
            for row, col in self.explored:
                self._matrix[row][col] = self.colornum(row, col)
            for cell in self.fringe:
                row, col = cell[1]
                self._matrix[row][col] = FRINGE
            self._image.set_data(self._matrix)
            plt.pause(0.000001)

    def showpath(self, path):
        """Montrer le chemin trouvé et laisser l'image visible."""
        for row, col in path:
            self._matrix[row][col] = PATH
            self._image.set_data(self._matrix)
        plt.pause(0.00001)
