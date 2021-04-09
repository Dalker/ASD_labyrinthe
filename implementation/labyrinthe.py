"""
Partie commune du projet ASD1-Labyrinthes.

Ce module est prévu pour être importé par les modules générateurs et solveurs.
Il a pour but de définier la/les structure(s) communes permettant à ceux-ci
de communiquer entre eux de manière claire.

Author: Dalker (daniel.kessler@dalker.org)
Date: 2021-04-09
"""

import abc  # Abstract Base Class


class Labyrinthe(abc.ABC):
    """
    Classe abstraite indiquant ce qu'un labyrinthe doit exposer aux solveurs.

    Les générateurs de labyrinthe doivent générer des objets d'une sous-classe
    de Labyrinthe. Les solveurs de labyrinthe doivent explorer un labyrinthe
    uniquement à partir des méthodes et attributs communs définis dans cette
    classe abstraite (qui joue donc le rôle d'une "interface" au sens java du
    terme).

    Attributs:
    - start: tuple (ligne, colonne) indiquant la cellule de départ
    - out: tuple (ligne, colonne) indiquant la sortie

    """

    @abc.abstractmethod
    def __contains__(self, cell):
        """
        La cellule cell est-elle accessible dans le labyrinthe?

        Permettra au solveur de savoir où il est possible d'aller.

        Entrée: cell est un tuple (ligne, colonne)
        Sortie: True si cell est dans le labyrinthe et est traversable,
                False sinon
        """
        return False

    @abc.abstractmethod
    def __str__(self):
        """
        Retourner une représentation ASCII du labyrinthe complet.

        Permettra une visualisation du labyrinthe complet dès le départ, pour
        visualiser la recherche de solution.
        """
        return ""
