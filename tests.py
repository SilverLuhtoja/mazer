import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_large(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        
    def test_break_and_exit(self):
        num_cols = 3
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False
        )
        self.assertEqual(
            m1._cells[num_rows-1][num_cols-1].has_bottom_wall,
            False
        )
    def test_reset_cells_visited(self):
        num_cols = 3
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        
        for row in m1._cells:
            for cell in row:
                cell.visited = False
                self.assertEqual(
                    cell.visited,
                    False
                )

    # cant test private units
    # def test_solve_r_True_value(self):
    #     num_cols = 3
    #     num_rows = 3
    #     m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
    #     self.assertEqual(m1._solve_r(3,3), True)


if __name__ == "__main__":
    unittest.main()