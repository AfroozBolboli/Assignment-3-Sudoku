class Game:

    def __init__(self, sudoku):
        self.sudoku = sudoku

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        # 
        queue = []
        board = self.sudoku.get_board()
        for row in range(9):
            for column in range(9):
                field = board[row][column]
                for neighbour in field.get_neighbours():
                    queue.append((field, neighbour))
                
        while queue:
            Xm, Xn = queue.pop(0)
            changed = self.revise(Xm, Xn)

            if len(Xm.get_domain()) == 0:
                return False
        
            if changed:
                neighbours = Xm.get_neighbours()
                for Xk in neighbours:     

                    if Xk != Xn:
                    # if (Xk, Xm) not on queue then add it
                        in_queue = False 
                        for arc in queue:
                            if arc[0] == Xk and arc[1] == Xm:
                                in_queue = True
                        if in_queue == False:
                            queue.append((Xk, Xm))

        return True

    def revise(self, Xm, Xn):
        """
        Revise deletes the value of Xm from domain Xm 
        if there are no values of Xn in domain Xn that match
        such that the constraint is satisfied.
        @return: True if there has been a change.
        """
        changed = False 
        # We need to remove from the real domain of Xm while safely looping 
        # So we need a copy of a list to iterate from
        domain_Xm = Xm.get_domain()[:]
        domain_Xn = Xn.get_domain()

        for value_Xm in domain_Xm:
            keep = False 
            for value_Xn in domain_Xn:
                if value_Xm != value_Xn:
                    keep = True
                    break
            if keep == False:
                Xm.remove_from_domain(value_Xm)
                changed = True
        return changed 
    
    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        board = self.sudoku.get_board()
        
        # Check row is not more than 9 or less than 1 or repetetive
        for row in range(9):
            checked = set()
            for column in range(9):
                value = board[row][column].get_value()
                if value < 1 or value > 9 or value in checked:
                    return False
                checked.add(value)
        
        # Check Column is not more than 9 or less than 1 or repetetive
        for column in range(9):
            checked = set()
            for row in range(9):
                value = board[row][column].get_value()
                if value < 1 or value > 9 or value in checked:
                    return False
                checked.add(value)
        
        # Check for each box 1-9 it is in value
        for box_row in range(0, 9, 3):
            for box_column in range(0, 9, 3):
                checked = set()
                for row in range(box_row, box_row + 3):
                    for column in range(box_column, box_column + 3):
                        value = board[row][column].get_value()
                        if value < 1 or value > 9 or value in checked:
                            return False
                        checked.add(value)

        return True
