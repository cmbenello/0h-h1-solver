def is_valid(grid, row, col, color):
    """
    Check if adding a tile of the given color at the given position is valid.
    """
    # Check if the two pieces on eithe side of it are the same color:
    # Start horizontally
    if(row + 1 < len(grid) and grid[row + 1][col] == color) and (row >= 0 and grid[row - 1][col] == color):
        return False
    # Then check the vertical
    if(col + 1 < len(grid) and grid[row][col + 1] == color) and (col - 1 >= 0 and grid[row][col - 1] == color):
        return False
    
    # Next check that there arne't already two conseuctive pieces of the same color next to it
    # Check horitzonally right then left
    if (row + 2 < len(grid) and grid[row + 1][col] == color and grid[row + 2][col] == color):
        return False
    if (row - 2 >= 0 and grid[row - 1][col] == color and grid[row - 2][col] == color):
        return False
    # check veritcally down then up
    if (col + 2 < len(grid) and grid[row][col + 1] == color and grid[row][col + 2] == color):
        return False
    if (col - 2 >= 0 and grid[row][col - 1] == color and grid[row][col - 2] == color):
        return False
    
    # Check for the equal number of blue and yellow tiles constraint in rows and columns.
    row_count = sum(1 for i in grid[row] if i == color)
    col_count = sum(1 for i in range(len(grid)) if grid[i][col] == color)
    if row_count == len(grid) // 2 or col_count == len(grid) // 2:
        return False

    grid[row][col] = color
    # Check if the row or column becomes identical to another.
    for i in range(len(grid)):

        if i != row and grid[i] == grid[row]:
            grid[row][col] = 0
            return False
        if i != col and [grid[r][i] for r in range(len(grid))] == [grid[r][col] for r in range(len(grid))]:
            grid[row][col] = 0
            return False

    return True

# Grid is the grid, n is the size of the grid
def solve(grid, n, row=0, col=0):
    """
    Solve the puzzle using backtracking.
    """
    if row == n:
        # Puzzle solved.
        return True
    if col == n:
        # Move to the next row.
        return solve(grid, n, row + 1, 0)
    # The cell is alreayd taken
    elif grid[row][col] != 0:
        return solve(grid, n, row, col + 1)
    
    # Red is 1, blue is 2
    for color in [1, 2]:
        if is_valid(grid, row, col, color):
            grid[row][col] = color
            if solve(grid, n, row, col + 1):
                return True
            # Undo the move (backtrack).
            grid[row][col] = 0
    # print_grid(grid)
    # print("hi")
    return False

def print_grid(grid):
    for row in grid:
        print(' '.join(str(row)))

def main(grid, n):
    # Initialize the grid with None to indicate empty cells.
    if solve(grid, n):
        # print_grid(grid)
        return(grid)
    else:
        print("No solution exists.")

if __name__ == "__main__":
    size = 6  # Size of the grid, change this to the desired even number between 4 and 12
    problematic_grid = ([ 1 ,   0 ,   0 ,   0 ,   0 ,   0 ],
[ 1 ,   0 ,   0 ,   0 ,   2 ,   0 ],
[ 0 ,   2 ,   0 ,   0 ,   2 ,   0 ],
[ 0 ,   0 ,   0 ,   1 ,   0 ,   0 ],
[ 0 ,   0 ,   0 ,   0 ,   0 ,   0 ],
[ 0 ,   0 ,   2 ,   0 ,   0 ,   0 ])
    print_grid(main(problematic_grid, size))
