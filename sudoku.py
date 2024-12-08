import argparse
from pathlib import Path

class DancingLinksNode:
    def __init__(self, row_idx=None, col_idx=None, column=None):
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.column = column
        self.left = self.right = self.up = self.down = self

class DancingLinksColumn:
    def __init__(self, col_idx):
        self.col_idx = col_idx
        self.size = 0
        self.head = DancingLinksNode(column=self)

class DancingLinks:
    def __init__(self, grid, base_size=9, hyper_boxes=None):
        self.base_size = base_size
        self.hyper_boxes = hyper_boxes or []
        self.num_constraints = base_size**2 * 4 + len(hyper_boxes) * base_size
        self.columns = [DancingLinksColumn(i) for i in range(self.num_constraints)]
        self.head = DancingLinksNode()
        self.solution = []
        self.setup_linked_grid(grid)
        self.link_headers()

    def setup_linked_grid(self, grid):
        # Iterate over all possible positions and numbers
        for i in range(self.base_size):
            for j in range(self.base_size):
                for n in range(1, self.base_size + 1):
                    if grid[i][j] == 0 or grid[i][j] == n:
                        row_idx = (i * self.base_size**2) + (j * self.base_size) + (n - 1)
                        columns = [
                            (self.base_size * i) + j,
                            self.base_size**2 + (self.base_size * i) + (n - 1),
                            2 * self.base_size**2 + (self.base_size * j) + (n - 1),
                            3 * self.base_size**2 + ((i // 3) * 3 + j // 3) * self.base_size + (n - 1)
                        ]
                        if self.is_in_hyper_box(i, j):
                            hyper_box_idx = self.get_hyper_index(i, j)
                            columns.append(4 * self.base_size**2 + hyper_box_idx * self.base_size + (n - 1))
                        self.add_row(row_idx, columns)

    def is_in_hyper_box(self, row, col):
        for box in self.hyper_boxes:
            if box[0] <= row < box[0] + 3 and box[1] <= col < box[1] + 3:
                return True
        return False

    def get_hyper_index(self, row, col):
        for index, box in enumerate(self.hyper_boxes):
            if box[0] <= row < box[0] + 3 and box[1] <= col < box[1] + 3:
                return index
        return -1

    def add_row(self, row_id, column_indices):
        first_node = None
        last_node = None
        for col_index in column_indices:
            column = self.columns[col_index]
            new_node = DancingLinksNode(row_idx=row_id, column=column)
            column.size += 1
            if not first_node:
                first_node = new_node
            if last_node:
                last_node.right = new_node
                new_node.left = last_node
            last_node = new_node

            # Vertically link
            new_node.down = column.head
            new_node.up = column.head.up
            column.head.up.down = new_node
            column.head.up = new_node
        first_node.left = last_node
        last_node.right = first_node

    def link_headers(self):
        current = self.head
        for column in self.columns:
            current.right = column.head
            column.head.left = current
            current = column.head
        current.right = self.head
        self.head.left = current

    def cover(self, column):
        column.head.right.left = column.head.left
        column.head.left.right = column.head.right
        row = column.head.down
        while row != column.head:
            right_node = row.right
            while right_node != row:
                right_node.down.up = right_node.up
                right_node.up.down = right_node.down
                right_node.column.size -= 1
                right_node = right_node.right
            row = row.down

    def uncover(self, column):
        row = column.head.up
        while row != column.head:
            left_node = row.left
            while left_node != row:
                left_node.column.size += 1
                left_node.down.up = left_node
                left_node.up.down = left_node
                left_node = left_node.left
            row = row.up
        column.head.right.left = column.head
        column.head.left.right = column.head

    def search(self, k=0):
        if self.head.right == self.head:
            self.solution_found()
            return True
        column = self.select_column()
        if column.size <= 0:
            return False
        self.cover(column)
        row = column.head.down
        while row != column.head:
            self.solution.append(row.row_idx)
            col_node = row.right
            while col_node != row:
                self.cover(col_node.column)
                col_node = col_node.right
            if self.search(k + 1):
                return True
            self.solution.pop()
            col_node = row.left
            while col_node != row:
                self.uncover(col_node.column)
                col_node = col_node.left
            row = row.down
        self.uncover(column)
        return False

    def select_column(self):
        smallest = float('inf')
        chosen_column = None
        current = self.head.right
        while current != self.head:
            if current.column.size < smallest:
                smallest = current.column.size
                chosen_column = current.column
            current = current.right
        return chosen_column

    def solution_found(self):
        solved_grid = [[0 for _ in range(self.base_size)] for _ in range(self.base_size)]
        for row_idx in self.solution:
            i = row_idx // (self.base_size**2)
            row_idx %= self.base_size**2
            j = row_idx // self.base_size
            n = row_idx % self.base_size + 1
            solved_grid[i][j] = n
        self.print_grid(solved_grid)
        
    def print_grid(self, grid):
        for row in grid:
            print(" ".join(str(num) if num != 0 else '.' for num in row))

def solve_hyper_sudoku(grid):
    hyper_boxes = [(1, 1), (1, 5), (5, 1), (5, 5)]  # Additional constraints
    dancing_links = DancingLinks(grid, hyper_boxes=hyper_boxes)
    if not dancing_links.search():
        print("No solution found.")




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=Path, help='Path to sudoku text file.')

    args = parser.parse_args()

    with args.filename.open('r') as f:
        grid = [list(map(int, x.strip().split(' '))) for x in f.readlines()]

    # print("GRID:::",grid)
    # Example grid setup
    # initial_grid = [
    #     [0, 0, 0, 0, 0, 0, 0, 3, 0],
    #     [3, 0, 9, 0, 0, 0, 0, 2, 0],
    #     [8, 0, 7, 0, 0, 0, 9, 6, 0],
    #     [0, 1, 0, 0, 0, 4, 3, 0, 6],
    #     [0, 0, 6, 0, 0, 0, 0, 0, 0],
    #     [0, 7, 5, 1, 0, 0, 0, 0, 9],
    #     [0, 8, 0, 0, 4, 0, 0, 0, 0],
    #     [0, 4, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 5, 0, 0, 0, 0, 2]
    # ]

    solve_hyper_sudoku(grid)


if __name__ == "__main__":
    main()


