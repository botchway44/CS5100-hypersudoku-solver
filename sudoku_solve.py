from math import sqrt
import dlinks_matrix as dlm
import time
import tkinter as tk


#GLobal Variables
#TODO : MODIFY THEM

# Initialize tkinter window
root = tk.Tk()
root.title("Sudoku Grid")
# GUI grid configuration
grid_size = 50  # size of each cell in pixels
start_x, start_y = 100, 100  # starting position of the grid

# Canvas size
cell_size = 50
canvas = tk.Canvas(root, width=cell_size * 9, height=cell_size * 9, bg="white")
canvas.pack()

#Create a puzzle as a list

puzzle = \
        [0,0,0,0,0,0,0,1,0,
        4,0,0,0,0,0,0,0,0,
        0,2,0,0,0,0,0,0,0,
        0,0,0,0,5,0,4,0,7,
        0,0,8,0,0,0,3,0,0,
        0,0,1,0,9,0,0,0,0,
        3,0,0,4,0,0,2,0,0,
        0,5,0,1,0,0,0,0,0,
        0,0,0,8,0,6,0,0,0]
        

# --- Constraints for a sudoku puzzle ---
# One value per cell
# Unique value per row
# Unique value per col
# Unique value per box
# ---------------------------------------
# These functions return the column of the matrix to be populated for a constraint when given
# a specified row of the matrix and the dimension of the sudoku puzzle
def _one_constraint(row: int, dim:int) -> int:
    return row//dim
