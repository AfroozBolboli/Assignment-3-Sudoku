from Field import Field


class Sudoku:

    def __init__(self, filename):
        self.board = self.read_sudoku(filename)

    def __str__(self):
        output = "╔═══════╦═══════╦═══════╗\n"
        # iterate through rows
        for i in range(9):
            if i == 3 or i == 6:
                output += "╠═══════╬═══════╬═══════╣\n"
            output += "║ "
            # iterate through columns
            for j in range(9):
                if j == 3 or j == 6:
                    output += "║ "
                output += str(self.board[i][j]) + " "
            output += "║\n"
        output += "╚═══════╩═══════╩═══════╝\n"
        return output

    @staticmethod
    def read_sudoku(filename):
        """
        Read in a sudoku file
        @param filename: Sudoku filename
        @return: A 9x9 grid of Fields where each field is initialized with all its neighbor fields
        """
        assert filename is not None and filename != "", "Invalid filename"
        # Setup 9x9 grid
        grid = [[Field for _ in range(9)] for _ in range(9)]

        try:
            with open(filename, "r") as file:
                for row, line in enumerate(file):
                    for col_index, char in enumerate(line):
                        if char == '\n':
                            continue
                        if int(char) == 0:
                            grid[row][col_index] = Field()
                        else:
                            grid[row][col_index] = Field(int(char))

        except FileNotFoundError:
            print("Error opening file: " + filename)

        Sudoku.add_neighbours(grid)
        return grid

    @staticmethod
    def add_neighbours(grid):
        """
        Adds a list of neighbors to each field
        @param grid: 9x9 list of Fields
        """

    # For each field, add its neighbors
        for row in range(9):
            for column in range(9):
                neighbours = set()

                # Row neigbour 
                for row_neighbour in range(9):
                    if row_neighbour != row:
                        neighbours.add(grid[row_neighbour][column])

                # Column neighbour
                for column_neighbour in range(9):
                    if column_neighbour != column:
                        neighbours.add(grid[row][column_neighbour])

                # Box neighbor 
                # To get the position of the current box
                box_row = (row//3)*3
                box_column = (column//3)*3
                for row_neighbour in range(box_row,box_row+3):
                    for column_neighbour in range(box_column,box_column+3):
                        if column_neighbour == column and row_neighbour == row :
                            continue
                        neighbours.add(grid[row_neighbour][column_neighbour])

                grid[row][column].set_neighbours(list(neighbours))

    # Bonus: Extra constraint
    def track_remaining_values(self):
        """
        Initializes the possible values for each row, column, and box
        based on the current board.
        """
        self.row_possibilities = [set(range(1, 10)) for _ in range(9)]
        self.col_possibilities = [set(range(1, 10)) for _ in range(9)]
        self.box_possibilities = [set(range(1, 10)) for _ in range(9)]

        for row in range(9):
            for col in range(9):
                val = self.board[row][col].get_value()
                if val != 0:
                    self.row_possibilities[row].discard(val)
                    self.col_possibilities[col].discard(val)
                    box_index = (row // 3) * 3 + (col // 3)
                    self.box_possibilities[box_index].discard(val)

    def board_to_string(self):
        
        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board
