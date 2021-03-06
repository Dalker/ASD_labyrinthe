"""
Construction de labyrinthes pour projet ASD1.

par M. Barros
démarré le 2021.04.06
"""

import random

GRILLE10x10 = """
#####################
I     #             #
# # ### ######### ###
# #   #   #         #
# # # ########### # #
# # #   # #   # # # #
####### # # # # ### #
#   #   #   #   #   #
### ### ### ##### ###
#   #   # #   # # # #
### ### # ### # # # #
#   # # # # # #     #
# # # # # # # # # ###
# # # # #   # # # # #
# # # # ### # ### # #
# #       #   # #   #
# ####### ### # ### #
# #   # #   # #     #
# # ### # # # # # # #
#     #   #     # # O
#####################
"""


GRILLE20x20 = """
#########################################
I     # #       #   #   #     #         #
# ### # ### ##### ##### ### # # ### #####
#   #   #   # #     #     # #   #       #
# ##### # # # # ### # # # ### ####### # #
#     # # #     # # # # #   #       # # #
# # ### # ### ### ####### # # # ### ### #
# # # #     #         # # # # # # # #   #
# ### ### ####### ### # ### ##### ##### #
# #     # #         #         #         #
# # # ########### # ### ##### # # ##### #
#   #     #   #   # #   #       #     # #
# ##### ##### ### # ### # ##### # ### ###
#   # # # #       # #   #   # # # #     #
# ### # # ### ##### ### ### # ### # ### #
# # # #   # # #   # # # #   #     #   # #
# # # ### # ### ### # ### ### ######### #
# #     # # #       #   # #   # #   #   #
# ##### ### # # ### # ### ##### ### ### #
# #   # #     # #       # #       #     #
### # # # ### ##### # ######### #########
# # #   #   # # #   # #     # #       # #
# ### # # # # # # ####### ### ##### # # #
# # # #   # # # # #   # # #   #     # # #
# # ##### # # # # ### # # # # # # # ### #
#       # # # #   #     #   # # # # #   #
# ##### # ####### ### # ##### ### # # # #
#   #     #       #   #   #     # #   # #
# # # ######### ### # ##### # ####### ###
# # #     #         #       #     #     #
####### # # ##### ### ### ### ######### #
# #   # # #   #     #   # #   #   #     #
# ### ######### ####### ##### # ##### # #
#     #   #   # #     #     #     #   # #
# ### # # ### # # ######### ########### #
#   #   # #   #         #     # #     # #
####### ##### # ### ##### ##### # # # # #
#             # #   # #   # # #   # #   #
# # ##### ##### ### # ### # # # ##### ###
# #   #         #       #         #     O
#########################################
"""

GRILLE30x30 = """
#############################################################
I           #   # #               #       #     #   #       #
# ######### ### # ##### # # ### # # ##### ##### # # ### #####
# # #     #         #   # # #   #     # #     # # # #     # #
# # ### # ##### ######### ### ##### ### ####### # ### ### # #
# #   # #   # #   #         #   #   # #     # #   #   #     #
##### ##### # ### # ######### ####### ### ### ### ####### ###
# # # #   #       #       #         # #         #   #   # # #
# # # ### ##### ##### # ############# # # ### ##### # ### # #
# #     # # #   #     #   #   #     # # # # # # #   #     # #
# # ### # # ### ### ##### # # ##### # ##### # # # ### ### # #
#     #       # #   #   #   # #     # #     #   #     #   # #
##### ######### ### # ##### ####### # ##### ### # ####### # #
# #     #   #     # # #           # #     #     # # #   #   #
# # ### # # # # ##### # ### ##### # # ##### ### ### # ### ###
# # #     # # #       # #       #         # # #         # # #
# # ####### ######### # # ####### # # ##### # ########### # #
# #       #         #   # #       # # #   #             #   #
# # ####### ### # ### # ##### ### ##### # # ########### # ###
#   #     # # # #   # # #       # #     # #   #   #   #     #
# ### # ##### ### ### ######### ### ##### ### # # # ##### # #
# #   #   #   #   #       # #   # #     # #     #     #   # #
# # ### # ### # ######### # ##### # # ### # # # #############
# # #   # # #   # # # #   #   #   # #   #   # # # #   #     #
# # # # ### # # # # # # ### ##### ############# # # ##### ###
#   # # #     # # #         #         # #   #   #   #       #
### ##### ####### ### ########### ##### # ### # # ### # #####
#       #   #   #   #         #               #       #   # #
### ########### # ### ##### ### # ### ######### # ### # ### #
# #       #         # #       # # # #     #   # # #   #   # #
# ####### # ####### ##### ### ##### ####### # # ### # # ### #
#       # # #   # #   # # #         # # # # #   # # # # #   #
# ### ### # ### # ### # ####### ##### # # ##### # ### ### ###
# #                 #             #       #       #     #   #
### ##### ####### ### ### # ######### ####### ### ##### # # #
# # #   # # #   #   #   # # #   #   # # # #     # #   #   # #
# # ### ### # # # # # ####### ### ### # # # # ##### ### ### #
# #   #   #   #   # #         #     #   #   # #       #   # #
# # # # # # ### # ############# # ### ### ### ##### #########
#   # # # # # # #     #     #   # #   #   #   #   # #       #
# # # # # # # ####### ### ##### ### ##### # ### ### # ##### #
# # # # #   # #           #   # # #     # #     #     #   # #
# ####### # # ##### # # ### ### # ### # ####### ##### ### # #
# # #     #   # #   # #   #     #     #         #         # #
# # ##### ### # # ##### # # ##### ##### ####### # # ### ### #
# #   #   #   #   #   # # #   #   #   # #       # # #     # #
# ### ### ####### ### ### # # ### # # ### ### ####### ### ###
# # #   # #         #   #   #     # #   # # # # # # # #     #
# # # ######### ####### ### ##### # ### # # ### # # # # # ###
#             # # #     # #   # # # # #       #   # # # # # #
# ### ##### # ### ### # # # # # ### # # ######### # ### ### #
# # # # #   #   #     #   # #   #   #   #     # #   # #   # #
### # # ####### ##### ####### # # ### ### ### # # # # ### # #
# # # # #   # #       #       # # #   #     # #   #   #     #
# # # # # ### ### ##### ######### ### # # ### ### ######### #
# #         # #     # #     #   # #   # # # # #   #         #
# ### # ### # # ### # ### ### ####### # # # # # ### ####### #
# # # #   #   #   #   #   # # # # #     #   #   #       #   #
# # # # ########### # ### # # # # # ### # ### # # # ### ### #
#     #           # # #       #       # #   # #   # #     # O
#############################################################
"""


