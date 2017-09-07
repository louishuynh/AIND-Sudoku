import unittest

from solution import solve
from utils import values_grid, grid_values


class TestDiagonalSolution(unittest.TestCase):
    def test_solve_diagonal(self):
        diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        expected_solution = '267945381853716249491823576576438192384192657129657438642379815935281764718564923'
        solution = values_grid(solve(diag_sudoku_grid))
        self.assertEquals(solution, expected_solution)


class TestSolution(unittest.TestCase):
    def test_solve_diagonal(self):
        before_naked_twins1 = '1.4.9..68956.18.34..84.695151.....868..6...1264..8..97781923645495.6.823.6.854179'
        expected_solution = '124292268956218234228436951517232386837635312642181397781923645495161823262854179'
        solution = values_grid(solve(before_naked_twins1))
        self.assertEquals(solution, expected_solution)
