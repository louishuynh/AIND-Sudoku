import unittest

from solution import solve, values_grid, grid_values, naked_twins, is_valid


class TestUtils(unittest.TestCase):
    values_1 = {'A1': '123456789', 'A2': '4', 'A3': '7',
                'A4': '6', 'A5': '8', 'A6': '5',
                'A7': '123456789', 'A8': '9', 'A9': '1',
                'B1': '6', 'B2': '9', 'B3': '8',
                'B4': '4', 'B5': '123456789', 'B6': '1',
                'B7': '123456789', 'B8': '5', 'B9': '123456789',
                'C1': '123456789', 'C2': '5', 'C3': '1',
                'C4': '123456789', 'C5': '123456789', 'C6': '123456789',
                'C7': '8', 'C8': '6', 'C9': '4',
                'D1': '8', 'D2': '123456789', 'D3': '9',
                'D4': '123456789', 'D5': '6', 'D6': '123456789',
                'D7': '4', 'D8': '123456789', 'D9': '123456789',
                'E1': '5', 'E2': '6', 'E3': '2',
                'E4': '8', 'E5': '123456789', 'E6': '123456789',
                'E7': '123456789', 'E8': '1', 'E9': '9',
                'F1': '4', 'F2': '123456789', 'F3': '3',
                'F4': '123456789', 'F5': '123456789', 'F6': '123456789',
                'F7': '6', 'F8': '8', 'F9': '123456789',
                'G1': '1', 'G2': '8', 'G3': '6',
                'G4': '123456789', 'G5': '123456789', 'G6': '123456789',
                'G7': '9', 'G8': '123456789', 'G9': '123456789',
                'H1': '7', 'H2': '2', 'H3': '4',
                'H4': '9', 'H5': '1', 'H6': '8',
                'H7': '5', 'H8': '3', 'H9': '6',
                'I1': '9', 'I2': '3', 'I3': '5',
                'I4': '7', 'I5': '2', 'I6': '6',
                'I7': '1', 'I8': '4', 'I9': '8'}

    grid_1 = '.47685.916984.1.5..51...8648.9.6.4..5628...194.3...68.186...9..724918536935726148'

    def test_values_grid(self):
        response = values_grid(self.values_1)
        print(response)
        self.assertEqual(response, self.grid_1)

    def test_grid_values(self):
        response = grid_values(self.grid_1)
        print(response)
        self.assertEqual(response, self.values_1)


class TestDiagonalSolution(unittest.TestCase):
    def test_solve_diagonal(self):
        diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        expected_solution = '267945381853716249491823576576438192384192657129657438642379815935281764718564923'
        solution = values_grid(solve(diag_sudoku_grid))
        self.assertEquals(solution, expected_solution)

    def test_solve_diagonal_2(self):
        diag_sudoku_grid_2 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
        expected_solution_2 = '961354287835276149274891365427138956583962714619547832342689571798415623156723498'
        solution_2 = values_grid(solve(diag_sudoku_grid_2))
        print('Expected: {}'.format(expected_solution_2))
        print('Solution: {}'.format(solution_2))
        self.assertEquals(expected_solution_2, solution_2)

    def test_solve_diagonal_3(self):
        diag_sudoku_grid_3 = '...8...1.781..........1....4.......5..8..7.....75.319................6.........3.'
        expected_solution_3 = '924876513781352946536419782493168275158927364267543198379685421812734659645291837'
        solution_3 = values_grid(solve(diag_sudoku_grid_3))
        print('Expected: {}'.format(expected_solution_3))
        print('Solution: {}'.format(solution_3))
        self.assertEquals(expected_solution_3, solution_3)

    def test_solve_diagonal_4(self):
        diag_sudoku_grid_4 = '..7..5..2.......13.........9...8.7......7...5..2.......1..3.......54.......7....4'
        expected_solution_4 = '397815642284697513681423957935284761846179325172356489418932576763541298529768134'
        solution_4 = values_grid(solve(diag_sudoku_grid_4))
        print('Expected: {}'.format(expected_solution_4))
        print('Solution: {}'.format(solution_4))
        self.assertEquals(expected_solution_4, solution_4)
        print(is_valid(grid_values(solution_4)))






class TestNakedTwinsSolution(unittest.TestCase):
    def test_solve_naked_twins(self):
        before_naked_twins1 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
        expected_solution = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
        solution = values_grid(naked_twins(grid_values(before_naked_twins1)))
        self.assertEquals(solution, expected_solution)