class Maze():
    """ randomly-generated labyrinth
        example of grid:
             WRWRWRWRW  
           W ##### ### <- first Wall row (0) has exit
           R #   # # # <- first Room row (1)
           W # ### # # <- second Wall row (2)
           . #  ...  #  ...
           R # # # # # <- last (ROWS_th) Room row (2*ROWS-1)
           W ### ##### <- last Wall row (2*ROWS) has entrance
            there are a total of 2*cell rows + 1 grid rows

        NB: matrix (whether np.array or list of lists) uses indices
            in the order row, col, which correspond to [-]y, x!
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # self.grid = ""
        # self.entrance = (0, 0)
        # self.exit = (rows, cols)
        self.fill_passable()
        self.generate()
    
    
    def fill_str(self):
        """ Sert à générer un grid ascii mais on va laisser tomber au profit du grid "passable"
        """
        self.grid = ""
        for _ in range(self.rows):
            self.grid += "#" * (2*self.cols+1) + "\n"
            self.grid += "# " * self.cols + "#\n"
        self.grid += "#" * (2*self.cols+1) + "\n"
        return True
            

    def fill_passable(self):
        """ Génère une grid 'passable' qui contient des True là où c'est libre et des False là où il y a un obstacle (un mur)
        """
        # self.passable = [[False] * (self.cols*2+1), [False, True] * self.cols + [False]] * self.rows, [[False] * (self.cols*2+1)]
        self.passable = []
        for row in range(rows):
            self.passable += [[False] * (cols*2+1)]
            self.passable += [[False, True] * (cols) + [False]]
        self.passable += [[False] * (cols*2+1)]
        # print(self.passable)
        return True
            

    def carve(self, cell, direction):
        "open path from a node in given direction"
        row = cell[0]*2+1
        col = cell[1]*2+1
        # if 0 <= row+direction[0] < self.rows and 0 <= col+direction[1] < self.cols:
        if direction == (-1, 0):  # up
            self.passable[row-1][col] = True
        elif direction == (1, 0):  # down
            self.passable[row+1][col] = True
        elif direction == (0, -1):  # left
            self.passable[row][col-1] = True
        elif direction == (0, 1):  # right
            self.passable[row][col+1] = True
        return True

    def generate(self):
        """ Aldous-Broder algorithm:
        random walk until all cells are added
        any time a non-visited cell is reach, a wall is broken on the way
        """
        directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
        visited = set()  # visited cells
        # initial node is random
        cell = (random.randrange(self.rows), random.randrange(self.cols))
        while len(visited) < self.rows * self.cols:
            visited.add(cell)
            # choose a direction for random walk from current
            next_exists = False
            while not next_exists:
                direction = random.sample(directions, 1)[0]
                nextcell = (cell[0]+direction[0], cell[1]+direction[1])
                next_exists = (0 <= nextcell[0] < self.rows
                               and 0 <= nextcell[1] < self.cols)
            # if next is new, break a wall to get there
            if nextcell not in visited:
                self.carve(cell, direction)
            # visit next
            cell = nextcell
        return True


    def __str__(self):
        """ sort un string qui représente grossièrement notre labyrinthe
            avec des "#" pour les obstacles (murs) et des " " pour les cases ouvertes
        """
        grid = ""
        for row in range(self.rows*2+1):
            for col in range(self.cols*2+1):
                grid += " " if self.passable[row][col] else "#"
            grid += "\n"
        return grid


if __name__ == "__main__":
    rows, cols = 5, 30
    
    GRILLE1 = Maze(rows,cols)
    print(GRILLE1)
    
    
# Cette merde (ci-dessous) ne fonctionne pas et je ne sais pas pourquoi parce que je suis un gros nul
# GRILLE1 = str(Maze(10, 10))
