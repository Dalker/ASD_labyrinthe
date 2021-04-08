"""
Construction de labyrinthes pour projet ASD1.

par M. Barros
démarré le 2021.04.06
"""

GRILLE1 = """
###############
####### #     I
#          ## #
# ## ##### ## #
# ## ## ## ## #
####    ## ## #
#    ## ##   ##
# ## ## ## # ##
# ##    ## # ##
# ## # ### # ##
# ## #   # #  #
###  ##### ## #
###        ## #
#####O#########
"""

GRILLE2 = """
#######I##
#     # ##
## #### ##
##      ##
#### ##  #
#### ### #
#    #   #
#### # ###
###  # ###
###O######
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
        self.grid = ""
        self.entrance = None
        self.exit = None
        self.reset()
    
    
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
        self.passable = [[False] * (self.cols*2+1)], [[False, True] * self.cols + [False]] * self.rows, [[False] * (self.cols*2+1)]
    return True
            

    def carve(self, cell, direction):
        "open path from a node in given direction"
        row = cell[0]
        col = cell[1]
        if 0 <= row+direction[0] < self.rows\
                and 0 <= col+direction[1] < self.cols:
            if direction == (-1, 0):  # up
                self.grid[row][col] = True
            elif direction == (1, 0):  # down
                self.grid[row+1][col] = True
            elif direction == (0, -1):  # left
                self.grid[row][col] = True
            elif direction == (0, 1):  # right
                self.grid[row][col+1] = True
            return True
        else:
            log.debug("tried impossible destination %d %d",
                      row+direction[0],
                      col+direction[1])
            return False


    def generate(self):
        """ Aldous-Broder algorithm:
        random walk until all cells are added
        any time a non-visited cell is reach, a wall is broken on the way
        """
        fill
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
                carve(cell, direction)
            # visit next
            cell = nextcell


if __name__ == "__main__":
    passable = [[False] * (3*2+1)], [[False, True] * 3 + [False]] * 2, [[False] * (3*2+1)]
    print(passable)
    # maze1 = Maze()
    # maze1.fill
    