class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.size = 9
        self.empty_value = 0

    def print_board(self):
        for row in range(self.size):
            if row % 3 == 0 and row != 0:
                print("- - - - - - - - - - -")
            for col in range(self.size):
                if col % 3 == 0 and col != 0:
                    print("|", end=" ")
                print(self.board[row][col], end=" ")
            print()

    def is_valid(self, num, pos):
        # Check row
        for col in range(self.size):
            if self.board[pos[0]][col] == num:
                return False

        # Check column
        for row in range(self.size):
            if self.board[row][pos[1]] == num:
                return False

        # Check 3x3 grid
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def find_empty(self):
        empty_positions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == self.empty_value:
                    empty_positions.append((i, j))

        if not empty_positions:
            return None

        # Apply Minimum Remaining Values (MRV) heuristic
        return min(empty_positions, key=lambda pos: len(self.possible_values(pos)))

    def possible_values(self, pos):
        possibilities = set(range(1, 10))
        for col in range(self.size):
            if self.board[pos[0]][col] != 0:
                possibilities.discard(self.board[pos[0]][col])

        for row in range(self.size):
            if self.board[row][pos[1]] != 0:
                possibilities.discard(self.board[row][pos[1]])

        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] != 0:
                    possibilities.discard(self.board[i][j])

        return possibilities

    def solve(self):
        empty_pos = self.find_empty()
        if not empty_pos:
            return True  # Puzzle solved

        row, col = empty_pos

        for num in self.possible_values((row, col)):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num

                if self.solve():
                    return True

                self.board[row][col] = 0  # Backtrack

        return False

def get_user_input():
    print("Enter the Sudoku puzzle row by row, with 0 for empty cells.")
    board = []
    for i in range(9):
        while True:
            row = input(f"Enter row {i + 1} (9 space-separated digits): ").split()
            if len(row) == 9 and all(digit.isdigit() and 0 <= int(digit) <= 9 for digit in row):
                board.append([int(digit) for digit in row])
                break
            else:
                print("Invalid input. Please enter exactly 9 digits between 0 and 9.")
    return board

if __name__ == "__main__":
    # Get puzzle input interactively from the user
    board = get_user_input()
    solver = SudokuSolver(board)

    print("\nOriginal Sudoku board:")
    solver.print_board()

    if solver.solve():
        print("\nSolved Sudoku board:")
        solver.print_board()
    else:
        print("\nNo solution exists for the given Sudoku puzzle.")
