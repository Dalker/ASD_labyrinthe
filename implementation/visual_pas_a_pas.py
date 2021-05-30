"""
Visualiseur comparatif d'A* avec distance Manhattan vs.  distance nulle
(équivalent Dijkstra), pas à pas.

Author: Dalker
Date: 2021.05.21

Usage:
  visual_pas_a_pas [-1|-2|-3] [-r]

Options:
  -1, -2: limiter le nombre de subplots
  -r: créer un labyrinthe au hasard
"""
import copy
import docopt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

from generateur_ab import Maze
from generateur_ascii import MAZE10
from solveur_astar_v3 import null_distance
from solveur_pas_a_pas import Astar

UNKNOWN = 0
WALL = 1
NULL = 2
MANHATTAN = 3
CHEMIN = 4  # en mettant "start" à 4, on garantit que le colormap fonctionne
# (cat matplotlib veut le range numérique complet des couleurs dès le départ)

COLORMAP = ListedColormap(('#111', 'dark blue', 'light green',
                           'light blue', 'orange'))

INTERVAL = 10  # intervalle pour animation


class DualViewer():
    """
    Visualiseur pour deux résolutions du même labyrinthe.

    Attributs:
    - solving: booléen, vrai après clic sur fenêtre pour démarrer
    - grid: le labyrinthe à résoudre
    - self.fig, self.ax1, self.ax2, self.axdiff: objets matplotlib persistants
    - img1, img2, imgdiff: images matplotlib
    """

    def __init__(self, grid, variante=None):
        """Mettre en place le visualiseur."""
        self.grid = grid
        # set up simulation, whatever is chosen for visuals later
        self.solving = False
        lignes = str(grid).split("\n")
        n_rows = len(lignes)
        n_cols = max(len(ligne) for ligne in lignes)
        self.solver1 = Astar(self.grid)
        self.solver0 = Astar(self.grid, distance=null_distance)
        self._matrix1 = [[UNKNOWN if (row, col) in self.grid
                          else WALL
                          for col in range(n_cols)]
                         for row in range(n_rows)]
        self._matrix0 = copy.deepcopy(self._matrix1)
        self._matrixd = [[UNKNOWN for col in range(n_cols)]
                         for row in range(n_rows)]
        self._matrixd[self.grid.start[0]][self.grid.start[1]] = CHEMIN
        for mat in (self._matrix0, self._matrix1):
            mat[self.grid.out[0]][self.grid.out[1]] = CHEMIN
        # prepare figure
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect("button_press_event", self.click)
        side = 0.35
        shifty = .35
        self.axes = []
        self.artists = []
        # add image of Null simulation unless variante 1
        if variante != 1:
            self.ax1 = self.fig.add_axes((.05, shifty, side, side))
            self.axt1 = self.fig.add_axes((.05, shifty-.05, side, .05))
            self.txt1 = self.axt1.text(.4, 0, "$N=0$")
            self.axes += [self.ax1, self.axt1]
            self.artists.append(self.txt1)
        else:
            self.ax1 = None
        # always add image of 1st simulation, but center if alone
        if variante == 1:
            self.ax2 = self.fig.add_axes((.35, shifty, side, side))
            self.axt2 = self.fig.add_axes((.35, shifty-.05, side, .05))
        else:
            self.ax2 = self.fig.add_axes((.65, shifty, side, side))
            self.axt2 = self.fig.add_axes((.65, shifty-.05, side, .05))
        self.txt2 = self.axt2.text(.4, 0, "$N=0$")
        self.axes += [self.ax2, self.axt2]
        self.artists.append(self.txt2)
        # add image of 3d simulation only in default case
        if variante not in (1, 2):
            self.axd = self.fig.add_axes((.35, shifty, side, side))
            self.axes.append(self.axd)
        else:
            self.axd = None
        for ax in self.axes:
            ax.set_axis_off()

    def animate(self):
        """Animer les solveurs."""
        self._anim = FuncAnimation(self.fig, self.step_anim,
                                   init_func=self.init_anim,
                                   blit=True, interval=INTERVAL)

    def click(self, event):
        """Recevoir un clic de souris."""
        self.solving = not self.solving

    def step_anim(self, frame):
        """Avancer d'un pas l'animation."""
        if not self.solving:
            # bizarement ces textes disparaissent sinon
            # return self.txt1, self.txt2
            return self.artists
        self.solver0.pas()
        self.solver1.pas()
        if self.solver0.etat == "backtrack":
            for _ in range(5):
                self.solver0.pas()
        if self.solver1.etat == "backtrack":
            for _ in range(5):
                self.solver1.pas()
        for x, y in self.solver0.cout_reel:
            self._matrix0[x][y] = NULL
            if (x, y) in self.solver1.cout_reel:
                self._matrixd[x][y] = UNKNOWN
            else:
                self._matrixd[x][y] = NULL
        for x, y in self.solver1.cout_reel:
            self._matrix1[x][y] = MANHATTAN
            if (x, y) in self.solver0.cout_reel:
                self._matrixd[x][y] = UNKNOWN
            else:
                self._matrixd[x][y] = MANHATTAN
        for x, y in self.solver1.chemin:
            self._matrix1[x][y] = CHEMIN
        for x, y in self.solver0.chemin:
            self._matrix0[x][y] = CHEMIN
        count1 = len(self.solver0.cout_reel)
        count2 = len(self.solver1.cout_reel)
        if self.ax1 is not None:
            self.img1.set_data(self._matrix0)
            self.txt1.set_text(f"$N={count1}$")
        if self.ax2 is not None:
            self.img2.set_data(self._matrix1)
            self.txt2.set_text(f"$N={count2}$")
        if self.axd is not None:
            self.imgd.set_data(self._matrixd)
        return self.artists

    def init_anim(self):
        """Initialisation de l'animation."""
        if self.ax1 is not None:
            self.ax1.set_title("heuristique nulle")
            self.img1 = self.ax1.matshow(self._matrix0)
            self.artists.append(self.img1)
        if self.ax2 is not None:
            self.ax2.set_title("heuristique Manhattan")
            self.img2 = self.ax2.matshow(self._matrix1)
            self.artists.append(self.img2)
        if self.axd is not None:
            self.axd.set_title("différence")
            self.imgd = self.axd.matshow(self._matrixd)
            self.artists.append(self.imgd)
        return self.artists


if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["-1"]:
        variante = 1
    elif options["-2"]:
        variante = 2
    else:
        variante = 3
    if options["-r"]:
        maze = Maze(20, 20, 0)
    else:
        maze = MAZE10
    viewer = DualViewer(maze, variante)
    viewer.animate()
    plt.show()
