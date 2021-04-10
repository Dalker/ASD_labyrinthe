"""
Tests expérimentaux de complexité algorithmique pour labyrinthes.

L'augmentation du temps en fonction de la taille de la grille est observée
pour un générateur et un solveur de labyrinthes.

Authors: JCB (juan-carlos@barros.ch) et Dalker (daniel.kessler@dalker.org)
Date: 2021-04-10
"""


import logging as log
import time

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
    time_gen = []
    time_solve = []
    size = 10
    while size <= max_size:
        time_gen, time_solve = single_test(size, astar)
        print(f"{size:4d}x{size:<4d}: {time_gen:.4f}s for generate,",
              f"{time_solve:.4f}s for solve")
        size += 10


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    time_tests(90)
