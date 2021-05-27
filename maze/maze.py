"""
Implemention of the Maze ADT using a 2-D array.
"""
import turtle
import pygame
from dataclasses import dataclass
from lliststack import Stack


class Maze:
    """
    Class for representing Maze objects.
    Attributes:
        maze: The list of lists representing the maze.
        _start: The starting position of the maze; marked as -1 on the maze.
        _exit: The exit position of the maze; marked as 2 on the maze.
    """
    FREE = 0
    MAZE_WALL = 1
    EXIT = 2
    PATH_TOKEN = 3
    TRIED_TOKEN = 4

    def __init__(self, maze_file: str, visualization=None):
        """
        Creates a maze object with all cells marked as open.
        """
        self._start = None
        self._exit = None
        self.maze = self._build_maze(maze_file)
        self.visualization = visualization

    def _build_maze(self, filename: str):
        """
        Builds a maze based on a text format in the given file.
        The grid must be square, ie an equal number of columns and rows;
        the initial cell and the final cell must be present.
        Otherwise an error with the corresponding message will be raised.
        """
        maze = []
        with open(filename, 'r') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            line = list(map(int, lines[i].split()))

            assert len(line) == len(
                lines), "Wrong number of symbols, please check your file"

            if -1 in line:
                self._start = _CellPosition(i, line.index(-1))
            if 2 in line:
                self._exit = _CellPosition(i, line.index(2))
            maze.append(line)

        assert self._start is not None, "No starting position found."
        assert self._exit is not None, "No final position found."

        return maze

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.

        Change the self.maze where:
        0 - not tried cells;
        1 - walls;
        2 - exit;
        3 - found path;
        4 - tried cells.
        """
        stack = Stack()
        current_cell = _CellPosition(
            self._start.row, self._start.col)

        self._mark_path(current_cell.row, current_cell.col)

        while not self._exit_found(current_cell.row, current_cell.col):

            # step up
            if self._valid_move(current_cell.row - 1, current_cell.col):
                stack.push(current_cell)
                self._mark_path(current_cell.row - 1, current_cell.col)
                current_cell = _CellPosition(
                    current_cell.row - 1, current_cell.col)

            # step right
            elif self._valid_move(current_cell.row, current_cell.col + 1):
                stack.push(current_cell)
                self._mark_path(current_cell.row, current_cell.col + 1)
                current_cell = _CellPosition(
                    current_cell.row, current_cell.col + 1)

            # step down
            elif self._valid_move(current_cell.row + 1, current_cell.col):
                stack.push(current_cell)
                self._mark_path(current_cell.row + 1, current_cell.col)
                current_cell = _CellPosition(
                    current_cell.row + 1, current_cell.col)

            # step left
            elif self._valid_move(current_cell.row, current_cell.col - 1):
                stack.push(current_cell)
                self._mark_path(current_cell.row, current_cell.col - 1)
                current_cell = _CellPosition(
                    current_cell.row, current_cell.col - 1)

            # step back if no other options are valid.
            else:

                # HERE SHOULD BE THE GRAPHICS
                if self.visualization:
                    self.visualization.all_sprites.update()
                    self.visualization.draw()
                    self.visualization.events()
                    pygame.time.wait(self.visualization.TIMESTEP)

                self._mark_tried(current_cell.row, current_cell.col)

                # if current cell is start cell and there are no other valid moves.
                if (current_cell == self._start and not
                        (self._valid_move(current_cell.row - 1, current_cell.col) or
                         self._valid_move(current_cell.row, current_cell.col + 1) or
                         self._valid_move(current_cell.row + 1, current_cell.col) or
                         self._valid_move(current_cell.row, current_cell.col - 1))):
                    self._mark_tried(self._start.row,
                                     self._start.col)
                    return False
                current_cell = stack.pop()

            # HERE SHOULD BE THE GRAPHICS
            if self.visualization:
                self.visualization.all_sprites.update()
                self.visualization.draw()
                self.visualization.events()
                pygame.time.wait(self.visualization.TIMESTEP)

        if self._exit_found(current_cell.row, current_cell.col):
            self._mark_path(current_cell.row, current_cell.col)
            return True

    def __str__(self):
        """
        Returns a text-based representation of the maze.
        """
        grid = ''
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                grid += str(self.maze[row][col]) + ' '
            if row != len(self.maze) - 1:
                grid += '\n'
        return grid

    def _valid_move(self, row: int, col: int):
        """
        Returns True if the given cell position is a valid move.
        """
        return (row >= 0 and row < len(self.maze)
                and col >= 0 and col < len(self.maze[0])
                and (self.maze[row][col] == self.FREE or
                     self.maze[row][col] == self.EXIT))

    def _exit_found(self, row: int, col: int):
        """
        Helper method to determine if the exit was found.
        """
        return row == self._exit.row and col == self._exit.col

    def _mark_tried(self, row: int, col: int):
        """
        Drops a "tried" token at the given cell.
        """
        self.maze[row][col] = self.TRIED_TOKEN

    def _mark_path(self, row: int, col: int):
        """
        Drops a "path" token at the given cell.
        """
        self.maze[row][col] = self.PATH_TOKEN


@dataclass
class _CellPosition():
    """
    Private storage class for holding a cell position.
    """
    row: int
    col: int

# -------------------VISUALIZATION-----------------------
# these functions are taken from the given resources (https://trinket.io/python/6ec2ecb76b)
# and are used not for algorithm, but for visualization.


def text(message, x, y, size):
    FONT = ('Arial', size, 'normal')
    myPen.penup()
    myPen.goto(x, y)
    myPen.write(message, align="left", font=FONT)


def box(intDim):
    """
    This function draws a box by drawing each side of the square
    and using the fill function.
    """
    myPen.begin_fill()
    # 0 deg.
    myPen.forward(intDim)
    myPen.left(90)
    # 90 deg.
    myPen.forward(intDim)
    myPen.left(90)
    # 180 deg.
    myPen.forward(intDim)
    myPen.left(90)
    # 270 deg.
    myPen.forward(intDim)
    myPen.end_fill()
    myPen.setheading(0)


def drawMaze(maze: list):
    boxSize = 15
    # Position myPen in top left area of the screen
    myPen.penup()
    myPen.goto(-130, 130)
    myPen.setheading(0)
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            myPen.color(palette[maze[i][j]])
            box(boxSize)
            myPen.penup()
            myPen.forward(boxSize)
            myPen.pendown()
        myPen.setheading(270)
        myPen.penup()
        myPen.forward(boxSize)
        myPen.setheading(180)
        myPen.forward(boxSize*len(maze[i]))
        myPen.setheading(0)
        myPen.pendown()


if __name__ == "__main__":
    from pprint import pprint
    maze = Maze('maze_file.txt', visualization=True)

    if maze.visualization:
        myPen = turtle.Turtle()
        turtle.tracer(0)
        myPen.hideturtle()
        palette = ["#FFFFFF", "#000000", "#00ff00", "#ff00ff", "#AAAAAA"]

    solved = maze.find_path()
    print('FINAL MAZE:\n',)
    pprint(maze.maze)

    if solved:
        print("\nMaze Solved")
    else:
        print("\nCannot Solve Maze")

    if maze.visualization:
        if solved:
            text("Maze Solved", -100, -150, 20)
        else:
            text("Cannot Solve Maze", -130, -150, 20)
        myPen.getscreen().update()
        turtle.exitonclick()
