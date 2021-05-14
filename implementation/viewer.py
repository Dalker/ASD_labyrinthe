"""Viewer for A* type solver."""

import matplotlib.pyplot as plt


class AstarView():
    """
    Visualisation de l'avancée de l'algorithme A*.

    Attributs:
    - axes: matplotlib Axes
    - grid: Grid
    - fringe: access to "fringe" that can be tested with "cell in fringe"
    - closed: access to "closed list" that can be tested with "cell in closed"
    Tous trois sont des références aux objects manipulés en cours d'algorithme.
    Les modifications sont donc visibles automatiquement.
    """

    def __init__(self, grid, fringe, closed, axes=None):
        """Initialiser la vue."""
        if axes is None or axes is True:
            _, self.axes = plt.subplots()
        else:
            self.axes = axes
        self.grid = grid
        lignes = str(grid).split("\n")
        n_rows = len(lignes)
        n_cols = max(len(ligne) for ligne in lignes)
        self.update_freq = int((n_rows * n_cols)**.5) // 2
        self.update_next = 1
        self.fringe = fringe
        self.closed = closed
        self._matrix = [[10 if (row, col) in self.grid
                         else 0
                         for col in range(n_cols)]
                        for row in range(n_rows)]
        self._image = self.axes.matshow(self._matrix,
                                        cmap=plt.get_cmap("twilight"))
        self.axes.set_axis_off()
        self.update()

    def update(self):
        """Update and display the view of the Maze."""
        self.update_next -= 1
        if self.update_next == 0:
            self.update_next = self.update_freq
            for row, col in self.closed:
                self._matrix[row][col] = 2
            for cell in self.fringe:
                try:
                    row, col = cell[1]
                except ValueError:
                    row, col = cell[-2]
                self._matrix[row][col] = 5
            self._image.set_data(self._matrix)
            plt.pause(0.000001)

    def showpath(self, path):
        """Montrer le chemin trouvé et laisser l'image visible."""
        for row, col in path:
            self._matrix[row][col] = 8
            self._image.set_data(self._matrix)
        plt.pause(0.00001)