def _row_constraint(row:int, dim:int) -> int:
    return dim**2 + dim*(row//(dim**2)) + row % dim
def _col_constraint(row:int, dim:int) -> int:
    return 2*(dim**2) + (row % (dim**2))
def _box_constraint(row:int, dim:int) -> int:
    return int(3*(dim**2) + (row//(sqrt(dim)*dim**2))*(dim*sqrt(dim)) + ((row//(sqrt(dim)*dim)) % sqrt(dim))*dim + (row % dim))

constraint_list = [_one_constraint, _row_constraint, _col_constraint, _box_constraint]

# convert list of ints representing the puzzle to a dancing link matrix
def _list_2_matrix(flat_list: list[int], row_size: int) -> dlm.DL_Matrix:
    """
    Converts a flat list into a 2D list (list of lists).

    Parameters:
        flat_list (list): The flat list to be converted.
        row_size (int): The number of elements per row.

    Returns:
        list of lists: The 2D grid representation.
    """
    return [flat_list[i:i + row_size] for i in range(0, len(flat_list), row_size)]


# convert list of ints representing the puzzle to a dancing link matrix
def _list_2_dl_matrix(puzzle: list[int], dim: int) -> dlm.DL_Matrix:
    num_rows = dim**3
    num_cols = (dim**2)*len(constraint_list)
    matrix: dlm.DL_Matrix = dlm.DL_Matrix(num_rows, num_cols)
    #iterate through puzzle
    for i, cell in enumerate(puzzle):
        if cell == 0: # if cell is unassigned
            # populate all rows representing cadidate values for this cell
            for j in range(dim):
                row = i*dim+j
                for constraint in constraint_list:
                    matrix.insert_node(row, constraint(row, dim))
        else: # if cell is assigned
            # populate the row representing the assigned value for this cell
            row = i*dim+cell-1
            for constraint in constraint_list:
                    matrix.insert_node(row, constraint(row, dim))
    return matrix

# takes list of ints representing a sudoku puzzle
# returns a list of ints representing the solution if one is found
def solve_puzzle(puzzle: list[int]) -> list[int]:
    dim = int(sqrt(len(puzzle)))
    print("DIMENSION", dim, int(dim+0.5)**2, len(puzzle))
    
    assert(int(dim+0.5)**2 == len(puzzle)) # only perfect square puzzles are supported
    solution_list = _list_2_dl_matrix(puzzle, dim).alg_x_search()
    if not solution_list: return []
    solved_puzzle = [0] * (dim**2)
    for row in solution_list:
        solved_puzzle[row // dim] = (row % dim) + 1
    return solved_puzzle

# prints a list of ints as a sudoku puzzle
def print_puzzle(puzzle: list[int]) -> None:
    uln = '\033[4m'
    res = '\033[0m'
    dim = int(sqrt(len(puzzle)))
    assert(int(dim+0.5)**2 == len(puzzle)) # only perfect square puzzles are supported
    for i in range(dim): print(uln + '   ', end='')
    print('     ' + res, end='')
   
    for i, cell in enumerate(puzzle):
        if i % int(sqrt(dim)) == 0 and i != 0: print("|", end='')
        if i//dim % int(sqrt(dim)) == int(sqrt(dim)) -1: print(uln + "", end='')
        if i % dim == 0: print('\n|', end='')
        print(f"{cell:3d}", end='')
        print(res, end='')
    print("|")

# Function to create and fill the Sudoku grid
def create_sudoku_grid(canvas, grid, cell_size=50):
    entries = []
    for row in range(9):
        row_entries = []
        for col in range(9):
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Add cell background color for sections
            if (row // 3 + col // 3) % 2 == 0:
                color = "#f0f0f0"  # Light gray
            else:
                color = "#ffffff"  # White
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#ccc")

            # Create an Entry widget inside each cell
            entry = tk.Entry(root, width=2, font=("Arial", 18), justify="center")
            entry_window = canvas.create_window(x1 + cell_size // 2, y1 + cell_size // 2, window=entry)

            # Prefill values and disable editing for fixed cells
            if grid[row][col] != 0:
                entry.insert(0, str(grid[row][col]))
                entry.config(state="disabled")

            row_entries.append(entry)
        entries.append(row_entries)

    # Draw bold grid lines for 3x3 sections
    for i in range(0, 10):
        line_width = 3 if i % 3 == 0 else 1
        canvas.create_line(0, i * cell_size, 9 * cell_size, i * cell_size, width=line_width, fill="red")
        canvas.create_line(i * cell_size, 0, i * cell_size, 9 * cell_size, width=line_width, fill="red")

    return entries

# Function to handle button click
def on_button_click():
    print("Button clicked!")
    #make 
    grid_solution = solve_9(puzzle);
    
    # Clear existing content on the canvas
    canvas.delete("all")
    row_size = 9
    print("SOLUTION::", _list_2_matrix(grid_solution,row_size))
    
    # Add updated content
    create_sudoku_grid(canvas, _list_2_matrix(grid_solution,row_size), cell_size)




if __name__ == '__main__':
    
    def solve_16():
        puzzle = \
        [15, 0, 0,13, 0,14,11, 8, 3, 0, 0, 1, 4, 0, 0, 7,
        3, 8, 0, 0,15, 2, 6, 0, 0, 0, 0, 0, 1, 0,14, 0,
        6, 0, 1, 0,10, 7, 0,12,15, 0, 5, 0, 2, 0,11, 3,
        11, 0, 0, 0, 0, 3, 0, 0, 4, 0,13,14, 0, 0, 0, 6,
        8, 3,10,15, 0,16,13, 0, 7, 0, 0, 6,14, 5, 0,12,
        0, 0, 0, 1, 0, 0,14, 0,13, 0, 0,15, 6, 7, 0, 0,
        7, 2,12, 6, 8, 4, 0,10, 5, 9, 0,16, 0,11, 1,15,
        0,13,14, 0, 7, 6, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0,
        0, 5,11, 0,14,13, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
        1, 7, 2,10,12, 8, 0, 4, 6, 3, 0, 5, 0,14, 9,13,
        0, 0, 0, 3, 0, 0,10, 0, 9, 0, 0, 4,12,16, 0, 0,
        14, 4, 9, 8, 0,15, 2, 0,12, 0, 0,11, 7, 6, 0,10,
        12, 0, 0, 0, 0,10, 0, 0,16, 0, 9,13, 0, 0, 0, 2,
        10, 0,13, 0, 4, 1, 0, 2,14, 0, 6, 0, 9, 0, 8,11,
        2,15, 0, 0, 6, 9, 7, 0, 0, 0, 0, 0,10, 0,13, 0,
        9, 0, 0,14, 0,12, 8, 3, 1, 0, 0, 2, 5, 0, 0,16]
        
        solution = solve_puzzle(puzzle)
        
        print_puzzle(puzzle)
        if solution: 
            print(f"\nSolution Found:")
            print_puzzle(solution)
        else: print("\nNo Solution Found")
        
    def solve_9(puzzle):
        
        
        solution = solve_puzzle(puzzle)
        
        print_puzzle(puzzle)
        if solution: 
            print(f"\nSolution Found:")
            print_puzzle(solution)
        else: print("\nNo Solution Found")
        return solution
    
    def solve_file():
        with open('small.txt', 'rb') as puzzle_file, open('solutions.txt', 'wb') as solution_file:
            while puzzle_str := puzzle_file.read(82).rstrip(b'\n'):
                puzzle = [c - 0x30 for c in puzzle_str]
                solution = solve_puzzle(puzzle)
                solution_str = bytes([i + 0x30 for i in solution]) + b'\n'
                solution_file.write(puzzle_str + b',' + solution_str)
        

    row_size = 9
    # Create the grid
    entries = create_sudoku_grid(canvas, _list_2_matrix(puzzle,row_size), cell_size)

    #add button to trigger solve
    button = tk.Button(root, text="Solve Sudoku", command=on_button_click)
    button.pack(pady=10)


    # Run the tkinter event loop
    root.mainloop()
