"""
Tests expérimentaux de complexité algorithmique pour labyrinthes.

L'augmentation du temps en fonction de la taille de la grille est observée
pour un générateur et un solveur de labyrinthes.

Authors: JCB (juan-carlos@barros.ch) et Dalker (daniel.kessler@dalker.org)
Date: 2021-04-10
"""


import logging as log
import time

import numpy as np
import matplotlib.pyplot as plt

import generateur_ab as ab
from solveur_astar_naif import astar


def single_test(size, solver):
    """Effectuer un test avec une grille aléatoire de la taille donnée."""
    log.debug("starting single test size %d" % size)
    start_time = time.time()
    log.debug("create maze")
    maze = ab.Maze(size, size)
    gen_duration = time.time() - start_time
    start_time = time.time()
    log.debug("solve maze")
    solver(maze)
    solve_duration = time.time() - start_time
    return gen_duration, solve_duration


def time_tests(max_size):
    """
    Effectuer des test avec des grilles aléatoires.

    Ces tailles seront 10x10, 20x20, ..., max_size x max_size
    """
    sizes = []
    gentimes = []
    soltimes = []
    size = 10
    while size <= max_size:
        gentime, soltime = single_test(size, astar)
        sizes.append(size)
        gentimes.append(gentime)
        soltimes.append(soltime)
        print(f"{size:4d}x{size:<4d}: {gentime:.4f}s for generate,",
              f"{soltime:.4f}s for solve")
        size += 10
    return sizes, gentimes, soltimes


def pente(x, y):
    """Déterminer la pente de la droite de régression."""
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    x_shifted = x - x_mean
    y_shifted = y - y_mean
    a = (x_shifted @ y_shifted) / (x_shifted @ x_shifted)
    return a


def analyze(size, gent, solt):
    """Analyzer complexité expérimentale de génération/résolution."""
    _, (axes_lin, axes_log) = plt.subplots(1, 2)
    axes_lin.plot(size, gent, "+b", label="generate")
    axes_lin.plot(size, solt, "+g", label="solve")
    axes_lin.set_xlabel("taille de la grille")
    axes_lin.set_ylabel("durée (s)")
    axes_lin.legend()
    axes_log.plot(np.log(size), np.log(gent), "+b", label="generate")
    axes_log.plot(np.log(size), np.log(solt), "+g", label="solve")
    axes_log.set_xlabel("log(taille)")
    axes_log.set_ylabel("log(durée)")
    axes_log.legend()
    pente_gen = pente(np.log(size), np.log(gent))
    pente_sol = pente(np.log(size), np.log(solt))
    print("le générateur a une complexité expérimentale polynomiale de degré",
          f"{pente_gen:.3f}")
    print("le solveur a une complexité expérimentale polynomiale de degré",
          f"{pente_sol:.3f}")
    plt.show()


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    analyze(*time_tests(50))
