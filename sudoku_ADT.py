class Sudoku:
    def __init__(self, path):
        self.grid = self.read_grid(path)

    def read_grid(self, path):
        """
        takes the path to conditions
        and convert them to grid -- 
        -- list of lines where each line is a list of numbers in it
        saves all the numbers as integers

        saves the grid as an attribute
        return None
        """
        grid = []
        with open(path, 'r', encoding='utf-8') as raw_grid:
            for line in raw_grid:
                line_lst = line[:-1].split()
                grid.append([int(x) for x in line_lst])
        return grid

    def safe_to_place_in_row(self, row, col, number):
        """
        checks whether the number on the coodinates (col, row)
        is the only one like that in the row

        return bool
        """
        if number in self.grid[row]:
            return False
        return True

    def safe_to_place_in_box(self, row, col, number):
        """
        checks whether the number on the coodinates (col, row)
        is the only one like that in the box 3x3

        return bool
        """
        box_col = col % 3
        box_row = row % 3
        for row_index in range(row - box_row, row - box_row + 3):
            for col_index in range(col - box_col, col - box_col + 3):
                if self.cell_is_number(row_index, col_index, number):
                    return False
        return True

    def safe_to_place_in_col(self, row, col, number):
        """
        checks whether the number on the coodinates (col, row)
        is the only one like that in the column

        return bool
        """
        for line_index in range(len(self.grid)):
            if self.cell_is_number(line_index, col, number):
                return False
        return True

    def cell_is_number(self, row, col, number):
        """
        checks whether the element on the coodinates (col, row)
        is equal to number

        return bool
        """
        if self.grid[row][col] == number:
            return True
        return False

    def safe_to_place(self, row, col, number):
        """
        checks whether the number on the coodinates (col, row)
        fits all the sudoku criteria

        return bool
        """
        if self.cell_is_number(row, col, 0) \
            and self.safe_to_place_in_box(row, col, number) \
                and self.safe_to_place_in_col(row, col, number) \
        and self.safe_to_place_in_row(row, col, number):
            return True
        return False

    def empty_cell(self):
        """
        returns the coordinates of the first empty cell on the grid
        if there is no such cell, return False
        """
        for row_index in range(9):
            for col_index in range(9):
                if self.cell_is_number(row_index, col_index, 0):
                    return [row_index, col_index]
        return False

    def solve(self):
        """
        solves the sudoku with backtraking using recurtion
        return True is there's no empty cells left
        return False if it is impossible to solve Sudoku
        """
        cell = self.empty_cell()
        if not cell:
            return True

        row = cell[0]
        col = cell[1]

        for number in range(1, 10):
            if self.safe_to_place(row, col, number):
                self.grid[row][col] = number
                # the place where the new number is placed
                if self.solve():
                    return True
                self.grid[row][col] = 0
                # the place when the assumption did not work and algorithm goes back
        return False

    def __str__(self):
        line_splitter = ' -------------------------\n'
        col_splitter = ' | '
        # line_splitter = ' *************************\n'
        # col_splitter = ' * '
        to_print = ''
        for row, line in enumerate(self.grid):
            if row % 3 == 0:
                to_print += line_splitter
            for col, number in enumerate(line):
                if col % 3 == 0:
                    to_print += col_splitter
                else:
                    to_print += ' '
                if number == 0:
                    number = '.'
                to_print += f'{number}'

            to_print += f'{col_splitter}\n'
        to_print += line_splitter
        return to_print


if __name__ == "__main__":
    sudoku = Sudoku("condition1.txt")
    print(sudoku)
    sudoku.solve()
    print(sudoku)
