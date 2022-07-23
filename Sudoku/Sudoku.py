#!/usr/bin/env python

#TODO solving Sudoku using backtracking
#TODO the solution here uses brute force method by recursively trying every possible solution untill it finds the right one

# . Returns tuple of next location with value 0 (value to be found)
# . or (None, None) in case the puzzle is completely filled
def find_next_empty(puzzle):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                return row, col

    return None, None


# . Returns True if the guess made is valid else false
def is_valid_guess(puzzle, row, col, guess):
    row_values = puzzle[row]  # ? Row in which the guessing spot belongs
    # ? Column in which the guessing spot belongs
    col_values = [puzzle[i][col] for i in range(9)]

    for value in row_values:
        if value == guess:  # ! guessed value is repeated along the row
            return False
    for value in col_values:
        if value == guess:  # ! guessed value is repeated along the column
            return False
        
    

    # ? for find the square in which the guessing spot belongs
    # squares begin from row 0 for row 0, 1, 2, and so on
    row_start = (row // 3) * 3
    # squares begin from col 0 for col 0, 1, 2 and so on
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:  # ! guessed value is repeated inside the 3x3 square
                return False
    return True


# . Returns whether a solution exists
def solve_sudoku(puzzle):
    # TODO Step 1: choose next location on puzzle to guwess
    row, col = find_next_empty(puzzle)

    if row is None:  # row is None means col will also be None
        # indicates we solved the sudoku
        return True

    # TODO Step 2: guess a digit between 1-9 to be placed at the location
    for guess in range(1, 10):
        # TODO Step 3: if the guess valid, assign the value to the cell
        # * Valid Guess is a guess which neither repeated in the row, col or in its 3x3 grid
        if is_valid_guess(puzzle, row, col, guess):
            puzzle[row][col] = guess

            # TODO Step 4: recursively call the function to solve the puzzle
            if solve_sudoku(puzzle):
                return True

        # TODO Step 5: Invalid guess is made or the guess made did not solve the puzzle so reset the value
        puzzle[row][col] = 0

    # TODO Step 6: Reaching here means none of the 1 to 9 guessed values could solve the puzzle Hence the puzzle must be incorrect
    return False


def display_puzzle(puzzle):

    if len(puzzle) != 9:
        print("Provided Puzzle not a Sudoku!!\n")
        return
    else:
        for i in range(9):
            if len(puzzle[i]) != 9:
                print("Provided Puzzle not a Sudoku!!\n")
                return

    for row in range(9):
        for col in range(9):
            if col % 3 == 0:
                print(end='  ')
            print(puzzle[row][col], end="  ")
        if row % 3 == 2:
            print()
        print()


def input_puzzle():
    print(f"Enter values of puzzle by replacing blanks with 0...(no space between two values)")
    valid_values = list(range(10))
    puzzle = list()
    row_count = 0
    while row_count < 9:
        row = list(input(f"\nenter row {row_count + 1}: "))
        if len(row) != 9:
            print("Invalid Input...\nExactly 9 row entries needed!!")
            continue

        try:
            row = list(map(int, row))
        except:
            print("Integer VaLue Only...")
            continue

        if all(i in valid_values for i in row):
            puzzle.append(row)
            row_count += 1
        else:
            print(
                f"Invalid Input Value...\n Valid input values are: {valid_values}")
    return puzzle


if __name__ == "__main__":
    # board = [
    #     [3, 9, 0,   0, 5, 0,   0, 0, 0],
    #     [0, 0, 0,   2, 0, 0,   0, 0, 5],
    #     [0, 0, 0,   7, 1, 9,   0, 8, 0],

    #     [0, 5, 0,   0, 6, 8,   0, 0, 0],
    #     [2, 0, 6,   0, 0, 3,   0, 0, 0],
    #     [0, 0, 0,   0, 0, 0,   0, 0, 4],

    #     [5, 0, 0,   0, 0, 0,   0, 0, 0],
    #     [6, 7, 0,   1, 0, 5,   0, 4, 0],
    #     [1, 0, 9,   0, 0, 0,   2, 0, 0]
    # ]

    board = input_puzzle()

    if solve_sudoku(board):
        print("\nSudoku Solved Successfully\n")
    else:
        print("\nSudoku Solving Failed\n")
        
    display_puzzle(board)
    print()
