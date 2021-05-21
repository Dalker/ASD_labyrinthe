"""
Visualiseur comparatif d'A* avec distance Manhattan vs.  distance nulle
(équivalent Dijkstra), pas à pas.

Author: Dalker
Date: 2021.05.21
"""

import matplotlib.pyplot as plt

from generateur_ab import Maze
from solveur_pas_a_pas import Astar

UNKNOWN = 0
WALL = 1


class DualViewer():
    """
    Visualiseur pour deux résolutions du même labyrinthe.

    Attributs:
    - grid: le labyrinthe à résoudre
    - ...
    """

    def __init__(self, grid):
        """Mettre en place le visualiseur."""
        self.grid = grid
        _, (self.ax1, self.axdiff, self.ax2) = plt.subplots(1, 3)
        lignes = str(grid).split("\n")
        n_rows = len(lignes)
        n_cols = max(len(ligne) for ligne in lignes)
        self._matrix = [[UNKNOWN if (row, col) in self.grid
                         else WALL
                         for col in range(n_cols)]
                        for row in range(n_rows)]
        for ax in (self.ax1, self.axdiff, self.ax2):
            ax.matshow(self._matrix)


if __name__ == "__main__":
    maze = Maze(20, 20, 0)
    viewer = DualViewer(maze)
    plt.show()
    
