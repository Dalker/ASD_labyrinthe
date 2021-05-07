"""
Construction de labyrinthes pour projet ASD1.

par M. Barros
démarré le 2021.04.06
"""

import random
import labyrinthe # abstract class pour communication avec solveurs
# import generateur_ascii # super classe pour générateurs de labyrinthes (inclut labyrinthe)


class Maze(labyrinthe.Labyrinthe):
    """ randomly-generated labyrinth
        example of grid:
             WRWRWRWRW  
           W ##### ### <- first Wall row (0) has exit
           R #   # # # <- first Room row (1)
           W # ### # # <- second Wall row (2)
           . #  ...  #  ...
           R # # # # # <- last (ROWS_th) Room row (2*ROWS-1)
           W ### ##### <- last Wall row (2*ROWS) has entrance
            there are a total of (2*Room_rows + 1) rows
            and (2*Room_cols + 1) cols

        NB: matrix uses indices
            in the order row, col, which correspond to [-]y, x!
            
        un paramètre destruction_murs permet d'enlever des murs après génération
        avec une valeur de 0, aucun mur n'est enlevé après génération
        avec une valeur de 1, tous les murs sont enlevés: seuls restent les murs extérieurs
    """
    def __init__(self, room_rows, room_cols, destruction_murs = 0):
        self.room_rows = room_rows
        self.rows = 2* room_rows + 1
        self.room_cols = room_cols
        self.cols = 2 * room_cols + 1
        # self.grid = ""
        self.start = (1, 1)
        self.out = (self.rows-2, self.cols-2)
        self.fill_passable()
        self.generate()
        self.destruction_murs = destruction_murs # ratio des murs qu'on détruit
        self.destr_murs()
    
    
    def fill_passable(self):
        """ Génère une grid 'passable' tout fermé:
            contient des True là où c'est libre (rooms)
            et des False partout ailleurs (là où il y a des murs)
            
            Exemple pour Grid avec 2x2 rooms:
            ("#" = False = mur / " " = True = passage libre)
            
            #####
            # # #
            #####
            # # #
            #####
            
        
        """
        self.passable = []
        for _ in range(self.rows):
            self.passable += [[False] * (self.cols)]
            self.passable += [[False, True] * (self.room_cols) + [False]]
        self.passable += [[False] * (self.cols)]
        # return True
            

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
        # return True

    def generate(self):
        """ Aldous-Broder algorithm:
        random walk until all cells are added
        any time a non-visited cell is reach, a wall is broken on the way
        """
        directions = {(-1, 0), (1, 0), (0, -1), (0, 1)}
        visited = set()  # visited cells
        # initial node is random
        cell = (random.randrange(self.room_rows), random.randrange(self.room_cols))
        while len(visited) < self.room_rows * self.room_cols:
            visited.add(cell)
            # choose a direction for random walk from current
            next_exists = False
            while not next_exists:
                direction = random.sample(directions, 1)[0]
                nextcell = (cell[0]+direction[0], cell[1]+direction[1])
                next_exists = (0 <= nextcell[0] < self.room_rows
                               and 0 <= nextcell[1] < self.room_cols)
            # if next is new, carve a wall to get there
            if nextcell not in visited:
                self.carve(cell, direction)
            # walk
            cell = nextcell
        # return True

    def destr_murs(self):
        wall_cells = []
        for row in range (1, self.rows-1):
            for col in range (1, self.cols-1):
                if not self.passable[row][col]:
                    wall_cells += [(row, col)]
        walls_abs_destr = int(self.destruction_murs * len(wall_cells))
        if walls_abs_destr>0:
            for i in range(walls_abs_destr):
                sentence = random.randrange(len(wall_cells))
                self.passable[wall_cells[sentence][0]][wall_cells[sentence][1]] = True
                wall_cells.pop(sentence)
        

    def __str__(self):
        """ sort un string qui représente grossièrement notre labyrinthe
            avec des "#" pour les obstacles (murs) et des " " pour les cases ouvertes
        """
        grid = ""
        for row in range(self.rows):
            for col in range(self.cols):
                grid += " " if self.passable[row][col] else "#"
            if row < self.rows-1:
                grid += "\n"
        return grid
    
    def __contains__(self, cell):
        """ renvoie True si l'emplacement défini par les coordonnées "cell"
            est vide (donc passable), False sinon (mur)
        """
        return self.passable[cell[0]][cell[1]]


if __name__ == "__main__":
    rows, cols = 10, 10
    for i in range(10):
        ratio = 0
        GRILLE = Maze(rows,cols, ratio)
        print(GRILLE)
