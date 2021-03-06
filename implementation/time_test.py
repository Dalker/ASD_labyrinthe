"""
Tests expérimentaux de complexité algorithmique pour labyrinthes.

L'augmentation du temps en fonction de la taille de la grille est observée
pour un générateur et un solveur de labyrinthes.

Authors: Dalker & JCB
Date: 2021-04-10
"""


import logging as log
import time

import numpy as np
import matplotlib.pyplot as plt

import generateur_ab as ab
from solveur_astar_naif import astar as astar_naif
from solveur_astar_heapq import astar as astar_heapq
from solveur_astar_v3 import astar as astar_v3
from solveur_astar_v3 import null_distance
# from solveur_astar_heapq import dijkstra


def single_test(size, solver, solver2=None, ratio_wall_destr=0):
    """Effectuer un test avec une grille aléatoire de la taille donnée."""
    log.debug("starting single test size %d" % size)
    start_time = time.time()
    log.debug("create maze")
    maze = ab.Maze(size, size, ratio_wall_destr)
    gen_duration = time.time() - start_time
    start_time = time.time()
    log.debug("solve maze" + " with solver 1" if solver2 is not None else "")
    solver(maze)
    solve_duration = time.time() - start_time
    if solver2 is not None:
        start_time = time.time()
        log.debug("solve maze with solver 2")
        solver2(maze)
        solve_duration2 = time.time() - start_time
        return gen_duration, solve_duration, solve_duration2
    else:
        return gen_duration, solve_duration


def time_tests(solver, max_size, solver2=None, rwd=0):
    """
    Effectuer des test avec des grilles aléatoires.

    Ces tailles seront 10x10, 20x20, ..., max_size x max_size
    """
    sizes = []
    gentimes = []
    soltimes = []
    soltimes2 = []
    size = 30
    while size <= max_size:
        gentime, *soltime = single_test(size, solver, solver2=solver2,
                                        ratio_wall_destr=rwd)
        sizes.append(size)
        log.debug("generating grid with size %d and rwd %f", size, rwd)
        gentimes.append(gentime)
        log.debug("solving 1")
        soltimes.append(soltime[0])
        if solver2 is not None:
            log.debug("solving 2")
            soltimes2.append(soltime[1])
            print(f"{size:4d}x{size:<4d}: generate={gentime:.4f}s",
                  f"solve1={soltime[0]:.4f}s",
                  f"solve2={soltime[1]:.4f}s")
        else:
            print(f"{size:4d}x{size:<4d}: generate={gentime:.4f}s",
                  f"solve={soltime[0]:.4f}s")
        size += 10
    if solver2 is not None:
        return sizes, gentimes, soltimes, soltimes2
    else:
        return sizes, gentimes, soltimes


def pente(x, y):
    """Déterminer la pente de la droite de régression par moindres carrés."""
    # recentrer les données sur leur barycentre
    x_shifted = x - np.mean(x)
    y_shifted = y - np.mean(y)
    # calculer la pente des moindres carrés
    res = (x_shifted @ y_shifted) / (x_shifted @ x_shifted)
    return res


def analyze(size, gent, solt, solt2=None, view=None):
    """Analyzer complexité expérimentale de génération/résolution."""
    if view:
        _, (axes_lin, axes_log) = plt.subplots(1, 2)
        # axes_lin.plot(size, gent, "+b", label="generate")
        axes_lin.plot(size, solt, "+g", label=view[0])
        if solt2 is not None:
            axes_lin.plot(size, solt2, "+c", label=view[1])
        axes_lin.set_xlabel("taille de la grille")
        axes_lin.set_ylabel("durée (s)")
        axes_lin.legend()
        # axes_log.plot(np.log(size), np.log(gent), "+b", label="generate")
        axes_log.plot(np.log(size), np.log(solt), "+g", label=view[0])
        if solt2 is not None:
            axes_log.plot(np.log(size), np.log(solt2), "+c", label=view[1])
        axes_log.set_xlabel("log(taille)")
        axes_log.set_ylabel("log(durée)")
        axes_log.legend()
    # la pente log/log est le degré d'une régression monômiale
    # vu que y=cx^d <=> log(x) = d * log(x) + log(c)
    pente_gen = pente(np.log(size), np.log(gent))
    print("le générateur a une complexité expérimentale polynomiale de degré",
          f"{pente_gen:.3f}")
    pente_sol = pente(np.log(size), np.log(solt))
    print("le solveur 1 a une complexité expérimentale polynomiale de degré",
          f"{pente_sol:.3f}")
    if solt2 is not None:
        pente_sol2 = pente(np.log(size), np.log(solt2))
        print("le solveur 2 a une complexité expérimentale polynomiale",
              "de degré", f"{pente_sol2:.3f}")
    plt.show()


def comparer_solveurs(maxsize, rwd):
    """Comparer les différentes implémentations, sans graphique."""
    print("* Comparaison implémentation v1 (sans heapq) "
          "vs v3 (heapq amélioré) *")
    print("  Algo1 = A* v1, Algo2 = A* v3")
    sz, gent, solt, solt2 = time_tests(astar_naif, maxsize, solver2=astar_v3,
                                       rwd=rwd)
    analyze(sz, gent, solt, solt2=solt2, view=False)

    print("* Comparaison implémentation v2 (heapq lourd) "
          "vs v3 (heapq amélioré) *")
    print("  Algo1 = A* v2, Algo2 = A* v3")
    sz, gent, solt, solt2 = time_tests(astar_heapq, maxsize, solver2=astar_v3,
                                       rwd=rwd)
    analyze(sz, gent, solt, solt2=solt2,
            view=("v2", "v3"))


def comparer_distances(maxsize, rwd):
    """Comparer choix de distance heuristique dans même algo."""
    print("* Comparaison heuristique nulle vs Manhattan distance *")
    print("  solveur1 = heuristique 0 (=Dijkstra), "
          "solveur2 = heuristique Manhattan")
    sz, gent, solt, solt2 = time_tests(lambda mz:
                                       astar_v3(mz, distance=null_distance),
                                       maxsize, solver2=astar_v3, rwd=rwd)
    analyze(sz, gent, solt, solt2=solt2,
            view=("heuristique nulle", "Manhattan"))


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    msz = 80  # max_size
    rwd = 0.01  # rate of wall destruction
    # comparer_solveurs(msz, rwd)
    comparer_distances(msz, rwd)
