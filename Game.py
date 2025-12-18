class Game:

    def __init__(self, sudoku, heuristic=None):
        self.sudoku = sudoku
        self.heuristic = heuristic

    def show_sudoku(self):
        print(self.sudoku)

    def backtracking(self):
        return 
    
    def solve(self) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        self.sudoku.track_remaining_values()
        queue = []
        board = self.sudoku.get_board()

        # Making the queue by adding the cell and its neighbors 
        for row in range(9):
            for column in range(9):
                field = board[row][column]
                for neighbour in field.get_neighbours():
                    queue.append((field, neighbour))

        # Adding these variables to measure complexity 
        handled_nodes = 0
        domain_shrinkage = 0 
        #time, heuristic, file, domain shrinkage, nodes handles 
        while queue:
            if self.heuristic:
                Xm, Xn = self.heuristic(queue)
            else:
                Xm, Xn = queue.pop(0)

            handled_nodes += 1
            changed = self.revise(Xm, Xn)

            if len(Xm.get_domain()) == 0 and not Xm.is_finalized():
                return False
        
            if changed:
                domain_shrinkage += 1
                neighbours = Xm.get_neighbours()

                for Xk in neighbours:     
                    if Xk != Xn:
                    # Check to see if (Xk, Xm) not on queue then add it
                        in_queue = False 
                        for arc in queue:
                            if arc[0] == Xk and arc[1] == Xm:
                                in_queue = True
                        if in_queue == False:
                            queue.append((Xk, Xm))
        if self.valid_solution():
            print(self.sudoku)
            print(f"Handled nodes: {handled_nodes}, Domain shrinkages: {domain_shrinkage}")
            return True
    
        def backtrack():
                # Find cells without value and smallest domain
                min_domain_size = 10
                current_field = None

                for row in range(9):
                    for column in range(9):
                        field = board[row][column]
                        if field.is_finalized():
                            continue
                        if len(field.get_domain()) < min_domain_size:
                            min_domain_size = len(field.get_domain())
                            current_field = field

                if current_field is None:
                    # All fields are assigned
                    return self.valid_solution()

                current_domain = current_field.get_domain()[:]
                for value in current_domain:
                    original_domain = current_domain
                    current_field.set_value(value)
                    if backtrack():
                        return True
                    
                    # Did not work restore the domain
                    current_field.value = 0
                    current_field.domain = original_domain  

        print(f"Handled nodes: {handled_nodes}, Domain shrinkages: {domain_shrinkage}")
        print(self.sudoku)
        return backtrack()



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
        
        # Check if the cell is compatible with the constaints(In this case neighbors)
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
        count = 0
        for row in range(9):
            checked = set()
            for column in range(9):
                count += 1
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
        # We should iterate over each subgrid first
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
