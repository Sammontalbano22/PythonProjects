"""
This is a program which simulates forest fire spread, and finds whether a randomly generated forest of a certain density will burn all the way through to the other side.
It does this in two different ways. The first (and much faster) method is the depth first search algorithm, and the second method is the breadth first search algorithm
File Name: project_3.py
Author: Sam Montalbano
Date: 5/6/24
Course: COMP1353
Assignment: Project 3: Percolation - Part 1 
Collaborators: Chase Johnson
Internet Sources: None
"""
import dudraw
import random
from my_queue import MyStack
from my_queue import MyQueue

EMPTY = 0
TREE = 1
FIRE = 2

class Cell :
    """
    Represents a cell in the forest grid.
    
    Attributes:
        column (int): The column index of the cell.
        row (int): The row index of the cell.
    """
    def __init__(self, c, r) -> None:
        self.column = c
        self.row = r

class Forest :
    """
    Represents a forest with trees and fire.

    Attributes:
        width (int): The width of the forest grid.
        height (int): The height of the forest grid.
        density (float): The density of trees in the forest.
        grid (list): A 2D list representing the forest grid.
    """
    def __init__( self, w: int, h: int, d: float ) -> None :
        """
        Initializes a Forest object.

        Args:
            w (int): The width of the forest.
            h (int): The height of the forest.
            d (float): The density of trees in the forest.
        """
        self.width = w
        self.height = h
        self.density = d
        self.grid = []
        for i in range(self.height) :
            row = []
            for j in range(self.width) :
                if random.random() < self.density :
                    row.append(TREE)
                else :
                    row.append(EMPTY)
            self.grid.append(row)

    def __str__( self ) -> str :
        """
        Returns a string representation of the forest grid.

        Returns:
            str: A string representation of the forest grid.
        """
        return str(self.grid)
    
    def draw( self ) :
        """
        Draws the forest grid.
        """
        for row in range(self.height) :
            for column in range(self.width) :
                if self.grid[column][row] == EMPTY :
                    dudraw.set_pen_color_rgb(196, 164, 132)
                elif self.grid[column][row] == TREE :
                    dudraw.set_pen_color_rgb(48, 69, 41)
                elif self.grid[column][row] == FIRE :
                    dudraw.set_pen_color_rgb(200, 0, 0)
                dudraw.filled_square(column+.5, row+.5, .5)

        dudraw.show(100)

    def depth_first_search(self, visual = False) -> bool:
        """
        Performs depth-first search to simulate fire spread in the forest.

        Args:
            visual (bool): If True, visually shows the forest grid during the search.

        Returns:
            bool: True if the fire spreads to the other side, False otherwise.
        """
        cells_to_explore = MyStack()
        for c in range(self.width):
            if self.grid[c][self.height - 1] == TREE:
                self.grid[c][self.height - 1] = FIRE
                cells_to_explore.push(Cell(c, self.height - 1))

        while not cells_to_explore.is_empty():
            current_cell = cells_to_explore.pop()
            c = current_cell.column
            r = current_cell.row
            if current_cell.row == 0:
                return True  # Fire has spread

            # Explore all neighboring cells
            if r != self.height - 1 and self.grid[c][r + 1] == TREE:
                self.grid[c][r + 1] = FIRE
                cells_to_explore.push(Cell(c, r + 1))

            if c != 0 and self.grid[c - 1][r] == TREE:
                self.grid[c - 1][r] = FIRE
                cells_to_explore.push(Cell(c - 1, r))

            if c != self.width - 1 and self.grid[c + 1][r] == TREE:
                self.grid[c + 1][r] = FIRE
                cells_to_explore.push(Cell(c + 1, r))

            if r != 0 and self.grid[c][r - 1] == TREE:
                self.grid[c][r - 1] = FIRE
                cells_to_explore.push(Cell(c, r - 1))

            if visual :
                self.draw()

        return False

    def breadth_first_search( self, visual = False ) -> bool :
        """
        Performs breadth-first search to simulate fire spread in the forest.

        Args:
            visual (bool): If True, visually shows the forest grid during the search.

        Returns:
            bool: True if the fire spreads to the other side, False otherwise.
        """
        cells_to_explore = MyQueue()
        for c in range(self.width):
            if self.grid[c][self.height - 1] == TREE:
                self.grid[c][self.height - 1] = FIRE
                cells_to_explore.enqueue(Cell(c, self.height - 1))

        while not cells_to_explore.is_empty():
            current_cell = cells_to_explore.dequeue()
            c = current_cell.column
            r = current_cell.row
            if current_cell.row == 0:
                return True  # Fire has spread

            # Explore all neighboring cells
            
            if c != self.width - 1 and self.grid[c + 1][r] == TREE:
                self.grid[c + 1][r] = FIRE
                cells_to_explore.enqueue(Cell(c + 1, r))

            if r != self.height - 1 and self.grid[c][r + 1] == TREE:
                self.grid[c][r + 1] = FIRE
                cells_to_explore.enqueue(Cell(c, r + 1))

            if c != 0 and self.grid[c - 1][r] == TREE:
                self.grid[c - 1][r] = FIRE
                cells_to_explore.enqueue(Cell(c - 1, r))

            if r != 0 and self.grid[c][r - 1] == TREE:
                self.grid[c][r - 1] = FIRE
                cells_to_explore.enqueue(Cell(c, r - 1))
                
            if visual :
                self.draw()

        return False

def main() :
    """
    Main function to run simulations using depth-first and breadth-first search algorithms.
    """
    width = 50
    height = 50

    dudraw.set_canvas_size(600, 600)
    dudraw.set_x_scale(0, width)
    dudraw.set_y_scale(0, height)

    print('Depth First Search')
    print('Testing forest of density .5')
    f = Forest(width, height, .8)
    print(f.depth_first_search(visual = False))

    print('Testing forest of density .4')
    f = Forest(width, height, .6)
    print(f.depth_first_search(visual = True ))

    # print('Breadth First Search')

    print('Testing forest of density .4')
    f = Forest(width, height, .8)
    print(f.breadth_first_search(visual = False))

if __name__ == '__main__' :
    main()





















