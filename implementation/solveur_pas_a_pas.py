"""
Solveur A* 3ème version après d'autres lectures.

Ce module fournit un solveur qui s'attend à travailler sur une
grille rectangulaire fournie comme un objet avec des attributs
start et out (tuples de coordonnée de départ et arrivée du
labyrinthe) et une métode __contains__ permettant de vérifier
si un tuple de coordonnées est accessible dans la grille.

Cette version permet d'avancer pas à pas dans le but de visualiser
la progression de l'algorithme.

Author: Dalker
Date: 2021.05.21
"""

from solveur_astar_v3 import manhattan_distance
from solveur_astar_v3 import QueuePrioritaire


class Astar():
    """
    Exécuteur d'algorithme A* pas à pas (à but de visualisation).

    Attributs:
    - grid: la grille à résoudre (consultable avec grid.start, grid.out,
            foo in grille)
    - marge, cout_reel, parent: structures de l'algorithme A*
      (cf. module solveur_astar_v3)
    - etape, chemin: données pour le backtrack
    """

    def __init__(self, grid, distance=manhattan_distance):
        """Préparer les structures de donnée pour A*."""
        self.grid = grid
        self.distance = distance
        # structures de donnée pour recherche A*
        self.marge = QueuePrioritaire(grid.start)
        self.cout_reel = {grid.start: 0}
        self.parent = {grid.start: None}
        # structures de donnée pour backtracking
        self.etape = self.grid.out
        self.chemin = []
        # état de départ
        self.etat = "recherche"  # passera ensuite à "backtrack" et "fini"

    def pas(self):
        """Exécuter un pas de l'algorithme, retourner False si fini."""
        if self.etat == "fini":
            return False
        if self.etat == "backtrack":
            self.backtrack()
        else:
            self.recherche()
        return True

    def recherche(self):
        """Exécuter un pas de recherche."""
        noeud_courant = self.marge.pop()
        if noeud_courant is None:
            raise ValueError("A*: la grille fournie n'a pas de solution")
        if noeud_courant == self.grid.out:
            self.etat = "backtrack"  # on a trouvé un chemin optimal
            return
        # après ces vérifications, on fait un vrai pas de A*
        for direction in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            # calculer coordonnées d'un voisin potentiel
            voisin = tuple([noeud_courant[i] + direction[i] for i in (0, 1)])
            if voisin not in self.grid:
                continue  # on ne peut pas accéder à ces coordonnées
            cout_voisin = self.cout_reel[noeud_courant] + 1
            if (voisin in self.cout_reel
                    and cout_voisin >= self.cout_reel[voisin]):
                continue  # on a un meilleur chemin pour arriver à ce voisin
            # on est arrivé jusqu'ici: ajouter le voisin à la marge
            self.cout_reel[voisin] = cout_voisin
            self.parent[voisin] = noeud_courant
            heuristique = cout_voisin + self.distance(voisin, self.grid.out)
            self.marge.insert(heuristique, voisin)

    def backtrack(self):
        """Faire un pas de backtracking."""
        if self.etape is None:
            self.etat = "fini"
            return
        self.chemin.append(self.etape)
        self.etape = self.parent[self.etape]


if __name__ == "__main__":
    # test minimal
    from generateur_ascii import MAZE10 as maze
    print(maze)
    astar = Astar(maze)
    while astar.pas():
        if astar.etat == "recherche":
            print(astar.marge)
        else:
            print(astar.chemin)
