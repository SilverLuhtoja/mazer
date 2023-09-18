from cell import Cell
import random
import time

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, class_window = None, seed = None):
        self._seed = seed
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols =  num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = class_window
        self._create_cells()
        self._break_entrace_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    def _create_cells(self):
        self._cells = [[Cell(self._win) for col in range(self._num_rows) ] for row in range(self._num_cols)]
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i,j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x_pos = self._x1 + (i * self._cell_size_x)
        y_pos = self._y1 + (j * self._cell_size_y)
        self._cells[i][j].draw(x_pos, y_pos, x_pos + self._cell_size_x, y_pos + self._cell_size_y)
        self._animate()
    
    def _animate(self):
        self._win.redraw()
        time.sleep(0.001)
    
    def _break_entrace_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
        
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        
        while True:
            next_index_list = []

            possible_direction_indexes = 0

            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
                possible_direction_indexes += 1
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
                possible_direction_indexes += 1
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
                possible_direction_indexes += 1
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
                possible_direction_indexes += 1

            # just break out
            if possible_direction_indexes == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(possible_direction_indexes)
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])
            
    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
                
    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if (i,j) == (self._num_rows - 1,self._num_cols -1):
            return True
        
        # left
        if i > 0 and not self._cells[i - 1][j].visited and self._cells[i][j].has_left_wall == False:
            to_cell = self._cells[i - 1][j]
            self._cells[i][j].draw_move(to_cell)
            if self._solve_r(i - 1, j):
                return True
            self._cells[i][j].draw_move(to_cell, True)
                
        # right
        if i < self._num_cols - 1 and not self._cells[i + 1][j].visited and self._cells[i][j].has_right_wall == False:
            to_cell = self._cells[i + 1][j]
            self._cells[i][j].draw_move(to_cell)
            if self._solve_r(i + 1, j):
                return True
            self._cells[i][j].draw_move(to_cell, True)
        # up
        if j > 0 and not self._cells[i][j - 1].visited and self._cells[i][j].has_top_wall == False:
            to_cell = self._cells[i][j - 1]
            self._cells[i][j].draw_move(to_cell)
            if self._solve_r(i, j - 1):
                return True
            self._cells[i][j].draw_move(to_cell, True)

        # down
        if j < self._num_rows - 1 and not self._cells[i][j + 1].visited and self._cells[i][j].has_bottom_wall == False:
            to_cell = self._cells[i][j + 1]
            self._cells[i][j].draw_move(to_cell)
            if self._solve_r(i, j + 1):
                return True
            self._cells[i][j].draw_move(to_cell, True)
        
        return False
